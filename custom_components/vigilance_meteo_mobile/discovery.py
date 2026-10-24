from homeassistant.helpers import entity_registry as er, device_registry as dr
from .logic import normalize


def geocoded_choices(hass):
    registry, devices = er.async_get(hass), dr.async_get(hass)
    choices = []
    for state in hass.states.async_all("sensor"):
        entry = registry.async_get(state.entity_id)
        if entry and entry.disabled_by is not None:
            continue
        identifiers = " ".join(str(v or "") for v in (state.entity_id, entry.unique_id if entry else "", entry.original_name if entry else "", state.attributes.get("friendly_name")))
        has_attributes = "iso_country_code" in state.attributes and "sub_administrative_area" in state.attributes
        if not has_attributes and not any(token in normalize(identifiers) for token in ("geocoded", "geocodee", "geocode")):
            continue
        device = devices.async_get(entry.device_id) if entry and entry.device_id else None
        label = (device.name_by_user or device.name) if device else None
        if not label:
            label = state.attributes.get("friendly_name") or state.entity_id
        status = "position pas encore reçue" if state.state == "unknown" else ("indisponible" if state.state == "unavailable" else ("localisation disponible" if has_attributes else "attributs à vérifier"))
        choices.append({"value": state.entity_id, "label": f"{label} — {status}", "name": label})
    return sorted(choices, key=lambda option: option["label"].lower())


def notification_choices(hass):
    return sorted("notify." + name for name in hass.services.async_services().get("notify", {}) if name.startswith("mobile_app_"))
