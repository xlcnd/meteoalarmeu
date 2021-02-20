"""The meteoalarmeu integration."""
import asyncio

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from meteoalarm_rssapi import MeteoAlarm

from .const import (
    DOMAIN,
    CONF_COUNTRY,
    CONF_REGION,
    CONF_LANGUAGE,
)

__version__ = "0.4.2"

PLATFORMS = ["binary_sensor"]


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the meteoalarmeu component."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up meteoalarmeu from a config entry."""
    hass.data[DOMAIN][entry.entry_id] = MeteoAlarm(
        entry.data[CONF_COUNTRY], entry.data[CONF_REGION], entry.data[CONF_LANGUAGE],
    )

    for component in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, component)
                for component in PLATFORMS
            ]
        )
    )
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
