from homeassistant.core import HomeAssistant
from homeassistant.const import PERCENTAGE
from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass
)
import logging
from .TemperatureHumiditySensor import TemperatureHumiditySensor

_LOGGER = logging.getLogger(__name__)

class THSBattery(SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, hass: HomeAssistant, ths: TemperatureHumiditySensor) -> None:
        """Initialize the DHT sensor"""

        self._hass = hass
        self._ths = ths
        self._tiny_tuya_device = ths.tiny_tuya_device
        self._device_id = ths.device_id
        self._name = (f"{self._ths.name} battery")
        self._attr_name = self._name
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = PERCENTAGE
        self._attr_device_class = SensorDeviceClass.BATTERY
        self._attr_native_value = 0
        self.entity_id = (f"sensor.local_tuya_ths_{self._name}").replace(" ", "_")

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
        return (f"{self._device_id} battery")

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

        try:
            data = self._tiny_tuya_device.status()
            _LOGGER.debug(f"THSHumidity {self.name} status {data}")
        except Exception as ex:
            _LOGGER.error(f"Exception: THSHumidity {self.name} {ex}")

        if data is None or not all(data.values()):
            _LOGGER.debug(f"THSHumidity {self,name} no data received. {data}")
            return -1

        if "Error" in data:
            _LOGGER.debug(f"Error in data: {data['Err']}: {data['Error']}")
            return -1

        if data and 'dps' in data and "4" in data['dps']:
            _LOGGER.debug(int(data['dps']["4"]))
            self._attr_native_value = (int(data['dps']["4"]))

        return data
