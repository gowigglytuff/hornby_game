from definitions import Direction, Types
import pygame

class Feature(object):
    def __init__(self):
        self.type = "default"
        self.name = "default"
        self.state = "idle"
        self.facing = Direction.DOWN
        self.current_skin = "default"

class PlayerGhost(object):
    def __init__(self, gs_input, x, y):
        self.gs_input = gs_input
        self.type = "Player"
        self.x = x
        self.y = y
        self.name = "default"
        self.cur_img = (0, 0)
        self.state = "idle"
        self.facing = Direction.DOWN
        self.current_outfit = "Normal Outfit"


class NpcGhost(object):
    def __init__(self, name, gs_input, room, x, y, direction):
        self.gs_input = gs_input
        self.type = Types.NPC
        self.x = x
        self.y = y
        self.name = name
        self.cur_img = (0, 0)
        self.state = "idle"
        self.facing = direction
        self.room = room

