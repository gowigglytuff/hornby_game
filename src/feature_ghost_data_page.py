from definitions import Direction, Types
from menu_ghosts_data_page import AcquireMenuGhost


class PlayerGhost(object):
    def __init__(self, gs_input, x, y):
        self.gs_input = gs_input
        self.feature_type = "Player"
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
    def __init__(self, name, gs_input, room, spawn_x, spawn_y, direction, feature_type, base_size_x, base_size_y, unique_name, feature_subtype):
        self.gs_input = gs_input
        self.feature_type = feature_type
        self.feature_subtype = feature_subtype
        self.name = name
        self.unique_name = unique_name
        self.state = "idle"
        self.spawn_x = spawn_x
        self.spawn_y = spawn_y
        self.x = spawn_x
        self.y = spawn_y
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
    def __init__(self, name, gs_input, room, spawn_x, spawn_y, direction, feature_type, base_size_x, base_size_y, unique_name, phrase, feature_subtype):
        super().__init__(name, gs_input, room,spawn_x, spawn_y, direction, feature_type, base_size_x, base_size_y, unique_name, feature_subtype)
        self.phrase = phrase
        self.feature_type = Types.NPC


class BirdGhost(FeatureGhost):
    def __init__(self, name, gs_input, room, spawn_x, spawn_y, direction, feature_type, base_size_x, base_size_y, unique_name, phrase, feature_subtype):
        super().__init__(name, gs_input, room,spawn_x, spawn_y, direction, feature_type, base_size_x, base_size_y, unique_name, feature_subtype)
        self.phrase = phrase
        self.proximity_x_trigger = 3
        self.proximity_y_trigger = 3

    def trigger_for_proximity(self):
        pass

    def produce_map_trigger(self, location_x, location_y):
        return MapTrigger(self.unique_name, location_x, location_y, self.proximity_x_trigger, self.proximity_y_trigger)

    def get_removed(self):
        pass

class PropGhost(FeatureGhost):
    def __init__(self, name, gs_input, room, spawn_x, spawn_y, direction, feature_type, base_size_x, base_size_y, unique_name, phrase, feature_subtype):
        super().__init__(name, gs_input, room,spawn_x, spawn_y, direction, feature_type, base_size_x, base_size_y, unique_name, feature_subtype)
        self.feature_type = Types.PROP

    def get_interacted_with(self):
        pass


class BasketGhost(PropGhost):
    def __init__(self, name, gs_input, room, spawn_x, spawn_y, direction, feature_type, base_size_x, base_size_y, unique_name, phrase, feature_subtype):
        super().__init__(name, gs_input, room,spawn_x, spawn_y, direction, feature_type, base_size_x, base_size_y, unique_name, phrase, feature_subtype)
        self.feature_type = Types.PROP

    def get_interacted_with(self):
        self.gs_input.ms.set_menu(AcquireMenuGhost.BASE, None)


class HouseGhost(FeatureGhost):
    def __init__(self, name, gs_input, room, spawn_x, spawn_y, direction, feature_type, base_size_x, base_size_y, unique_name, phrase, feature_subtype):
        super().__init__(name, gs_input, room,spawn_x, spawn_y, direction, feature_type, base_size_x, base_size_y, unique_name, feature_subtype)
        self.feature_type = Types.HOUSE


class DecoGhost(FeatureGhost):
    def __init__(self, name, gs_input, room, spawn_x, spawn_y, direction, feature_type, base_size_x, base_size_y, unique_name, phrase, feature_subtype):
        super().__init__(name, gs_input, room,spawn_x, spawn_y, direction, feature_type, base_size_x, base_size_y, unique_name, feature_subtype)
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