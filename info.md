# Local Tuya Temperature Humidity Sensor

This is a minimum implementation of an integration providing a sensor measurement via a Zigbee gateway (Temperature and Humidity) from Tuya using TinyTuya.
These was implemented since for the moment no Tuya integrations supports such sensors.
You may want to use same think that is implemented in TinyTuya Cloud, to use date that are stored in Tuya Cloud.

### Installation

Copy this folder to `<config_dir>/custom_components/local_tuya_ths/`.

Add the following to your `configuration.yaml` file:

```yaml
sensor:
  - platform: local_tuya_ths
    gw_device_id: "bf58...zgjr" # device_id
    gw_local_key: "8d2f...d068" # device_id
    gw_ip_address: "192.168.xxx.xxx" # device_id
    sensors:
      entities:
        - device_id: "bf24...n8xt"
          local_key: "a4c1...4d89" # it is shown as node_id in tuya iot platform
          name: "THS name 1"
          type: "wsdcg" # type of the sensor https://eu.iot.tuya.com/cloud/device/detail/?id={id}}&sourceId={sourceId}&sourceType={sourceType}&region={region}&deviceKey=basicInfo&deviceId={deviceId}
        - device_id: "bf26...m2gu"
          local_key: "a4c1...56c4" # it is shown as node_id in tuya iot platform
          name: "THS name 2"
          type: "wsdcg" # type of the sensor https://eu.iot.tuya.com/cloud/device/detail/?id={id}}&sourceId={sourceId}&sourceType={sourceType}&region={region}&deviceKey=basicInfo&deviceId={deviceId}
        - device_id: "bf25...ygxv"
          local_key: "a4c1...625b" # it is shown as node_id in tuya iot platform
          name: "THS name 3"
          type: "wsdcg" # type of the sensor https://eu.iot.tuya.com/cloud/device/detail/?id={id}}&sourceId={sourceId}&sourceType={sourceType}&region={region}&deviceKey=basicInfo&deviceId={deviceId}

```

In order to create sensors from all attributes from the sensors you have tu add templates like this from the example:

```yaml

template:
  - sensor:
    - name: "THS name 1 ITU"
      unit_of_measurement: "u"
      state: >
        {% set THSName1HumidityLocal = states('sensor.ths_name_1') | round(1, default=0) %}
        {% set HSName1TemperatureLocal = states('sensor.ths_name_1') | round(1, default=0) %}
      
        {{ int((HSName1TemperatureLocal * 1.8 + 32) - (0.55 - 0.0055 * THSName1HumidityLocal) * ((HSName1TemperatureLocal * 1.8 + 32) - 58) | round(1, default=0)) }}
    - name: "THS name 1 humidity"
      state_class: measurement
      unit_of_measurement: "%"
      icon: mdi:battery
      state: >
        {{ state_attr('sensor.ths_name_1', 'humidity') }}
    - name: "THS name 1 battery"
      state_class: measurement
      unit_of_measurement: "%"
      icon: mdi:battery
      state: >
        {{ state_attr('sensor.ths_name_1', 'battery_percentage') }}

```
Author: Romică Iarca [@romicaiarca](https://github.com/romicaiarca)
