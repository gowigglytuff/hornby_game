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
            # frames_list = []
            # for frame in self.frame_action_dict.keys():
            #     frames_list.append(frame*self.interval)
            result_dict = self.check_action(self.current_frame)
            print(result_dict)
            if "x_speed" in result_dict.keys():
                self.x_speed = result_dict["x_speed"]

            if "y_speed" in result_dict.keys():
                self.y_speed = result_dict["y_speed"]

            if "current_image_x" in result_dict.keys():
                self.current_image_x = result_dict["current_image_x"]

            if "current_image_y" in result_dict.keys():
                self.current_image_y = result_dict["current_image_y"]

            if self.current_frame == self.total_acts:
                self.y_change = 0
                self.x_change = 0
                self.current_frame = 0
                self.complete = True
                self.current_image_x = 0
                # self.direction_y_to_return_to()
            else:
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

        valid_options = [x for x in numbs if x >= frame_number]
        index = numbs.index(min(valid_options))
        result = self.frame_action_dict[index]
        return result

    def result(self):
        y_change = self.y_change
        x_change = self.x_change
        sheet_x = self.current_image_x
        sheet_y = self.current_image_y
        complete = self.complete
        if self.complete:
            self.reset()

        return x_change, y_change, sheet_x, sheet_y, complete

    def reset(self):
        self.current_frame = 0
        self.complete = False


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
        self.total_acts = 80
        self.hit_every_xth_frame = 0
        self.number_of_intervals = 4
        self.interval = self.total_acts / self.number_of_intervals
        self.frame_action_dict = {0: {"x_speed": self.x_direct,
                                      "y_speed": -1},
                                  1: {"y_speed": 1},
                                  2: {"y_speed": -1},
                                  3: {"y_speed": 1}
                                  }


# class UpdownAnimation(Animationy):
#     def __init__(self, direction):
#         super().__init__(direction)
#         self.changing_variable = self.y_change
#         self.total_distance_x = 0
#         self.total_distance_y = 10
#         self.interval = 20
#         self.number_of_intervals = 4
#         self.rate = self.interval/self.total_distance_y
#         self.total_frames = self.interval * self.number_of_intervals
#         self.frame_action_dict = {0: {"x_speed": self.x_direct,
#                                       "y_speed": self.y_direct,
#                                       "current_image_x": 0,
#                                       "current_image_y": 0
#                                       },
#                                   self.interval*1: {"current_image_x": self.x_direct,
#                                       "current_image_y": self.y_direct},
#                                   self.interval*2: {"current_image_x": self.x_direct,
#                                       "current_image_y": self.y_direct},
#                                   self.interval*3: {"current_image_x": self.x_direct,
#                                       "current_image_y": self.y_direct}
#                                   }

class LookAroundAnimation(Animationy):
    def __init__(self, direction):
        super().__init__(direction)
        self.direction = direction
        self.current_frame = 0
        self.frequency = 0

        self.complete = False

        self.y_change = 0
        self.x_change = 0
        self.y_speed = 0
        self.x_speed = 0
        self.current_image_x = 0
        self.current_image_y = 0
        self.changing_variable = self.y_change
        self.total_distance_x = 0
        self.total_distance_y = 20
        self.interval = 40
        self.number_of_intervals = 4
        self.rate = self.interval/self.total_distance_y
        self.total_frames = self.interval * self.number_of_intervals
        self.frame_action_dict = {self.interval*0: {"current_image_x": 0,
                                                    "current_image_y": 2},
                                  self.interval*1: {"current_image_x": 0,
                                                    "current_image_y": 3},
                                  self.interval*2: {"current_image_x": 0,
                                                     "current_image_y": 2},
                                  self.interval*3: {"current_image_x": 0,
                                                    "current_image_y": 3}
                                  }

    def direction_to_y_image(self):
        self.current_image_y = Mundane.direction_feedback(self.direction, 4, 3, 1, 0)

    def direction_y_to_return_to(self):
        self.current_image_y = Mundane.direction_feedback(self.direction, 3, 2, 1, 0)

    def animate(self):
        if self.current_frame in self.frame_action_dict.keys():
            result_dict = self.check_action(self.current_frame)
            if "x_speed" in result_dict.keys():
                self.x_speed = result_dict["x_speed"]
            else:
                self.x_speed = 0

            if "y_speed" in result_dict.keys():
                self.y_speed = result_dict["y_speed"]
            else:
                self.y_speed = 0

            if "current_image_x" in result_dict.keys():
                self.current_image_x = result_dict["current_image_x"]
            else:
                pass

            if "current_image_y" in result_dict.keys():
                self.current_image_y = result_dict["current_image_y"]
            else:
                pass

        if self.current_frame == self.total_frames:
            self.y_change = 0
            self.x_change = 0
            self.current_frame = 0
            self.complete = True
            self.current_image_x = 0
            self.direction_y_to_return_to()
        else:
            if Mundane.is_factor(self.current_frame, self.rate) or self.current_frame == 0:
                self.x_change = self.x_speed
                self.y_change = self.y_speed
            else:
                self.x_change = 0
                self.y_change = 0

        self.current_frame += 1
        return self.result()

    def check_action(self, frame_number):
        result = self.frame_action_dict[frame_number]
        return result

    def result(self):
        y_change = self.y_change
        x_change = self.x_change
        sheet_x = self.current_image_x
        sheet_y = self.current_image_y
        complete = self.complete
        if self.complete:
            self.reset()

        return x_change, y_change, sheet_x, sheet_y, complete

    def reset(self):
        self.current_frame = 0
        self.complete = False