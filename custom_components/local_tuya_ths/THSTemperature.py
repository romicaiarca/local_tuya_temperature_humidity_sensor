from homeassistant.core import HomeAssistant
from homeassistant.const import TEMP_CELSIUS
from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass
)
import logging
from .TemperatureHumiditySensor import TemperatureHumiditySensor

_LOGGER = logging.getLogger(__name__)

class THSTemperature(SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, hass: HomeAssistant, ths: TemperatureHumiditySensor) -> None:
        """Initialize the DHT sensor"""

        self._hass = hass
        self._ths = ths
        self._tiny_tuya_device = ths.tiny_tuya_device
        self._device_id = ths.device_id
        self._name = (f"{self._ths.name} temperature")
        self._attr_name = self._name
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = TEMP_CELSIUS
        self._attr_device_class = SensorDeviceClass.TEMPERATURE
        self._attr_native_value = 0
        self.entity_id = (f"sensor.local_tuya_ths_{self._name}").replace(" ", "_")

        if self._hass.states.get(self.entity_id) is not None and self._attr_native_value == 0:
            self._attr_native_value = self._hass.states.get(self.entity_id)
            
        # self._hass.states.set(self.entity_id, self._attr_native_value)

    async def async_update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """

        self._hass.async_add_executor_job(self.get_data_from_sensor)

    @property
    def name(self):
        return self._name

    @property
    def unique_id(self):
        """Return the unique id for this device (the dev_id)."""
        return (f"{self._device_id}_temperature")

    @property
    def device_info(self):
        """Return the device information for this device."""
        return {
            "identifiers": {("local_tuya_ths", self.unique_id)},
            "name": self.name,
            "manufacturer": "Tuya",
        }

    def get_data_from_sensor(self):
        data = {}

        # _LOGGER.error(f"self._attr_last_update {self._attr_last_update}")
        # _LOGGER.error(f"SensorEntity {SensorEntity}")

        try:
            data = self._tiny_tuya_device.status()
            _LOGGER.warning(f"THSTemperature status {data}")
        except Exception as ex:
            _LOGGER.warning(f"Exception catched: THSTemperature {self.name} {ex}")
            return -1

        if data is None or not all(data.values()):
            _LOGGER.warning(f"THSTemperature {self.name} no data received. {data}")
            return -1

        if "Error" in data:
            _LOGGER.warning(f"Error in data: {data['Err']}: {data['Error']}")
            return -1

        if data and 'dps' in data and "1" in data['dps']:
            _LOGGER.warning(int(data['dps']["1"]) / 10)
            self._attr_native_value = (int(data['dps']["1"]) / 10)
            self._hass.states.set(self.entity_id, self._attr_native_value)

        return data
