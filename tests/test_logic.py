import copy
import json
import unittest
from pathlib import Path
from datetime import datetime, timezone
from custom_components.vigilance_meteo_mobile.api import extract_product
from custom_components.vigilance_meteo_mobile.const import DEFAULT_OPTIONS
from custom_components.vigilance_meteo_mobile.logic import department, excluded_departments, current_period, zone_for, build_payload, timestamp, normalize_options

class LogicTests(unittest.TestCase):
    def setUp(self):
        self.period = {"echeance":"J", "begin_validity_time":"2026-10-24T04:00:00Z", "end_validity_time":"2026-10-24T22:00:00Z", "timelaps":{"domain_ids":[]}}
        self.zone = {"domain_id":"56", "max_color_id":2, "phenomenon_items":[{"phenomenon_id":"1", "phenomenon_max_color_id":2, "timelaps_items":[{"begin_time":"2026-10-24T18:00:00Z", "end_time":"2026-10-24T22:00:00Z", "color_id":2}]}]}
        self.product = {"periods":[self.period], "update_time":"2026-10-24T04:00:11Z"}
    def payload(self):
        return build_payload(self.product,self.period,self.zone,"56","Morbihan","Europe/Paris")
    def test_no_default_exclusion(self):
        self.assertEqual(excluded_departments(DEFAULT_OPTIONS["exclusions"]),set())
    def test_defaults_safe(self):
        self.assertFalse(DEFAULT_OPTIONS["enabled"])
        self.assertEqual(DEFAULT_OPTIONS["recipients"],[])
    def test_department(self):
        self.assertEqual(department({"iso_country_code":"FR","sub_administrative_area":"Morbihan"},{"56":"Morbihan"}),"56")
    def test_apostrophe(self):
        self.assertEqual(department({"iso_country_code":"FR","sub_administrative_area":"Côtes-d’Armor"},{"22":"Côtes-d'Armor"}),"22")
    def test_foreign(self):
        self.assertIsNone(department({"iso_country_code":"BE","sub_administrative_area":"Morbihan"},{"56":"Morbihan"}))
    def test_unknown(self):
        self.assertIsNone(department({}, {"56":"Morbihan"}))
    def test_exclusions(self):
        self.assertEqual(excluded_departments("2a;01,35"),{"2A","01","35"})
    def test_corsica(self):
        self.assertEqual(department({"iso_country_code":"FR","sub_administrative_area":"Haute-Corse"},{"2B":"Haute-Corse"}),"2B")
    def test_valid(self):
        self.assertIsNotNone(current_period(self.product,datetime(2026,10,24,12,tzinfo=timezone.utc)))
    def test_expired(self):
        self.assertIsNone(current_period(self.product,datetime(2026,10,25,12,tzinfo=timezone.utc)))
    def test_end_exclusive(self):
        self.assertIsNone(current_period(self.product,datetime(2026,10,24,22,tzinfo=timezone.utc)))
    def test_bad_date(self):
        self.period["begin_validity_time"]="wrong"
        self.assertIsNone(current_period(self.product))
    def test_naive_rejected(self):
        with self.assertRaises(ValueError):timestamp("2026-10-24T12:00:00")
    def test_missing_zone(self):
        self.assertIsNone(zone_for(self.period,"56"))
    def test_coastal_not_department(self):
        self.period["timelaps"]["domain_ids"]=[{"domain_id":"5610"}]
        self.assertIsNone(zone_for(self.period,"56"))
    def test_wind(self):
        p=self.payload()
        self.assertEqual(p["icon"],"mdi:weather-windy")
        self.assertEqual(p["color"],"#FFEB3B")
        self.assertIn("24/10 à 20:00",p["message"])
    def test_tie(self):
        self.zone["phenomenon_items"].append({"phenomenon_id":"2","phenomenon_max_color_id":2})
        self.assertEqual(self.payload()["icon"],"mdi:alert")
    def test_priority(self):
        self.zone["max_color_id"]=3
        self.zone["phenomenon_items"].append({"phenomenon_id":"6","phenomenon_max_color_id":3})
        self.assertEqual(self.payload()["icon"],"mdi:thermometer-high")
    def test_green(self):
        self.zone.update(max_color_id=1,phenomenon_items=[])
        self.assertEqual(self.payload()["icon"],"mdi:weather-partly-cloudy")
    def test_invalid_level(self):
        self.zone["max_color_id"]=7
        with self.assertRaises(ValueError):self.payload()
    def test_publication_not_signature(self):
        a=self.payload()["signature"]
        self.product["update_time"]="2026-10-24T12:00:00Z"
        self.assertEqual(a,self.payload()["signature"])
    def test_windows_change_signature(self):
        a=self.payload()["signature"]
        self.zone["phenomenon_items"][0]["timelaps_items"][0]["begin_time"]="2026-10-24T17:00:00Z"
        self.assertNotEqual(a,self.payload()["signature"])
    def test_direct_shape(self):
        self.assertIs(extract_product({"product":self.product}),self.product)
    def test_wrapped_shape(self):
        self.assertIs(extract_product({"content":{"product":self.product}}),self.product)
    def test_invalid_shape(self):
        with self.assertRaises(ValueError):extract_product({"error":"bad"})
    def test_departments(self):
        names=json.loads((Path(__file__).resolve().parents[1]/"custom_components/vigilance_meteo_mobile/departments.json").read_text())
        self.assertEqual(len(names),96)
        self.assertEqual(len(set(names.values())),96)
        self.assertEqual(names["07"],"Ardèche")
        self.assertEqual(names["65"],"Hautes-Pyrénées")
    def test_migration_single_action(self):
        old={"recipients":[{"id":"a","name":"A","sensor":"sensor.a","notification":"notify.mobile_app_a"}]}
        new=normalize_options(old)
        self.assertEqual(new["recipients"][0]["notifications"],["notify.mobile_app_a"])
        self.assertIn("notification",old["recipients"][0])
    def test_multiple_destinations_unique(self):
        opts=normalize_options({"recipients":[{"notifications":["notify.a","notify.a","notify.b"]}]})
        self.assertEqual(opts["recipients"][0]["notifications"],["notify.a","notify.b"])
    def test_dashboard_details(self):
        p=self.payload()
        self.assertEqual(p["phenomena"][0]["name"],"Vent violent")
        self.assertEqual(p["bulletin_updated"],self.product["update_time"])
    def test_options_independent(self):
        a,b=normalize_options({}),normalize_options({})
        a["recipients"].append({"id":"x"})
        self.assertEqual(b["recipients"],[])
