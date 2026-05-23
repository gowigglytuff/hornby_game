import random

from definitions import Direction, GameSettings, Types
from spritesheet import Spritesheet


class Animation(object):
    def __init__(self, direction):
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
    def __init__(self, direction):
        super().__init__(direction)
        self.foot = "left"
        self.current_frame = 0
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
        if self.current_frame <= (GameSettings.TILESIZE-1):
            if self.current_frame == 0:
                if self.foot == "left":
                    self.current_image_x = 3
                elif self.foot == "right":
                    self.current_image_x = 1
                self.current_frame += 1

            elif self.current_frame == (GameSettings.TILESIZE-1):
                self.current_frame = 0
                self.current_image_x = 0
                self.complete = True
            else:
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


class StationaryAnimation(object):
    def __init__(self, direction):
        self.direction = direction
        self.current_frame = 0
        self.frequency = 0

        self.complete = False

        self.y_change = 0
        self.x_change = 0
        self.current_image_x = 0
        self.current_image_y = 0
        self.changing_variable = self.x_change

    def direction_to_y_image(self):
        if self.direction == Direction.UP:
            self.current_image_y = 5

        elif self.direction == Direction.LEFT:
            self.current_image_y = 7

        elif self.direction == Direction.DOWN:
            self.current_image_y = 4

        elif self.direction == Direction.RIGHT:
            self.current_image_y = 6

    def direction_y_to_return_to(self):
        if self.direction == Direction.UP:
            self.current_image_y = 1

        elif self.direction == Direction.LEFT:
            self.current_image_y = 3

        elif self.direction == Direction.DOWN:
            self.current_image_y = 0

        elif self.direction == Direction.RIGHT:
            self.current_image_y = 2

    def animate(self):
        self.direction_to_y_image()
        if self.current_frame == 0:
            self.current_image_x = 0
        elif self.current_frame == 20:
            self.current_image_x = 1
        elif self.current_frame == 40:
            self.current_image_x = 2
        elif self.current_frame == 60:
            self.current_image_x = 3
        self.current_frame += 1
        if self.current_frame == 80:
            self.current_frame = 0
            self.complete = True
            self.current_image_x = 0
            self.direction_y_to_return_to()

        return self.result()

    def result(self):
        y_change = 0
        x_change = 0
        sheet_x = self.current_image_x
        sheet_y = self.current_image_y
        complete = self.complete
        if self.complete:
            self.reset()

        return x_change, y_change, sheet_x, sheet_y, complete

    def reset(self):
        self.current_frame = 0
        self.complete = False


class BirdAnimation(object):
    def __init__(self, direction):
        self.direction = direction
        self.current_frame = 0
        self.frequency = 0

        self.complete = False

        self.y_change = 0
        self.x_change = 0
        self.current_image_x = 0
        self.current_image_y = 0
        self.changing_variable = self.x_change

    def direction_to_y_image(self):
        if self.direction == Direction.UP:
            self.current_image_y = 1

        elif self.direction == Direction.LEFT:
            self.current_image_y = 4

        elif self.direction == Direction.DOWN:
            self.current_image_y = 0

        elif self.direction == Direction.RIGHT:
            self.current_image_y = 3

    def direction_y_to_return_to(self):
        if self.direction == Direction.UP:
            self.current_image_y = 1

        elif self.direction == Direction.LEFT:
            self.current_image_y = 3

        elif self.direction == Direction.DOWN:
            self.current_image_y = 0

        elif self.direction == Direction.RIGHT:
            self.current_image_y = 2

    def animate(self):
        self.direction_to_y_image()
        if self.current_frame == 0:
            self.current_image_x = 0
        elif self.current_frame == 20:
            self.current_image_x = 1
        elif self.current_frame == 40:
            self.current_image_x = 2
        elif self.current_frame == 60:
            self.current_image_x = 3
        self.current_frame += 1
        if self.current_frame == 80:
            self.current_frame = 0
            self.complete = True
            self.current_image_x = 0
            self.direction_y_to_return_to()

        return self.result()

    def result(self):
        y_change = 0
        x_change = 0
        sheet_x = self.current_image_x
        sheet_y = self.current_image_y
        complete = self.complete
        if self.complete:
            self.reset()

        return x_change, y_change, sheet_x, sheet_y, complete

    def reset(self):
        self.current_frame = 0
        self.complete = False


