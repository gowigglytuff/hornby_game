import ast
import copy
import random
from abc import ABC
from typing import TYPE_CHECKING

from animations_page_view_page import Action, Switch, CustomAction
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
        self.bubble_text = "Fuck"
        self.bubble_volume = "shout"

    def return_base_coordinates_list(self, bottom_left_x, bottom_left_y):
        coordinates_list = []
        for x in range(self.base_size_x):
            for y in range(self.base_size_y):
                x_coordinate = bottom_left_x + x
                y_coordinate = bottom_left_y - y
                coordinates_list.append([x_coordinate, y_coordinate])
        return coordinates_list


class FeatureGhost(ABC):
    def __init__(self, gc_input, unique_name, display_name, function, spawn_room, spawn_x, spawn_y, spawn_facing, spawn_active):
        self.gs_input = gc_input  # type: GameState
        self.feature_type = None  # example: "Prop"
        self.feature_subtype = None  # example: "Tree"
        self.species = None  # example: "Arbutus"
        self.figure_size_x = None
        self.figure_size_y = None
        self.base_size_x = None
        self.base_size_y = None

        self.unique_name = unique_name  # example "Arbutus_102"
        self.display_name = display_name
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
        self.currently_animating = False
        self.currently_chatting = False
        self.marked_for_death = False
        self.action_frequency = 1


    def initiate_animation(self, animation_name):
        self.currently_animating = True

    def initiate_chat(self, animation_name):
        self.currently_chatting = True

    def check_if_busy(self):
        busy = False
        if self.currently_animating:
            busy = True
        if self.currently_chatting:
            busy = True
        return busy


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
        function_setup = self.break_out_combined_attr(self.function)
        self.function = function_setup[0]
        self.function_items = function_setup[1]

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
        self.currently_animating = False
        self.currently_chatting = False

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

    def break_out_combined_attr(self, attr_string):
        base = None
        details = None
        if attr_string != "None":
            my_dict = ast.literal_eval(attr_string)
            base = list(my_dict)[0]
            function_values = list(my_dict.values())
            list_access = function_values[0]
            function_values_split = list_access.split("-")
            details = function_values_split
        else:
            pass
        return base, details

class ActorGhost(FeatureGhost, ABC):
    def __init__(self, gc_input, unique_name, display_name, function, spawn_room, spawn_x, spawn_y, spawn_facing, spawn_active):
        super().__init__(gc_input, unique_name, display_name, function, spawn_room, spawn_x, spawn_y, spawn_facing, spawn_active)
        self.feature_type = Types.ACTOR
        self.trigger_list = []
        self.action_list = None
        self.behaviour_trigger = self.assign_behaviour_trigger()
        self.behaviour_counter = copy.copy(self.behaviour_trigger)

    def assign_behaviour_trigger(self):
        return random.randint(1, 100)

    def reset_to_spawn(self):
        self.x = self.spawn_x
        self.y = self.spawn_y
        self.facing = self.spawn_facing
        self.currently_animating = False
        self.currently_chatting = False
        self.behaviour_counter = copy.copy(self.behaviour_trigger)


class CharacterGhost(ActorGhost):
    def __init__(self, gc_input, unique_name, display_name, function, spawn_room, spawn_x, spawn_y, spawn_facing, spawn_active):
        super().__init__(gc_input, unique_name, display_name, function, spawn_room, spawn_x, spawn_y, spawn_facing, spawn_active)
        self.feature_subtype = Types.CHARACTER
        self.base_phrase = None
        self.good_gift_phrase = None
        self.bad_gift_phrase = None
        self.neutral_gift_phrase = None
        self.bird_hint_phrase = None
        self.friend_phrase = None
        self.friendship_level = 15
        self.max_friendship = 16
        self.good_gift_list = None
        self.bad_gift_list = None
        self.action_list = Switch()

    def get_action(self):
        return Switch()


