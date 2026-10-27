"""Tests for the robot state calculation in SystemDetails."""

from __future__ import annotations

import pytest
from homeassistant.components.vacuum import VacuumActivity
from homeassistant.const import ATTR_MODE

from custom_components.mydolphin_plus.common.calculated_state import CalculatedState
from custom_components.mydolphin_plus.common.clean_modes import CleanModes
from custom_components.mydolphin_plus.common.consts import (
    DATA_CYCLE_INFO_CLEANING_MODE,
    DATA_SECTION_CYCLE_INFO,
    DATA_SECTION_SYSTEM_STATE,
    DATA_SYSTEM_STATE_PWS_STATE,
    DATA_SYSTEM_STATE_ROBOT_STATE,
)
from custom_components.mydolphin_plus.common.power_supply_state import PowerSupplyState
from custom_components.mydolphin_plus.common.robot_state import RobotState
from custom_components.mydolphin_plus.models.system_details import SystemDetails


def _aws_data(
    power_supply_state: PowerSupplyState,
    robot_state: RobotState,
    mode: CleanModes = CleanModes.REGULAR,
) -> dict:
    return {
        DATA_SECTION_SYSTEM_STATE: {
            DATA_SYSTEM_STATE_PWS_STATE: power_supply_state,
            DATA_SYSTEM_STATE_ROBOT_STATE: robot_state,
        },
        DATA_SECTION_CYCLE_INFO: {DATA_CYCLE_INFO_CLEANING_MODE: {ATTR_MODE: mode}},
    }


def test_defaults_before_update() -> None:
    """A new SystemDetails reports off and docked."""
    details = SystemDetails()

    assert not details.is_updated
    assert details.calculated_state == CalculatedState.OFF
    assert details.vacuum_state == VacuumActivity.DOCKED


@pytest.mark.parametrize(
    ("power_supply_state", "robot_state", "calculated_state", "vacuum_state"),
    [
        (
            PowerSupplyState.ERROR,
            RobotState.SCANNING,
            CalculatedState.ERROR,
            VacuumActivity.ERROR,
        ),
        (
            PowerSupplyState.ON,
            RobotState.FAULT,
            CalculatedState.ERROR,
            VacuumActivity.ERROR,
        ),
        (
            PowerSupplyState.ON,
            RobotState.INIT,
            CalculatedState.INIT,
            VacuumActivity.CLEANING,
        ),
        (
            PowerSupplyState.ON,
            RobotState.SCANNING,
            CalculatedState.CLEANING,
            VacuumActivity.CLEANING,
        ),
        (
            PowerSupplyState.ON,
            RobotState.FINISHED,
            CalculatedState.OFF,
            VacuumActivity.CLEANING,
        ),
        (
            PowerSupplyState.PROGRAMMING,
            RobotState.PROGRAMMING,
            CalculatedState.PROGRAMMING,
            VacuumActivity.DOCKED,
        ),
        (
            PowerSupplyState.PROGRAMMING,
            RobotState.SCANNING,
            CalculatedState.CLEANING,
            VacuumActivity.DOCKED,
        ),
        (
            PowerSupplyState.HOLD_DELAY,
            RobotState.NOT_CONNECTED,
            CalculatedState.HOLD_DELAY,
            VacuumActivity.DOCKED,
        ),
        (
            PowerSupplyState.HOLD_WEEKLY,
            RobotState.NOT_CONNECTED,
            CalculatedState.HOLD_WEEKLY,
            VacuumActivity.DOCKED,
        ),
        (
            PowerSupplyState.OFF,
            RobotState.SCANNING,
            CalculatedState.OFF,
            VacuumActivity.DOCKED,
        ),
    ],
)
def test_state_calculation(
    power_supply_state: PowerSupplyState,
    robot_state: RobotState,
    calculated_state: CalculatedState,
    vacuum_state: VacuumActivity,
) -> None:
    """Power supply and robot states map to the expected states."""
    details = SystemDetails()

    assert details.update(_aws_data(power_supply_state, robot_state))
    assert details.is_updated
    assert details.calculated_state == calculated_state
    assert details.vacuum_state == vacuum_state


def test_pickup_mode_reports_returning() -> None:
    """Pickup mode while powered on reports the vacuum as returning."""
    details = SystemDetails()

    details.update(
        _aws_data(PowerSupplyState.ON, RobotState.SCANNING, CleanModes.PICKUP)
    )

    assert details.vacuum_state == VacuumActivity.RETURNING


def test_update_reports_no_change_for_same_data() -> None:
    """A second update with the same data reports no change."""
    details = SystemDetails()
    data = _aws_data(PowerSupplyState.ON, RobotState.SCANNING)

    assert details.update(data)
    assert not details.update(data)
