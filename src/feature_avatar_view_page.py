import pygame

from animations_page_view_page import WalkAnimation, StationaryAnimation, BirdAnimation, DeedleAnimation, SpeedWalkAnimation
from spritesheet import Spritesheet
from definitions import Direction, GameSettings, Types, Mundane


class PlayerAvatar(object):
    def __init__(self, image_x, image_y):
        self.species = "Player"
        self.feature_type = "Player"
        self.drawing_priority = 1
        self.character_frame_x = 32
        self.character_frame_y = 48
        self.spritesheet = Spritesheet("player_base_spritesheet", "assets/spritesheets/player_spritesheets/player_green_shirt_spritesheet.png", self.character_frame_x, self.character_frame_y)
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
                               "walk_up": WalkAnimation(Direction.UP),
                               "snap_photo_down": StationaryAnimation(Direction.DOWN),
                               "snap_photo_left": StationaryAnimation(Direction.LEFT),
                               "snap_photo_right": StationaryAnimation(Direction.RIGHT),
                               "snap_photo_up": StationaryAnimation(Direction.UP),
                               "peck": BirdAnimation(Direction.DOWN)}
        self.animation_frame = 0
        self.currently_animating = False
        self.current_animation = None

    def get_face_image(self):
        face = self.spritesheet.get_image(0, 0)
        face = face.subsurface(0, 0, 24, 24)
        face = pygame.transform.scale(face, [24 * 4, 24 * 4])
        return face

    def face_character(self, direction):
        y_img = Mundane.direction_feedback(direction, 3, 2, 1, 0)
        self.update_avatar_image(0, y_img)


    def initiate_animation(self, animation_name):
        self.current_animation = animation_name
        self.currently_animating = True

    def update_avatar_image(self, image_x, image_y):
        self.current_image_x = image_x
        self.current_image_y = image_y


class FeatureAvatar(object):
    def __init__(self, species, image_x, image_y, unique_name, base_size_x, base_size_y, spawn_facing):
        self.species = species
        self.spawn_facing = spawn_facing
        self.unique_name = unique_name
        self.drawing_priority = 1
        self.feature_type = Types.DEFAULT
        self.character_frame_x = 24
        self.character_frame_y = 36
        self.current_image_x = 0
        self.current_image_y = 0
        self.image_x = image_x
        self.image_y = image_y
        self.image_offset_y = self.character_frame_y - GameSettings.TILESIZE*3/4 - (base_size_y * GameSettings.TILESIZE - GameSettings.TILESIZE)
        self.image_offset_x = (base_size_x*GameSettings.TILESIZE - self.character_frame_x)/2
        self.animation_list = {}
        self.animation_frame = 0
        self.currently_animating = False
        self.current_animation = None

    def face_feature(self, direction):
        y_img = Mundane.direction_feedback(direction, 3, 2, 1, 0)
        self.update_avatar_image(0, y_img)

    def initiate_animation(self, animation_name):
        self.current_animation = animation_name
        self.currently_animating = True

    def update_avatar_image(self, image_x, image_y):
        self.current_image_x = image_x
        self.current_image_y = image_y

    def move_avatar(self, x_change, y_change):
        self.image_x += x_change/GameSettings.TILESIZE
        self.image_y += y_change/GameSettings.TILESIZE

    def reset_to_base(self):
        self.face_feature(self.spawn_facing)
        self.animation_frame = 0
        self.currently_animating = False
        self.current_animation = None

    def reset_to_spawn(self, ghost):
        self.image_x = ghost.spawn_x
        self.image_y = ghost.spawn_y
        self.face_feature(self.spawn_facing)
        self.animation_frame = 0
        self.currently_animating = False
        self.current_animation = None

    def run_setup(self, base_size_x, base_size_y):
        self.spritesheet = Spritesheet(self.species + "_base_spritesheet", "assets/spritesheets/npc_spritesheets/" + self.species + "_spritesheet.png", self.character_frame_x, self.character_frame_y)
        # self.image_offset_y = self.character_frame_y - GameSettings.TILESIZE*3/4 - (base_size_y * GameSettings.TILESIZE - GameSettings.TILESIZE)
        basic_y_offset = GameSettings.TILESIZE - GameSettings.TILESIZE*2/4 + GameSettings.TILESIZE*1/4
        self.image_offset_y = basic_y_offset + ((base_size_y - 1) * GameSettings.TILESIZE)
        self.image_offset_x = (base_size_x*GameSettings.TILESIZE - self.character_frame_x)/2
        self.face_image = self.get_face_image()
        self.face_feature(self.spawn_facing)

    def get_face_image(self):
        face = self.spritesheet.get_image(0, 0)
        face = face.subsurface(0, 0, 24, 24)
        face = pygame.transform.scale(face, [24 * 5, 24 * 5])
        return face