class DeedleAnimation(BirdAnimation):
    def __init__(self, direction):
        super().__init__(direction)
        self.x_change = 0
        self.y_change = 0
        self.action = 1
        self.action_name = None
        self.current_alignment = "left"

    def animate(self):
        self.direction_to_y_image()
        self.x_change = 0
        self.y_change = 0
        print(self.current_frame)
        if self.current_frame == 20:
            if self.action == 1:
                my_list = []
                if self.current_alignment == "left":
                    my_list = ["hop_right", "deedle_right", "hop_up"]
                elif self.current_alignment == "right":
                    my_list = ["hop_left", "deedle_left", "hop_up"]
                random_item = random.choice(my_list)
                if random_item == "hop_left":
                    self.x_change = -2
                    self.y_change = -2
                    self.current_alignment = "left"
                elif random_item == "deedle_left":
                    self.x_change = -6
                    self.y_change = 0
                    self.current_alignment = "left"
                elif random_item == "hop_right":
                    self.x_change = 2
                    self.y_change = -2
                    self.current_alignment = "right"
                elif random_item == "deedle_right":
                    self.x_change = 6
                    self.y_change = 0
                    self.current_alignment = "right"
                elif random_item == "hop_up":
                    self.x_change = 0
                    self.y_change = -2
                self.action_name = random_item
                self.action = 2
        if self.current_frame == 40:
            if self.action == 2:
                if self.action_name == "hop_left":
                    self.x_change = -2
                    self.y_change = 2
                elif self.action_name == "hop_right":
                    self.x_change = 2
                    self.y_change = 2
                elif self.action_name == "deedle_right":
                    self.x_change = -2
                    self.y_change = 0
                elif self.action_name == "deedle_left":
                    self.x_change = 2
                    self.y_change = 0
                elif self.action_name == "hop_up":
                    self.x_change = 0
                    self.y_change = 2
                self.action_name = None
                self.action = 1
        # if self.current_frame == 20:
        #     self.x_change = -2
        #     self.y_change = -2
        # elif self.current_frame == 40:
        #     self.x_change = -2
        #     self.y_change = 2
        # elif self.current_frame == 120:
        #     self.x_change = 0
        #     self.y_change = -2
        # elif self.current_frame == 140:
        #     self.x_change = 0
        #     self.y_change = 2
        # elif self.current_frame == 160:
        #     self.x_change = 0
        #     self.y_change = -2
        # elif self.current_frame == 180:
        #     self.x_change = 0
        #     self.y_change = 2
        # elif self.current_frame == 280:
        #     self.x_change = 1
        #     self.y_change = 0
        # elif self.current_frame == 300:
        #     self.x_change = -2
        #     self.y_change = 0
        # elif self.current_frame == 320:
        #     self.x_change = 1
        #     self.y_change = 0
        # elif self.current_frame == 380:
        #     self.x_change = 2
        #     self.y_change = -2
        # elif self.current_frame == 400:
        #     self.x_change = 2
        #     self.y_change = 2

        self.current_frame += 1
        if self.current_frame == 200:
            self.current_frame = 0
            self.complete = True
            self.current_image_x = 0
            self.direction_y_to_return_to()
        return self.result()

    def result(self):
        y_change = self.y_change
        x_change = self.x_change
        sheet_x = 0
        sheet_y = 0
        complete = self.complete
        if self.complete:
            self.reset()

        return x_change, y_change, sheet_x, sheet_y, complete

    def reset(self):
        self.current_frame = 0
        self.complete = False


