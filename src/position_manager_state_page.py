import copy
import math
from typing import TYPE_CHECKING
import pygame
from definitions import Direction, Types
from tile_map import TileMap, ElevationMap, TerrainMap, FakeCSVMap

if TYPE_CHECKING:
    from game_controller import GameController


class PositionManager(object):
    def __init__(self, gc):
        self.gc = gc  # type: GameController

    # region PLAYER MOVEMENT
    def check_if_player_can_move(self, direction, checker, room):

        #alt test
        alt_test = True
        if pygame.K_LALT in self.gc.get_held_keys():
            alt_test = False
        if pygame.K_RALT in self.gc.get_held_keys():
            alt_test = False

        # already moving test
        moving_test = True
        if self.gc.check_if_player_already_animating():
            moving_test = False

        # room edge test
        edge_test = True
        if self.check_rooms_edges(checker, direction, room):
            edge_test = False

        #tile full test
        full_test = True
        if edge_test:
            if self.check_if_adjacent_tiles_full(checker, direction, room):
                full_test = False

        # elevation test
        elevation_test = True
        if edge_test:
            current_elevation = self.gc.gs.get_current_player_elevation()
            adjacent_elevation = self.get_adjacent_tile_elevation(checker, direction, room)
            if abs(int(adjacent_elevation) - current_elevation) > 1:
                elevation_test = False

        # elevation test
        terrain_test = True
        if edge_test:
            # current_terrain = self.gc.gs.get_current_player_elevation()
            adjacent_terrain = self.get_adjacent_tile_terrain(checker, direction, room)
            if not self.gc.gs.check_if_in_accessible_terrains(adjacent_terrain):
                terrain_test = False

        # mermaid crown test
        mermaid_crown_test = True
        if edge_test:
            if self.gc.gs.using_mermaid_crown:
                adjacent_terrain = self.get_adjacent_tile_terrain(checker, direction, room)
                if adjacent_terrain != 1:
                    mermaid_crown_test = True

        # door test
        door_test = False
        target_tile = self.get_adjacent_tile(self.gc.gs.player_ghost, direction, room)
        door_test = self.check_for_door(room.room_name, target_tile.x, target_tile.y, checker, direction)

        door_result = False
        if alt_test and door_test:
            door_result = True

        move_result = False
        if alt_test and moving_test and edge_test and full_test and elevation_test and terrain_test and terrain_test:
            move_result = True

        return move_result, door_result

    def check_if_spirit_can_move(self, direction, checker, room):

        #alt test
        alt_test = True
        if pygame.K_LALT in self.gc.get_held_keys():
            alt_test = False
        if pygame.K_RALT in self.gc.get_held_keys():
            alt_test = False

        # already moving test
        moving_test = True
        if self.gc.check_if_player_already_animating():
            moving_test = False

        # room edge test
        edge_test = True
        if self.check_rooms_edges(checker, direction, room):
            edge_test = False

        move_result = False
        if alt_test and moving_test and edge_test:
            move_result = True

        return move_result

    def check_for_door(self, room_name, x, y, checker, direction):
        door = False
        proper_angle = False
        hypothetical_door = room_name + "_" + str(x) + "_" + str(y)
        for door_name in self.gc.game_data.door_data_list.keys():
            if door_name == hypothetical_door:
                door = True
                door_object = self.gc.game_data.door_data_list[door_name]
                if door_object.access_from == Direction.ALL:
                    proper_angle = True
                elif (door_object.access_from == Direction.DOWN) and (checker.y == door_object.y_from + 1):
                    proper_angle = True
                elif (door_object.access_from == Direction.UP) and (checker.y == door_object.y_from - 1):
                    proper_angle = True
                else:
                    pass
        return proper_angle

    def move_ghost(self, feature, current_room, target_room, target_x, target_y):
        self.gc.move_counter += 1
        feature_ghost = feature
        current_x = copy.copy(feature_ghost.x)
        current_y = copy.copy(feature_ghost.y)

        # empty old cube
        current_room_object = current_room
        target_room_object = target_room
        current_cube = current_room_object.access_cube(current_x, current_y)
        current_cube.empty_cube()

        # update feature coords
        feature_ghost.x = target_x
        feature_ghost.y = target_y

        #fill new cupe
        new_cube = target_room_object.access_cube(target_x, target_y)
        new_cube.fill_cube(feature_ghost.unique_name, feature_ghost.species, feature_ghost.feature_subtype)

        if feature_ghost.feature_type == "Player":
            target_tile_elevation = self.get_tile_elevation(target_room_object.room_name, target_x, target_y)
            self.gc.gs.set_player_elevation(target_tile_elevation)
        else:
            pass
        if feature_ghost.feature_subtype == Types.BIRD:
            self.gc.trigger_manager.update_features_triggers(current_room_object, feature_ghost)

    def move_spirit_ghost(self, feature, current_room, target_room, target_x, target_y):
        feature_ghost = feature
        current_x = copy.copy(feature_ghost.x)
        current_y = copy.copy(feature_ghost.y)

        # empty old cube
        current_room_object = current_room
        target_room_object = target_room

        # update feature coords
        feature_ghost.x = target_x
        feature_ghost.y = target_y

    def match_player_elevation_to_target(self, target_room, target_x, target_y):
        new_tile_elevation = self.get_tile_elevation(target_room.room_name, target_x, target_y)
        self.gc.gs.set_player_elevation(new_tile_elevation)
    # endregion

    # region FEATURE MOVEMENT

    def check_if_feature_can_move(self, checker_ghost, direction, room_object):
        # room edge test
        edge_test = True
        if self.check_rooms_edges(checker_ghost, direction, room_object):
            edge_test = False

        # tile full test
        full_test = True
        if edge_test:
            if self.check_if_adjacent_tiles_full(checker_ghost, direction, room_object):
                full_test = False

        # elevation test
        elevation_test = True
        if edge_test:
            current_elevation = self.get_tile_elevation(room_object.room_name, checker_ghost.x, checker_ghost.y)
            adjacent_elevation = self.get_adjacent_tile_elevation(checker_ghost, direction, room_object)
            if abs(int(adjacent_elevation) - current_elevation) > 1:
                elevation_test = False

        # no door test
        no_door_test = True
        target_tile = self.get_adjacent_tile(checker_ghost, direction, room_object)
        door_test = self.check_for_door(room_object.room_name, target_tile.x, target_tile.y, checker_ghost, direction)
        if door_test:
            no_door_test = False

        move_result = False
        if edge_test and full_test and elevation_test and no_door_test:
            move_result = True

        return move_result

    # endregion

    # region CHECKING FOR MOVEMENT
    # def check_if_adjacent_tiles_full(self, checker_ghost, direction, room_object):
    #     room_object.access_adjacent_cube(checker_ghost, direction)
    #     x = checker_ghost.x
    #     y = checker_ghost.y
    #     size_x = checker_ghost.base_size_x
    #     size_y = checker_ghost.base_size_y
    #
    #     x_array = []
    #     y_array = []
    #
    #     final_report = False
    #
    #     x_counter = 0
    #     for size in range(size_x):
    #         x_counter += 1
    #         x_array.append(x_counter)
    #
    #     y_counter = 0
    #     for size in range(size_y):
    #         y_counter += 1
    #         y_array.append(y_counter)
    #
    #     for x_space in range(size_x):
    #         for y_space in range(size_y):
    #             hold_x = x
    #             hold_y = y
    #             if direction == Direction.DOWN:
    #                 hold_y = hold_y + y_array[y_space]
    #             elif direction == Direction.UP:
    #                 hold_y = hold_y - y_array[y_space]
    #             elif direction == Direction.LEFT:
    #                 hold_x = hold_x - x_array[x_space]
    #             elif direction == Direction.RIGHT:
    #                 hold_x = hold_x + x_array[x_space]
    #             cube_fill_status = room_object.check_cube_full(hold_x, hold_y)
    #
    #             if cube_fill_status:
    #                 final_report = True
    #
    #     return final_report

    def get_adjacent_tile_elevation(self, checker, direction, room):
        target_tile_x = checker.x
        target_tile_y = checker.y
        if direction == Direction.DOWN:
            target_tile_y = checker.y + 1
        elif direction == Direction.UP:
            target_tile_y = checker.y - 1
        elif direction == Direction.LEFT:
            target_tile_x = checker.x - 1
        elif direction == Direction.RIGHT:
            target_tile_x = checker.x + 1
        elevation_result = self.get_tile_elevation(room.room_name, target_tile_x, target_tile_y)
        return elevation_result

    def get_adjacent_tile_terrain(self, checker, direction, room):
        target_tile_x = checker.x
        target_tile_y = checker.y
        if direction == Direction.DOWN:
            target_tile_y = checker.y + 1
        elif direction == Direction.UP:
            target_tile_y = checker.y - 1
        elif direction == Direction.LEFT:
            target_tile_x = checker.x - 1
        elif direction == Direction.RIGHT:
            target_tile_x = checker.x + 1
        terrain_result = self.get_tile_terrain(room.room_name, target_tile_x, target_tile_y)
        return terrain_result

    def get_tile_terrain(self, room_name, x, y):
        chosen_plot_address = self.get_chosen_plot_address(room_name, x, y)
        chosen_room = self.gc.gs.get_room(room_name)
        chosen_plot = chosen_room.get_plot(chosen_plot_address[0], chosen_plot_address[1])
        terrain_result = chosen_plot.get_terrain(x * chosen_plot_address[0], y * chosen_plot_address[1])
        return terrain_result

    def get_tile_elevation(self, room_name, x, y):
        chosen_plot_address = self.get_chosen_plot_address(room_name, x, y)
        chosen_room = self.gc.gs.get_room(room_name)
        chosen_plot = chosen_room.get_plot(chosen_plot_address[0], chosen_plot_address[1])
        elevation_result = chosen_plot.get_elevation(x * chosen_plot_address[0], y * chosen_plot_address[1])
        return elevation_result

    def get_current_plot_address(self):
        current_room = self.gc.gs.get_current_room
        plot_info_list = current_room.get_plot_information
        player_coordinates = self.gc.gs.get_player_ghost_location
        total_room_x = plot_info_list[0] * plot_info_list[2]
        total_room_y = plot_info_list[1] * plot_info_list[3]
        proportion_x = total_room_x / player_coordinates[0]
        proportion_y = total_room_y / player_coordinates[1]
        result_x = int(proportion_x / plot_info_list[2])
        result_y = int(proportion_y / plot_info_list[3])
        return [result_x, result_y]

    def get_chosen_plot_address(self, room_name, x, y):
        chosen_room = self.gc.gs.get_room(room_name)
        plot_info_list = chosen_room.get_plot_information()

        total_room_x = plot_info_list[0] * plot_info_list[2]
        total_room_y = plot_info_list[1] * plot_info_list[3]
        proportion_x = x / total_room_x
        proportion_y = y / total_room_y

        result_x = math.ceil(proportion_x * plot_info_list[0])
        result_y = math.ceil(proportion_y * plot_info_list[1])

        return [result_x, result_y]

    def get_adjacent_tile(self, checker, direction, room):
        x = copy.copy(checker.x)
        y = copy.copy(checker.y)
        if direction == Direction.DOWN:
            y = y + 1
        elif direction == Direction.UP:
            y = y - 1
        elif direction == Direction.LEFT:
            x = x - 1
        elif direction == Direction.RIGHT:
            x = x + 1
        chosen_cube = room.access_cube(x, y)
        return chosen_cube

    def check_rooms_edges(self, checker, direction, room):
        result = False
        if direction == Direction.DOWN:
            if room.bottom_edge_y == checker.y:
                result = True
        elif direction == Direction.UP:
            if room.top_edge_y == checker.y:
                result = True
        elif direction == Direction.LEFT:
            if room.left_edge_x == checker.x:
                result = True
        elif direction == Direction.RIGHT:
            if room.right_edge_x == checker.x:
                result = True
        return result
    # endregion

    def despawn_feature(self, feature_name, room_object):
        feature_ghost = self.gc.gs.get_feature_ghost(feature_name)
        feature_avatar = self.gc.game_view.get_feature_avatar(feature_name)
        feature_ghost.active = False

        if feature_ghost.feature_type != Types.DECO:
            self.remove_feature_from_grid(feature_ghost, room_object)

        if feature_ghost.unique_name in self.gc.gs.action_queue.keys():
            self.gc.gs.remove_from_action_queue(feature_ghost.unique_name)

        if feature_ghost.feature_subtype == Types.BIRD:
            remove_trigger_list = feature_ghost.get_triggered()
            self.gc.trigger_manager.remove_triggers(room_object, feature_ghost)
        feature_ghost.reset_to_spawn()
        feature_avatar.reset_to_spawn(feature_ghost)
        if feature_avatar.unique_name in self.gc.feature_animations_in_progress:
            self.gc.feature_animations_in_progress.remove(feature_avatar.unique_name)
            for item in feature_avatar.animation_list.values():
                item.reset()

    def despawn_all_room_elements(self, room_object):
        feature_ghosts = self.gc.gs.get_all_features_in_room(room_object.room_name)
        for ghost in feature_ghosts:
            if ghost.species == "Player":
                pass
            else:
                self.despawn_feature(ghost.unique_name, room_object)

    def spawn_all_initial_room_elements(self, room_object):
        feature_ghosts = self.gc.gs.get_all_features_in_room(room_object.room_name)
        for ghost in feature_ghosts:
            if ghost.species == "Player":
                pass
            else:
                if ghost.spawn_active:
                    self.spawn_room_feature(ghost.unique_name, room_object)

    def spawn_room_feature(self, feature_name, room_object):
        feature_ghost = self.gc.gs.get_feature_ghost(feature_name)
        feature_ghost.active = True

        if feature_ghost.feature_type != Types.DECO:
            self.add_feature_to_grid(feature_ghost, room_object)

        if feature_ghost.feature_subtype == Types.BIRD:
            add_trigger_list = feature_ghost.produce_trigger_list()
            self.gc.trigger_manager.add_triggers(room_object, add_trigger_list)


    # region CHECKING FOR MOVEMENT
    def check_if_adjacent_tiles_full(self, checker_ghost, direction, room_object):
        adjacent_cube = room_object.access_adjacent_cube(checker_ghost, direction)
        x = checker_ghost.x
        y = checker_ghost.y
        size_x = checker_ghost.base_size_x
        size_y = checker_ghost.base_size_y

        x_array = []
        y_array = []

        final_report = False

        x_counter = 0
        for size in range(size_x):
            x_counter += 1
            x_array.append(x_counter)

        y_counter = 0
        for size in range(size_y):
            y_counter += 1
            y_array.append(y_counter)

        for x_space in range(size_x):
            for y_space in range(size_y):
                hold_x = x
                hold_y = y
                if direction == Direction.DOWN:
                    hold_y = hold_y + y_array[y_space]
                elif direction == Direction.UP:
                    hold_y = hold_y - y_array[y_space]
                elif direction == Direction.LEFT:
                    hold_x = hold_x - x_array[x_space]
                elif direction == Direction.RIGHT:
                    hold_x = hold_x + x_array[x_space]
                cube_fill_status = room_object.check_cube_full(hold_x, hold_y)

                if cube_fill_status:
                    final_report = True
        return final_report

    def get_adjacent_tile_elevation(self, checker, direction, room):
        target_tile_x = checker.x
        target_tile_y = checker.y
        if direction == Direction.DOWN:
            target_tile_y = checker.y + 1
        elif direction == Direction.UP:
            target_tile_y = checker.y - 1
        elif direction == Direction.LEFT:
            target_tile_x = checker.x - 1
        elif direction == Direction.RIGHT:
            target_tile_x = checker.x + 1
        elevation_result = self.get_tile_elevation(room.room_name, target_tile_x, target_tile_y)
        return elevation_result

    def get_tile_elevation(self, room_name, x, y):
        chosen_plot_address = self.get_chosen_plot_address(room_name, x, y)
        chosen_room = self.gc.gs.get_room(room_name)
        chosen_plot = chosen_room.get_plot(chosen_plot_address[0], chosen_plot_address[1])
        elevation_result = chosen_plot.get_elevation(x * chosen_plot_address[0], y * chosen_plot_address[1])
        return elevation_result

    def get_current_plot_address(self):
        current_room = self.gc.gs.get_current_room
        plot_info_list = current_room.get_plot_information
        player_coordinates = self.gc.gs.get_player_ghost_location
        total_room_x = plot_info_list[0] * plot_info_list[2]
        total_room_y = plot_info_list[1] * plot_info_list[3]
        proportion_x = total_room_x / player_coordinates[0]
        proportion_y = total_room_y / player_coordinates[1]
        result_x = int(proportion_x / plot_info_list[2])
        result_y = int(proportion_y / plot_info_list[3])
        return [result_x, result_y]

    def get_chosen_plot_address(self, room_name, x, y):
        chosen_room = self.gc.gs.get_room(room_name)
        plot_info_list = chosen_room.get_plot_information()

        total_room_x = plot_info_list[0] * plot_info_list[2]
        total_room_y = plot_info_list[1] * plot_info_list[3]
        proportion_x = x / total_room_x
        proportion_y = y / total_room_y

        result_x = math.ceil(proportion_x * plot_info_list[0])
        result_y = math.ceil(proportion_y * plot_info_list[1])

        return [result_x, result_y]

    def get_adjacent_tile(self, checker, direction, room):
        x = copy.copy(checker.x)
        y = copy.copy(checker.y)
        if direction == Direction.DOWN:
            y = y + 1
        elif direction == Direction.UP:
            y = y - 1
        elif direction == Direction.LEFT:
            x = x - 1
        elif direction == Direction.RIGHT:
            x = x + 1
        chosen_cube = room.access_cube(x, y)
        return chosen_cube

    def check_rooms_edges(self, checker, direction, room):
        result = False
        if direction == Direction.DOWN:
            if room.bottom_edge_y == checker.y:
                result = True
        elif direction == Direction.UP:
            if room.top_edge_y == checker.y:
                result = True
        elif direction == Direction.LEFT:
            if room.left_edge_x == checker.x:
                result = True
        elif direction == Direction.RIGHT:
            if room.right_edge_x == checker.x:
                result = True
        return result
    # endregion

    def fill_room_grid(self, room_to_fill):
        selected_room = self.gc.game.game_view.game_data.room_data_list[room_to_fill]
        fill_list = []
        feature_ghost_list = self.gc.game.gs.feature_ghost_list #ToDO: add a componenet that has lists of what is in what room
        for feature in feature_ghost_list.keys():
            feature_ghost = self.gc.gs.get_feature_ghost(feature)
            if feature_ghost.feature_type != Types.DECO:
                if feature_ghost.spawn_room == room_to_fill and feature_ghost.active:
                    fill_list.append(feature_ghost)

        for item in fill_list:
            self.add_feature_to_grid(item, selected_room)

    def add_feature_to_grid(self, feature_ghost, selected_room):
        coordinates_list = feature_ghost.return_base_coordinates_list(feature_ghost.x, feature_ghost.y)
        selected_room.add_feature(feature_ghost.unique_name, feature_ghost.species, feature_ghost.feature_subtype, coordinates_list)

    def remove_feature_from_grid(self, feature_ghost, selected_room):
        coordinates_list = feature_ghost.return_base_coordinates_list(feature_ghost.x, feature_ghost.y)
        selected_room.remove_feature(coordinates_list)

    def add_player_to_grid(self, room_name):
        selected_room = self.gc.game.game_view.game_data.room_data_list[room_name]
        player = self.gc.gs.get_player_ghost()
        player_coordinates = [[player.x, player.y]]
        selected_room.add_feature("Player", "Player", player.feature_subtype, player_coordinates)

    def clear_room_grid(self, room_to_clear):
        selected_room = self.gc.game.game_view.game_data.room_data_list[room_to_clear]
        for x in range(selected_room.x_size):
            for y in range(selected_room.y_size):
                coords = [(x, y)]
                selected_room.remove_feature(coords)

    def add_door(self, door_type, room_from, room_to, door_from_x, door_from_y, door_to_x, door_to_y):
        door1_name = room_from + "_" + str(door_from_x) + "_" + str(door_from_y)
        door1_species = None
        door1_display_name = None
        door1_entrance_x_offset = 0
        door1_entrance_y_offset = 0
        door1_exit_x_offset = 0
        door1_exit_y_offset = 0
        door1_access_from = None
        door1_exit_direction = None
        door1_has_image = True

        door2_name = room_to + "_" + str(door_to_x) + "_" + str(door_to_y)
        door2_species = None
        door2_display_name = None
        door2_entrance_x_offset = 0
        door2_entrance_y_offset = 0
        door2_exit_x_offset = 0
        door2_exit_y_offset = 0
        door2_access_from = None
        door2_exit_direction = None
        door2_has_image = True

        install_list = {"doorway1": None,
                        "doormat1": None,
                        "doorway2": None,
                        "doormat2": None}

        doorway1_deco_name = False
        doormat1_deco_name = False
        doorway2_deco_name = False
        doormat2_deco_name = False

        if door_type == "Ladder":
            door1_species = "LadderTop"
            door1_display_name = "Ladder"
            door1_access_from = Direction.ALL
            door1_exit_direction = Direction.MATCH

            door2_species = "LadderBottom"
            door2_display_name = "Ladder"
            door2_access_from = Direction.ALL
            door2_exit_direction = Direction.MATCH

            doorway1_deco_name = True
            doormat1_deco_name = False
            doorway2_deco_name = True
            doormat2_deco_name = False

        elif door_type == "Passage":
            door1_species = "Doorway"
            door1_display_name = None
            door1_exit_y_offset = -1
            door1_access_from = Direction.DOWN
            door1_exit_direction = Direction.MATCH

            door2_exit_y_offset = 1
            door2_access_from = Direction.UP
            door2_exit_direction = Direction.MATCH
            door2_has_image = False

            doormat1_dict = {"species": "DoormatEnter", "display_name": "Doormat", "function": "None", "spawn_room": str(room_from), "spawn_x": str(door_from_x), "spawn_y": str(door_from_y + 1), "spawn_facing": "Down", "spawn_active": "yes"}
            install_list["doormat1"] = doormat1_dict
            doormat2_dict = {"species": "DoormatExit", "display_name": "Doormat", "function": "None", "spawn_room": str(room_to), "spawn_x": str(door_to_x), "spawn_y": str(door_to_y - 1), "spawn_facing": "Down", "spawn_active": "yes"}
            install_list["doormat2"] = doormat2_dict

            doorway1_deco_name = True
            doormat1_deco_name = True
            doorway2_deco_name = False
            doormat2_deco_name = True

        elif door_type == "Double_back":
            door1_species = "Doorway"
            door1_display_name = "Doorway"
            door1_exit_y_offset = 1
            door1_access_from = Direction.DOWN
            door1_exit_direction = Direction.SWITCH

            door2_species = "Doorway"
            door2_display_name = "Doorway"
            door2_exit_y_offset = 1
            door2_access_from = Direction.DOWN
            door2_exit_direction = Direction.SWITCH

            doormat1_dict = {"species": "DoormatEnter", "display_name": "Doormat", "function": "None", "spawn_room": str(room_from), "spawn_x": str(door_from_x), "spawn_y": str(door_from_y + 1), "spawn_facing": "Down", "spawn_active": "yes"}
            install_list["doormat1"] = doormat1_dict
            doormat2_dict = {"species": "DoormatEnter", "display_name": "Doormat", "function": "None", "spawn_room": str(room_to), "spawn_x": str(door_to_x), "spawn_y": str(door_to_y + 1), "spawn_facing": "Down", "spawn_active": "yes"}
            install_list["doormat2"] = doormat2_dict

            doorway1_deco_name = True
            doormat1_deco_name = True
            doorway2_deco_name = True
            doormat2_deco_name = True

        elif door_type == "Feature_Passage":

            door1_exit_y_offset = -1
            door1_access_from = Direction.DOWN
            door1_exit_direction = Direction.MATCH
            door1_has_image = False

            door2_exit_y_offset = 1
            door2_access_from = Direction.UP
            door2_exit_direction = Direction.MATCH
            door2_has_image = False

            doorway1_deco_name = False
            doormat1_deco_name = False
            doorway2_deco_name = False
            doormat2_deco_name = False

        # Door 1
        door1_object = Door(room_from, room_to, door_from_x + door1_entrance_x_offset, door_from_y + door1_entrance_y_offset, door_to_x + door1_exit_x_offset, door_to_y + door1_exit_y_offset, door1_access_from, door1_exit_direction)
        if door1_has_image:
            doorway1_dict = {"species": door1_species, "display_name": door1_display_name, "function": "None", "spawn_room": str(room_from), "spawn_x": str(door_from_x), "spawn_y": str(door_from_y), "spawn_facing": "Down", "spawn_active": "yes"}
            install_list["doorway1"] = doorway1_dict

        # Door 2
        door2_object = Door(room_to, room_from, door_to_x + door2_entrance_x_offset, door_to_y + door2_entrance_y_offset, door_from_x + door2_exit_x_offset, door_from_y + door2_exit_y_offset, door2_access_from, door2_exit_direction)
        if door2_has_image:
            doorway2_dict = {"species": door2_species, "display_name": door2_display_name, "function": "None", "spawn_room": str(room_to), "spawn_x": str(door_to_x), "spawn_y": str(door_to_y), "spawn_facing": "Down", "spawn_active": "yes"}
            install_list["doorway2"] = doorway2_dict

        return_dict = {}

        for item in install_list.keys():
            if install_list[item] is not None:
                item_ghost = self.gc.gs.install_element(install_list[item])
                return_dict[item] = item_ghost
            else:
                return_dict[item] = None
        self.gc.gs.gd.add_door_data(door1_name, door1_object)
        self.gc.gs.gd.add_door_data(door2_name, door2_object)

        return return_dict

    # region FEATURE DICTIONARY
    def check_location_full(self, room_name, cube_coordinates):
        return self.gc.game.game_data.room_data_list[room_name].check_cube_full(cube_coordinates[0], cube_coordinates[1], cube_coordinates[2])
    # endregion

    def access_cube(self, x, y):
        current_room = self.gc.gs.get_current_room()
        cube = current_room.access_cube(x, y)
        return cube

