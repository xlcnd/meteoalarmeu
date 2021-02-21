
[![GitHub issues by-label](https://img.shields.io/github/issues/xlcnd/meteoalarmeu/bug?label=bugs&style=for-the-badge)][2]
[![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/xlcnd/meteoalarmeu?label=version&sort=semver&style=for-the-badge)][3]
[![GitHub download zip](https://img.shields.io/badge/download-zip-blue?style=for-the-badge)][1]
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/hacs/default/blob/master/integration)


A `custom_component` for [Home-Assistant](https://www.home-assistant.io/) that implements a `binary_sensor`
for the existence of weather alerts for your (Country, Region) on [meteoalarm.eu][9].


> *DISCLAIMER: This is an open source project and doesn't have
> any affiliation with [meteoalarm.eu](https://www.meteoalarm.eu/)*.


You will get a `binary_sensor.meteoalarmeu` identity that is `on` when there are alerts for your region and
with attributes useful for automations.

> WARNING: If you are updating from a previous version you should delete any configuration text related
> with this integration from your `configuration.yaml`, since `yaml configuration` is now **NOT supported**.


**How to install?**<a name="install"></a>

> *Before install read [this][5]*.

If you have [HACS][4], use the normal procedure to install a new integration (*meteoalarmeu*)
and see point 3 below.

To do it manually:

1. Download [this][1] file and unzip it.

2. Copy the folder `meteoalarmeu` to the folder `custom_components` on your Home-Assistant folder.

3. Restart Home-Assistant.


To continue the installation, you need to know the 2-letter iso code of your country (e.g. DE) and the **exact name** of your region
**as reported by your national agency to meteoalarm.eu** (e.g. Kreis Ahrweiler).
For that, please check the page for your country in [meteoalarm.eu](https://www.meteoalarm.eu/)
or search [here][6] (just the **exact name of the region** without the code).

You need to know, too, the [ISO 639-1 code][7] for the message's language (usually the languages available for each country are english ('en') and the local language (e.g. 'de')). The indication of **language is optional**, and if no language is specified the *message will come unparsed and in all available languages*.


Now do the following steps:

```
1. go to Configuration > Integrations
2. then click '+ ADD INTEGRATION'
3. choose 'meteoalarmeu'
4. on Country choose (e.g. DE) (adapt to your case!)
5. on Region write (e.g. Kreis Ahrweiler) (adapt to your case!)
6. on Language choose (e.g. 'de') (adapt to your case!)
7. left the rest as it is OR unselect some events
8. click 'SUBMIT'
```

If all goes well (be carefull with step 5), now you have a new sensor `binary_sensor.meteoalarmeu`. You should wait for some minutes (up until 30m!) for HA to start to update the sensor. Meanwhile, add your automations for the sensor and **don't forget** to reload them.


You can do a lot with automations... some useful ones would be:<a name="automations"></a>

```
automation:

- alias: Alert me about weather warnings
  trigger:
  - platform: state
    entity_id: binary_sensor.meteoalarmeu
    attribute: message_id
  condition:
  - condition: state
    entity_id: binary_sensor.meteoalarmeu
    state: 'on'
  action:
  - repeat:
      count: "{{ state_attr('binary_sensor.meteoalarmeu', 'alerts') | int }}"
      sequence:
      - service: persistent_notification.create
        data:
          title: >
            {% set ext = "" if repeat.first else "_" + (repeat.index-1)|string %}
            {{ state_attr('binary_sensor.meteoalarmeu', 'awareness_type' + ext) }} ({{ state_attr('binary_sensor.meteoalarmeu', 'awareness_level' + ext) }})
          message: >
            {% set ext = "" if repeat.first else "_" + (repeat.index-1)|string %}
            {{ state_attr('binary_sensor.meteoalarmeu', 'message' + ext) }}

            Effective from **{{ state_attr('binary_sensor.meteoalarmeu', 'from' + ext) }}** until **{{ state_attr('binary_sensor.meteoalarmeu', 'until' + ext) }}**
          notification_id: >
            {% set ext = "" if repeat.first else "_" + (repeat.index-1)|string %}
            meteoalarm-{{ state_attr('binary_sensor.meteoalarmeu', 'alert_id' + ext) }}


- alias: Update weather warnings on HA start
  trigger:
  - platform: homeassistant
    event: start
  action:
  - service: homeassistant.update_entity
    entity_id: binary_sensor.meteoalarmeu


- alias: Dismiss obsolete PNs about weather warnings
  mode: restart
  trigger:
  - platform: event
    event_type: persistent_notifications_updated
  action:
  - delay: '00:00:10'
  - service: persistent_notification.dismiss
    data:
      notification_id: >
        {%- for item in states.persistent_notification if item |regex_search("until \*\*(.*?)\*\*") -%}
        {%- if item | regex_search("meteoalarm") -%}
        {%- if item  | regex_findall_index("until \*\*(.*?)\*\*") | as_timestamp() < as_timestamp(now()) -%}
        {{ item.entity_id | replace('persistent_notification.', '') }}{%- if not loop.last %},{% endif -%}
        {%- endif -%}
        {%- endif -%}
        {%- endfor -%}

```


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


```
Red
  The weather is very dangerous. Exceptionally intense meteorological phenomena have been forecast.
  Major damage and accidents are likely, in many cases with threat to life and limb, over a wide
  area. Keep frequently informed about detailed expected meteorological conditions and risks.
  Follow orders and any advice given by your authorities under all circumstances,
  be prepared for extraordinary measures.

Orange
  The weather is dangerous. Unusual meteorological phenomena have been forecast.
  Damage and casualties are likely to happen. Be very vigilant and keep regularly informed
  about the detailed expected meteorological conditions. Be aware of the risks that might be
  unavoidable. Follow any advice given by your authorities.

Yellow
  The weather is potentially dangerous. The weather phenomena that have been forecast are not
  unusual, but be attentive if you intend to practice activities exposed to meteorological risks.
  Keep informed about the expected meteorological conditions and do not take any avoidable risk.

Green (empty alert)
  No particular awareness of the weather is required.

White (error MeteoAlarmMissingInfo)
  Missing, insufficient, outdated or suspicious data.

```


If by any reason the server becames unavailable or sends an error status (and this happens a lot with meteoalarm.eu!)
the **sensor becomes unavailable too**, if in the next update the server is ok, **it becomes available again**.

This component uses [meteoalarm.eu][9]'s **rss feeds** which are available for **all** [(active) countries][8].

[1]: https://github.com/xlcnd/meteoalarmeu/archive/v2021.4.2.zip
[2]: https://github.com/xlcnd/meteoalarmeu/issues?q=is%3Aissue+is%3Aopen+is%3Abug
[3]: https://github.com/xlcnd/meteoalarmeu/releases
[4]: https://hacs.xyz/
[5]: https://github.com/xlcnd/meteoalarmeu/issues/3
[6]: https://github.com/xlcnd/meteoalarm-rssapi/blob/main/meteoalarm_rssapi/_resources.py
[7]: https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2
[8]: https://github.com/xlcnd/meteoalarmeu/issues/2
[9]: https://www.meteoalarm.eu
