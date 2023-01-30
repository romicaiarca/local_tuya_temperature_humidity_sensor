# Local Tuya Temperature Humidity Sensor

This is a minimum implementation of an integration providing a sensor measurement via a Zigbee gateway (Temperature and Humidity) from Tuya using TinyTuya.
These was implemented since for the moment no Tuya integrations doesn't support such sensors.
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
        - device_id: "bf25...ygxv" # THS_OFFICE_WALL_2
          local_key: "a4c1...625b" # it is shown as node_id in tuya iot platform
          name: "THS naem 3"
          type: "wsdcg" # type of the sensor https://eu.iot.tuya.com/cloud/device/detail/?id={id}}&sourceId={sourceId}&sourceType={sourceType}&region={region}&deviceKey=basicInfo&deviceId={deviceId}

```
Author: Romică Iarca [@romicaiarca](https://github.com/romicaiarca)
