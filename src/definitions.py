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
    MENU_STYLE = "assets/spritesheets/menu_spritesheets/menu_structure_gray.png"
    TILESET_SIZE = 10
    RESOLUTION = (312*4, 312*3)
    MENUSEGMENTSIZE = 5
    MENUEDGE = 50

    FONT_SIZE = 10


class Types(Enum):
    PROP = "Prop"
    NPC = "Npc"
    BASE = "Base"
    OVERWORLD = "Overworld"

class Names(Enum):
    BASICMENU = "Basic Menu"
