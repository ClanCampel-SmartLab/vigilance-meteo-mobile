from homeassistant.helpers.device_registry import DeviceInfo
from .const import DOMAIN, NAME, VERSION

def hub_info(entry_id):
    return DeviceInfo(identifiers={(DOMAIN, entry_id)}, name=NAME, manufacturer="by clan'campel", model="Bulletin national Météo-France", sw_version=VERSION)

def recipient_info(entry_id, phone):
    return DeviceInfo(identifiers={(DOMAIN, f"{entry_id}_{phone['id']}")}, name=f"Vigilance météo — {phone['name']}", manufacturer="by clan'campel", model="Suivi virtuel d'un destinataire", sw_version=VERSION, via_device=(DOMAIN, entry_id))
