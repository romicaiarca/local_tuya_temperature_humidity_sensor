from homeassistant.const import TEMP_CELSIUS
import logging
from .TemperatureHumiditySensor import TemperatureHumiditySensor
from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import SensorEntity
import tinytuya
_LOGGER = logging.getLogger(__name__)

class THSensor(Entity):
    def __init__(self, sensorsEntities, hass, gateway):
        self._device_id = sensorsEntities["device_id"]
        self._name = sensorsEntities["name"]
        self._type = sensorsEntities["type"]

        self._tiny_tuya_device = tinytuya.Device(
            dev_id=self._device_id,
            cid=sensorsEntities["local_key"],
            parent=gateway,
            persist=True,
            version=3.5
        )

        self._state = None
        self._attr_name = self._name
        self._unit_of_measurement = TEMP_CELSIUS
        self._state_attributes = {
            'temperature': 0,
            'humidity': 0,
            'battery_percentage': 0,
        }
        self.entity_id = (f"sensor.local_tuya_ths_{self._name}").replace(" ", "_")

    @property
    def name(self):
        return self._name

    @property
    def unique_id(self):
        """Return the unique id for this device (the dev_id)."""
        return (f"local_tuya_ths_{self._device_id}")

    @property
    def device_info(self):
        """Return the device information for this device."""
        return {
            "identifiers": {("local_tuya_ths", self.unique_id)},
            "name": self.name,
            "manufacturer": "Tuya",
        }

    @property
    def state(self):
        return self._state

    @property
    def unit_of_measurement(self):
        return self._unit_of_measurement

    async def async_update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """

        self.get_data_from_sensor()

    @property
    def extra_state_attributes(self):
        """Return the device state attributes."""
        return self._state_attributes

    def get_data_from_sensor(self):
        data = {}

        # _LOGGER.error(f"self._attr_last_update {self._attr_last_update}")
        # _LOGGER.error(f"SensorEntity {SensorEntity}")

        try:
            data = self._tiny_tuya_device.status()
            _LOGGER.debug(f"THSTemperature status {data}")
        except Exception as ex:
            _LOGGER.debug(f"Exception catched: THSTemperature {self.name} {ex}")
            return -1

        if data is None or not all(data.values()):
            _LOGGER.debug(f"THSTemperature {self.name} no data received. {data}")
            return -1

        if "Error" in data:
            _LOGGER.debug(f"Error in data: {data['Err']}: {data['Error']}")
            return -1

        if data and 'dps' in data and "1" in data['dps']:
            self._state = self._state_attributes["temperature"] = (int(data['dps']["1"]) / 10)
            _LOGGER.debug("temperature = " + str(self._state))
            

        if data and 'dps' in data and "2" in data['dps']:
            self._state_attributes["humidity"] = (int(data['dps']["2"]) / 10)
            _LOGGER.debug("humidity = " + str(self._state_attributes["humidity"]))

        if data and 'dps' in data and "4" in data['dps']:
            self._state_attributes["battery_percentage"] = (int(data['dps']["4"]))
            _LOGGER.debug("battery_percentage = " + str(self._state_attributes["battery_percentage"]))
