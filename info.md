# Local Tuya Temperature Humidity Sensor

This is a minimum implementation of an integration providing a sensor measurement via a Zigbee gateway (Temperature and Humidity) from Tuya using TinyTuya.
These was implemented since for the moment no Tuya integrations doesn't support such sensors.
You may want to use same think that is implemented in TinyTuya Cloud, to use date that are stored in Tuya Cloud.

### Installation

Copy this folder to `<config_dir>/custom_components/local_tuya_ths/`.

Add the following to your `configuration.yaml` file:

```yaml
# Example configuration.yaml entry
sensor:
  - platform: local_tuya_ths
    zigbee_gateway: "bf26...m2gu" # device_id
    sensors:
      category: "wsdcg"
      entities:
        - device_id: "bf26...m2gu" # device_id
        - device_id: "bf24...n8xt" # device_id
        - device_id: "bf25...ygxv" # device_id
```
Author: Romică Iarca [@romicaiarca](https://github.com/romicaiarca)