class TreeAvatar(FeatureAvatar):
    def __init__(self, species, image_x, image_y, unique_id, base_size_x, base_size_y, spawn_facing):
        super().__init__(species, image_x, image_y, unique_id, base_size_x, base_size_y, spawn_facing)
        self.feature_type = Types.NPC
        self.character_frame_x = 32
        self.character_frame_y = 48
        self.run_setup(base_size_x, base_size_y)


class PropAvatar(FeatureAvatar):
    def __init__(self, species, image_x, image_y, unique_id, base_size_x, base_size_y, spawn_facing):
        super().__init__(species, image_x, image_y, unique_id, base_size_x, base_size_y, spawn_facing)
        self.feature_type = Types.PROP
        self.character_frame_x = 32 * base_size_x
        self.character_frame_y = 32 * base_size_y + 16
        self.run_setup(base_size_x, base_size_y)


class HouseAvatar(FeatureAvatar):
    def __init__(self, species, image_x, image_y, unique_id, base_size_x, base_size_y, spawn_facing):
        super().__init__(species, image_x, image_y, unique_id, base_size_x, base_size_y, spawn_facing)
        self.feature_type = Types.PROP
        self.character_frame_x = 32 * base_size_x
        self.character_frame_y = 32 * base_size_y + 16
        self.run_setup(base_size_x, base_size_y)


class NPCAvatar(FeatureAvatar):
    def __init__(self, species, image_x, image_y, unique_id, base_size_x, base_size_y, spawn_facing):
        super().__init__(species, image_x, image_y, unique_id, base_size_x, base_size_y, spawn_facing)
        self.feature_type = Types.NPC
        self.character_frame_x = 32
        self.character_frame_y = 48
        self.run_setup(base_size_x, base_size_y)

        self.animation_list = {"walk_front": WalkAnimation(Direction.DOWN),
                               "walk_left": WalkAnimation(Direction.LEFT),
                               "walk_right": WalkAnimation(Direction.RIGHT),
                               "walk_up": WalkAnimation(Direction.UP)}
        self.step_of_walk_pattern = 0
        self.walk_pattern = [Direction.LEFT, Direction.LEFT, Direction.LEFT, Direction.LEFT, Direction.RIGHT, Direction.RIGHT, Direction.RIGHT, Direction.RIGHT]

    def next_walk_pattern_step(self):
        current_step = self.walk_pattern[self.step_of_walk_pattern]
        if self.step_of_walk_pattern < 7:
            self.step_of_walk_pattern += 1
        else:
            self.step_of_walk_pattern = 0
        return current_step

    def get_face_image(self):
        face = self.spritesheet.get_image(0, 0)
        face = face.subsurface(4, 11, 24, 24)
        face = pygame.transform.scale(face, [24 * 5, 24 * 5])
        return face


