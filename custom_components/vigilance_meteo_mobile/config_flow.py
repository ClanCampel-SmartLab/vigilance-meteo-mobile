import uuid
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .api import InvalidAuth, async_fetch
from .const import DOMAIN, NAME, DEFAULT_OPTIONS
from .logic import excluded_departments


class RecipientWizard:
    def begin(self, options=None):
        self.settings = {**DEFAULT_OPTIONS, **(options or {})}
        self.phones = [dict(p) for p in self.settings.get("recipients", [])]

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
            choices += ["remove_recipient", "finish"]
        return self.async_show_menu(step_id="menu", menu_options=choices)

    async def async_step_add_recipient(self, user_input=None):
        available = sorted("notify." + name for name in self.hass.services.async_services().get("notify", {}) if name.startswith("mobile_app_"))
        if not available:
            return self.async_abort(reason="no_notification_service")
        errors = {}
        if user_input is not None:
            if user_input["notification"] not in available:
                errors["base"] = "invalid_service"
            elif any(p["sensor"] == user_input["sensor"] or p["notification"] == user_input["notification"] for p in self.phones):
                errors["base"] = "duplicate_recipient"
            else:
                self.phones.append({"id": uuid.uuid4().hex, **user_input})
                return await self.async_step_menu()
        schema = vol.Schema({
            vol.Required("name"): str,
            vol.Required("sensor"): selector.EntitySelector(selector.EntitySelectorConfig(domain="sensor")),
            vol.Required("notification"): selector.SelectSelector(selector.SelectSelectorConfig(options=available)),
        })
        return self.async_show_form(step_id="add_recipient", data_schema=schema, errors=errors)

    async def async_step_remove_recipient(self, user_input=None):
        if user_input is not None:
            self.phones = [p for p in self.phones if p["id"] != user_input["recipient"]]
            return await self.async_step_menu()
        schema = vol.Schema({vol.Required("recipient"): selector.SelectSelector(selector.SelectSelectorConfig(options=[{"value": p["id"], "label": p["name"]} for p in self.phones]))})
        return self.async_show_form(step_id="remove_recipient", data_schema=schema)


class ConfigFlow(RecipientWizard, config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

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
                return await self.async_step_settings()
        schema = vol.Schema({vol.Required("api_key"): selector.TextSelector(selector.TextSelectorConfig(type=selector.TextSelectorType.PASSWORD))})
        return self.async_show_form(step_id=step_id, data_schema=schema, errors=errors)

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

    async def async_step_finish(self, user_input=None):
        if not self.phones:
            return await self.async_step_menu()
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

    async def async_step_finish(self, user_input=None):
        if not self.phones:
            return await self.async_step_menu()
        return self.async_create_entry(title="", data={**self.settings, "recipients": self.phones})
