
[![GitHub issues by-label](https://img.shields.io/github/issues/xlcnd/meteoalarmeu/bug?label=bugs&style=for-the-badge)][2] [![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/xlcnd/meteoalarmeu?label=version&sort=semver&style=for-the-badge)][3] [![GitHub download zip](https://img.shields.io/badge/download-zip-blue?style=for-the-badge)][1] [![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/hacs/default/blob/6cf19e87412d44ca56f7e1c8312f23ba5292de1f/integration#L475)

A `custom_component` for [Home-Assistant](https://www.home-assistant.io/) that implements a `binary_sensor` for the existence of weather alerts for your (Country, Region) on [meteoalarm.eu][9].


You will get a `binary_sensor.meteoalarmeu` identity that is `on` when there are alerts for your region and with attributes useful for automations.



**How to install?**<a name="install"></a>


If you have [HACS][4], use the normal procedure to install a new integration (search for *meteoalarmeu*).

To do it manually:

1. Download [this][1] file and unzip it.

2. Copy the folder `meteoalarmeu` to the folder `custom_components` on your Home-Assistant folder.

3. Restart Home-Assistant.


Now do the following steps:

```markdown
1. go to Configuration > Integrations
2. then click '+ ADD INTEGRATION'
3. choose 'meteoalarmeu'
4. on Country choose (e.g. Deutschland) and then click 'SUBMIT'
5. on Region choose (e.g. Kreis Ahrweiler)
6. on Language choose (e.g. deutsch)
7. left the rest as it is OR unselect some events
8. click 'SUBMIT'
```


If all goes well, you have a new sensor `binary_sensor.meteoalarmeu`. You should wait for some minutes (up until 30m!) for HA to start to update the sensor.

For the attribute `awareness_type` (**events**) the possible values are:<a name="events"></a>

```
 Avalanches
 Coastal Event
 Extreme high temperature
 Extreme low temperature
 Flood
 Fog
 Forestfire
 Rain
 Rain-Flood
 Snow/Ice
 Thunderstorms
 Wind
```


For the attribute `awareness_level` (**severity**) the possibilities are (with the meaning following):<a name="severity"></a>


**Red**
> The weather is very dangerous. Exceptionally intense meteorological phenomena have been forecast.  Major damage and accidents are likely, in many cases with threat to life and limb, over a wide area. Keep frequently informed about detailed expected meteorological conditions and risks.  Follow orders and any advice given by your authorities under all circumstances, be prepared for extraordinary measures.

**Orange**
> The weather is dangerous. Unusual meteorological phenomena have been forecast.  Damage and casualties are likely to happen. Be very vigilant and keep regularly informed about the detailed expected meteorological conditions. Be aware of the risks that might be unavoidable. Follow any advice given by your authorities.

**Yellow**
> The weather is potentially dangerous. The weather phenomena that have been forecast are not unusual, but be attentive if you intend to practice activities exposed to meteorological risks.  Keep informed about the expected meteorological conditions and do not take any avoidable risk.

**Green** (empty alert)
> No particular awareness of the weather is required.

**White** (error MeteoAlarmMissingInfo)
> Missing, insufficient, outdated or suspicious data.


If by any reason the server becomes unavailable or sends an error status (and this happens a lot with meteoalarm.eu!) the **sensor becomes unavailable too**, if in the next update the server is ok, **it becomes available again**.

This component uses [meteoalarm.eu][9]'s **rss feeds** which are available for **all** [(active) countries][8].

[More info...][5]


[1]: https://github.com/xlcnd/meteoalarmeu/archive/v2021.5.8.zip
[2]: https://github.com/xlcnd/meteoalarmeu/issues?q=is%3Aissue+is%3Aopen+label%3Abug
[3]: https://github.com/xlcnd/meteoalarmeu/releases
[4]: https://hacs.xyz/
[5]: https://github.com/xlcnd/meteoalarmeu/issues?q=is%3Aissue+is%3Aopen+label%3Ainfo
[6]: https://github.com/xlcnd/meteoalarm-rssapi/blob/main/meteoalarm_rssapi/_resources.py
[7]: https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
[8]: https://github.com/xlcnd/meteoalarm-rssapi/issues/1
[9]: https://www.meteoalarm.eu
[10]: https://community.home-assistant.io/search?q=meteoalarmeu%20after%3A2021-02-22%20status%3Aopen%20tags%3Aautomation%2Ctemplates%2Cblueprint
[11]: https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2