class SellerGhost(ActorGhost):
    def __init__(self, gc_input, unique_name, display_name, function, spawn_room, spawn_x, spawn_y, spawn_facing, spawn_active):
        super().__init__(gc_input, unique_name, display_name, function, spawn_room, spawn_x, spawn_y, spawn_facing, spawn_active)
        self.feature_subtype = Types.SELLER
        self.base_phrase = None
        self.good_gift_phrase = None
        self.bad_gift_phrase = None
        self.neutral_gift_phrase = None
        self.bird_hint_phrase = None
        self.friend_phrase = None
        self.friendship_level = 15
        self.max_friendship = 16
        self.good_gift_list = None
        self.bad_gift_list = None
        self.action_list = Switch()
        self.items_list = ["Milk", "Cheese"]
        self.prices_list = {"Milk": 100, "Cheese": 200}

    def get_items_list(self):
        items_list = self.items_list
        prices_list = self.prices_list
        return items_list, prices_list

    def get_action(self):
        return Switch()


class FriendGhost(ActorGhost):
    def __init__(self, gc_input, unique_name, display_name, function, spawn_room, spawn_x, spawn_y, spawn_facing, spawn_active):
        super().__init__(gc_input, unique_name, display_name, function, spawn_room, spawn_x, spawn_y, spawn_facing, spawn_active)
        self.feature_subtype = Types.FRIEND
        self.base_phrase = None
        self.good_gift_phrase = None
        self.bad_gift_phrase = None
        self.neutral_gift_phrase = None
        self.bird_hint_phrase = None
        self.friend_phrase = None
        self.friendship_level = 15
        self.max_friendship = 16
        self.good_gift_list = None
        self.bad_gift_list = None
        self.action_list = Switch()

    def get_action(self):
        return Switch()

    def receive_gift(self, gift_name):
        result_phrase = None
        follow_up = None
        if gift_name in self.good_gift_list:
            result_phrase = self.good_gift_phrase
            self.friendship_level += 5
        elif gift_name in self.bad_gift_list:
            result_phrase = self.bad_gift_phrase
            self.friendship_level -= 5
        else:
            result_phrase = self.neutral_gift_phrase
            self.friendship_level += 1

        if not self.is_friend:
            if self.friendship_level >= self.max_friendship:
                self.achieve_friendship()
                result_phrase = result_phrase + " " + self.friend_phrase
                follow_up = {"action": self.friend_action,
                             "item": self.friend_action_details,
                             "quantity": self.friend_action_quantity}

        return result_phrase, follow_up

    def achieve_friendship(self):
        self.is_friend = True


class BirdGhost(ActorGhost):
    def __init__(self, gc_input, unique_name, display_name, function, spawn_room, spawn_x, spawn_y, spawn_facing, spawn_active):
        super().__init__(gc_input, unique_name, display_name, function, spawn_room, spawn_x, spawn_y, spawn_facing, spawn_active)
        self.feature_subtype = Types.BIRD
        self.proximity_x_trigger = 2
        self.proximity_y_trigger = 2
        self.action_list = CustomAction([("up_down", Action.stationary())])
        self.approach_outfit = None
        self.approach_word = None
        self.approach_angle = None
        self.is_calm = False

    def get_action(self):
        result = CustomAction([("up_down", Action.stationary())])
        if self.species == "Pigeon":
            result = CustomAction([("up_down", Action.stationary())])
        return result

    def check_if_calm(self):
        is_calm = False
        if self.is_calm:
            is_calm = True
        else:
            pass

        outfit_test = False
        if self.approach_outfit == self.gs_input.current_outfit:
            outfit_test = True
        elif self.approach_outfit == "none":
            outfit_test = True

        angle_test = False
        if (self.approach_angle == "up" and self.y > self.gs_input.get_player_ghost_location()[1])  or (self.approach_angle == "down" and self.y < self.gs_input.get_player_ghost_location()[1]) or (self.approach_angle == "left" and self.x > self.gs_input.get_player_ghost_location()[0]) or (self.approach_angle == "right" and self.x < self.gs_input.get_player_ghost_location()[0]):
            angle_test = True
        elif self.approach_angle == "none":
            angle_test = True
        else:
            pass

        word_test = False
        if self.approach_word != "none":
            word_test = self.gs_input.cc.check_if_word_in_posted_notice(self.approach_word)
        else:
            word_test = True

        advanced_test = self.gs_input.gc.trigger_manager.advanced_trigger_test(self.species)

        # else:
        #     if self.species == "Blackbird":
        #         tree_check = self.gs_input.cc.check_if_word_in_posted_notice("Clock")
        #         if tree_check:
        #             is_calm = True
        #     elif self.species == "Robin":
        #         time_check = self.gs_input.cc.check_clock_time(None, 10, None, 20)
        #         if time_check:
        #             is_calm = True
        #     elif self.species == "Crow":
        #             is_calm = False
        if outfit_test and angle_test and word_test and advanced_test:
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

