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


class MundaneTasks(object):

    @classmethod
    def center_text_x(cls, box_width, offset_x, text_to_center):
        offset = (offset_x / GameSettings.MENUSEGMENTSIZE)
        width_less_offsets = box_width / 2 - offset

        text_length = len(text_to_center) * 2
        even_shift = 0
        if len(text_to_center) % 2 == 0:
            even_shift = GameSettings.FONT_SIZE/2

        header_spaces = int((width_less_offsets - text_length / 2) / 2)

        text = text_to_center
        for space in range(header_spaces):
            text = " " + text
        return text, even_shift

    @classmethod
    def center_image_x(cls, box_width, offset_x, surface):
        box_width_less_offsets = (box_width * GameSettings.MENUSEGMENTSIZE) - offset_x

        image_width = surface.get_width()
        print(image_width, box_width_less_offsets)
        x_spacing = (box_width_less_offsets - image_width)/2

        return x_spacing