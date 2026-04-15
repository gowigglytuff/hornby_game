import math

from definitions import Direction
from tile_map import TileMap, ElevationMap


class PositionManager(object):
    def __init__(self, gc_input):
        self.gc_input = gc_input  # type: GameController

    # region PLAYER MOVEMENT
    def check_if_player_can_move(self, direction, checker, room):
        result = True
        if self.check_rooms_edges(checker, direction, room):
            result = False
        elif not self.check_rooms_edges(checker, direction, room):
            if self.check_if_adjacent_tiles_full(checker, direction, room):
                result = False

            current_elevation = self.gc_input.game_state.get_current_player_elevation()
            adjacent_elevation = self.get_adjacent_tile_elevation(checker, direction, room)
            if abs(int(adjacent_elevation) - current_elevation) > 1:
                result = False

        return result

    def check_for_door(self, room_name, x, y):
        door = False
        print(self.gc_input.game_data.door_data_list.keys())
        try:
            print(room_name + "_" + str(x) + "_" + str(y))
            check = self.gc_input.game_data.door_data_list[room_name + "_" + str(x) + "_" + str(y)]
            if check:
                door = True
            print("there's the door")
        except:
            print("no door found")
            pass
        return door

    def nudge_player_ghost(self, direction):
        room_object = self.gc_input.game_data.room_data_list[self.gc_input.game_state.current_room]
        current_cube = room_object.access_cube(self.gc_input.game_state.player_ghost.x, self.gc_input.game_state.player_ghost.y, self.gc_input.game_state.player_ghost.z)
        new_cube_x = self.gc_input.game_state.player_ghost.x
        new_cube_y = self.gc_input.game_state.player_ghost.y
        new_cube_z = self.gc_input.game_state.player_ghost.z
        if direction == Direction.DOWN:
            new_cube_y += 1
            self.gc_input.game_state.player_ghost.y += 1
        elif direction == Direction.UP:
            new_cube_y -= 1
            self.gc_input.game_state.player_ghost.y -= 1
        elif direction == Direction.LEFT:
            new_cube_x -= 1
            self.gc_input.game_state.player_ghost.x -= 1
        elif direction == Direction.RIGHT:
            new_cube_x += 1
            self.gc_input.game_state.player_ghost.x += 1
        new_cube = room_object.access_cube(new_cube_x, new_cube_y, new_cube_z)
        current_cube.empty_cube()
        new_cube.fill_cube("Player")

        # update player elevation
        new_tile_elevation = self.get_tile_elevation(room_object.name, new_cube_x, new_cube_y)
        self.gc_input.game_state.set_player_elevation(new_tile_elevation)

    def move_player_ghost(self, target_room_name, target_x, target_y, target_z):
        x_from = self.gc_input.game_state.get_player_location()[0]
        y_from = self.gc_input.game_state.get_player_location()[1]

        room = self.gc_input.game_state.get_room(target_room_name)
        room.access_cube(target_x, target_y, target_z).fill_cube("Player")
        target_tile_elevation = self.get_tile_elevation(target_room_name, target_x, target_y)
        self.gc_input.game_state.set_player_elevation(target_tile_elevation)
        player_ghost = self.gc_input.game_state.get_player_ghost()
        player_ghost.x = target_x
        player_ghost.y = target_y
        player_ghost.z = target_z
        self.gc_input.game_view.update_player_avatar_location(target_x, target_y)

        self.gc_input.game_view.manually_update_camera((target_x - x_from), (target_y -  y_from))

    # endregion

    # region FEATURE MOVEMENT
    def check_if_feature_can_move(self, checker, direction, room):
        result = True
        if self.check_if_adjacent_tiles_full(checker, direction, room):
            result = False
        if self.check_rooms_edges(checker, direction, room):
            result = False
        return result

    def move_feature_ghost(self, name, direction):
        feature = self.gc_input.game_state.get_feature_ghost(name)
        room_object = self.gc_input.game_data.room_data_list[self.gc_input.game_state.current_room]
        current_cube = room_object.access_cube(feature.x, feature.y, feature.z)
        new_cube_x = feature.x
        new_cube_y = feature.y
        new_cube_z = feature.z
        if direction == Direction.DOWN:
            new_cube_y += 1
            feature.y += 1
        elif direction == Direction.UP:
            new_cube_y -= 1
            feature.y -= 1
        elif direction == Direction.LEFT:
            new_cube_x -= 1
            feature.x -= 1
        elif direction == Direction.RIGHT:
            new_cube_z += 1
            feature.x += 1
        new_cube = room_object.access_cube(new_cube_x, new_cube_y, new_cube_z)
        current_cube.empty_cube()
        new_cube.fill_cube(feature.name)
    # endregion

    # region CHECKING FOR MOVEMENT
    def check_if_adjacent_tiles_full(self, checker, direction, room):
        room.access_adjacent_cube(checker, direction)
        x = checker.x
        y = checker.y
        z = checker.z
        size_x = checker.base_size_x
        size_y = checker.base_size_y

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
                cube_fill_status = room.check_cube_full(hold_x, hold_y, z)

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
        elevation_result = self.get_tile_elevation(room.name, target_tile_x, target_tile_y)
        return elevation_result

    def get_tile_elevation(self, room_name, x, y):
        chosen_plot_address = self.get_chosen_plot_address(room_name, x, y)
        chosen_room = self.gc_input.game_state.get_room(room_name)
        chosen_plot = chosen_room.get_plot(chosen_plot_address[0], chosen_plot_address[1])
        elevation_result = chosen_plot.get_elevation(x * chosen_plot_address[0], y * chosen_plot_address[1])
        return elevation_result

    def get_current_plot_address(self):
        current_room = self.gc_input.game_state.get_current_room
        plot_info_list = current_room.get_plot_information
        player_coordinates = self.gc_input.game_state.get_player_location
        total_room_x = plot_info_list[0] * plot_info_list[2]
        total_room_y = plot_info_list[1] * plot_info_list[3]
        proportion_x = total_room_x / player_coordinates[0]
        proportion_y = total_room_y / player_coordinates[1]
        result_x = int(proportion_x / plot_info_list[2])
        result_y = int(proportion_y / plot_info_list[3])
        return [result_x, result_y]

    def get_chosen_plot_address(self, room_name, x, y):
        chosen_room = self.gc_input.game_state.get_room(room_name)
        plot_info_list = chosen_room.get_plot_information()

        total_room_x = plot_info_list[0] * plot_info_list[2]
        total_room_y = plot_info_list[1] * plot_info_list[3]
        proportion_x = x / total_room_x
        proportion_y = y / total_room_y

        result_x = math.ceil(proportion_x * plot_info_list[0])
        result_y = math.ceil(proportion_y * plot_info_list[1])

        return [result_x, result_y]

    def get_adjacent_tile(self, checker, direction, room):
        x = checker.x
        y = checker.y
        z = checker.z
        if direction == Direction.DOWN:
            y = y + 1
        elif direction == Direction.UP:
            y = y - 1
        elif direction == Direction.LEFT:
            x = x - 1
        elif direction == Direction.RIGHT:
            x = x + 1
        chosen_cube = room.access_cube(x, y, z)
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
        selected_room = self.gc_input.game.game_view.game_data.room_data_list[room_to_fill]
        fill_list = []
        npc_ghost_list = self.gc_input.game.game_state.feature_ghost_list #ToDO: add a componenet that has lists of what is in what room
        for npc in npc_ghost_list.keys():
            npc_ghost = self.gc_input.game_state.get_feature_ghost(npc)
            if npc_ghost_list[npc].room == room_to_fill:
                fill_list.append(npc_ghost)

        for item in fill_list:
            coordinates_list = item.return_base_coordinates_list(item.x, item.y)
            selected_room.add_feature(item.name, coordinates_list)

    def add_player_to_grid(self, room_name):
        selected_room = self.gc_input.game.game_view.game_data.room_data_list[room_name]
        player = self.gc_input.game_state.get_player_ghost()
        player_coordinates = [[player.x, player.y, player.z]]
        selected_room.add_feature("Player", player_coordinates)

    def clear_room_grid(self, room_to_clear):
        selected_room = self.gc_input.game.game_view.game_data.room_data_list[room_to_clear]
        for x in range(selected_room.x_size):
            for y in range(selected_room.y_size):
                for z in range(selected_room.z_size):
                    selected_room.remove_feature(x, y, z)

    # region FEATURE DICTIONARY
    def get_feature_location(self, feature_name):
        feature_data = self.gc_input.game_state.feature_location_dictionary[feature_name]
        return feature_data

    def update_feature_dictionary(self, feature_name, location):
        self.gc_input.game_state.feature_location_dictionary[feature_name][1] = location

    def update_locations(self, room_name, feature_name, previous_cube_coordinates, new_cube_coordinates):
        self.gc_input.game.game_data.room_data_list[room_name].remove_feature(previous_cube_coordinates[0], previous_cube_coordinates[1], previous_cube_coordinates[2])
        self.gc_input.game.game_data.room_data_list[room_name].add_feature(feature_name, new_cube_coordinates[0], new_cube_coordinates[1], new_cube_coordinates[2])

    def check_location_full(self, room_name, cube_coordinates):
        return self.gc_input.game.game_data.room_data_list[room_name].check_cube_full(cube_coordinates[0], cube_coordinates[1], cube_coordinates[2])
    # endregion


