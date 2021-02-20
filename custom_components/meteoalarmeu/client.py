from meteoalarm_rssapi import (
    MeteoAlarm,
    MeteoAlarmException,
    MeteoAlarmUnavailableLanguageError,
    MeteoAlarmUnrecognizedCountryError,
    MeteoAlarmUnrecognizedRegionError,
)
from meteoalarm_rssapi import awareness_types as _awareness_types
from meteoalarm_rssapi import countries_list as _countries_list
from meteoalarm_rssapi import get_languages, get_regions
from meteoalarm_rssapi import languages_list as _languages_list

AWARENESS_TYPES = _awareness_types
COUNTRIES = _countries_list
LANGUAGES = _languages_list


class Client:
    def __init__(self, country, region, language=None, awareness_types=AWARENESS_TYPES):
        self._country = country
        self._region = region
        self._language = language
        self._awareness_types = awareness_types
        self._api = self._get_api()

    def update(self, country=None, region=None, language=None, awareness_types=None):
        self._country = country or self._country
        self._region = region or self._region
        self._language = language or self._language
        self._awareness_types = awareness_types or self._awareness_types
        self._api = self._get_api()

    def _get_api(self):
        try:
            return MeteoAlarm(self._country, self._region, self._language)
        except MeteoAlarmUnrecognizedCountryError:
            raise MeteoAlarmUnrecognizedCountryError()
        except MeteoAlarmUnrecognizedRegionError:
            raise MeteoAlarmUnrecognizedRegionError()
        except MeteoAlarmUnavailableLanguageError:
            raise MeteoAlarmUnavailableLanguageError()

    @staticmethod
    def languages(self):
        return _languages_list

    @staticmethod
    def countries(self):
        return _countries_list

    def languages_for_country(self):
        return self._api.country_languages()

    def alerts(self):
        alarms = self._api.alerts()
        return [m for m in alarms if m["awareness_type"] in self._awareness_types]
