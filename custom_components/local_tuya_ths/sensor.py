"""Platform for sensor integration."""
from __future__ import annotations
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    TEMP_CELSIUS,
    PERCENTAGE,
    CONF_REGION,
    CONF_CLIENT_ID,
    CONF_CLIENT_SECRET,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
import logging
from .SilverCrestGateway import SilverCrestGateway
from .THSensor import THSensor
import voluptuous as vol

_LOGGER = logging.getLogger(__name__)

SENSOR_TYPES = [
    "wsdcg", # Temperature and humidity sensor
]

ENTITIES_SCHEMA = vol.Schema({
    vol.Required("device_id", default=""): cv.string,
    vol.Required("local_key", default=""): cv.string,
    vol.Required("name", default=""): cv.string,
    vol.Required("type", default="wsdcg"): vol.All(cv.ensure_list, [vol.In(SENSOR_TYPES)]),
})

SENSORS_SCHEMA = vol.All({
    vol.Required("entities", default=[]): vol.All(cv.ensure_list, [ENTITIES_SCHEMA]),
})

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required("gw_device_id", default=""): cv.string,
    vol.Required("gw_local_key", default=""): cv.string,
    vol.Required("gw_ip_address", default=""): cv.string,
    vol.Required("sensors", default={}): SENSORS_SCHEMA,
})

async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the sensor platform."""

    sensors = config.get("sensors")
    sensorsEntities = sensors["entities"]
    gw_device_id = config.get("gw_device_id")
    gw_local_key = config.get("gw_local_key")
    gw_ip_address = config.get("gw_ip_address")

    gw = SilverCrestGateway(hass, gw_device_id, gw_local_key, gw_ip_address)
    THSensors = []
    entities = []

    for sensorEntity in sensorsEntities:
        THSensors.append(THSensor(sensorEntity, hass, gw.get_gw))

    async_add_entities(THSensors, True)
