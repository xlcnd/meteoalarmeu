"""Config flow for meteoalarmeu integration."""
import logging

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant import config_entries, exceptions
from homeassistant.const import CONF_NAME

from .client import AWARENESS_TYPES as AWARENESS_TYPES_API
from .client import (
    MeteoAlarmUnavailableLanguageError,
    MeteoAlarmUnrecognizedCountryError,
    MeteoAlarmUnrecognizedRegionError,
    get_languages,
    get_regions,
)
from .const import DOMAIN  # pylint:disable=unused-import
from .const import (
    CONF_AWARENESS_TYPES,
    CONF_COUNTRY,
    CONF_LANGUAGE,
    CONF_REGION,
    DEFAULT_LANGUAGE,
    DEFAULT_NAME,
)
from .resources import cmap, lmap, ui_countries_list, ui_languages_list

COUNTRIES = ui_countries_list
LANGUAGES = [DEFAULT_LANGUAGE]
LANGUAGES.extend(ui_languages_list)
DEFAULT_AWARENESS_TYPES = sorted(AWARENESS_TYPES_API)

_LOGGER = logging.getLogger(__name__)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for meteoalarmeu."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        self._languages = LANGUAGES
        self._regions = [""]
        self._country = ""
        self._data = {}

    async def async_already_configured(self):
        for entry in self._async_current_entries():
            if entry.unique_id == DEFAULT_NAME:
                return True
        return False

    # pylint: disable=broad-except
    async def async_step_user(self, user_input=None):
        """Handle the main step."""
        if await self.async_already_configured():
            return self.async_abort(reason="already_configured")

        errors = {}

        if user_input is not None:
            try:
                info = await self.validate_country(user_input)

                # Sync 'regions' and 'languages'
                await self.async_get_regions()
                await self.async_get_languages()

                # Add 'name'
                info[CONF_NAME] = DEFAULT_NAME

                return await self.async_step_other(data=info)

            except MeteoAlarmUnrecognizedCountryError:
                errors["country"] = "unrecognized_country"
                user_input[CONF_COUNTRY] = ""
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_COUNTRY): vol.In(COUNTRIES),
                }
            ),
            errors=errors,
        )

    async def validate_country(self, data):
        """Validate country."""
        if data[CONF_COUNTRY] not in COUNTRIES:
            raise MeteoAlarmUnrecognizedCountryError
        self._country = data[CONF_COUNTRY]

        # Return info that you want to store in the config entry.
        return {
            CONF_COUNTRY: data[CONF_COUNTRY],
        }

    # pylint: disable=broad-except
    async def async_step_other(self, user_input=None, data=None):
        """Handle the sub step."""
        errors = {}

        # Hold passed 'data'
        if data:
            self._data = data

        if user_input is not None:
            try:
                info = await self.validate_input(user_input)
                # Complement 'info' with passed 'data'
                info.update(self._data)
            except MeteoAlarmUnrecognizedRegionError:
                errors["region"] = "unrecognized_region"
                user_input[CONF_REGION] = ""
            except MeteoAlarmUnavailableLanguageError:
                errors["language"] = "not_available_language"
                user_input[CONF_LANGUAGE] = DEFAULT_LANGUAGE
            except InvalidAwarenessType:
                errors["awareness_type"] = "invalid_awareness_type"
                user_input[CONF_AWARENESS_TYPES] = DEFAULT_AWARENESS_TYPES
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            if errors:
                return self.async_show_form(
                    step_id="other",
                    data_schema=vol.Schema(
                        {
                            vol.Required(
                                CONF_REGION, default=user_input[CONF_REGION]
                            ): vol.In(self._regions),
                            vol.Optional(
                                CONF_LANGUAGE, default=user_input[CONF_LANGUAGE]
                            ): vol.In(self._languages),
                            vol.Optional(
                                CONF_AWARENESS_TYPES,
                                default=user_input[CONF_AWARENESS_TYPES],
                            ): cv.multi_select(DEFAULT_AWARENESS_TYPES),
                        }
                    ),
                    errors=errors,
                )
            try:

                # Set 'unique_id' and abort flow if already configured
                await self.async_set_unique_id(DEFAULT_NAME)
                self._abort_if_unique_id_configured()

                # Convert 'country' and 'language' to ISO
                info[CONF_COUNTRY] = cmap(info[CONF_COUNTRY])
                info[CONF_LANGUAGE] = lmap(info[CONF_LANGUAGE])

                # Create new entry in 'core.config_entries'
                return self.async_create_entry(title=info[CONF_NAME], data=info)

            except exceptions.HomeAssistantError:
                return self.async_abort(reason="already_configured")

        return self.async_show_form(
            step_id="other",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_REGION,
                    ): vol.In(self._regions),
                    vol.Optional(
                        CONF_LANGUAGE,
                    ): vol.In(self._languages),
                    vol.Optional(
                        CONF_AWARENESS_TYPES,
                        default=DEFAULT_AWARENESS_TYPES,
                    ): cv.multi_select(DEFAULT_AWARENESS_TYPES),
                }
            ),
            errors=errors,
        )

    async def validate_input(self, data):
        """Validate region, language and list of awareness_types."""
        # Clean and update
        data[CONF_REGION] = data[CONF_REGION].strip("'\"")

        if data[CONF_REGION] not in self._regions:
            raise MeteoAlarmUnrecognizedRegionError

        if data[CONF_LANGUAGE] and data[CONF_LANGUAGE] not in self._languages:
            raise MeteoAlarmUnavailableLanguageError

        for awt in data[CONF_AWARENESS_TYPES]:
            if awt not in DEFAULT_AWARENESS_TYPES:
                raise InvalidAwarenessType

        # Return info that you want to store in the config entry.
        return {
            CONF_REGION: data[CONF_REGION],
            CONF_LANGUAGE: data[CONF_LANGUAGE],
            CONF_AWARENESS_TYPES: data[CONF_AWARENESS_TYPES],
        }

    async def async_get_languages(self):
        """Get available languages for country if possible."""
        if self._country:
            self._languages = [DEFAULT_LANGUAGE]
            self._languages.extend(
                map(
                    lmap,
                    await self.hass.async_add_executor_job(
                        get_languages, cmap(self._country)
                    ),
                )
            )
        else:
            self._languages = LANGUAGES

    async def async_get_regions(self):
        """Get the regions of the country if possible."""
        if self._country:
            self._regions = await self.hass.async_add_executor_job(
                get_regions, cmap(self._country)
            )
        else:
            self._regions = [""]


# pylint:disable=too-few-public-methods
class InvalidAwarenessType(exceptions.HomeAssistantError):
    """Error to indicate there is invalid awareness type."""
