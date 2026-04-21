import pygame

from animations_page_view_page import WalkAnimation
from spritesheet import Spritesheet
from definitions import Direction, GameSettings


class PlayerAvatar(object):
    def __init__(self, image_x, image_y):
        self.name = "Player"
        self.type = "Player"
        self.drawing_priority = 1
        self.character_frame_x = 24
        self.character_frame_y = 36
        self.spritesheet = Spritesheet("player_base_spritesheet", "assets/spritesheets/player_spritesheets/player_base_spritesheet.png", self.character_frame_x, self.character_frame_y)
        self.face_image = self.get_face_image()
        self.current_image_x = 0
        self.current_image_y = 0
        self.image_x = image_x
        self.image_y = image_y
        self.size_x = 1
        self.size_y = 1
        self.image_offset_y = self.character_frame_y - GameSettings.TILESIZE*3/4
        self.image_offset_x = (GameSettings.TILESIZE - self.character_frame_x)/2
        self.animation_list = {"walk_front": WalkAnimation(Direction.DOWN),
                               "walk_left": WalkAnimation(Direction.LEFT),
                               "walk_right": WalkAnimation(Direction.RIGHT),
                               "walk_up": WalkAnimation(Direction.UP)}
        self.animation_frame = 0
        self.currently_animating = False
        self.current_animation = None

    def get_face_image(self):
        face = self.spritesheet.get_image(0, 0)
        face = face.subsurface(0, 0, 24, 24)
        face = pygame.transform.scale(face, [24 * 5, 24 * 5])
        return face

    def face_character(self, direction):
        if direction == Direction.DOWN:
            self.update_avatar_image(0, 0)
        elif direction == Direction.UP:
            self.update_avatar_image(0, 1)
        elif direction == Direction.LEFT:
            self.update_avatar_image(0, 3)
        elif direction == Direction.RIGHT:
            self.update_avatar_image(0, 2)

    def initiate_animation(self, animation_name):
        self.current_animation = animation_name
        self.currently_animating = True

    def update_avatar_image(self, image_x, image_y):
        self.current_image_x = image_x
        self.current_image_y = image_y


class FeatureAvatar(object):
    def __init__(self, name, image_x, image_y, unique_name):
        self.name = name
        self.unique_name = unique_name
        self.drawing_priority = 1
        self.type = "default"
        self.character_frame_x = 24
        self.character_frame_y = 36
        self.spritesheet = Spritesheet(self.name + "_base_spritesheet", "assets/spritesheets/npc_spritesheets/" + self.name + "_spritesheet.png", self.character_frame_x, self.character_frame_y)
        self.current_image_x = 0
        self.current_image_y = 0
        self.image_x = image_x
        self.image_y = image_y
        self.image_offset_y = self.character_frame_y - GameSettings.TILESIZE*3/4
        self.image_offset_x = (GameSettings.TILESIZE - self.character_frame_x)/2
        self.animation_frame = 0
        self.currently_animating = False
        self.current_animation = None

    def face_feature(self, direction):
        if direction == Direction.DOWN:
            self.update_avatar_image(0, 0)
        elif direction == Direction.UP:
            self.update_avatar_image(0, 1)
        elif direction == Direction.LEFT:
            self.update_avatar_image(0, 3)
        elif direction == Direction.RIGHT:
            self.update_avatar_image(0, 2)

    def initiate_animation(self, animation_name):
        self.current_animation = animation_name
        self.currently_animating = True

    def update_avatar_image(self, image_x, image_y):
        self.current_image_x = image_x
        self.current_image_y = image_y

    def move_avatar(self, x_change, y_change):
        self.image_x += x_change/GameSettings.TILESIZE
        self.image_y += y_change/GameSettings.TILESIZE

    def reset_to_base(self, direction):
        self.face_feature(direction)
        self.animation_frame = 0
        self.currently_animating = False
        self.current_animation = None


class TreeAvatar(FeatureAvatar):
    def __init__(self, name, image_x, image_y, unique_id):
        super().__init__(name, image_x, image_y, unique_id)
        self.type = "Npc"
        self.character_frame_x = 48
        self.character_frame_y = 72
        self.spritesheet = Spritesheet(self.name + "_base_spritesheet", "assets/spritesheets/npc_spritesheets/" + self.name + "_spritesheet.png", self.character_frame_x, self.character_frame_y)
        self.image_offset_y = self.character_frame_y - GameSettings.TILESIZE*3/4
        self.image_offset_x = (GameSettings.TILESIZE - self.character_frame_x)/2