class HopAnimation(object):
    def __init__(self, direction):
        self.direction = direction
        self.current_frame = 0
        self.frequency = 0

        self.complete = False

        self.y_change = 0
        self.x_change = 0
        self.current_image_x = 0
        self.current_image_y = 0
        self.changing_variable = self.x_change

    def direction_to_y_image(self):
        if self.direction == Direction.UP:
            self.current_image_y = 1

        elif self.direction == Direction.LEFT:
            self.current_image_y = 4

        elif self.direction == Direction.DOWN:
            self.current_image_y = 0

        elif self.direction == Direction.RIGHT:
            self.current_image_y = 3

    def direction_y_to_return_to(self):
        if self.direction == Direction.UP:
            self.current_image_y = 1

        elif self.direction == Direction.LEFT:
            self.current_image_y = 3

        elif self.direction == Direction.DOWN:
            self.current_image_y = 0

        elif self.direction == Direction.RIGHT:
            self.current_image_y = 2

    def animate(self):
        self.direction_to_y_image()
        if self.current_frame == 0:
            self.current_image_x = 0
        elif self.current_frame == 20:
            self.current_image_x = 1
        elif self.current_frame == 40:
            self.current_image_x = 2
        elif self.current_frame == 60:
            self.current_image_x = 3
        self.current_frame += 1
        if self.current_frame == 80:
            self.current_frame = 0
            self.complete = True
            self.current_image_x = 0
            self.direction_y_to_return_to()

        return self.result()

    def result(self):
        y_change = 0
        x_change = 0
        sheet_x = self.current_image_x
        sheet_y = self.current_image_y
        complete = self.complete
        if self.complete:
            self.reset()

        return x_change, y_change, sheet_x, sheet_y, complete

    def reset(self):
        self.current_frame = 0
        self.complete = False


class IndependentAnimation(object):
    def __init__(self, animation_name):
        self.unique_name = animation_name
        self.direction = None
        self.current_frame = 0
        self.frequency = 0
        self.drawing_priority = 1
        self.feature_type = Types.INDANIM
        self.unique_name = None

        self.complete = False

        self.y_change = 0
        self.x_change = 0
        self.current_image_x = 0
        self.current_image_y = 0
        self.spritesheet = None

        self.image_offset_x = 0
        self.image_offset_y = 0

        self.room = None
        self.frame_counter = 0
        self.total_images = 0
        self.frame_speed = 0

    def animate(self):
        if self.frame_counter >= self.frame_speed:
            self.frame_counter = 0
            self.current_image_x += 1

        else:
            self.frame_counter += 1
        self.current_frame += 1

        if self.current_image_x == (self.total_images + 1):
            self.complete = True

        return self.result()

    def result(self):
        y_change = 0
        x_change = 0
        sheet_x = self.current_image_x
        sheet_y = self.current_image_y
        complete = self.complete
        if self.complete:
            self.reset()

        return x_change, y_change, sheet_x, sheet_y, complete

    def reset(self):
        self.current_frame = 0
        self.complete = False


class BirdDisappearAnimation(IndependentAnimation):
    def __init__(self, animation_name, bird_unique_name, room, drawing_priority, image_x, image_y, image_offset_x, image_offset_y):
        super().__init__(animation_name)
        self.drawing_priority = drawing_priority
        self.complete = False
        self.y_change = 0
        self.x_change = 0
        self.current_image_x = 0
        self.current_image_y = 0
        self.spritesheet = Spritesheet("bird_disappear", "assets/spritesheets/independent_animation_spritesheets/bird_disappear_animation_spritesheet.png", 32, 48)

        self.image_x = image_x
        self.image_y = image_y

        self.image_offset_x = image_offset_x
        self.image_offset_y = image_offset_y

        self.room = room
        self.frame_counter = 0
        self.total_images = 22
        self.frame_speed = 10