class Room2(object):
    def __init__(self, room_name, x_size, y_size, z_size=4):
        self.name = room_name
        self.x_size = x_size
        self.y_size = y_size
        self.z_size = z_size
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
                section2_name = []
                for section3 in range(self.z_size):
                    section3_name = Cube(self.name, section+1, section2+1, section3+1)
                    section2_name.append(section3_name)
                section_name.append(section2_name)
            self.tiles_array.append(section_name)

    def display_room_grid(self):
        for section3 in range(self.z_size):
            print("level " +str(section3+1))
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
                self.add_room_plot(self.name + "_" + str(x) + "_" + str(y), Plot(self.name, x, y))

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
    def access_cube(self, x, y, z):
        chosen_cube = self.tiles_array[x-1][y-1][z-1]
        return chosen_cube

    def access_adjacent_cube(self, feature, direction):
        new_cube_x = feature.x
        new_cube_y = feature.y
        new_cube_z = feature.z
        if direction == Direction.DOWN:
            new_cube_y += 1
        elif direction == Direction.UP:
            new_cube_y -= 1
        elif direction == Direction.LEFT:
            new_cube_x -= 1
        elif direction == Direction.RIGHT:
            new_cube_z += 1
        new_cube = self.access_cube(new_cube_x, new_cube_y, new_cube_z)
        return new_cube

    def check_cube_full(self, x, y, z):
        chosen_cube = self.access_cube(x, y, z)
        fill_status = False
        if not chosen_cube.object_filling:
            fill_status = False
        else:
            fill_status = True
        return fill_status

    def move_feature(self, feature, direction):
        current_cube = self.access_cube(feature.x, feature.y, feature.z)
        new_cube = self.access_adjacent_cube(feature, direction)
        current_cube.empty_cube()
        new_cube.fill_cube(feature.name)

    def teleport_feature(self, feature, new_x, new_y, new_z):
        current_cube = self.access_cube(feature.x, feature.y, feature.z)
        new_cube = self.access_cube(new_x, new_y, new_z)
        current_cube.empty_cube()
        new_cube.fill_cube(feature.name)

    def remove_feature(self, x, y, z):
        feature_cube = self.access_cube(x, y, z)
        feature_cube.empty_cube()
        pass

    def add_feature(self, feature_name, coordinates_list):
        for coordinates in coordinates_list:
            feature_cube = self.access_cube(coordinates[0], coordinates[1], coordinates[2])
            feature_cube.fill_cube(feature_name)
            pass

    # endregion

    def get_plot_information(self):
        plots_x = self.total_plots_x
        plots_y = self.total_plots_y
        plot_size_x = self.plot_size_x
        plot_size_y = self.plot_size_y
        return [plots_x, plots_y, plot_size_x, plot_size_y]

    def get_plot(self, plot_x, plot_y):
        chosen_plot = self.plot_list[self.name + "_" + str(plot_x) + "_" + str(plot_y)]
        return chosen_plot


