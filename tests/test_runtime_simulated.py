"""Tests du coordinateur avec doubles locaux ; PAS un test Home Assistant réel."""
import asyncio
import importlib
import sys
import types
import unittest
from datetime import datetime, timezone, timedelta
from types import SimpleNamespace as N

def module(name):
    m=types.ModuleType(name)
    sys.modules[name]=m
    return m
ha=module("homeassistant");ha.__path__=[]
helpers=module("homeassistant.helpers");helpers.__path__=[]
exc=module("homeassistant.exceptions")
class HAError(Exception):pass
exc.HomeAssistantError=HAError
exc.ConfigEntryAuthFailed=type("ConfigEntryAuthFailed",(HAError,),{})
aio=module("homeassistant.helpers.aiohttp_client");aio.async_get_clientsession=lambda hass:None
storage=module("homeassistant.helpers.storage")
class Store:
    def __init__(self,*args):self.saved=None
    async def async_load(self):return {}
    async def async_save(self,data):self.saved=dict(data)
storage.Store=Store
updates=module("homeassistant.helpers.update_coordinator")
class Coordinator:
    def __init__(self,hass,*args,**kwargs):self.hass=hass;self.data=None;self.last_update_success=True;self.publications=0
    async def async_request_refresh(self):pass
    def async_update_listeners(self):self.publications+=1
updates.DataUpdateCoordinator=Coordinator
updates.UpdateFailed=type("UpdateFailed",(HAError,),{})
util=module("homeassistant.util");util.__path__=[]
dt=module("homeassistant.util.dt");dt.utcnow=lambda:datetime.now(timezone.utc)
reg=module("homeassistant.helpers.entity_registry");reg.async_get=lambda hass:hass.registry
dev=module("homeassistant.helpers.device_registry");dev.async_get=lambda hass:hass.devices
from custom_components.vigilance_meteo_mobile.coordinator import VigilanceCoordinator
from custom_components.vigilance_meteo_mobile.discovery import geocoded_choices

class Services:
    def __init__(self):self.calls=[];self.missing=set();self.fail=set()
    def has_service(self,domain,service):return domain+"."+service not in self.missing
    async def async_call(self,domain,service,data,blocking=False):
        action=domain+"."+service
        if action in self.fail:raise HAError("simulated")
        self.calls.append((action,data))

class RuntimeTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.phone={"id":"a","name":"A","sensor":"sensor.a","notifications":["notify.mobile_app_a"]}
        self.states={"sensor.a":N(state="Adresse fictive",attributes={"iso_country_code":"FR","sub_administrative_area":"Morbihan"})}
        self.hass=N(states=N(get=self.states.get),services=Services(),config=N(time_zone="Europe/Paris"),bus=N(async_fire=lambda *args:None))
        self.entry=N(entry_id="entry",data={"api_key":"FAKE_TEST_KEY"},options={"enabled":True,"recipients":[self.phone]})
        self.c=VigilanceCoordinator(self.hass,self.entry)
        self.c.names={"56":"Morbihan","35":"Ille-et-Vilaine"}
        now=datetime.now(timezone.utc)
        window={"begin_time":(now+timedelta(hours=1)).isoformat(),"end_time":(now+timedelta(hours=2)).isoformat(),"color_id":2}
        zone={"domain_id":"56","max_color_id":2,"phenomenon_items":[{"phenomenon_id":"1","phenomenon_max_color_id":2,"timelaps_items":[window]}]}
        period={"echeance":"J","begin_validity_time":(now-timedelta(hours=1)).isoformat(),"end_validity_time":(now+timedelta(hours=8)).isoformat(),"timelaps":{"domain_ids":[zone]}}
        self.c.data={"update_time":now.isoformat(),"periods":[period]}
    async def test_automatic_disabled(self):
        self.c.settings["enabled"]=False
        self.assertEqual((await self.c.async_notify())["a"]["status"],"automatique_desactive")
        self.assertEqual(self.hass.services.calls,[])
    async def test_manual_bypasses_disabled_and_threshold(self):
        self.c.settings.update(enabled=False,minimum=4)
        self.assertEqual((await self.c.async_test("a"))["a"]["status"],"test_envoye")
        self.assertTrue(self.hass.services.calls[0][1]["message"].startswith("TEST —"))
    async def test_manual_no_dedup_write(self):
        await self.c.async_test("a")
        self.assertEqual(self.c.sent,{})
        self.assertEqual(self.c.last_tests["a"]["status"],"test_envoye")
    async def test_duplicate_suppressed(self):
        await self.c.async_notify()
        result=await self.c.async_notify()
        self.assertEqual(result["a"]["status"],"deja_envoye")
        self.assertEqual(len(self.hass.services.calls),1)
    async def test_unknown_skipped(self):
        self.states["sensor.a"].state="unknown"
        self.assertEqual((await self.c.async_test("a"))["a"]["status"],"position_inconnue")
    async def test_exclusion_applies_to_manual(self):
        self.c.settings["exclusions"]="56"
        self.assertEqual((await self.c.async_test("a"))["a"]["status"],"departement_exclu")
        self.assertEqual(self.hass.services.calls,[])
    async def test_multiple_destinations(self):
        self.c.settings["recipients"][0]["notifications"].append("notify.mobile_app_b")
        await self.c.async_test("a")
        self.assertEqual(len(self.hass.services.calls),2)
    async def test_retry_only_failed_destination(self):
        self.c.settings["recipients"][0]["notifications"].append("notify.mobile_app_b")
        self.hass.services.fail.add("notify.mobile_app_b")
        await self.c.async_notify()
        self.hass.services.fail.clear()
        await self.c.async_notify()
        self.assertEqual([a for a,_ in self.hass.services.calls],["notify.mobile_app_a","notify.mobile_app_b"])
    async def test_threshold(self):
        self.c.settings["minimum"]=3
        self.assertEqual((await self.c.async_notify())["a"]["status"],"sous_le_seuil")
    async def test_missing_action(self):
        self.hass.services.missing.add("notify.mobile_app_a")
        r=await self.c.async_test("a")
        self.assertEqual(r["a"]["destinations"]["notify.mobile_app_a"],"action_notification_absente")
    async def test_no_data_on_api_failure(self):
        self.c.last_update_success=False
        self.assertEqual((await self.c.async_test("a"))["a"]["status"],"api_indisponible")
    async def test_unknown_target_is_error(self):
        with self.assertRaises(HAError):await self.c.async_test("missing")

class DiscoveryTests(unittest.TestCase):
    def choices(self,states,entries=None):
        entries=entries or {}
        hass=N(states=N(async_all=lambda domain:states),registry=N(async_get=entries.get),devices=N(async_get=lambda id:None))
        return geocoded_choices(hass)
    def test_battery_is_not_listed(self):
        s=N(entity_id="sensor.phone_battery",state="80",attributes={})
        self.assertEqual(self.choices([s]),[])
    def test_unknown_geocoded_is_listed(self):
        s=N(entity_id="sensor.phone_geocoded_location",state="unknown",attributes={"friendly_name":"Mon téléphone"})
        r=self.choices([s]);self.assertEqual(len(r),1);self.assertIn("pas encore reçue",r[0]["label"])
    def test_attributes_allow_renamed_entity(self):
        s=N(entity_id="sensor.position_personnelle",state="ok",attributes={"iso_country_code":"FR","sub_administrative_area":"Morbihan"})
        self.assertEqual(len(self.choices([s])),1)
    def test_disabled_not_listed(self):
        s=N(entity_id="sensor.phone_geocoded_location",state="unknown",attributes={})
        e=N(disabled_by="user",unique_id="geo",original_name="Geo",device_id=None)
        self.assertEqual(self.choices([s],{s.entity_id:e}),[])
