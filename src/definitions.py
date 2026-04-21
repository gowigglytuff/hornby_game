import copy
from enum import Enum

_ENUM_BASE = 83571983457


class Direction(Enum):
    LEFT = _ENUM_BASE + 1
    RIGHT = _ENUM_BASE + 2
    UP = _ENUM_BASE + 3
    DOWN = _ENUM_BASE + 4
    MATCH = _ENUM_BASE + 5
    SWITCH = _ENUM_BASE + 6


class GameSettings(object):
    TILESIZE = 32
    TILESET_IMAGE = "assets/tile_set/MapTilesetFrame1.png"
    TILESET_IMAGE2 = "assets/tile_set/MapTilesetFrame2.png"
    MENU_STYLE = "assets/spritesheets/menu_spritesheets/menu_structure_gray.png"
    TILESET_SIZE = 40
    RESOLUTION = (312*4, 312*3)
    MENUSEGMENTSIZE = 5
    MENUEDGE = 50
    UNIQUEID = 1

    FONT_SIZE = 10

    @classmethod
    def get_unique_ID(cls):
        ID = copy.copy(GameSettings.UNIQUEID)
        GameSettings.UNIQUEID += 1
        return ID

class Types(Enum):
    PROP = "Prop"
    NPC = "Npc"
    BASE = "Base"
    OVERWORLD = "Overworld"

class Names(Enum):
    BASICMENU = "Basic Menu"
