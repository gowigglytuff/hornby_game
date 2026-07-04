import random
from definitions import Direction, GameSettings, Types, Mundane
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

        self.changing_variable = self.x_change
        self.x_vector = 0
        self.y_vector = 0
        self.set_directions()

    def animate(self):
        pass

    def set_directions(self):
        self.x_vector = Mundane.direction_feedback(self.direction, -1, 1, 0, 0)
        self.y_vector = Mundane.direction_feedback(self.direction, 0, 0, -1, 1)
        self.changing_variable = Mundane.direction_feedback(self.direction, self.x_change, self.x_change, self.y_change, self.y_change)
        self.current_image_y = Mundane.direction_feedback(self.direction, 3, 2, 1, 0)



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
        self.delta_time_tracker = 0

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

class SpeedWalkAnimation(Animation):
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
        self.x_vector = Mundane.direction_feedback(self.direction, -2, 2, 0, 0)
        self.y_vector = Mundane.direction_feedback(self.direction, 0, 0, -2, 2)
        self.changing_variable = Mundane.direction_feedback(self.direction, self.x_change, self.x_change, self.y_change, self.y_change)
        self.current_image_y = Mundane.direction_feedback(self.direction, 3, 2, 1, 0)

    def animate(self):
        if self.current_frame <= (GameSettings.TILESIZE/2-1):
            if self.current_frame == 0:
                if self.foot == "left":
                    self.current_image_x = 3
                elif self.foot == "right":
                    self.current_image_x = 1
                self.current_frame += 1
            elif self.current_frame == (GameSettings.TILESIZE/2-1):
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
        self.current_image_y = Mundane.direction_feedback(self.direction, 7, 6, 5, 4)

    def direction_y_to_return_to(self):
        self.current_image_y = Mundane.direction_feedback(self.direction, 3, 2, 1, 0)

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
        self.current_image_y = Mundane.direction_feedback(self.direction, 3, 2, 1, 0)


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
        self.current_image_y = Mundane.direction_feedback(self.direction, 4, 3, 1, 0)

    def direction_y_to_return_to(self):
        self.current_image_y = Mundane.direction_feedback(self.direction, 3, 2, 1, 0)

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


class CameraPanAnimation(object):
    AN_TYPE = "camera"
    def __init__(self, direction, number_of_tiles):
        self.complete = False
        self.y_change = 0
        self.x_change = 0
        self.y_speed = 0
        self.x_speed = 0


        self.total_tiles = 0
        self.total_movement_distance = 0
        self.frame_counter = 0
        self.frame_speed = 10
        self.direction = None
        self.current_frame = 0
        self.speed_multiplier = 1
        self.speed_tracker = 0
        self.set_animation(direction, number_of_tiles)

    def set_animation(self, direction, number_of_tiles):
        self.complete = False
        self.total_tiles = number_of_tiles
        self.total_movement_distance = abs(number_of_tiles) * GameSettings.TILESIZE

        vector_x, vector_y = Direction.get_vector_from_direction(direction)
        self.y_speed = vector_y * 2
        self.x_speed = vector_x * 2

    def animate(self):
        if self.speed_tracker == self.speed_multiplier:
            self.y_change = self.y_speed
            self.x_change = self.x_speed
            self.speed_tracker = 0
        else:
            self.y_change = 0
            self.x_change = 0
            self.speed_tracker += 1

        if self.frame_counter == self.total_movement_distance:
            self.complete = True
        else:
            self.frame_counter += 1

        return self.result()

    def result(self):
        camera_y_change = self.y_change
        camera_x_change = self.x_change
        complete = self.complete
        follow_up_package = {}
        if self.x_speed != 0:
            follow_up_package = {"x_move": self.total_tiles, "y_move": 0}
        elif self.y_speed != 0:
            follow_up_package = {"x_move": 0, "y_move": self.total_tiles}
        if self.complete:
            self.reset()

        return camera_x_change, camera_y_change, complete, follow_up_package

    def reset(self):
        self.y_change = 0
        self.x_change = 0
        self.speed_tracker = 0
        self.current_frame = 0
        self.frame_counter = 0
        # self.complete = False


class Action(object):
    def __init__(self):
        self.action_type = "movement"
        self.movement_list = []
        self.animation_sequence = []
        self.initial_direction_facing = None
        self.current_action = 0
        self.total_actions = len(self.movement_list)

    def initiate(self, initial_direction_facing):
        self.initial_direction_facing = initial_direction_facing
        self.total_actions = len(self.movement_list)

    def check_if_complete(self):
        result = False
        if self.current_action == self.total_actions:
            result = True
        return result

    def reset(self):
        self.current_action = 0


class Switch(Action):
    def __init__(self):
        super().__init__()
        self.movement_list = [(-1, 0), (1, 0)]
        self.animation_sequence = ["walk_left", "look_around", "up_down", "look_around", "walk_right", "look_around", "up_down", "look_around"]
        self.animation_sequence = ["walk_left", "walk_right"]
        assert len(self.movement_list) == len(self.animation_sequence)
        self.initial_direction_facing = Direction.RIGHT
        self.current_action = 0
        self.total_actions = len(self.movement_list)