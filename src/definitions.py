from enum import Enum

_ENUM_BASE = 83571983457


class Direction(Enum):
    LEFT = _ENUM_BASE + 1
    RIGHT = _ENUM_BASE + 2
    UP = _ENUM_BASE + 3
    DOWN = _ENUM_BASE + 4


class GameSettings(object):
    TILESIZE = 24
    TILESET_IMAGE = "assets/tile_set/tile_set_1.png"
    TILESET_SIZE = 10
    RESOLUTION = (312*4, 312*3)


class Types(Enum):
    PROP = "Prop"
    NPC = "Npc"
    BASE = "Base"

class Names(Enum):
    BASICMENU = "Basic Menu"
