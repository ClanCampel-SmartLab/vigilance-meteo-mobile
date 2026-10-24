from homeassistant.const import Platform
from homeassistant.core import SupportsResponse
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.event import async_track_state_change_event
from .const import DOMAIN
from .coordinator import VigilanceCoordinator

PLATFORMS = [Platform.SENSOR]

async def async_setup_entry(hass, entry):
    coordinator = VigilanceCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    def schedule():
        if coordinator.last_update_success and not coordinator.suspend_notifications:
            entry.async_create_background_task(hass, coordinator.async_notify(), "Vigilance notifications")
    entry.async_on_unload(coordinator.async_add_listener(schedule))
    def position_changed(event):
        coordinator.async_update_listeners()
    sensors = [p["sensor"] for p in coordinator.settings["recipients"]]
    entry.async_on_unload(async_track_state_change_event(hass, sensors, position_changed))
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    async def handle_service(call):
        requested = call.data.get("entry_id")
        entries = hass.data.get(DOMAIN, {})
        if requested and requested not in entries:
            raise HomeAssistantError("Entrée introuvable")
        results = {}
        for identifier, current in list(entries.items()):
            if requested and requested != identifier:
                continue
            recipient = call.data.get("recipient_id")
            if recipient and recipient not in {p["id"] for p in current.settings["recipients"]}:
                raise HomeAssistantError("Destinataire inconnu")
            if call.service == "test":
                current.suspend_notifications = True
                try:
                    await current.async_request_refresh()
                    results[identifier] = await current.async_notify(test=True, recipient=recipient)
                finally:
                    current.suspend_notifications = False
            else:
                await current.async_request_refresh()
                results[identifier] = {"updated": current.last_update_success}
        return {"results": results}

    for name in ("test", "refresh"):
        if not hass.services.has_service(DOMAIN, name):
            hass.services.async_register(DOMAIN, name, handle_service, supports_response=SupportsResponse.OPTIONAL)
    if coordinator.settings["enabled"]:
        schedule()
    return True

async def async_reload_entry(hass, entry):
    await hass.config_entries.async_reload(entry.entry_id)

async def async_unload_entry(hass, entry):
    if await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id, None)
        if not hass.data[DOMAIN]:
            for name in ("test", "refresh"):
                hass.services.async_remove(DOMAIN, name)
        return True
    return False
