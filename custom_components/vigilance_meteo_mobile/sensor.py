from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, COLORS

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([VigilanceSensor(coordinator, phone) for phone in coordinator.settings["recipients"]])

class VigilanceSensor(CoordinatorEntity, SensorEntity):
    _attr_icon = "mdi:weather-cloudy-alert"
    _attr_should_poll = False

    def __init__(self, coordinator, phone):
        super().__init__(coordinator)
        self.phone = phone
        self._attr_unique_id = f"{DOMAIN}_{phone['id']}"
        self._attr_name = f"Vigilance météo {phone['name']}"

    @property
    def native_value(self):
        result = self.coordinator.result(self.phone)
        return COLORS.get(result.get("level")) if result["status"] == "ok" else result["status"]

    @property
    def extra_state_attributes(self):
        result = self.coordinator.result(self.phone)
        return {"status": result["status"], "department": result.get("department"), "recipient_id": self.phone["id"], "position_sensor": self.phone["sensor"], "automatic_notifications": bool(self.coordinator.settings["enabled"]), "minimum_level": int(self.coordinator.settings["minimum"])}
