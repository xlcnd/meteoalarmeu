
[![GitHub issues by-label](https://img.shields.io/github/issues/xlcnd/meteoalarmeu/bug?label=bugs&style=for-the-badge)][2]
[![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/xlcnd/meteoalarmeu?label=version&sort=semver&style=for-the-badge)][3]
[![GitHub download zip](https://img.shields.io/badge/download-zip-blue?style=for-the-badge)][1]


A `custom_component` for [Home-Assistant](https://www.home-assistant.io/) that implements a `binary_sensor`
for the existence of weather alerts for your (Country, Region) on [meteoalarm.eu](https://www.meteoalarm.eu/).


> :warning: *DISCLAIMER: This is an open source project and doesn't have 
> any connection with [meteoalarm.eu](https://www.meteoalarm.eu/)*.


You will get a `binary_sensor.meteoalarmeu` identity that is `on` when there are alerts for your region and
with attributes useful for automations.



**How to install?**

> :warning:  *BEFORE install read [this][5]*.


1. Download [this][1] file and unzip it.

2. Copy the folder `meteoalarmeu` to the folder `custom_components` on your Home-Assistant folder.

3. Write in your `configuration.yaml` file, the following:

```
binary_sensor:
- platform: meteoalarmeu
  country: 'DE'
  region: 'Kreis Ahrweiler'
```

**NOTE**: You should adapt the country and region to your case!

You need to know your 2-letter iso country code (e.g. DE) and the **exact name** of your region
**as reported by your national agency to meteoalarm.eu** (e.g. Kreis Ahrweiler).
For that, please check the page for your country in [meteoalarm.eu](https://www.meteoalarm.eu/).


You can do a lot with automations... an useful one would be:

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
  - service: notify.notify
    data_template:
      title: >
        {{ state_attr('binary_sensor.meteoalarmeu', 'awareness_type') }} ({{ state_attr('binary_sensor.meteoalarmeu', 'awareness_level') }})
      message: >
        {{ state_attr('binary_sensor.meteoalarmeu', 'message') }}

        Effective from {{ state_attr('binary_sensor.meteoalarmeu', 'from') }} until {{ state_attr('binary_sensor.meteoalarmeu', 'until') }}
  - service: persistent_notification.create
    data:
      title: >
        {{ state_attr('binary_sensor.meteoalarmeu', 'awareness_type') }} ({{ state_attr('binary_sensor.meteoalarmeu', 'awareness_level') }})
      message: >
        {{ state_attr('binary_sensor.meteoalarmeu', 'message') }}

        Effective from {{ state_attr('binary_sensor.meteoalarmeu', 'from') }} until {{ state_attr('binary_sensor.meteoalarmeu', 'until') }}
      notification_id: "meteoalarm-{{ state_attr('binary_sensor.meteoalarmeu', 'alert_id') }}"

```



For the attribute `awareness_type` the possible values are:

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


For the attribute `awareness_level` the possibilities are (with the meaning following):


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

Green
  No particular awareness of the weather is required.

White
  Missing, insufficient, outdated or suspicious data.

```


### More advanced stuff

These alarms could get very noisy (with date/time revisions every 30 minutes as
best forecasts are available)! By default you subscribe to **all** type of events.
So is best to limit the type of events that you subscribe. For that, you can use
the `awareness_types` list. As an example:

```
binary_sensor:
- platform: meteoalarmeu
  name: 'meteoalarmeu_ahrweiler'
  country: 'DE'
  region: 'Kreis Ahrweiler'
  awareness_types:
  - Extreme high temperature
  - Extreme low temperature
  - Flood
  - Fog
  - Forestfire
  - Thunderstorms
  - Wind

```

As you can see, the **name** of the sensor can be changed too.


If by any reason the server becames unavailable or sends an error status (and this happens a lot with meteoalarm.eu!)
the **sensor becomes unavailable too**, if in the next update the server is ok, **it becomes available again**.

[1]: https://github.com/xlcnd/meteoalarmeu/archive/v2021.2.1.zip
[2]: https://github.com/xlcnd/meteoalarmeu/issues?q=is%3Aissue+is%3Aopen+is%3Abug
[3]: https://github.com/xlcnd/meteoalarmeu/releases
[4]: https://hacs.xyz/
[5]: https://github.com/xlcnd/meteoalarmeu/issues/3
