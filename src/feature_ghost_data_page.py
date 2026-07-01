import ast
import copy
import random
from abc import ABC
from typing import TYPE_CHECKING

from definitions import Direction, Types
from menu_ghosts_data_page import AcquireMenuGhost

if TYPE_CHECKING:
    from game_state import GameState


class PlayerGhost(object):
    def __init__(self, gs_input, x, y):
        self.gs_input = gs_input
        self.feature_type = "Player"
        self.feature_subtype = None
        self.x = x
        self.y = y
        self.base_size_x = 1
        self.base_size_y = 1
        self.unique_name = "Player"
        self.species = "Player"
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
                coordinates_list.append([x_coordinate, y_coordinate])
        return coordinates_list


class FeatureGhost(ABC):
    def __init__(self, gc_input, unique_name, function, spawn_room, spawn_x, spawn_y, spawn_facing, spawn_active):
        self.gs_input = gc_input  # type: GameState
        self.feature_type = None  # example: "Prop"
        self.feature_subtype = None  # example: "Tree"
        self.species = None  # example: "Arbutus"
        self.display_name = None
        self.figure_size_x = None
        self.figure_size_y = None
        self.base_size_x = None
        self.base_size_y = None

        self.unique_name = unique_name  # example "Arbutus_102"
        self.function = function  # example: "Basket"
        self.set_up_function(self.function)
        self.spawn_x = spawn_x
        self.spawn_y = spawn_y
        self.spawn_active = spawn_active
        self.spawn_facing = spawn_facing
        self.spawn_room = spawn_room

        self.x = copy.copy(self.spawn_x)
        self.y = copy.copy(self.spawn_y)
        self.active = False
        self.facing = copy.copy(self.spawn_facing)

    def run_initialization(self):
        self.x = copy.copy(self.spawn_x)
        self.y = copy.copy(self.spawn_y)
        if self.spawn_active == "yes":
            self.active = False
            self.spawn_active = True
        else:
            self.active = False
            self.spawn_active = False
        self.facing = copy.copy(self.spawn_facing)
        self.set_up_function(self.function)

    def return_base_coordinates_list(self, bottom_left_x, bottom_left_y):
        coordinates_list = []
        for x in range(self.base_size_x):
            for y in range(self.base_size_y):
                x_coordinate = bottom_left_x + x
                y_coordinate = bottom_left_y - y
                coordinates_list.append([x_coordinate, y_coordinate])
        return coordinates_list

    def reset_to_spawn(self):
        self.x = self.spawn_x
        self.y = self.spawn_y
        self.facing = self.spawn_facing

    def get_removed(self):
        pass

    def set_up_function(self, function_string):
        if function_string != "None":
            my_dict = ast.literal_eval(function_string)
            self.function = list(my_dict)[0]
            function_values = list(my_dict.values())
            list_access = function_values[0]
            function_values_split = list_access.split("-")
            self.function_items = function_values_split
        else:
            pass


class ActorGhost(FeatureGhost, ABC):
    def __init__(self, gc_input, unique_name, function, spawn_room, spawn_x, spawn_y, spawn_facing, spawn_active):
        super().__init__(gc_input, unique_name, function, spawn_room, spawn_x, spawn_y, spawn_facing, spawn_active)
        self.feature_type = Types.ACTOR
        self.trigger_list = []
        self.action_list = []


class CharacterGhost(ActorGhost):
    def __init__(self, gc_input, unique_name, function, spawn_room, spawn_x, spawn_y, spawn_facing, spawn_active):
        super().__init__(gc_input, unique_name, function, spawn_room, spawn_x, spawn_y, spawn_facing, spawn_active)
        self.feature_subtype = Types.CHARACTER
        self.base_phrase = None
        self.good_gift_phrase = None
        self.bad_gift_phrase = None
        self.neutral_gift_phrase = None
        self.bird_hint_phrase = None
        self.friendship_level = 0
        self.good_gift_list = None
        self.bad_gift_list = None

    def receive_gift(self, gift_name):
        result_phrase = None
        if gift_name in self.good_gift_list:
            result_phrase = self.good_gift_phrase
            self.friendship_level += 5
        elif gift_name in self.bad_gift_list:
            result_phrase = self.bad_gift_phrase
            self.friendship_level -= 5
        else:
            result_phrase = self.neutral_gift_phrase
            self.friendship_level += 1
        return result_phrase


