from spritesheet import Spritesheet
from definitions import Direction


class PlayerAvatar:
    def __init__(self, gv_input, image_x, image_y):
        self.gv_input = gv_input
        self.character_frame_x = 24
        self.character_frame_y = 36
        self.spritesheet = Spritesheet("player_base_spritesheet", "assets/spritesheets/player.png", self.character_frame_x, self.character_frame_y)
        self.current_image_x = 0
        self.current_image_y = 0
        self.image_x = image_x
        self.image_y = image_y
        self.image_offset_y = self.character_frame_y/2
        self.animation_list = {"walk_front": WalkAnimation(self, Direction.DOWN),
                               "walk_left": WalkAnimation(self, Direction.LEFT),
                               "walk_right": WalkAnimation(self, Direction.RIGHT),
                               "walk_up": WalkAnimation(self, Direction.UP)}
        self.animation_frame = 0
        self.currently_animating = False
        self.current_animation = None

    def face_character(self, direction):
        if direction == Direction.DOWN:
            self.current_image_x = 0
            self.current_image_y = 0
        elif direction == Direction.UP:
            self.current_image_x = 0
            self.current_image_y = 1
        elif direction == Direction.LEFT:
            self.current_image_x = 0
            self.current_image_y = 3
        elif direction == Direction.RIGHT:
            self.current_image_x = 0
            self.current_image_y = 2

    def initiate_animation(self, animation_name):
        self.current_animation = animation_name
        self.currently_animating = True

    def perform_animation(self):
        animation_result = (self.animation_list[self.current_animation].animate())
        self.current_image_x = animation_result[2]
        self.current_image_y = animation_result[3]
        self.gv_input.camera[0] += animation_result[0]
        self.gv_input.camera[1] += animation_result[1]
        complete = animation_result[4]
        if complete:
            self.currently_animating = False
            self.current_animation = None


class Animation(object):
    def __init__(self, gv_input, direction):
        self.gv_input = gv_input
        self.total_distance = 0
        self.direction = direction
        self.current_frame = 0
        self.frequency = 0

        self.complete = False

        self.y_change = 0
        self.x_change = 0
        self.current_image_x = 0
        self.current_image_y = 0
        self.vector = 1
        self.changing_variable = self.x_change
        if self.direction == Direction.UP:
            self.vector = -1
            self.changing_variable = self.y_change
            self.current_image_y = 1

        elif self.direction == Direction.LEFT:
            self.vector = -1
            self.current_image_y = 2

        elif self.direction == Direction.DOWN:
            self.current_image_y = 0
            self.changing_variable = self.y_change

        elif self.direction == Direction.RIGHT:
            self.current_image_y = 3

    def animate(self):
        pass


class WalkAnimation(Animation):
    def __init__(self, gv_input, direction):
        super().__init__(gv_input, direction)
        self.foot = "left"
        self.current_image_x = 0
        self.current_image_y = 0
        self.x_vector = 0
        self.y_vector = 0
        self.set_directions()

    def set_directions(self):
        if self.direction == Direction.UP:
            self.y_vector = -1
            self.x_vector = 0
            self.changing_variable = self.y_change
            self.current_image_y = 1
        elif self.direction == Direction.LEFT:
            self.y_vector = 0
            self.x_vector = -1
            self.current_image_y = 3
        elif self.direction == Direction.DOWN:
            self.y_vector = 1
            self.x_vector = 0
            self.current_image_y = 0
            self.changing_variable = self.y_change
        elif self.direction == Direction.RIGHT:
            self.y_vector = 0
            self.x_vector = 1
            self.current_image_y = 2

    def animate(self):
        if self.current_frame <= 23:
            if self.current_frame == 0:
                if self.foot == "left":
                    self.current_image_x = 3
                elif self.foot == "right":
                    self.current_image_x = 1

            elif self.current_frame == 23:
                self.current_frame = 0
                self.current_image_x = 0
                self.complete = True

            self.current_frame += 1
        return self.result()

    def reset(self):
        self.current_frame = 0
        self.switch_foot()
        self.complete = False

    def switch_foot(self):
        if self.foot == "left":
            self.foot = "right"
        elif self.foot == "right":
            self.foot = "left"

    def result(self):
        y_change = self.y_vector
        x_change = self.x_vector
        sheet_x = self.current_image_x
        sheet_y = self.current_image_y
        complete = self.complete
        if self.complete:
            self.reset()

        return x_change, y_change, sheet_x, sheet_y, complete
