import copy
import json
import unittest
from pathlib import Path
from datetime import datetime, timezone
from custom_components.vigilance_meteo_mobile.api import extract_product
from custom_components.vigilance_meteo_mobile.const import DEFAULT_OPTIONS
from custom_components.vigilance_meteo_mobile.logic import department, excluded_departments, current_period, zone_for, build_payload, timestamp

class LogicTests(unittest.TestCase):
    def setUp(self):
        self.period = {"echeance":"J", "begin_validity_time":"2026-10-24T04:00:00Z", "end_validity_time":"2026-10-24T22:00:00Z", "timelaps":{"domain_ids":[]}}
        self.zone = {"domain_id":"56", "max_color_id":2, "phenomenon_items":[{"phenomenon_id":"1", "phenomenon_max_color_id":2, "timelaps_items":[{"begin_time":"2026-10-24T18:00:00Z", "end_time":"2026-10-24T22:00:00Z", "color_id":2}]}]}
        self.product = {"periods":[self.period], "update_time":"2026-10-24T04:00:11Z"}
    def payload(self):
        return build_payload(self.product,self.period,self.zone,"56","Morbihan","Europe/Paris")
    def test_default_no_exclusion(self):
        self.assertEqual(DEFAULT_OPTIONS["exclusions"], "")
        self.assertEqual(excluded_departments(DEFAULT_OPTIONS["exclusions"]), set())
    def test_default_automatic_disabled(self):
        self.assertFalse(DEFAULT_OPTIONS["enabled"])
    def test_no_default_phone(self):
        self.assertEqual(DEFAULT_OPTIONS["recipients"], [])
    def test_department(self):
        self.assertEqual(department({"iso_country_code":"FR","sub_administrative_area":"Morbihan"},{"56":"Morbihan"}),"56")
    def test_apostrophe(self):
        self.assertEqual(department({"iso_country_code":"FR","sub_administrative_area":"Côtes-d’Armor"},{"22":"Côtes-d'Armor"}),"22")
    def test_foreign(self):
        self.assertIsNone(department({"iso_country_code":"BE","sub_administrative_area":"Morbihan"},{"56":"Morbihan"}))
    def test_missing_attributes(self):
        self.assertIsNone(department({}, {"56":"Morbihan"}))
    def test_exclusions(self):
        self.assertEqual(excluded_departments("2a;01,35"),{"2A","01","35"})
    def test_corsica(self):
        self.assertEqual(department({"iso_country_code":"FR","sub_administrative_area":"Haute-Corse"},{"2B":"Haute-Corse"}),"2B")
    def test_valid_period(self):
        self.assertIsNotNone(current_period(self.product,datetime(2026,10,24,12,tzinfo=timezone.utc)))
    def test_expired_period(self):
        self.assertIsNone(current_period(self.product,datetime(2026,10,25,12,tzinfo=timezone.utc)))
    def test_end_exclusive(self):
        self.assertIsNone(current_period(self.product,datetime(2026,10,24,22,tzinfo=timezone.utc)))
    def test_bad_dates(self):
        self.period["begin_validity_time"]="wrong"
        self.assertIsNone(current_period(self.product))
    def test_naive_dates_rejected(self):
        with self.assertRaises(ValueError): timestamp("2026-10-24T12:00:00")
    def test_missing_zone(self):
        self.assertIsNone(zone_for(self.period,"56"))
    def test_coastal_not_department(self):
        self.period["timelaps"]["domain_ids"]=[{"domain_id":"5610"}]
        self.assertIsNone(zone_for(self.period,"56"))
    def test_wind_icon_color_and_time(self):
        p=self.payload()
        self.assertEqual(p["icon"],"mdi:weather-windy")
        self.assertEqual(p["color"],"#FFEB3B")
        self.assertIn("24/10 à 20:00",p["message"])
    def test_tied_level(self):
        self.zone["phenomenon_items"].append({"phenomenon_id":"2","phenomenon_max_color_id":2})
        self.assertEqual(self.payload()["icon"],"mdi:alert")
    def test_highest_priority(self):
        self.zone["max_color_id"]=3
        self.zone["phenomenon_items"].append({"phenomenon_id":"6","phenomenon_max_color_id":3})
        self.assertEqual(self.payload()["icon"],"mdi:thermometer-high")
        self.assertEqual(self.payload()["color"],"#FF9800")
    def test_green(self):
        self.zone.update(max_color_id=1,phenomenon_items=[])
        self.assertEqual(self.payload()["icon"],"mdi:weather-partly-cloudy")
    def test_invalid_level(self):
        self.zone["max_color_id"]=7
        with self.assertRaises(ValueError):self.payload()
    def test_signature_ignores_publication(self):
        a=self.payload()["signature"]
        self.product["update_time"]="2026-10-24T12:00:00Z"
        self.assertEqual(a,self.payload()["signature"])
    def test_signature_changes_with_window(self):
        a=self.payload()["signature"]
        self.zone["phenomenon_items"][0]["timelaps_items"][0]["begin_time"]="2026-10-24T17:00:00Z"
        self.assertNotEqual(a,self.payload()["signature"])
    def test_direct_api_shape(self):
        self.assertIs(extract_product({"product":self.product}),self.product)
    def test_wrapped_api_shape(self):
        self.assertIs(extract_product({"content":{"product":self.product}}),self.product)
    def test_bad_api_shape(self):
        with self.assertRaises(ValueError): extract_product({"error":"bad"})
    def test_department_list_complete_and_unique(self):
        path=Path(__file__).resolve().parents[1]/"custom_components/vigilance_meteo_mobile/departments.json"
        names=json.loads(path.read_text())
        self.assertEqual(len(names),96)
        self.assertEqual(len(set(names.values())),96)
        self.assertEqual(names["48"],"Lozère")
        self.assertEqual(names["65"],"Hautes-Pyrénées")