class Room(object):
    def __init__(self, room_name, x_size, y_size):
        self.room_name = room_name
        self.x_size = x_size
        self.y_size = y_size
        self.left_edge_x = 1
        self.top_edge_y = 1

        self.tiles_array = []
        self.active_tiles = []

        self.total_plots_x = 1
        self.total_plots_y = 1
        self.plot_list = {}
        self.right_edge_x = 0
        self.bottom_edge_y = 0
        self.plot_size_x = 0
        self.plot_size_y = 0
        # self.access_cube(3, 3, 3).fill_cube("John")

    # region PLOTS AND ROOM INITIATION

    def generate_room_grid(self):
        for section in range(self.x_size+2):
            section_name = []
            for section2 in range(self.y_size+2):
                section2_name = Cube(self.room_name, section+1, section2+1)
                section_name.append(section2_name)
            self.tiles_array.append(section_name)

    def display_room_grid(self):
            final_image = []
            for section2 in range(self.y_size):
                section2_name = []
                list = []
                for section1 in range(self.x_size):
                    x_name = section1
                    if section1+1<10:

                        x_name = '0'+str(section1+1)
                    else:
                        x_name = str(section1+1)
                    y_name = section2
                    if section2+1<10:
                        y_name = '0'+str(section2+1)
                    else:
                        y_name = str(section2+1)
                    list.append([x_name, y_name])
                final_image.append(list)

    def add_all_plots(self):
        for x in range(self.total_plots_x):
            x += 1
            for y in range(self.total_plots_y):
                y += 1
                self.add_room_plot(self.room_name + "_" + str(x) + "_" + str(y), Plot(self.room_name, x, y, self.plot_size_x, self.plot_size_y))

    def add_room_plot(self, plot_name, plot_object):
        self.plot_list[plot_name] = plot_object

    def initiate_room(self):
        self.right_edge_x = self.left_edge_x + self.x_size - 1
        self.bottom_edge_y = self.top_edge_y + self.y_size - 1
        self.plot_size_x = int(self.x_size / self.total_plots_x)
        self.plot_size_y = int(self.y_size / self.total_plots_y)
        self.generate_room_grid()
        self.display_room_grid()
        self.add_all_plots()
    # endregion

    # region CUBE ACCESS FUNCTIONS
    def access_cube(self, x, y):
        chosen_cube = self.tiles_array[x-1][y-1]
        return chosen_cube

    def return_list_all_cubes(self):
        all_tiles = []
        for x in range(self.x_size):
            for y in range(self.y_size):
                chosen_cube = self.tiles_array[x][y]
                all_tiles.append(chosen_cube)
        return all_tiles

    def access_adjacent_cube(self, feature, direction):
        new_cube_x = feature.x
        new_cube_y = feature.y
        if direction == Direction.DOWN:
            new_cube_y += 1
        elif direction == Direction.UP:
            new_cube_y -= 1
        elif direction == Direction.LEFT:
            new_cube_x -= 1
        elif direction == Direction.RIGHT:
            new_cube_x += 1
        new_cube = self.access_cube(new_cube_x, new_cube_y)
        return new_cube

    def check_cube_full(self, x, y):
        chosen_cube = self.access_cube(x, y)
        fill_status = False
        if not chosen_cube.filling_unique_name:
            fill_status = False
        else:
            fill_status = True
        return fill_status

    def move_feature(self, feature, direction):
        current_cube = self.access_cube(feature.x, feature.y)
        new_cube = self.access_adjacent_cube(feature, direction)
        current_cube.empty_cube()
        new_cube.fill_cube(feature.species)

    def teleport_feature(self, feature, new_x, new_y):
        current_cube = self.access_cube(feature.x, feature.y)
        new_cube = self.access_cube(new_x, new_y)
        current_cube.empty_cube()
        new_cube.fill_cube(feature.species)

    def remove_feature(self, coordinates_list):
        for coordinates in coordinates_list:
            feature_cube = self.access_cube(coordinates[0], coordinates[1])
            feature_cube.empty_cube()

    def add_feature(self, feature_name, feature_type, feature_subtype, coordinates_list):
        for coordinates in coordinates_list:
            feature_cube = self.access_cube(coordinates[0], coordinates[1])
            feature_cube.fill_cube(feature_name, feature_type, feature_subtype)

    # endregion

    def get_plot_information(self):
        plots_x = self.total_plots_x
        plots_y = self.total_plots_y
        plot_size_x = self.plot_size_x
        plot_size_y = self.plot_size_y
        return [plots_x, plots_y, plot_size_x, plot_size_y]

    def get_plot(self, plot_x, plot_y):
        chosen_plot = self.plot_list[self.room_name + "_" + str(plot_x) + "_" + str(plot_y)]
        return chosen_plot


