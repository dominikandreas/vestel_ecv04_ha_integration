import time

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import UnitOfElectricCurrent

from . import DOMAIN, VestelEcv04Coordinator


class VestelEcv04Sensor(SensorEntity):
    """Representation of a Vestel ECV04 sensor."""

    def __init__(self, coordinator: VestelEcv04Coordinator, sensor_type: str):
        self.coordinator = coordinator
        self.sensor_type = sensor_type
        self._last_poll = 0

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"Vestel ECV04 {self.sensor_type}"

    @property
    def unique_id(self):
        """Return a unique ID to use for this sensor."""
        return f"vestel_ecv04_{self.sensor_type}"

    @property
    def state(self):
        """Return the state of the sensor."""
        return getattr(self.coordinator.data, self.sensor_type, "Unavailable")

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        if self.sensor_type == "current":
            return UnitOfElectricCurrent.AMPERE
        elif self.sensor_type == "num_phases":
            return ""

    @property
    def should_poll(self):
        """Return if the sensor should be polled."""
        if time.time() - self._last_poll < 30:
            return False
        return True

    async def async_update(self):
        """Fetch new state data for the sensor."""
        await self.coordinator.async_request_refresh()


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Vestel ECV04 sensors."""
    data = hass.data[DOMAIN][config_entry.entry_id]

    # Create sensor entities based on the available data
    sensors = [
        VestelEcv04Sensor(data, "current"),
        VestelEcv04Sensor(data, "num_phases"),
    ]

    async_add_entities(sensors, True)
