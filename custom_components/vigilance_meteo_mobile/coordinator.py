import asyncio
import json
import logging
from datetime import timedelta
from pathlib import Path
from homeassistant.exceptions import ConfigEntryAuthFailed, HomeAssistantError
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.storage import Store
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .api import InvalidAuth, async_fetch
from .const import DOMAIN, NAME, DEFAULT_OPTIONS
from .logic import department, excluded_departments, current_period, zone_for, build_payload

_LOGGER = logging.getLogger(__name__)

class VigilanceCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, entry):
        self.settings = {**DEFAULT_OPTIONS, **entry.options}
        self.api_key = entry.data["api_key"]
        super().__init__(hass, _LOGGER, name=NAME, config_entry=entry, update_interval=timedelta(minutes=int(self.settings["interval"])))
        self.store = Store(hass, 1, f"{DOMAIN}.{entry.entry_id}")
        self.sent = {}
        self.names = {}
        self.lock = asyncio.Lock()
        self.suspend_notifications = False

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
        if code in excluded_departments(self.settings["exclusions"]):
            return {"status": "departement_exclu", "department": code}
        period = current_period(self.data)
        if not period:
            return {"status": "bulletin_perime"}
        zone = zone_for(period, code)
        if not zone:
            return {"status": "departement_absent", "department": code}
        try:
            result = build_payload(self.data, period, zone, code, self.names[code], self.hass.config.time_zone)
        except (ValueError, TypeError, KeyError):
            return {"status": "bulletin_invalide", "department": code}
        return {**result, "status": "ok", "department": code}

    async def async_notify(self, test=False, recipient=None):
        outcomes = {}
        async with self.lock:
            if not test and self.suspend_notifications:
                return outcomes
            dirty = False
            for phone in self.settings.get("recipients", []):
                if recipient and phone["id"] != recipient:
                    continue
                result = self.result(phone)
                outcomes[phone["id"]] = result["status"]
                if result["status"] != "ok":
                    continue
                if not test:
                    if not self.settings["enabled"]:
                        outcomes[phone["id"]] = "automatique_desactive"
                        continue
                    if result["level"] < int(self.settings["minimum"]):
                        outcomes[phone["id"]] = "sous_le_seuil"
                        continue
                    if self.sent.get(phone["id"]) == result["signature"]:
                        outcomes[phone["id"]] = "deja_envoye"
                        continue
                domain, service = phone["notification"].split(".", 1)
                if not self.hass.services.has_service(domain, service):
                    outcomes[phone["id"]] = "action_notification_absente"
                    continue
                try:
                    await self.hass.services.async_call(domain, service, {
                        "message": ("TEST — " if test else "") + result["message"],
                        "data": {"notification_icon": result["icon"], "color": result["color"], "tag": f"{DOMAIN}_{phone['id']}_{'test' if test else 'alert'}"}
                    }, blocking=True)
                except HomeAssistantError:
                    _LOGGER.warning("Échec d'envoi à un destinataire configuré")
                    outcomes[phone["id"]] = "erreur_notification"
                    continue
                outcomes[phone["id"]] = "test_envoye" if test else "envoye"
                if not test:
                    self.sent[phone["id"]] = result["signature"]
                    dirty = True
            if dirty:
                await self.store.async_save(self.sent)
        self.hass.bus.async_fire(f"{DOMAIN}_result", {"test": test, "results": outcomes})
        return outcomes
