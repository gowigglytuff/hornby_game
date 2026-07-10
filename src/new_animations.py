import copy
import random
from definitions import Direction, GameSettings, Types, Mundane
from spritesheet import Spritesheet


class Animationy(object):
    def __init__(self, direction):
        self.direction = direction
        self.current_frame = 0
        self.frequency = 0
        self.step_distance = 1
        self.set_up_step_distances_and_images()
        self.distance_tracker = 0

        self.x_direct = 0
        self.y_direct = 0
        self.y_image_set = None

        self.complete = False
        self.current_tick = 0
        self.y_change = 0
        self.x_change = 0
        self.y_speed = 0
        self.x_speed = 0
        self.current_image_x = None
        self.current_image_y = None
        self.total_acts = 10
        self.hit_every_xth_frame = 1
        self.number_of_intervals = 4
        self.interval = self.total_acts / self.number_of_intervals
        self.frame_action_dict = {0: {"x_speed": self.x_direct,
                                      "y_speed": self.y_direct,
                                      "current_image_x": 0,
                                      "current_image_y": self.y_image_set},
                                  1: {"x_speed": self.x_direct,
                                      "y_speed": self.y_direct},
                                  2: {"x_speed": self.x_direct,
                                      "y_speed": self.y_direct},
                                  3: {"x_speed": self.x_direct,
                                      "y_speed": self.y_direct}
                                  }

    def set_up_step_distances_and_images(self):
        if self.direction == Direction.LEFT:
            self.x_direct = -self.step_distance
            self.y_image_set = 3
        elif self.direction == Direction.RIGHT:
            self.x_direct = self.step_distance
            self.y_image_set = 2
        elif self.direction == Direction.UP:
            self.y_direct = -self.step_distance
            self.y_image_set = 1
        elif self.direction == Direction.DOWN:
            self.y_direct = self.step_distance
            self.y_image_set = 0
        else:
            pass

    def tick_animation(self):
        result = False
        if self.current_tick < self.hit_every_xth_frame:
            self.current_tick += 1
        else:
            self.current_tick = 0
            result = True
        return result

    def direction_to_y_image(self):
        self.current_image_y = Mundane.direction_feedback(self.direction, 4, 3, 1, 0)

    def direction_y_to_return_to(self):
        self.current_image_y = Mundane.direction_feedback(self.direction, 3, 2, 1, 0)

    def animate(self):
        if self.tick_animation():

            result_dict = self.check_action(self.current_frame)
            if "x_speed" in result_dict.keys():
                self.x_speed = result_dict["x_speed"]

            if "y_speed" in result_dict.keys():
                self.y_speed = result_dict["y_speed"]

            if "current_image_x" in result_dict.keys():
                self.current_image_x = result_dict["current_image_x"]

            if "current_image_y" in result_dict.keys():
                self.current_image_y = result_dict["current_image_y"]

            self.x_change = self.x_speed
            self.y_change = self.y_speed

            self.current_frame += 1
        else:
            self.y_change = 0
            self.x_change = 0
        return self.result()

    def check_action(self, frame_number):
        numbs = []
        for x in range(self.number_of_intervals):
            numbs.append((x+1)*self.interval)

        valid_options = [x for x in numbs if x > frame_number]
        if frame_number < self.total_acts:
            index = numbs.index(min(valid_options))
            result = self.frame_action_dict[index]
        else:
            result = {}
        return result

    def result(self):
        y_change = copy.copy(self.y_change)
        x_change = copy.copy(self.x_change)
        sheet_x = copy.copy(self.current_image_x)
        sheet_y = copy.copy(self.current_image_y)
        complete = False
        if self.current_frame == self.total_acts:
            complete = True
            sheet_x = 0
            self.reset()

        return x_change, y_change, sheet_x, sheet_y, complete

    def reset(self):
        self.current_frame = 0
        self.complete = False
        self.y_change = 0
        self.x_change = 0
        self.y_speed = 0
        self.x_speed = 0
        self.current_image_x = None
        self.current_image_y = None


class WalkyAnimationy(Animationy):
    def __init__(self, direction):
        super().__init__(direction)
        self.step_distance = 1
        self.set_up_step_distances_and_images()
        self.total_acts = 32
        self.hit_every_xth_frame = 1
        self.number_of_intervals = 2
        self.interval = self.total_acts/self.number_of_intervals
        self.frame_action_dict = {0: {"x_speed": self.x_direct,
                                      "y_speed": self.y_direct,
                                      "current_image_x": 1,
                                      "current_image_y": self.y_image_set},
                                  1: {"current_image_x": 3}
                                  }


