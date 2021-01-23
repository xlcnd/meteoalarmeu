"""Binary Sensor for MeteoAlarmEU."""

import logging
from datetime import timedelta

import homeassistant.helpers.config_validation as cv
from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    DEVICE_CLASS_SAFETY,
    PLATFORM_SCHEMA,
)
from homeassistant.const import ATTR_ATTRIBUTION, CONF_NAME

from meteoalarm_rssapi import (
    MeteoAlarm,
    MeteoAlarmException,
)

import voluptuous as vol


_LOGGER = logging.getLogger(__name__)

ATTRIBUTION = "Information provided by meteoalarm.eu"
CONF_COUNTRY = "country"
CONF_REGION = "region"
CONF_AWARENESS_TYPES = "awareness_types"
DEFAULT_NAME = "meteoalarmeu"
DEFAULT_AWARENESS_TYPES = [
    "Avalanches",
    "Coastal Event",
    "Extreme high temperature",
    "Extreme low temperature",
    "Flood",
    "Fog",
    "Forestfire",
    "Rain",
    "Rain-Flood",
    "Snow/Ice",
    "Thunderstorms",
    "Wind",
]
SCAN_INTERVAL = timedelta(minutes=30)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_COUNTRY): cv.string,
        vol.Required(CONF_REGION): cv.string,
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Optional(CONF_AWARENESS_TYPES, default=DEFAULT_AWARENESS_TYPES): vol.All(
            cv.ensure_list, [cv.string]
        ),
        # cv.ensure_list, [vol.In(DEFAULT_AWARENESS_TYPES)]
    },
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the MeteoAlarmEU binary sensor platform."""
    country = config[CONF_COUNTRY]
    region = config[CONF_REGION]
    name = config[CONF_NAME]
    awareness_types = config[CONF_AWARENESS_TYPES]

    try:
        api = MeteoAlarm(country, region)
    except (KeyError, MeteoAlarmException):
        _LOGGER.error("Wrong country code or region name")
        return

    add_entities([MeteoAlarmBinarySensor(api, name, awareness_types)], True)


class MeteoAlarmBinarySensor(BinarySensorEntity):
    """Representation of a MeteoAlarmEU binary sensor."""

    def __init__(self, api, name, awareness_types):
        """Initialize the MeteoAlarmEU binary sensor."""
        self._name = name
        self._attributes = {}
        self._awareness_types = awareness_types
        self._state = None
        self._api = api
        self._available = True

    @property
    def name(self):
        """Return the name of the binary sensor."""
        return self._name

    @property
    def is_on(self):
        """Return the status of the binary sensor."""
        return self._state

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        self._attributes[ATTR_ATTRIBUTION] = ATTRIBUTION
        return self._attributes

    @property
    def device_class(self):
        """Return the device class of this binary sensor."""
        return DEVICE_CLASS_SAFETY

    @property
    def available(self):
        """Return true if the device is available."""
        return self._available

    def update(self):
        """Update device state."""
        try:
            msgs = self._api.alerts()
            alert = [m for m in msgs if m["awareness_type"] in self._awareness_types]
        except (KeyError, MeteoAlarmException):
            _LOGGER.error("Bad response from meteoalarm.eu")
            self._available = False
            return
        self._available = True
        if alert:
            self._attributes = alert[0]
            self._state = True
        else:
            self._attributes = {}
            self._state = False