class BirdAvatar(FeatureAvatar):
    def __init__(self, species, image_x, image_y, unique_id, base_size_x, base_size_y, spawn_facing):
        super().__init__(species, image_x, image_y, unique_id, base_size_x, base_size_y, spawn_facing)
        self.feature_type = Types.NPC
        self.character_frame_x = 32
        self.character_frame_y = 48
        self.run_setup(base_size_x, base_size_y)

        self.animation_list = {"walk_front": SpeedWalkAnimation(Direction.DOWN),
                               "walk_left": SpeedWalkAnimation(Direction.LEFT),
                               "walk_right": SpeedWalkAnimation(Direction.RIGHT),
                               "walk_up": SpeedWalkAnimation(Direction.UP),
                               "snap_photo_down": StationaryAnimation(Direction.DOWN),
                               "snap_photo_left": StationaryAnimation(Direction.LEFT),
                               "snap_photo_right": StationaryAnimation(Direction.RIGHT),
                               "snap_photo_up": StationaryAnimation(Direction.UP),
                               "peck": BirdAnimation(Direction.DOWN),
                               "deedle": DeedleAnimation(Direction.DOWN)}
        self.step_of_walk_pattern = 0
        self.walk_pattern = [Direction.LEFT, Direction.LEFT, Direction.LEFT, Direction.LEFT, Direction.RIGHT, Direction.RIGHT, Direction.RIGHT, Direction.RIGHT]

    def next_walk_pattern_step(self):
        current_step = self.walk_pattern[self.step_of_walk_pattern]
        if self.step_of_walk_pattern < 7:
            self.step_of_walk_pattern += 1
        else:
            self.step_of_walk_pattern = 0
        return current_step

    def get_face_image(self):
        face = self.spritesheet.get_image(0, 0)
        face = face.subsurface(4, 11, 24, 24)
        face = pygame.transform.scale(face, [24 * 5, 24 * 5])
        return face

    def initiate_animation(self, animation_name):
        self.current_animation = animation_name
        self.currently_animating = True


class OldgodAvatar(FeatureAvatar):
    def __init__(self, species, image_x, image_y, unique_id, base_size_x, base_size_y, spawn_facing):
        super().__init__(species, image_x, image_y, unique_id, base_size_x, base_size_y, spawn_facing)
        self.feature_type = Types.NPC
        self.character_frame_x = 96
        self.character_frame_y = 108
        self.spritesheet = Spritesheet(self.species + "_base_spritesheet", "assets/spritesheets/npc_spritesheets/" + self.species + "_spritesheet.png", self.character_frame_x, self.character_frame_y)
        self.image_offset_y = self.character_frame_y - GameSettings.TILESIZE*3/4 - (base_size_y * GameSettings.TILESIZE - GameSettings.TILESIZE)
        self.image_offset_x = (base_size_x*GameSettings.TILESIZE - self.character_frame_x)/2


class DecoAvatar(object):
    def __init__(self, species, image_x, image_y, unique_id, base_size_x, base_size_y, spawn_facing):
        self.feature_type = Types.DECO
        self.species = species
        self.unique_name = unique_id
        self.drawing_priority = 1
        self.character_frame_x = 32
        self.character_frame_y = 48
        self.spritesheet = Spritesheet(self.species + "_base_spritesheet", "assets/spritesheets/deco_spritesheets/Grass_spritesheet.png", 32, 48)
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
        self.run_setup(base_size_x, base_size_y)

    def run_setup(self, base_size_x, base_size_y):
        self.spritesheet = Spritesheet(self.species + "_base_spritesheet", "assets/spritesheets/deco_spritesheets/" + self.species + "_spritesheet.png", self.character_frame_x, self.character_frame_y)
        basic_y_offset = GameSettings.TILESIZE - GameSettings.TILESIZE*2/4
        self.image_offset_y = basic_y_offset + ((base_size_y - 1) * GameSettings.TILESIZE)
        self.image_offset_x = (base_size_x*GameSettings.TILESIZE - self.character_frame_x)/2