class Cube(object):
    def __init__(self, room_name, x, y):
        self.room_name = room_name
        self.x = x
        self.y = y

        self.name = self.room_name + "_" + "tile" + str(x) + "_" + str(y)

        self.filling_unique_name = None
        self.filling_type = None
        self.filling_subtype = None

    def give_coordinates(self):
        coords = [self.x, self.y]
        return coords

    def fill_cube(self, filling_unique_name, object_type, object_subtype):
        self.filling_unique_name = filling_unique_name
        self.filling_type = object_type
        self.filling_subtype = object_subtype

    def empty_cube(self):
        self.filling_unique_name = None
        self.filling_type = None
        self.filling_subtype = None


class Door(object):
    def __init__(self, room_from, room_to, x_from, y_from, x_to, y_to, access_from, exit_direction):
        self.room_from = room_from
        self.room_to = room_to
        self.x_from = x_from
        self.y_from = y_from
        self.x_to = x_to
        self.y_to = y_to
        self.access_from = access_from
        self.exit_direction = exit_direction


class Plot(object):
    def __init__(self, room, plot_x, plot_y, plot_size_x, plot_size_y):
        self.plot_x = plot_x
        self.plot_y = plot_y
        self.plot_size_x = plot_size_x
        self.plot_size_y = plot_size_y
        self.room = room
        self.plot_name = self.room + "_" + str(plot_x) + "_" + str(plot_y)
        self.background_csv_file = "assets/rooms/" + str(self.room) + "/" + self.room + "_" + str(plot_x) + "_" + str(plot_y) + "_" + "Background.csv"
        self.terrain_csv_file = "assets/rooms/" + str(self.room) + "/" + self.room + "_" + str(plot_x) + "_" + str(plot_y) + "_" + "Terrain.csv"
        self.elevation_csv_file = "assets/rooms/" + str(self.room) + "/" + self.room + "_" + str(plot_x) + "_" + str(plot_y) + "_" + "Elevation.csv"
        self.elevation_map = None
        self.terrain_map = None
        self.background_map = [TileMap(self.background_csv_file).return_map(), TileMap(self.background_csv_file).return_map_2()]
        self.make_elevation_map()
        self.make_terrain_map()

    def make_elevation_map(self):
        self.elevation_map = ElevationMap(self.plot_name, self.elevation_csv_file)

    def make_terrain_map(self):
        if self.plot_name == "Marsh_1_1" or self.plot_name == "Beach_1_1" or self.plot_name == "Habitat_Room_1_1" or self.plot_name == "Mountain_Room_1_1":
            self.terrain_map = TerrainMap(self.plot_name, self.terrain_csv_file)
        else:
            self.terrain_map = FakeCSVMap(self.plot_name, self.terrain_csv_file, self.plot_size_x, self.plot_size_y)

    def get_elevation(self, x, y):
        elevation = self.elevation_map.get_elevation(x, y)
        return elevation

    def get_terrain(self, x, y):
        terrain = self.terrain_map.get_terrain(x, y)
        return terrain

