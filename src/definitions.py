from enum import Enum

_ENUM_BASE = 83571983457

class Direction(Enum):
    LEFT = _ENUM_BASE + 1
    RIGHT = _ENUM_BASE + 2
    UP = _ENUM_BASE + 3
    DOWN = _ENUM_BASE + 4

