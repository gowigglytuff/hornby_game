from definitions import Direction

class PositionManager(object):
    def __init__(self, gc_input):
        self.gc_input = gc_input  # type: GameController

    def check_if_player_can_move(self, direction, checker, room):
        result = True
        if self.check_adjacent_tile(direction, checker, room).is_full:
            result = False
        if self.check_rooms_edges(direction, checker, room):
            result = False

        return result

    def check_adjacent_tile(self, direction, checker, room):
        x = checker.x
        y = checker.y
        if direction == Direction.DOWN:
            y = y + 1
        elif direction == Direction.UP:
            y = y - 1
        elif direction == Direction.LEFT:
            x = x - 1
        elif direction == Direction.RIGHT:
            x = x + 1
        return room.tiles_array[x][y]

    def check_rooms_edges(self, direction, checker, room):
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

    def fill_room_grid(self, room_to_fill):
        fill_list = []
        npc_ghost_list = self.gc_input.game.game_state.npc_ghost_list
        for npc in npc_ghost_list.keys():
            npc_ghost = self.gc_input.get_npc_ghost(npc)
            npc_avatar = self.gc_input.get_npc_avatar(npc)
            if npc_ghost_list[npc].room == room_to_fill:
                fill_list.append(npc_ghost)
        fill_list.append(self.gc_input.game.game_state.player_ghost)
        for item in fill_list:
            self.gc_input.game.game_view.game_data.room_data_list[room_to_fill].tiles_array[item.x][item.y].fill_tile(item.type, item.name)

    def get_feature_location(self, feature_name):
        feature_data = self.gc_input.game_state.feature_location_dictionary[feature_name]
        return feature_data

    def update_feature_dictionary(self, feature_name, location):
        self.gc_input.game_state.feature_location_dictionary[feature_name][1] = location

    def update_locations(self, room_name, feature_name, previous_cube_coordinates, new_cube_coordinates):
        self.gc_input.game.game_data.room_data_list[room_name].remove_feature(previous_cube_coordinates[0], previous_cube_coordinates[1], previous_cube_coordinates[2])
        self.gc_input.game.game_data.room_data_list[room_name].add_feature(feature_name, new_cube_coordinates[0], new_cube_coordinates[1], new_cube_coordinates[2])

    def check_location_full(self, room_name, cube_coordinates):
        return self.gc_input.game.game_data.room_dictionary[room_name].check_cube_full(cube_coordinates[0], cube_coordinates[1], cube_coordinates[2])

class Room2(object):
    def __init__(self, room_name, x_size, y_size, z_size=4):
        self.name = room_name
        self.x_size = x_size
        self.y_size = y_size
        self.z_size = z_size

        self.tiles_array = []
        self.active_tiles = []
        self.generate_room_grid()
        self.access_cube(3, 3, 3).fill_cube("John")

    def generate_room_grid(self):
        for section in range(self.x_size):
            section_name = []
            for section2 in range(self.y_size):
                section2_name = []
                for section3 in range(self.z_size):
                    section3_name = Cube(self.name, section+1, section2+1, section3+1)
                    section2_name.append(section3_name)
                section_name.append(section2_name)
            print(section_name)
            self.tiles_array.append(section_name)
        print(self.access_cube(1, 1, 1).give_coordinates())

    def access_cube(self, x, y, z):
        chosen_cube = self.tiles_array[x-1][y-1][z-1]
        return chosen_cube

    def tile(self, x, y, z):
        chosen_cube = self.tiles_array[x-1][y-1][z-1]

    def check_cube_full(self, x, y, z):
        chosen_cube = self.access_cube(x, y, z)
        fill_status = False
        if not chosen_cube.object_filling:
            fill_status = False
        else:
            fill_status = True
        return fill_status

    def move_feature(self, direction):
        feature_cube = self.access_cube(1, 1, 1)
        if direction == Direction.DOWN:
            feature_cube.y += 1
        elif direction == Direction.UP:
            feature_cube.y -= 1
        elif direction == Direction.LEFT:
            feature_cube.x -= 1
        elif direction == Direction.RIGHT:
            feature_cube.x += 1

    def teleport_feature(self):
        boop = self.access_cube(1, 1, 1)
        print(boop.object_filling)
        pass

    def remove_feature(self, x, y, z):
        feature_cube = self.access_cube(x, y, z)
        feature_cube.empty_cube()
        pass

    def add_feature(self, feature_name, x, y, z):
        feature_cube = self.access_cube(x, y, z)
        feature_cube.fill_cube(feature_name)
        pass

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