import random
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
        self.name = "Player"
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


class FeatureGhost(object):
    '''
    :type gs_input: GameState
    '''
    def __init__(self, name, gs_input, room, spawn_x, spawn_y, direction, feature_type, base_size_x, base_size_y, unique_name, feature_subtype, figure_size_x, figure_size_y, spawn_active, function):
        self.gs_input = gs_input # type: GameState
        self.feature_type = feature_type
        self.feature_subtype = feature_subtype
        self.name = name
        self.function = function
        self.unique_name = unique_name
        self.state = "idle"
        self.spawn_x = spawn_x
        self.spawn_y = spawn_y
        self.x = spawn_x
        self.y = spawn_y
        if spawn_active == "yes":
            # print("yes", self.unique_name)
            self.active = False
            self.spawn_active = True
        else:
            # print("no", self.unique_name)
            self.active = False
            self.spawn_active = False
        self.figure_size_x = figure_size_x
        self.figure_size_y = figure_size_y
        self.base_size_x = base_size_x
        self.base_size_y = base_size_y
        self.spawn_facing = direction
        self.facing = direction
        self.cur_img = (0, 0)
        self.current_skin = "default"
        self.room = room

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
        self.state = "idle"
        self.facing = self.spawn_facing

    def get_removed(self):
        pass


class NpcGhost(FeatureGhost):
    def __init__(self, name, gs_input, room, spawn_x, spawn_y, direction, feature_type, base_size_x, base_size_y, unique_name, phrase, feature_subtype, figure_size_x, figure_size_y, spawn_active, function):
        super().__init__(name, gs_input, room,spawn_x, spawn_y, direction, feature_type, base_size_x, base_size_y, unique_name, feature_subtype, figure_size_x, figure_size_y, spawn_active, function)
        self.phrase = phrase
        self.feature_type = Types.NPC


class BirdGhost(FeatureGhost):
    def __init__(self, name, gs_input, room, spawn_x, spawn_y, direction, feature_type, base_size_x, base_size_y, unique_name, phrase, feature_subtype, figure_size_x, figure_size_y, spawn_active, function):
        super().__init__(name, gs_input, room,spawn_x, spawn_y, direction, feature_type, base_size_x, base_size_y, unique_name, feature_subtype, figure_size_x, figure_size_y, spawn_active, function)
        self.phrase = phrase
        self.proximity_x_trigger = 2
        self.proximity_y_trigger = 2
        self.trigger_list = []
        self.action_list = ["walk_front", "walk_left", "walk_right", "walk_up"]
        # self.directions = [Direction.DOWN, Direction.UP, Direction.LEFT, Direction.RIGHT]

    def get_movement(self):
        movement = random.choice(self.action_list)
        return movement

    def check_if_calm(self):
        is_calm = False
        if self.name == "Blackbird":
            tree_check = self.gs_input.cc.check_if_word_in_posted_notice("Clock")
            if tree_check:
                is_calm = True
        elif self.name == "Robin":
            time_check = self.gs_input.cc.check_clock_time(None, 10, None, 20)
            if time_check:
                is_calm = True
        elif self.name == "Crow":
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
                tracker +=1
        print(self.unique_name, tracker)

        print(self.unique_name, coords_list)
        self.trigger_list = coords_list
        return coords_list

    def get_triggered(self):
        return self.trigger_list

    def get_removed(self):
        pass


class PigeonGhost(BirdGhost):
    def __init__(self, name, gs_input, room, spawn_x, spawn_y, direction, feature_type, base_size_x, base_size_y, unique_name, phrase, feature_subtype, figure_size_x, figure_size_y, spawn_active, function):
        super().__init__(name, gs_input, room,spawn_x, spawn_y, direction, feature_type, base_size_x, base_size_y, unique_name, feature_subtype, figure_size_x, figure_size_y, spawn_active, function)
        self.phrase = phrase
        self.proximity_x_trigger = 2
        self.proximity_y_trigger = 2
        self.trigger_list = []
        self.action_list = ["walk_front", "walk_left", "walk_right", "walk_up"]
        self.directions = [Direction.DOWN, Direction.UP, Direction.LEFT, Direction.RIGHT]

    def get_movement(self):
        movement = random.choice(self.directions)
        return movement


class PropGhost(FeatureGhost):
    def __init__(self, name, gs_input, room, spawn_x, spawn_y, direction, feature_type, base_size_x, base_size_y, unique_name, phrase, feature_subtype, figure_size_x, figure_size_y, spawn_active, function):
        super().__init__(name, gs_input, room,spawn_x, spawn_y, direction, feature_type, base_size_x, base_size_y, unique_name, feature_subtype, figure_size_x, figure_size_y, spawn_active, function)
        self.feature_type = Types.PROP

    def get_interacted_with(self):
        if self.function == "Basket":
            self.gs_input.ms.post_notice("You looked in the " + self.name)
            self.gs_input.ms.set_menu(AcquireMenuGhost.BASE, None)
        else:
            pass


class BasketGhost(PropGhost):
    def __init__(self, name, gs_input, room, spawn_x, spawn_y, direction, feature_type, base_size_x, base_size_y, unique_name, phrase, feature_subtype, figure_size_x, figure_size_y, spawn_active, function):
        super().__init__(name, gs_input, room,spawn_x, spawn_y, direction, feature_type, base_size_x, base_size_y, unique_name, phrase, feature_subtype, figure_size_x, figure_size_y, spawn_active, function)
        self.feature_type = Types.PROP

    def get_interacted_with(self):
        self.gs_input.ms.set_menu(AcquireMenuGhost.BASE, None)


class HouseGhost(FeatureGhost):
    def __init__(self, name, gs_input, room, spawn_x, spawn_y, direction, feature_type, base_size_x, base_size_y, unique_name, phrase, feature_subtype, figure_size_x, figure_size_y, spawn_active, function):
        super().__init__(name, gs_input, room,spawn_x, spawn_y, direction, feature_type, base_size_x, base_size_y, unique_name, feature_subtype, figure_size_x, figure_size_y, spawn_active, function)
        self.feature_type = Types.HOUSE


class DecoGhost(FeatureGhost):
    def __init__(self, name, gs_input, room, spawn_x, spawn_y, direction, feature_type, base_size_x, base_size_y, unique_name, phrase, feature_subtype, figure_size_x, figure_size_y, spawn_active, function):
        super().__init__(name, gs_input, room,spawn_x, spawn_y, direction, feature_type, base_size_x, base_size_y, unique_name, feature_subtype, figure_size_x, figure_size_y, spawn_active, function)
        self.phrase = phrase
        self.feature_type = Types.DECO


class MapTrigger(object):
    def __init__(self, trigger_owner_unique_name, current_location_x, current_location_y, x_range, y_range):
        self.triggers_name = trigger_owner_unique_name
        self.trigger_owner_unique_name = trigger_owner_unique_name
        self.current_location_x = current_location_x
        self.current_location_y = current_location_y
        self.x_range = x_range
        self.y_range = y_range
        self.coords_list = self.produce_trigger_coords_list()

    def produce_trigger_coords_list(self):
        base_x = self.current_location_x
        base_y = self.current_location_y
        left_extreme = base_x - self.x_range
        right_extreme = base_x + self.x_range
        up_extreme = base_y - self.y_range
        down_extreme = base_y + self.y_range

        total_x_range = 1 + (self.x_range*2)
        total_y_range = 1 + (self.y_range*2)

        coords_list = []

        for x in range(total_x_range):
            for y in range(total_y_range):
                coords_list.append([left_extreme + x, up_extreme + y])

        return coords_list