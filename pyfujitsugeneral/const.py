"""Constants for FGLair Home Assistant Integration."""

from enum import IntEnum, unique

DEVICE_CAPABILITIES = "device_capabilities"

CAPABILITY_NOT_AVAILABLE: int = 65535


@unique
class Capability(IntEnum):
    OP_COOL = 1
    OP_DRY = 1 << 1
    OP_FAN = 1 << 2
    OP_HEAT = 1 << 3
    OP_AUTO = 1 << 4
    OP_MIN_HEAT = 1 << 13

    FAN_QUIET = 1 << 9
    FAN_LOW = 1 << 8
    FAN_MEDIUM = 1 << 7
    FAN_HIGH = 1 << 6
    FAN_AUTO = 1 << 5

    POWERFUL_MODE = 1 << 16
    ECO_MODE = 1 << 12
    ENERGY_SWING_FAN = 1 << 14
    COIL_DRY = 1 << 18
    OUTDOOR_LOW_NOISE = 1 << 17
    SWING_VERTICAL = 1 << 10
    SWING_HORIZONTAL = 1 << 11