class Cube(object):
    def __init__(self, room_name, x, y, z):
        self.room_name = room_name
        self.x = x
        self.y = y
        self.z = z
        self.name = self.room_name + "_" + "tile" + str(x) + "_" + str(y) + "_" + str(z)

        self.object_filling = None

    def give_coordinates(self):
        coords = [self.x, self.y, self.z]
        return coords

    def fill_cube(self, object_name):
        self.object_filling = object_name

    def empty_cube(self):
        self.object_filling = None


class Door(object):
    def __init__(self, room_from, room_to, x_from, y_from, x_to, y_to):
        self.room_from = room_from
        self.room_to = room_to
        self. x_from = x_from
        self.y_from = y_from
        self.x_to = x_to
        self.y_to = y_to

class Plot(object):
    def __init__(self, room, plot_x, plot_y):
        self.plot_x = plot_x
        self.plot_y = plot_y
        self.room = room
        self.name = self.room + "_" + str(plot_x) + "_" + str(plot_y)
        self.background_csv_file = "assets/room_csv/background_csv" + "/" + self.room + "_" + str(plot_x) + "_" + str(plot_y) + "_" + "Background.csv"
        self.terrain_csv_file = "assets/room_csv/terrain_csv" + "/" + self.room + "_" + str(plot_x) + "_" + str(plot_y) + "_" + "Terrain.csv"
        self.elevation_csv_file = "assets/room_csv/elevation_csv" + "/" + self.room + "_" + str(plot_x) + "_" + str(plot_y) + "_" + "Elevation.csv"
        self.elevation_map = None
        self.background_map = TileMap(self.background_csv_file).return_map()
        self.try_elevation_map()

    def try_elevation_map(self):
         self.elevation_map = ElevationMap(self.name, self.elevation_csv_file)


    def get_elevation(self, x, y):
        elevation = self.elevation_map.get_elevation(x, y)
        return elevation