class OldgodAvatar(FeatureAvatar):
    def __init__(self, name, image_x, image_y, unique_id):
        super().__init__(name, image_x, image_y, unique_id)
        self.type = "Npc"
        self.character_frame_x = 96
        self.character_frame_y = 108
        self.spritesheet = Spritesheet(self.name + "_base_spritesheet", "assets/spritesheets/npc_spritesheets/" + self.name + "_spritesheet.png", self.character_frame_x, self.character_frame_y)
        self.image_offset_y = self.character_frame_y - GameSettings.TILESIZE*3/4
        self.image_offset_x = (GameSettings.TILESIZE - self.character_frame_x)/2



class MoveableFeature(object):
    def __init__(self, name, image_x, image_y, unique_name):
        self.name = name
        self.unique_name = unique_name
        self.drawing_priority = 1
        self.character_frame_x = 24
        self.character_frame_y = 36
        self.spritesheet = Spritesheet(self.name + "_base_spritesheet", "assets/spritesheets/npc_spritesheets/" + self.name + "_spritesheet.png", self.character_frame_x, self.character_frame_y)
        self.current_image_x = 0
        self.current_image_y = 0
        self.image_x = image_x
        self.image_y = image_y
        self.size_x = 1
        self.size_y = 1
        self.image_offset_y = self.character_frame_y / 2
        self.image_offset_x = (GameSettings.TILESIZE - self.character_frame_x)/2
        self.animation_list = {}
        self.animation_frame = 0
        self.currently_animating = False
        self.current_animation = None

    def face_feature(self, direction):
        if direction == Direction.DOWN:
            self.update_avatar_image(0, 0)
        elif direction == Direction.UP:
            self.update_avatar_image(0, 1)
        elif direction == Direction.LEFT:
            self.update_avatar_image(0, 3)
        elif direction == Direction.RIGHT:
            self.update_avatar_image(0, 2)

    def initiate_animation(self, animation_name):
        self.current_animation = animation_name
        self.currently_animating = True

    def update_avatar_image(self, image_x, image_y):
        self.current_image_x = image_x
        self.current_image_y = image_y

    def move_avatar(self, x_change, y_change):
        self.image_x += x_change/GameSettings.TILESIZE
        self.image_y += y_change/GameSettings.TILESIZE

    def reset_to_base(self, direction):
        self.face_feature(direction)
        self.animation_frame = 0
        self.currently_animating = False
        self.current_animation = None

class NpcAvatar(MoveableFeature):
    def __init__(self, name, image_x, image_y, unique_id):
        super().__init__(name, image_x, image_y, unique_id)
        self.type = "Npc"
        self.face_image = self.get_face_image()
        self.animation_list = {"walk_front": WalkAnimation(Direction.DOWN),
                               "walk_left": WalkAnimation(Direction.LEFT),
                               "walk_right": WalkAnimation(Direction.RIGHT),
                               "walk_up": WalkAnimation(Direction.UP)}
        self.walk_pattern = [Direction.LEFT, Direction.LEFT, Direction.LEFT, Direction.LEFT, Direction.RIGHT, Direction.RIGHT, Direction.RIGHT, Direction.RIGHT]
        self.currently_animating = False
        self.current_animation = None
        self.step_of_walk_pattern = 0

    def next_walk_pattern_step(self):
        current_step = self.walk_pattern[self.step_of_walk_pattern]
        if self.step_of_walk_pattern < 7:
            self.step_of_walk_pattern += 1
        else:
            self.step_of_walk_pattern = 0
        return current_step

    def get_face_image(self):
        face = self.spritesheet.get_image(0, 0)
        face = face.subsurface(0, 0, 24, 24)
        face = pygame.transform.scale(face, [24 * 5, 24 * 5])
        return face


class Deco(object):
    def __init__(self, name, image_x, image_y):
        self.type = "Deco"
        self.name = name
        self.drawing_priority = 1
        self.character_frame_x = 24
        self.character_frame_y = 36
        self.spritesheet = Spritesheet(self.name + "_base_spritesheet", "assets/spritesheets/decos/grass_deco.png", 20, 20)
        self.current_image_x = 0
        self.current_image_y = 0
        self.image_x = image_x
        self.image_y = image_y
        self.size_x = 1
        self.size_y = 1
        self.image_offset_y = self.character_frame_y / 2
        self.image_offset_x = (GameSettings.TILESIZE - self.character_frame_x)/2
        self.animation_list = {}
        self.animation_frame = 0
        self.currently_animating = False
        self.current_animation = None