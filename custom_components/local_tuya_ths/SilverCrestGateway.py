from homeassistant.core import HomeAssistant
import logging
import tinytuya

_VERSION=3.5
_LOGGER = logging.getLogger(__name__)

class SilverCrestGateway():
    """Representation of a Sensor."""

    def __init__(self, hass: HomeAssistant, gw_device_id, gw_local_key, gw_ip_address=None):
        """Initialize the DHT sensor"""
        self.device_id = gw_device_id
        self.local_key = gw_local_key
        self.ip_address = gw_ip_address
        self.hass = hass
        self.name = "Silver Crest Gateway"
        self.supported_dps = ['temperature', 'humidity', 'battery_percentage']
        self.data = {}
        self._cached_state = {}
        self.gw = tinytuya.Device(
            gw_device_id,
            address=self.ip_address,
            local_key=gw_local_key,
            persist=True,
            version=_VERSION
        )
        self.ip_address = self.gw.address

    @property
    def get_gw(self) -> tinytuya.Device:
        return self.gw

    @property
    def get_device_id(self):
        return self.device_id

    @property
    def get_local_key(self):
        return self.local_key

    @property
    def get_ip_address(self):
        return self.ip_address

    @property
    def get_sensor_data(self):
        return self.data

    @property
    def get_supported_dps(self):
        return self.supported_dps
