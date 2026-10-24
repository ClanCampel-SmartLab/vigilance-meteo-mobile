from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, COLORS
from .entity import recipient_info

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([VigilanceSensor(coordinator, p) for p in coordinator.settings["recipients"]])

class VigilanceSensor(CoordinatorEntity, SensorEntity):
    _attr_should_poll = False
    _attr_has_entity_name = True
    _attr_name = "Vigilance"

    def __init__(self, coordinator, phone):
        super().__init__(coordinator)
        self.phone = phone
        self._attr_unique_id = f"{DOMAIN}_{phone['id']}"
        self._attr_device_info = recipient_info(coordinator.entry.entry_id, phone)

    @property
    def native_value(self):
        info = self.coordinator.result(self.phone)
        return COLORS.get(info.get("level")) if info["status"] == "ok" else info["status"]

    @property
    def icon(self):
        return self.coordinator.result(self.phone).get("icon", "mdi:weather-cloudy-alert")

    @property
    def extra_state_attributes(self):
        info = self.coordinator.result(self.phone)
        test = self.coordinator.last_tests.get(self.phone["id"], {})
        return {
            "status": info["status"], "recipient_id": self.phone["id"], "recipient_name": self.phone["name"],
            "position_sensor": self.phone["sensor"], "department": info.get("department"), "department_name": info.get("department_name"),
            "level": info.get("level"), "level_name": COLORS.get(info.get("level")), "color": info.get("color"),
            "phenomena": info.get("phenomena", []), "bulletin_updated": info.get("bulletin_updated"),
            "period_end": info.get("period_end"), "automatic_notifications": bool(self.coordinator.settings["enabled"]),
            "minimum_level": int(self.coordinator.settings["minimum"]), "last_test_status": test.get("status"),
            "last_test_time": test.get("time"), "notification_destination_count": len(self.phone["notifications"]),
        }
