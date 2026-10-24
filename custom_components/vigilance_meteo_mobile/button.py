from homeassistant.components.button import ButtonEntity
from .const import DOMAIN
from .entity import hub_info, recipient_info

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([RefreshButton(coordinator)] + [TestButton(coordinator, p) for p in coordinator.settings["recipients"]])

class RefreshButton(ButtonEntity):
    _attr_has_entity_name = True
    _attr_name = "Actualiser le bulletin"
    _attr_icon = "mdi:refresh"
    _attr_should_poll = False

    def __init__(self, coordinator):
        self.coordinator = coordinator
        self._attr_unique_id = f"{DOMAIN}_{coordinator.entry.entry_id}_refresh"
        self._attr_device_info = hub_info(coordinator.entry.entry_id)

    async def async_press(self):
        await self.coordinator.async_request_refresh()

class TestButton(ButtonEntity):
    _attr_has_entity_name = True
    _attr_name = "Envoyer une notification de test"
    _attr_icon = "mdi:bell-check-outline"
    _attr_should_poll = False

    def __init__(self, coordinator, phone):
        self.coordinator, self.phone = coordinator, phone
        self._attr_unique_id = f"{DOMAIN}_{phone['id']}_test"
        self._attr_device_info = recipient_info(coordinator.entry.entry_id, phone)

    async def async_press(self):
        await self.coordinator.async_test(recipient=self.phone["id"])
