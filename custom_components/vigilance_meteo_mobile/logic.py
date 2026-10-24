import hashlib
import json
import unicodedata
from copy import deepcopy
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from .const import COLORS, HEX_COLORS, PHENOMENA, ICONS, DEFAULT_OPTIONS


def normalize(value):
    value = str(value or "").lower().replace("’", "'")
    return " ".join("".join(c for c in unicodedata.normalize("NFKD", value) if not unicodedata.combining(c)).split())


def normalize_options(options):
    result = {**deepcopy(DEFAULT_OPTIONS), **deepcopy(dict(options))}
    for phone in result["recipients"]:
        if "notifications" not in phone:
            phone["notifications"] = [phone.pop("notification")] if phone.get("notification") else []
        phone["notifications"] = list(dict.fromkeys(phone["notifications"]))
    return result


def department(attributes, names):
    if str(attributes.get("iso_country_code", "")).upper().strip() != "FR":
        return None
    name = normalize(attributes.get("sub_administrative_area"))
    return next((code for code, label in names.items() if normalize(label) == name), None)


def excluded_departments(value):
    return {v.strip().upper().zfill(2) for v in str(value or "").replace(";", ",").split(",") if v.strip()}


def timestamp(value):
    if not isinstance(value, str):
        raise ValueError("Horodatage absent")
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if result.tzinfo is None:
        raise ValueError("Fuseau horaire absent")
    return result


def current_period(product, now=None):
    now = now or datetime.now(timezone.utc)
    for period in product.get("periods", []):
        if period.get("echeance") != "J":
            continue
        try:
            if timestamp(period.get("begin_validity_time")) <= now < timestamp(period.get("end_validity_time")):
                return period
        except (TypeError, ValueError):
            continue
    return None


def zone_for(period, code):
    return next((z for z in (period or {}).get("timelaps", {}).get("domain_ids", []) if str(z.get("domain_id")) == code), None)


def build_payload(product, period, zone, code, name, tz_name):
    level = int(zone.get("max_color_id", 0))
    if level not in COLORS:
        raise ValueError("Niveau inconnu")
    tz = ZoneInfo(tz_name)
    lines = [f"Vigilance météo : {name} ({code}).", f"Niveau maximal du bulletin d'aujourd'hui : {COLORS[level]}."]
    signed, details = [], []
    for item in zone.get("phenomenon_items", []):
        maximum = int(item.get("phenomenon_max_color_id", 0))
        if maximum <= 1:
            continue
        if maximum not in COLORS:
            raise ValueError("Niveau de phénomène inconnu")
        identifier = str(item.get("phenomenon_id"))
        windows, signed_windows = [], []
        for window in item.get("timelaps_items", []):
            color = int(window.get("color_id", 0))
            if color <= 1:
                continue
            if color not in COLORS:
                raise ValueError("Niveau de créneau inconnu")
            begin, end = timestamp(window.get("begin_time")), timestamp(window.get("end_time"))
            if end <= begin:
                raise ValueError("Créneau invalide")
            windows.append(f"{COLORS[color]} du {begin.astimezone(tz):%d/%m à %H:%M} au {end.astimezone(tz):%d/%m à %H:%M}")
            signed_windows.append((begin.isoformat(), end.isoformat(), color))
        detail = "; ".join(windows) if windows else f"{COLORS[maximum]} — horaires non fournis"
        label = PHENOMENA.get(identifier, 'Phénomène ' + identifier)
        lines.append(f"{label} : {detail}.")
        details.append({"id": identifier, "name": label, "level": maximum, "color": COLORS[maximum], "windows": windows})
        signed.append((identifier, maximum, sorted(signed_windows)))
    if not details:
        lines.append("Aucun phénomène départemental en jaune, orange ou rouge dans ce bulletin.")
    lines.extend(["Bulletin selon votre dernière position connue.", "Bulletin mis à jour : " + str(product.get("update_time", "non fourni"))])
    highest = max((p[1] for p in signed), default=1)
    leading = [p[0] for p in signed if p[1] == highest]
    icon = ICONS.get(leading[0], "mdi:alert") if len(leading) == 1 else ("mdi:alert" if leading else "mdi:weather-partly-cloudy")
    signature = hashlib.sha256(json.dumps([code, period.get("begin_validity_time"), level, sorted(signed)], ensure_ascii=False).encode()).hexdigest()
    return {"message": "\n".join(lines), "icon": icon, "color": HEX_COLORS[level], "signature": signature, "level": level, "phenomena": details, "bulletin_updated": product.get("update_time"), "period_end": period.get("end_validity_time")}
