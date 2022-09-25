from definitions import GameSettings
from tile_map import TileMap


class Room(object):
    def __init__(self):
        self.id = None
        self.room_width = 0
        self.room_height = 0
        self.left_edge_x = 0
        self.top_edge_y = 0
        self.total_plots_x = 0
        self.total_plots_y = 0
        self.plot_list = {}

        self.right_edge_x = 0
        self.bottom_edge_y = 0
        self.plot_size_x = 0
        self.plot_size_y = 0
        self.tiles_array = 0
        self.background = None

    def add_all_plots(self):
        for x in range(self.total_plots_x):
            x += 1
            for y in range(self.total_plots_y):
                y += 1
                self.add_room_plot(self.id + "_" + str(x) + "_" + str(y), Plot(self.id, x, y))

    def add_room_plot(self, plot_name, plot_object):
        self.plot_list[plot_name] = plot_object

    def initiate_room(self):
        self.right_edge_x = self.left_edge_x + self.room_width - 1
        self.bottom_edge_y = self.top_edge_y + self.room_height - 1
        self.plot_size_x = int(self.room_width / self.total_plots_x)
        self.plot_size_y = int(self.room_height / self.total_plots_y)
        self.tiles_array = self.generate_room_grid()
        self.add_all_plots()

    def generate_room_grid(self):
        tiles_array = []
        for section in range(self.room_width + 2):
            section_name = []
            tiles_array.append(section_name)

        for x in range(self.room_width + 2):
            for y in range(self.room_height + 2):
                spot_name = Tile(x, y, False, "None", "None", 1, 1)
                tiles_array[x].append(spot_name)
        return tiles_array

    def display_tile_grid(self):
        for row in self.tiles_array:
            list = []
            for item in row:
                # list.append([item.x, item.y])
                list.append(item.object_filling)
            print(list)


class Plot(object):
    def __init__(self, room, plot_x, plot_y):
        self.plot_x = plot_x
        self.plot_y = plot_y
        self.room = room
        self.name = self.room + "_" + str(plot_x) + "_" + str(plot_y)
        self.background_csv_file = "assets/room_csv/background_csv" + "/" + self.room + "_" + str(plot_x) + "_" + str(plot_y) + "_" + "Background.csv"
        self.terrain_csv_file = "assets/room_csv/terrain_csv" + "/" + self.room + "_" + str(plot_x) + "_" + str(plot_y) + "_" + "Terrain.csv"
        self.elevation_csv_file = "assets/room_csv/elevation_csv" + "/" + self.room + "_" + str(plot_x) + "_" + str(plot_y) + "_" + "Elevation.csv"
        self.background_map = TileMap(self.background_csv_file).return_map()


class Tile(object):
    def __init__(self, x, y, is_full, filling_type, object_filling, elevation, terrain_type):
        self.x = x
        self.y = y
        self.is_full = is_full
        self.filling_type = filling_type
        self.object_filling = object_filling
        self.name = "tile" + str(x) + "_" + str(y)
        self.elevation = elevation
        self.terrain_type = terrain_type

    def fill_tile(self, type, object):
        self.is_full = True
        self.filling_type = type
        self.object_filling = object


class BasicRoom(Room):
    ID = "Basic_Room"

    def __init__(self):
        super().__init__()

        self.id = self.ID
        self.room_width = 80
        self.room_height = 33
        self.left_edge_x = 1
        self.top_edge_y = 1
        self.total_plots_x = 2
        self.total_plots_y = 1
        self.initiate_room()





