import logging
import tinytuya

_VERSION=3.5
_LOGGER = logging.getLogger(__name__)

class TemperatureHumiditySensor():
    """Representation of a Sensor."""

    def __init__(self, gw, deviceEntry) -> None:
        """Initialize the DHT sensor"""

        self._gw = gw
        self._device_id = deviceEntry["device_id"]
        self._local_key = deviceEntry["local_key"]
        self._name = deviceEntry["name"]
        self._type = deviceEntry["type"]
        
        self._device = tinytuya.Device(
            dev_id=self._device_id,
            cid=self._local_key,
            parent=self._gw,
            persist=True,
            version=_VERSION
        )

    @property
    def tiny_tuya_device(self):
        return self._device

    @property
    def device_id(self):
        return self._device_id

    @property
    def local_key(self):
        return self._local_key

    @property
    def gateway(self):
        return self._gw

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type
