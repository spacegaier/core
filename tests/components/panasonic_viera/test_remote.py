"""Test the Panasonic Viera remote entity."""

from unittest.mock import call

from panasonic_viera import Keys

from homeassistant.components.panasonic_viera.const import ATTR_UDN, DOMAIN
from homeassistant.components.remote import (
    ATTR_COMMAND,
    DOMAIN as REMOTE_DOMAIN,
    SERVICE_SEND_COMMAND,
)
from homeassistant.const import ATTR_ENTITY_ID, SERVICE_TURN_OFF, SERVICE_TURN_ON

from .conftest import MOCK_CONFIG_DATA, MOCK_DEVICE_INFO, MOCK_ENCRYPTION_DATA

from tests.common import MockConfigEntry


async def setup_panasonic_viera(hass):
    """Initialize integration for tests."""
    mock_entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id=MOCK_DEVICE_INFO[ATTR_UDN],
        data={**MOCK_CONFIG_DATA, **MOCK_ENCRYPTION_DATA, **MOCK_DEVICE_INFO},
    )

    mock_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(mock_entry.entry_id)
    await hass.async_block_till_done()


async def test_onoff(hass, mock_remote):
    """Test the on/off service calls."""

    await setup_panasonic_viera(hass)

    data = {ATTR_ENTITY_ID: "remote.panasonic_viera_tv"}

    await hass.services.async_call(REMOTE_DOMAIN, SERVICE_TURN_OFF, data)
    await hass.services.async_call(REMOTE_DOMAIN, SERVICE_TURN_ON, data)
    await hass.async_block_till_done()

    power = getattr(Keys.power, "value", Keys.power)
    assert mock_remote.send_key.call_args_list == [call(power), call(power)]


async def test_send_command(hass, mock_remote):
    """Test the send_command service call."""

    await setup_panasonic_viera(hass)

    data = {ATTR_ENTITY_ID: "remote.panasonic_viera_tv", ATTR_COMMAND: "command"}
    await hass.services.async_call(REMOTE_DOMAIN, SERVICE_SEND_COMMAND, data)
    await hass.async_block_till_done()

    assert mock_remote.send_key.call_args == call("command")
