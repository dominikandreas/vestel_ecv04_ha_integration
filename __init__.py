"""The vestel_ecv04 integration."""
from __future__ import annotations

from datetime import timedelta
import logging

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN
from .vestel_ecv04_client import ECV04ClientConfig, VestelChargerClient

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up vestel_ecv04_2 from a config entry."""

    hass.data.setdefault(DOMAIN, {})

    config = ECV04ClientConfig(
        host=entry.data[CONF_HOST],
        user=entry.data[CONF_USERNAME],
        password=entry.data[CONF_PASSWORD],
    )
    # 1. Create API instance
    charger_client = VestelChargerClient(config)

    # 2. Validate the API connection (and authentication)
    if not await charger_client.login():
        return False

    # Create and assign the coordinator
    coordinator = VestelEcv04Coordinator(hass, charger_client)

    # populate initial data
    await coordinator.async_refresh()

    # 3. Store an API object for your platforms to access
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Setup platforms (sensor, switch, etc.)
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    )

    async def handle_set_phases_and_current_service_call(service_call):
        """Handle the service call."""
        await charger_client.set_phases_and_current(
            service_call.data["num_phases"], service_call.data["current"]
        )
        # set the setate of num_phases and current
        hass.states.async_set(
            f"{DOMAIN}.current",
            service_call.data["current"],
        )
        hass.states.async_set(
            f"{DOMAIN}.num_phases",
            service_call.data["num_phases"],
        )

    # Setup service
    hass.services.async_register(
        DOMAIN,
        "set_phases_and_current",
        handle_set_phases_and_current_service_call,
        schema=vol.Schema(
            {
                vol.Optional("num_phases"): vol.In([1, 3]),
                vol.Optional("current"): vol.In(
                    [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
                ),
            }
        ),
    )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


class VestelEcv04Coordinator(DataUpdateCoordinator):
    """Coordinator for fetching data from Vestel Charger."""

    def __init__(self, hass: HomeAssistant, client: VestelChargerClient) -> None:
        """Initialize the Vestel ECV04 Coordinator."""
        self.client = client
        super().__init__(
            hass,
            _LOGGER,
            name="Vestel Charger ECV04 Coordinator",
            update_interval=timedelta(seconds=15),
            update_method=self.client.get_phases_and_current,
            always_update=True,
        )