class BirdGhost(ActorGhost):
    def __init__(self, gc_input, unique_name, function, spawn_room, spawn_x, spawn_y, spawn_facing, spawn_active):
        super().__init__(gc_input, unique_name, function, spawn_room, spawn_x, spawn_y, spawn_facing, spawn_active)
        self.feature_subtype = Types.BIRD
        self.proximity_x_trigger = 2
        self.proximity_y_trigger = 2
        self.action_list = ["up_down", "look_around"]


    def get_movement(self):
        movement = random.choice(self.action_list)
        return movement

    def check_if_calm(self):
        is_calm = False
        if self.species == "Blackbird":
            tree_check = self.gs_input.cc.check_if_word_in_posted_notice("Clock")
            if tree_check:
                is_calm = True
        elif self.species == "Robin":
            time_check = self.gs_input.cc.check_clock_time(None, 10, None, 20)
            if time_check:
                is_calm = True
        elif self.species == "Crow":
                is_calm = True
        return is_calm

    def check_trigger_result(self, trigger):
        result = None
        if trigger == "flee":
            is_calm = self.check_if_calm()
            if not is_calm:
                result = "remove"
            else:
                pass
        else:
            pass
        return result

    def trigger_for_proximity(self):
        pass

    def produce_trigger_list(self):
        base_x = self.x
        base_y = self.y
        left_extreme = base_x - self.proximity_x_trigger
        up_extreme = base_y - self.proximity_y_trigger

        total_x_range = 1 + (self.proximity_x_trigger*2)
        total_y_range = 1 + (self.proximity_y_trigger*2)

        coords_list = {}
        trigger_name = "flee"
        tracker = 0
        for x in range(total_x_range):
            for y in range(total_y_range):
                coords_list[left_extreme + x, up_extreme + y] = [self.unique_name, trigger_name]
                tracker += 1

        self.trigger_list = coords_list
        return coords_list

    def get_triggered(self):
        return self.trigger_list

    def get_removed(self):
        pass


class PropGhost(FeatureGhost):
    def __init__(self, gc_input, unique_name, function, spawn_room, spawn_x, spawn_y, spawn_facing, spawn_active):
        super().__init__(gc_input, unique_name, function, spawn_room, spawn_x, spawn_y, spawn_facing, spawn_active)
        self.feature_type = Types.PROP
        self.feature_subtype = Types.PROP

    def get_interacted_with(self):
        if self.function == "Basket":
            basket_items = copy.copy(self.function_items)
            self.gs_input.gc.look_in_basket(self.unique_name, basket_items)
        elif self.function == "Package":
            self.gs_input.gc.pick_up_package("Package", self.unique_name, self.spawn_room, self.function_items)
        elif self.function == "Page":
            self.gs_input.gc.pick_up_package("Page", self.unique_name, self.spawn_room, self.function_items)
        else:
            self.gs_input.gc.menu_controller.post_notice("It's a " + self.display_name + ".")

class HuskGhost(PropGhost):
    def __init__(self, gc_input, unique_name, function, spawn_room, spawn_x, spawn_y, spawn_facing, spawn_active):
        super().__init__(gc_input, unique_name, function, spawn_room, spawn_x, spawn_y, spawn_facing, spawn_active)
        self.feature_type = Types.PROP
        self.feature_subtype = Types.PROP

    def get_interacted_with(self):
        if self.function == "Basket":
            basket_items = copy.copy(self.function_items)
            self.gs_input.gc.look_in_basket(self.unique_name, basket_items)
        elif self.function == "Package":
            self.gs_input.gc.pick_up_package("Package", self.unique_name, self.spawn_room, self.function_items)
        elif self.function == "Page":
            self.gs_input.gc.pick_up_package("Page", self.unique_name, self.spawn_room, self.function_items)
        else:
            self.gs_input.gc.menu_controller.post_notice("It's a " + self.display_name + ".")


class DecoGhost(FeatureGhost):
    def __init__(self, gc_input, unique_name, function, spawn_room, spawn_x, spawn_y, spawn_facing, spawn_active):
        super().__init__(gc_input, unique_name, function, spawn_room, spawn_x, spawn_y, spawn_facing, spawn_active)
        self.feature_type = Types.DECO
        self.feature_subtype = Types.DECO
