from enum import StrEnum

from homeassistant.util import slugify


class CleanModes(StrEnum):
    REGULAR = "all"
    FAST_MODE = "short"
    FLOOR_ONLY = "floor"
    WATER_LINE = "water"
    ULTRA_CLEAN = "ultra"
    FULL_COVERAGE = "stairs"
    PICKUP = "pickup"


# ID of the features API entry that lists the clean modes
CLEANING_MODE_FEATURE = "2"

# Clean modes by the ID the features API gives them. The app shows these
# names, while the robot uses the values of CleanModes.
CLEAN_MODE_FEATURES = {
    "291": CleanModes.REGULAR,
    "22": CleanModes.FAST_MODE,
    "23": CleanModes.FLOOR_ONLY,
    "211": CleanModes.FULL_COVERAGE,
}

# Features the app hides unless the robot turns them on, so Home Assistant
# leaves them out too. 292 is Tic tac.
HIDDEN_CLEAN_MODE_FEATURES = {"292"}

# Keys of the cycle time presets for each clean mode, which older versions
# created as entities and kept in storage
LEGACY_CYCLE_TIME_KEYS = [
    slugify(f"Cycle Time {mode}")
    for mode in ("all", "short", "floor", "water", "ultra", "pickup")
]


def supported_clean_modes(features: list[dict]) -> list[str] | None:
    """
    Return the clean modes the features API lists, plus pickup.

    Return None when the API lists no clean modes, or one this integration
    doesn't know, so the caller can offer every mode instead.
    """
    cleaning_mode = next(
        (feature for feature in features if feature.get("id") == CLEANING_MODE_FEATURE),
        None,
    )
    if cleaning_mode is None:
        return None

    ids = [sub.get("id") for sub in cleaning_mode.get("subFeatures") or []]
    ids = [
        feature_id for feature_id in ids if feature_id not in HIDDEN_CLEAN_MODE_FEATURES
    ]

    if not ids or any(feature_id not in CLEAN_MODE_FEATURES for feature_id in ids):
        return None

    return [CLEAN_MODE_FEATURES[feature_id] for feature_id in ids] + [CleanModes.PICKUP]
