import uuid
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .api import InvalidAuth, async_fetch
from .const import DOMAIN, NAME, REPOSITORY, API_PORTAL
from .logic import excluded_departments, normalize_options
from .discovery import geocoded_choices, notification_choices

LINKS = {"api_guide": REPOSITORY + "/blob/main/docs/API.md", "api_portal": API_PORTAL, "phone_guide": REPOSITORY + "/blob/main/docs/INSTALLATION.md"}

class RecipientWizard:
    def begin(self, options=None):
        self.settings = normalize_options(options or {})
        self.phones = self.settings.pop("recipients")
        self.editing = None

    async def async_step_settings(self, user_input=None):
        errors = {}
        if user_input is not None:
            codes = {f"{n:02}" for n in range(1, 96) if n != 20} | {"2A", "2B"}
            if not excluded_departments(user_input.get("exclusions", "")) <= codes:
                errors["base"] = "invalid_departments"
            else:
                self.settings.update(user_input)
                return await self.async_step_menu()
        schema = vol.Schema({
            vol.Required("interval", default=self.settings["interval"]): vol.All(vol.Coerce(int), vol.Range(min=15, max=1440)),
            vol.Required("minimum", default=str(self.settings["minimum"])): selector.SelectSelector(selector.SelectSelectorConfig(options=[{"value": "1", "label": "Vert (y compris sans alerte)"}, {"value": "2", "label": "Jaune"}, {"value": "3", "label": "Orange"}, {"value": "4", "label": "Rouge"}])),
            vol.Optional("exclusions", default=self.settings["exclusions"]): str,
            vol.Required("enabled", default=self.settings["enabled"]): bool,
        })
        return self.async_show_form(step_id="settings", data_schema=schema, errors=errors)

    async def async_step_menu(self, user_input=None):
        choices = ["add_recipient", "settings"]
        if self.phones:
            choices += ["edit_recipient", "remove_recipient", "finish"]
        return self.async_show_menu(step_id="menu", menu_options=choices, description_placeholders={"count": str(len(self.phones))})

    async def async_step_add_recipient(self, user_input=None):
        self.editing = None
        return await self.async_step_recipient(user_input)

    async def async_step_edit_recipient(self, user_input=None):
        if user_input is not None:
            self.editing = next(p for p in self.phones if p["id"] == user_input["recipient"])
            return await self.async_step_recipient()
        return self.async_show_form(step_id="edit_recipient", data_schema=self.pick_recipient())

    def pick_recipient(self):
        return vol.Schema({vol.Required("recipient"): selector.SelectSelector(selector.SelectSelectorConfig(options=[{"value": p["id"], "label": p["name"]} for p in self.phones]))})

    async def async_step_recipient(self, user_input=None):
        sensors, notifications = geocoded_choices(self.hass), notification_choices(self.hass)
        if not sensors or not notifications:
            return await self.async_step_phone_help()
        errors = {}
        values = self.editing or {}
        if user_input is not None:
            selected = user_input.get("notifications", [])
            if user_input["sensor"] not in {s["value"] for s in sensors}:
                errors["base"] = "invalid_sensor"
            elif not selected or not set(selected) <= set(notifications):
                errors["base"] = "invalid_service"
            elif any(p["sensor"] == user_input["sensor"] for p in self.phones if not self.editing or p["id"] != self.editing["id"]):
                errors["base"] = "duplicate_sensor"
            else:
                default_name = next(s["name"] for s in sensors if s["value"] == user_input["sensor"])
                phone = {"id": self.editing["id"] if self.editing else uuid.uuid4().hex, "name": user_input.get("name", "").strip() or default_name, "sensor": user_input["sensor"], "notifications": list(dict.fromkeys(selected))}
                self.phones = [p for p in self.phones if p["id"] != phone["id"]] + [phone]
                self.editing = None
                return await self.async_step_menu()
            values = user_input
        sensor_field = vol.Required("sensor", default=values["sensor"]) if values.get("sensor") else vol.Required("sensor")
        notification_field = vol.Required("notifications", default=values["notifications"]) if values.get("notifications") else vol.Required("notifications")
        schema = vol.Schema({
            sensor_field: selector.SelectSelector(selector.SelectSelectorConfig(options=[{"value": s["value"], "label": s["label"]} for s in sensors])),
            notification_field: selector.SelectSelector(selector.SelectSelectorConfig(options=notifications, multiple=True)),
            vol.Optional("name", default=values.get("name", "")): str,
        })
        return self.async_show_form(step_id="recipient", data_schema=schema, errors=errors, description_placeholders=LINKS)

    async def async_step_phone_help(self, user_input=None):
        if user_input is not None:
            return await self.async_step_recipient()
        return self.async_show_form(step_id="phone_help", data_schema=vol.Schema({}), description_placeholders=LINKS)

    async def async_step_remove_recipient(self, user_input=None):
        if user_input is not None:
            self.phones = [p for p in self.phones if p["id"] != user_input["recipient"]]
            return await self.async_step_menu()
        return self.async_show_form(step_id="remove_recipient", data_schema=self.pick_recipient())

    def summary(self):
        phones = "\n".join(f"- **{p['name']}** : {len(p['notifications'])} destination(s) de notification." for p in self.phones)
        return {"recipients": phones, "interval": str(self.settings["interval"]), "minimum": str(self.settings["minimum"]), "exclusions": self.settings["exclusions"] or "Aucune", "automatic": "Activées" if self.settings["enabled"] else "Désactivées"}

    async def async_step_finish(self, user_input=None):
        if not self.phones:
            return await self.async_step_menu()
        if user_input is not None:
            return self.save_result()
        return self.async_show_form(step_id="finish", data_schema=vol.Schema({}), description_placeholders=self.summary())

class ConfigFlow(RecipientWizard, config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 2

    async def key_form(self, step_id, user_input):
        errors = {}
        if user_input is not None:
            try:
                await async_fetch(async_get_clientsession(self.hass), user_input["api_key"].strip())
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except ValueError:
                errors["base"] = "invalid_response"
            except Exception:
                errors["base"] = "cannot_connect"
            else:
                key = user_input["api_key"].strip()
                if step_id == "reauth_confirm":
                    return self.async_update_reload_and_abort(self._get_reauth_entry(), data_updates={"api_key": key})
                if step_id == "reconfigure":
                    return self.async_update_reload_and_abort(self._get_reconfigure_entry(), data_updates={"api_key": key})
                self.api_key = key
                self.begin()
                return await self.async_step_menu()
        return self.async_show_form(step_id=step_id, data_schema=vol.Schema({vol.Required("api_key"): selector.TextSelector(selector.TextSelectorConfig(type=selector.TextSelectorType.PASSWORD))}), errors=errors, description_placeholders=LINKS)

    async def async_step_user(self, user_input=None):
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")
        return await self.key_form("user", user_input)

    async def async_step_reauth(self, entry_data):
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(self, user_input=None):
        return await self.key_form("reauth_confirm", user_input)

    async def async_step_reconfigure(self, user_input=None):
        return await self.key_form("reconfigure", user_input)

    def save_result(self):
        return self.async_create_entry(title=NAME, data={"api_key": self.api_key}, options={**self.settings, "recipients": self.phones})

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return OptionsFlow(config_entry)

class OptionsFlow(RecipientWizard, config_entries.OptionsFlow):
    def __init__(self, entry):
        self.begin(entry.options)

    async def async_step_init(self, user_input=None):
        return await self.async_step_menu()

    def save_result(self):
        return self.async_create_entry(title="", data={**self.settings, "recipients": self.phones})
