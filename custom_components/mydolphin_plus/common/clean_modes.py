from enum import StrEnum

from homeassistant.util import slugify


class CleanModes(StrEnum):
    REGULAR = "all"
    FAST_MODE = "short"
    FLOOR_ONLY = "floor"
    WATER_LINE = "water"
    ULTRA_CLEAN = "ultra"
    PICKUP = "pickup"


# Keys of the cycle time presets for each clean mode, which older versions
# created as entities and kept in storage
LEGACY_CYCLE_TIME_KEYS = [slugify(f"Cycle Time {mode}") for mode in CleanModes]
