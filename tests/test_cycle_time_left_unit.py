"""Cycle Time Left shows minutes on entities made by older versions."""

from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.mydolphin_plus import _show_cycle_time_left_in_minutes
from custom_components.mydolphin_plus.common.consts import DOMAIN


def _duration_sensor(
    entity_registry: er.EntityRegistry,
    entry: MockConfigEntry,
    unique_id: str,
    unit: str,
) -> er.RegistryEntry:
    return entity_registry.async_get_or_create(
        "sensor",
        DOMAIN,
        unique_id,
        config_entry=entry,
        original_device_class=SensorDeviceClass.DURATION,
        unit_of_measurement=unit,
    )


async def test_cycle_time_left_moves_to_minutes(hass: HomeAssistant) -> None:
    """Only the sensor that shows seconds changes, and keeps its other options."""
    entry = MockConfigEntry(domain=DOMAIN)
    entry.add_to_hass(hass)

    entity_registry = er.async_get(hass)

    time_left = _duration_sensor(
        entity_registry, entry, "time_left", UnitOfTime.SECONDS
    )
    entity_registry.async_update_entity_options(
        time_left.entity_id, "sensor", {"display_precision": 1}
    )
    cycle_time = _duration_sensor(
        entity_registry, entry, "cycle_time", UnitOfTime.MINUTES
    )

    _show_cycle_time_left_in_minutes(hass, entry)

    time_left = entity_registry.async_get(time_left.entity_id)
    cycle_time = entity_registry.async_get(cycle_time.entity_id)

    assert time_left.options["sensor"] == {
        "display_precision": 1,
        "unit_of_measurement": UnitOfTime.MINUTES,
    }
    assert "sensor" not in cycle_time.options


async def test_cycle_time_left_keeps_user_unit(hass: HomeAssistant) -> None:
    """A unit the user already picked stays."""
    entry = MockConfigEntry(domain=DOMAIN)
    entry.add_to_hass(hass)

    entity_registry = er.async_get(hass)

    time_left = _duration_sensor(
        entity_registry, entry, "time_left", UnitOfTime.SECONDS
    )
    entity_registry.async_update_entity_options(
        time_left.entity_id, "sensor", {"unit_of_measurement": UnitOfTime.HOURS}
    )

    _show_cycle_time_left_in_minutes(hass, entry)

    time_left = entity_registry.async_get(time_left.entity_id)

    assert time_left.options["sensor"]["unit_of_measurement"] == UnitOfTime.HOURS