class JayGhost(BirdGhost):
    def __init__(self, gc_input, unique_name, display_name, function, spawn_room, spawn_x, spawn_y, spawn_facing, spawn_active):
        super().__init__(gc_input, unique_name, display_name, function, spawn_room, spawn_x, spawn_y, spawn_facing, spawn_active)
        self.feature_subtype = Types.BIRD
        self.proximity_x_trigger = 0
        self.proximity_y_trigger = 0
        # self.action_list = ["up_down", "look_around"]
        self.feature_type = Types.ACTOR  # example: "Prop"
        self.feature_subtype = Types.BIRD  # example: "Tree"
        self.species = "Jay"  # example: "Arbutus"
        self.display_name = "Jay"
        self.figure_size_x = 1
        self.figure_size_y = 1
        self.base_size_x = 1
        self.base_size_y = 1

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
        self.active = True
        self.facing = copy.copy(self.spawn_facing)
        self.run_initialization()


class PropGhost(FeatureGhost):
    def __init__(self, gc_input, unique_name, display_name, function, spawn_room, spawn_x, spawn_y, spawn_facing, spawn_active):
        super().__init__(gc_input, unique_name, display_name, function, spawn_room, spawn_x, spawn_y, spawn_facing, spawn_active)
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
        elif self.function == "Lock":
            required_key = self.function_items[0] + " Key"
            current_inventory = self.gs_input.current_treasure_inventory_dictionary
            if required_key in current_inventory:
                self.gs_input.gc.unlock_lock(self.unique_name, self.spawn_room)
            else:
                self.gs_input.gc.menu_controller.post_notice("You don't have the right key")

        elif self.function == "Feeder":
            required_seed = self.function_items[0] + " Seed"
            current_inventory = self.gs_input.current_treasure_inventory_dictionary
            if required_seed in current_inventory:
                feature_avatar = self.gs_input.gv.get_feature_avatar(self.unique_name)
                feature_avatar.update_avatar_image(1, 0)
                self.filled_with_seed = True

            else:
                self.gs_input.gc.menu_controller.post_notice("You've no seed for this feeder...")
        else:
            self.gs_input.gc.menu_controller.post_notice("It's a " + self.display_name + ".")


class HuskGhost(PropGhost):
    def __init__(self, gc_input, unique_name, display_name, function, spawn_room, spawn_x, spawn_y, spawn_facing, spawn_active):
        super().__init__(gc_input, unique_name, display_name, function, spawn_room, spawn_x, spawn_y, spawn_facing, spawn_active)
        self.feature_type = Types.PROP
        self.feature_subtype = Types.PROP


class FeederGhost(PropGhost):
    def __init__(self, gc_input, unique_name, display_name, function, spawn_room, spawn_x, spawn_y, spawn_facing, spawn_active):
        super().__init__(gc_input, unique_name, display_name, function, spawn_room, spawn_x, spawn_y, spawn_facing, spawn_active)
        self.feature_type = Types.PROP
        self.feature_subtype = Types.FEEDER
        self.filled_with_seed = False


class DecoGhost(FeatureGhost):
    def __init__(self, gc_input, unique_name, display_name, function, spawn_room, spawn_x, spawn_y, spawn_facing, spawn_active):
        super().__init__(gc_input, unique_name, display_name, function, spawn_room, spawn_x, spawn_y, spawn_facing, spawn_active)
        self.feature_type = Types.DECO
        self.feature_subtype = Types.DECO