class SpeedWalkyAnimationy(Animationy):
    def __init__(self, direction):
        super().__init__(direction)
        self.step_distance = 2
        self.set_up_step_distances_and_images()

        self.total_acts = 16
        self.hit_every_xth_frame = 2
        self.number_of_intervals = 2
        self.interval = self.total_acts/self.number_of_intervals
        self.frame_action_dict = {0: {"x_speed": self.x_direct,
                                      "y_speed": self.y_direct,
                                      "current_image_x": 1,
                                      "current_image_y": self.y_image_set},
                                  1: {"current_image_x": 3}
                                  }

class RunAnimationy(Animationy):
    def __init__(self, direction):
        super().__init__(direction)
        self.step_distance = 1
        self.set_up_step_distances_and_images()
        self.total_acts = 32
        self.hit_every_xth_frame = 0
        self.number_of_intervals = 2
        self.interval = self.total_acts/self.number_of_intervals
        self.frame_action_dict = {0: {"x_speed": self.x_direct,
                                      "y_speed": self.y_direct,
                                      "current_image_x": 1,
                                      "current_image_y": self.y_image_set},
                                  1: {"current_image_x": 3}
                                  }


class UpdownAnimation(Animationy):
    def __init__(self, direction):
        super().__init__(direction)
        self.step_distance = 1
        self.set_up_step_distances_and_images()
        self.total_acts = 60

        self.hit_every_xth_frame = 1
        self.number_of_intervals = 4
        self.interval = self.total_acts / self.number_of_intervals
        self.frame_action_dict = {0: {"x_speed": 0,
                                      "y_speed": -1},
                                  1: {"y_speed": 1},
                                  2: {"y_speed": -1},
                                  3: {"y_speed": 1}
                                  }

class HoldAnimation(Animationy):
    def __init__(self, direction, seconds):
        super().__init__(direction)
        self.step_distance = 1
        self.set_up_step_distances_and_images()
        self.total_acts = self.calculate_frames_to_seconds(seconds)

        self.hit_every_xth_frame = 1
        self.number_of_intervals = 1
        self.interval = self.total_acts / self.number_of_intervals
        self.frame_action_dict = {0: {"x_speed": 0,
                                      "y_speed": 0}
                                  }

    def animate(self):
        if self.tick_animation():
            self.current_frame += 1
        else:
            self.y_change = 0
            self.x_change = 0
        return self.result()

    def calculate_frames_to_seconds(self, seconds):
        fps = GameSettings.FPS
        number_of_frames = fps * seconds
        return number_of_frames


class LookAroundAnimation(Animationy):
    def __init__(self, direction):
        super().__init__(direction)
        self.step_distance = 1
        self.set_up_step_distances_and_images()
        self.total_acts = 80
        self.hit_every_xth_frame = 3
        self.number_of_intervals = 4
        self.interval = self.total_acts / self.number_of_intervals
        self.frame_action_dict = {0: {"current_image_y": 2},
                                  1: {"current_image_y": 3},
                                  2: {"current_image_y": 2},
                                  3: {"current_image_y": 3}}


class SnapPhotoAnimation(Animationy):
    def __init__(self, direction):
        super().__init__(direction)
        self.step_distance = 1
        self.set_up_step_distances_and_images()
        self.total_acts = 80
        self.hit_every_xth_frame = 0
        self.number_of_intervals = 4
        self.interval = self.total_acts / self.number_of_intervals
        self.frame_action_dict = {0: {"current_image_x": 0,
                                      "current_image_y": self.y_image_set+4},
                                  1: {"current_image_x": 1},
                                  2: {"current_image_x": 2},
                                  3: {"current_image_x": 3}}

    def result(self):
        y_change = copy.copy(self.y_change)
        x_change = copy.copy(self.x_change)
        sheet_x = copy.copy(self.current_image_x)
        sheet_y = copy.copy(self.current_image_y)
        complete = False
        if self.current_frame == self.total_acts:
            complete = True
            sheet_x = 0
            sheet_y = copy.copy(self.current_image_y-4)
            self.reset()

        return x_change, y_change, sheet_x, sheet_y, complete