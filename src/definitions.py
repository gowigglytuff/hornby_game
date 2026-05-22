import copy
from enum import Enum

_ENUM_BASE = 83571983457


class Direction(Enum):
    LEFT = "Left"
    RIGHT = "Right"
    UP = "Up"
    DOWN = "Down"
    MATCH = "Match"
    SWITCH = "Switch"

    def get_vector_from_direction(self, direction):
        vector_x = 0
        vector_y = 0
        if direction == Direction.UP:
            vector_y = -1

        elif direction == Direction.LEFT:
            vector_x = -1

        elif direction == Direction.DOWN:
            vector_y = 1

        elif direction == Direction.RIGHT:
            vector_x = 1
        return vector_x, vector_y



class GameSettings(object):
    TILESIZE = 32
    TILESET_IMAGE1 = "assets/tile_set/16x16tileset_frame1.png"
    TILESET_IMAGE2 = "assets/tile_set/16x16tileset_frame2.png"
    TILESET_IMAGE3 = "assets/tile_set/16x16tileset_frame3.png"
    TILESET_IMAGE4 = "assets/tile_set/16x16tileset_frame4.png"
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
    NPC = "NPC"
    DECO = "Deco"
    DEFAULT = "Default"
    HOUSE = "House"
    BASE = "Base"
    STATIC = "Static"
    SUB = "Sub"
    OVERWORLD = "Overworld"
    BASKET = "Basket"
    BIRD = "Bird"
    INDANIM = "independent_animation"

class Names(Enum):
    BASICMENU = "Basic Menu"
