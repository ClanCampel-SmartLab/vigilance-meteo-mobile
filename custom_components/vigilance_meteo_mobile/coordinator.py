import asyncio
import json
import logging
from datetime import timedelta
from pathlib import Path
from homeassistant.exceptions import ConfigEntryAuthFailed, HomeAssistantError
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.storage import Store
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util
from .api import InvalidAuth, async_fetch
from .const import DOMAIN, NAME
from .logic import normalize_options, department, excluded_departments, current_period, zone_for, build_payload

_LOGGER = logging.getLogger(__name__)

class VigilanceCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, entry):
        self.entry = entry
        self.settings = normalize_options(entry.options)
        self.api_key = entry.data["api_key"]
        super().__init__(hass, _LOGGER, name=NAME, config_entry=entry, update_interval=timedelta(minutes=int(self.settings["interval"])))
        self.store = Store(hass, 1, f"{DOMAIN}.{entry.entry_id}")
        self.sent, self.names, self.last_tests = {}, {}, {}
        self.notify_lock, self.test_lock = asyncio.Lock(), asyncio.Lock()
        self.suspend_notifications = False
        self.publishing_status = False

    async def _async_setup(self):
        self.sent = await self.store.async_load() or {}
        self.names = await self.hass.async_add_executor_job(lambda: json.loads(Path(__file__).with_name("departments.json").read_text(encoding="utf-8")))

    async def _async_update_data(self):
        try:
            return await async_fetch(async_get_clientsession(self.hass), self.api_key)
        except InvalidAuth as err:
            raise ConfigEntryAuthFailed("Accès Météo-France refusé") from err
        except Exception as err:
            raise UpdateFailed("Impossible de récupérer un bulletin Météo-France valide") from err

    def result(self, phone):
        if not self.last_update_success or not self.data:
            return {"status": "api_indisponible"}
        state = self.hass.states.get(phone["sensor"])
        if state is None or state.state in ("unknown", "unavailable"):
            return {"status": "position_inconnue"}
        code = department(state.attributes, self.names)
        if not code:
            return {"status": "departement_non_pris_en_charge"}
        common = {"department": code, "department_name": self.names[code]}
        period = current_period(self.data)
        if not period:
            return {**common, "status": "bulletin_perime"}
        zone = zone_for(period, code)
        if not zone:
            return {**common, "status": "departement_absent"}
        try:
            info = build_payload(self.data, period, zone, code, self.names[code], self.hass.config.time_zone)
        except (ValueError, TypeError, KeyError):
            return {**common, "status": "bulletin_invalide"}
        excluded = code in excluded_departments(self.settings["exclusions"])
        return {**common, **info, "status": "departement_exclu" if excluded else "ok"}

    def publish_status(self):
        self.publishing_status = True
        try:
            self.async_update_listeners()
        finally:
            self.publishing_status = False

    async def async_test(self, recipient=None):
        if recipient and recipient not in {p["id"] for p in self.settings["recipients"]}:
            raise HomeAssistantError("Destinataire introuvable")
        async with self.test_lock:
            self.suspend_notifications = True
            try:
                await self.async_request_refresh()
                return await self.async_notify(test=True, recipient=recipient)
            finally:
                self.suspend_notifications = False

    async def async_notify(self, test=False, recipient=None):
        results = {}
        async with self.notify_lock:
            if not test and self.suspend_notifications:
                return results
            dirty = False
            for phone in self.settings["recipients"]:
                if recipient and phone["id"] != recipient:
                    continue
                info = self.result(phone)
                status = info["status"]
                destinations = {}
                if status == "ok" and not test:
                    if not self.settings["enabled"]:
                        status = "automatique_desactive"
                    elif info["level"] < int(self.settings["minimum"]):
                        status = "sous_le_seuil"
                if status == "ok":
                    for action in phone["notifications"]:
                        signature_key = f"{phone['id']}|{action}"
                        if not test and self.sent.get(signature_key) == info["signature"]:
                            destinations[action] = "deja_envoye"
                            continue
                        domain, service = action.split(".", 1)
                        if not self.hass.services.has_service(domain, service):
                            destinations[action] = "action_notification_absente"
                            continue
                        try:
                            await self.hass.services.async_call(domain, service, {
                                "message": ("TEST — " if test else "") + info["message"],
                                "data": {"notification_icon": info["icon"], "color": info["color"], "tag": f"{DOMAIN}_{phone['id']}_{'test' if test else 'alert'}"}
                            }, blocking=True)
                        except HomeAssistantError:
                            _LOGGER.warning("Échec d'envoi à une destination configurée")
                            destinations[action] = "erreur_notification"
                            continue
                        destinations[action] = "test_envoye" if test else "envoye"
                        if not test:
                            self.sent[signature_key] = info["signature"]
                            dirty = True
                    values = list(destinations.values())
                    success = "test_envoye" if test else "envoye"
                    status = success if values and all(v == success for v in values) else ("deja_envoye" if values and all(v == "deja_envoye" for v in values) else "resultat_partiel")
                outcome = {"status": status, "destinations": destinations}
                results[phone["id"]] = outcome
                if test:
                    self.last_tests[phone["id"]] = {"status": status, "time": dt_util.utcnow().isoformat()}
            if dirty:
                await self.store.async_save(self.sent)
        self.hass.bus.async_fire(f"{DOMAIN}_result", {"test": test, "results": results})
        if test:
            self.publish_status()
        return results
