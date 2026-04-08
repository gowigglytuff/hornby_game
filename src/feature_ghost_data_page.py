from definitions import Direction, Types
import pygame


class FeatureGhost(object):
    def __init__(self, name, gs_input, room, x, y, direction):
        self.gs_input = gs_input
        self.type = "default"
        self.name = name
        self.state = "idle"
        self.x = x
        self.y = y
        self.z = 1
        self.base_size_x = 1
        self.base_size_y = 1
        self.facing = direction
        self.cur_img = (0, 0)
        self.current_skin = "default"
        self.room = room

    def return_base_coordinates_list(self, bottom_left_x, bottom_left_y):
        coordinates_list = []
        for x in range(self.base_size_x):
            for y in range(self.base_size_y):
                x_coordinate = bottom_left_x + x
                y_coordinate = bottom_left_y - y
                coordinates_list.append([x_coordinate, y_coordinate, self.z])
        print(coordinates_list)
        return coordinates_list


class TreeGhost(FeatureGhost):
    def __init__(self, name, gs_input, room, x, y, direction):
        super().__init__(name, gs_input, room, x, y, direction)
        self.type = Types.PROP
        self.base_size_x = 2


class OldgodGhost(FeatureGhost):
    def __init__(self, name, gs_input, room, x, y, direction):
        super().__init__(name, gs_input, room, x, y, direction)
        self.type = Types.PROP
        self.base_size_x = 4


class PlayerGhost(object):
    def __init__(self, gs_input, x, y):
        self.gs_input = gs_input
        self.type = "Player"
        self.x = x
        self.y = y
        self.z = 1
        self.base_size_x = 1
        self.base_size_y = 1
        self.name = "default"
        self.cur_img = (0, 0)
        self.state = "idle"
        self.facing = Direction.DOWN
        self.current_outfit = "Normal Outfit"

    def return_base_coordinates_list(self, bottom_left_x, bottom_left_y):
        coordinates_list = []
        for x in range(self.base_size_x):
            for y in range(self.base_size_y):
                x_coordinate = bottom_left_x + x
                y_coordinate = bottom_left_y - y
                coordinates_list.append([x_coordinate, y_coordinate, self.z])
        print(coordinates_list)
        return coordinates_list


class NpcGhost(FeatureGhost):
    def __init__(self, name, gs_input, room, x, y, direction):
        super().__init__(name, gs_input, room, x, y, direction)
        self.type = Types.NPC

