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

from meteoalarm_rssapi import MeteoAlarm, MeteoAlarmException

import voluptuous as vol


_LOGGER = logging.getLogger(__name__)

ATTRIBUTION = "Information provided by meteoalarm.eu"
CONF_COUNTRY = "country"
CONF_REGION = "region"
DEFAULT_NAME = "meteoalarmeu"
SCAN_INTERVAL = timedelta(minutes=30)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_COUNTRY): cv.string,
        vol.Required(CONF_REGION): cv.string,
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    },
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the MeteoAlarmEU binary sensor platform."""
    country = config[CONF_COUNTRY]
    region = config[CONF_REGION]
    name = config[CONF_NAME]

    try:
        api = MeteoAlarm(country, region)
    except (KeyError, MeteoAlarmException):
        _LOGGER.error("Wrong country code or region name")
        return

    add_entities([MeteoAlarmBinarySensor(api, name)], True)


class MeteoAlarmBinarySensor(BinarySensorEntity):
    """Representation of a MeteoAlarmEU binary sensor."""

    def __init__(self, api, name):
        """Initialize the MeteoAlarmEU binary sensor."""
        self._name = name
        self._attributes = {}
        self._state = None
        self._api = api

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

    def update(self):
        """Update device state."""
        alert = self._api.alerts()
        if alert:
            self._attributes = alert[0]
            self._state = True
        else:
            self._attributes = {}
            self._state = False
