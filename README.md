

A `custom_component` for [Home-Assistant](https://www.home-assistant.io/) that implements a `binary_sensor`
for the existence of weather alerts for your (Country, Region) on [meteoalarmm.eu](https://www.meteoalarm.eu/).

You will get a `binary_sensor.meteoalarmeu` identity that is `on` when there are alerts for your region and 
with attributes useful for automations.


**How to install?**

1. Copy the folder `meteoalarmeu` to the folder `custom_components` on your Home-Assistant folder.

2. Write in your `configuration.yaml` file, the following:

```
binary_sensor:
- platform: meteoalarmeu
  country: 'DE'
  region: 'Kreis Ahrweiler'

```

**NOTE**: You should adapt the country and region to your case!

You need to know your iso 2-letter country code (e.g. DE) and the name of your region
**as reported by your national agency to meteoalarm.eu** (e.g. Kreis Ahrweiler).
For that, please check the page for your country in [meteoalarm.eu](https://www.meteoalarm.eu/).
