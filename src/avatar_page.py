from animations_page import WalkAnimation
from spritesheet import Spritesheet
from definitions import Direction


class PlayerAvatar(object):
    def __init__(self, image_x, image_y):
        self.name = "Player"
        self.type = "Player"
        self.drawing_priority = 1
        self.character_frame_x = 24
        self.character_frame_y = 36
        self.spritesheet = Spritesheet("player_base_spritesheet", "assets/spritesheets/player_spritesheets/player_base_spritesheet.png", self.character_frame_x, self.character_frame_y)
        self.current_image_x = 0
        self.current_image_y = 0
        self.image_x = image_x
        self.image_y = image_y
        self.size_x = 1
        self.size_y = 1
        self.image_offset_y = self.character_frame_y/2
        self.animation_list = {"walk_front": WalkAnimation(Direction.DOWN),
                               "walk_left": WalkAnimation(Direction.LEFT),
                               "walk_right": WalkAnimation(Direction.RIGHT),
                               "walk_up": WalkAnimation(Direction.UP)}
        self.animation_frame = 0
        self.currently_animating = False
        self.current_animation = None

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


class NpcAvatar(object):
    def __init__(self, name, image_x, image_y):
        self.name = name
        self.drawing_priority = 1
        self.type = "Npc"
        self.character_frame_x = 24
        self.character_frame_y = 36
        self.spritesheet = Spritesheet(self.name + "_base_spritesheet", "assets/spritesheets/npc_spritesheets/" + self.name + "_spritesheet.png", self.character_frame_x, self.character_frame_y)
        self.current_image_x = 0
        self.current_image_y = 0
        self.image_x = image_x
        self.image_y = image_y
        self.size_x = 1
        self.size_y = 1
        self.image_offset_y = self.character_frame_y/2
        self.animation_list = {"walk_front": WalkAnimation(Direction.DOWN),
                               "walk_left": WalkAnimation(Direction.LEFT),
                               "walk_right": WalkAnimation(Direction.RIGHT),
                               "walk_up": WalkAnimation(Direction.UP)}
        self.animation_frame = 0
        self.currently_animating = False
        self.current_animation = None

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