class ConsolidatedPlot(Plot):
    def __init__(self, room, plot_x, plot_y, plot_size_x, plot_size_y):
        super().__init__(room, plot_x, plot_y, plot_size_x, plot_size_y)
        self.background_csv_file = "assets/rooms/" + str(self.room) + "/" + self.room + "_" + str(plot_x) + "_" + str(plot_y) + "_" + "Background.csv"
        self.elevation_csv_file = "assets/rooms/" + str(self.room) + "/" + self.room + "_" + str(plot_x) + "_" + str(plot_y) + "_" + "Elevation.csv"
        self.background_map = [TileMap(self.background_csv_file).return_map(), TileMap(self.background_csv_file).return_map_2(), TileMap(self.background_csv_file).return_map_3(), TileMap(self.background_csv_file).return_map_4()]
        self.make_elevation_map()


class Consolidated(Room):
    def __init__(self, room_name, x_size, y_size, total_plots_x, total_plots_y):
        super().__init__(room_name, x_size, y_size)
        self.total_plots_x = total_plots_x
        self.total_plots_y = total_plots_y
        self.initiate_room()

    def add_all_plots(self):
        for x in range(self.total_plots_x):
            x += 1
            for y in range(self.total_plots_y):
                y += 1
                self.add_room_plot(self.room_name + "_" + str(x) + "_" + str(y), ConsolidatedPlot(self.room_name, x, y, self.plot_size_x, self.plot_size_y))