class NewBasicRoom(Room2):
    ID = "New_Basic_Room"

    def __init__(self):
        super().__init__(self.ID, 10, 10)
        self.initiate_room()


class RingsidePlot(Plot):
    def __init__(self, room, plot_x, plot_y):
        super().__init__(room, plot_x, plot_y)
        self.background_csv_file = "assets/room_csv/background_csv/Ringside_1_1_Background.csv"
        self.elevation_csv_file = "assets/room_csv/elevation_csv/Ringside_1_1_elevation.csv"
        self.background_map = TileMap(self.background_csv_file).return_map()
        self.try_elevation_map()


class Ringside(Room2):
    ID = "Ringside"

    def __init__(self):
        super().__init__(self.ID, 55, 106)
        self.initiate_room()

    def add_all_plots(self):
        for x in range(self.total_plots_x):
            x += 1
            for y in range(self.total_plots_y):
                y += 1
                self.add_room_plot(self.name + "_" + str(x) + "_" + str(y), RingsidePlot(self.name, x, y))


class IslandPlot(Plot):
    def __init__(self, room, plot_x, plot_y):
        super().__init__(room, plot_x, plot_y)
        self.background_csv_file = "assets/room_csv/background_csv/Island_1_1_Background.csv"
        self.background_map = TileMap(self.background_csv_file).return_map()
        self.elevation_csv_file = "assets/room_csv/elevation_csv" + "/" + self.room + "_" + str(plot_x) + "_" + str(plot_y) + "_" + "Elevation.csv"


class Island(Room2):
    ID = "Island"

    def __init__(self):
        super().__init__(self.ID, 13, 13)
        self.initiate_room()

    def add_all_plots(self):
        for x in range(self.total_plots_x):
            x += 1
            for y in range(self.total_plots_y):
                y += 1
                self.add_room_plot(self.name + "_" + str(x) + "_" + str(y), IslandPlot(self.name, x, y))


class MountainPlot(Plot):
    def __init__(self, room, plot_x, plot_y):
        super().__init__(room, plot_x, plot_y)
        self.background_csv_file = "assets/room_csv/background_csv/Mountain_1_1_Background.csv"
        self.background_map = TileMap(self.background_csv_file).return_map()
        self.elevation_csv_file = "assets/room_csv/elevation_csv" + "/" + self.room + "_" + str(plot_x) + "_" + str(plot_y) + "_" + "Elevation.csv"


class Mountain(Room2):
    ID = "Mountain"

    def __init__(self):
        super().__init__(self.ID, 13, 13)
        self.initiate_room()

    def add_all_plots(self):
        for x in range(self.total_plots_x):
            x += 1
            for y in range(self.total_plots_y):
                y += 1
                self.add_room_plot(self.name + "_" + str(x) + "_" + str(y), MountainPlot(self.name, x, y))