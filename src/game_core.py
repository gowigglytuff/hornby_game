from enum import Enum

import pygame

from player import Player_Avatar
from spritesheet import Spritesheet
from tile_map import TileMap, TileSet

_ENUM_BASE = 83571983457


class Direction(Enum):
    LEFT = _ENUM_BASE + 1
    RIGHT = _ENUM_BASE + 2
    UP = _ENUM_BASE + 3
    DOWN = _ENUM_BASE + 4


class Game(object):
    def __init__(self):
        self.game_running = True
        self.game_controller = GameController(self)
        self.game_state = GameState(self.game_controller)
        self.game_data = GameData()
        self.position_manager = PositionManager()
        self.game_view = GameView(self.game_controller, self.game_data)
        self.inventory_manager = InventoryManager()  # type:InventoryManager

        self.keyboard_manager = KeyboardManager(self.game_view)


class GameController(object):
    def __init__(self, game):
        self.game = game  # type: Game

        self.five_second_timer_id = pygame.USEREVENT + 150
        self.ten_second_timer_id = pygame.USEREVENT + 151
        self.one_second_timer_id = pygame.USEREVENT + 152
        self.quarter_second_timer_id = pygame.USEREVENT + 153
        self.eighth_second_timer_id = pygame.USEREVENT + 154
        self.timer_list = [self.one_second_timer_id, self.five_second_timer_id, self.ten_second_timer_id, self.quarter_second_timer_id, self.eighth_second_timer_id]

    def parse_timer_event(self, event):
        if event.type in [self.five_second_timer_id, self.ten_second_timer_id, self.one_second_timer_id, self.eighth_second_timer_id]:
            pass

    def initiate_timers(self):
        eighth_second_timer = self.eighth_second_timer_id
        pygame.time.set_timer(eighth_second_timer, 5)

        quarter_second_timer = self.quarter_second_timer_id
        pygame.time.set_timer(quarter_second_timer, 20)

        one_second_timer = self.one_second_timer_id
        pygame.time.set_timer(one_second_timer, 1000)

        five_second_timer = self.five_second_timer_id
        pygame.time.set_timer(five_second_timer, 5000)

        ten_second_timer = self.ten_second_timer_id
        pygame.time.set_timer(ten_second_timer, 10000)

    def close_game(self):
        self.game.game_running = False

    def get_player_state(self):
        return self.game.game_state.player_state

    def move_right(self):
        self.game.game_state.camera[0] -= 1
        self.game.game_state.player_state.x += 1


class PositionManager(object):
    def __init__(self):
        self.room = Room()


class Room(object):
    def __init__(self):
        self.id = "room1"
        self.room_width = 10
        self.room_height = 10
        self.left_edge_x = 0
        self.top_edge_y = 0
        self.right_edge_x = self.left_edge_x + self.room_width - 1
        self.bottom_edge_y = self.top_edge_y + self.room_height - 1

        self.tiles_array = self.generate_room_grid()

    def generate_room_grid(self):
        tiles_array = []
        for section in range(self.room_width + 3):
            section_name = []
            tiles_array.append(section_name)

        for x in range(self.room_width + 2):
            for y in range(self.room_height + 3):
                spot_name = Tile(x, y, False, "None", "None", 1, 1)
                tiles_array[x].append(spot_name)
        return tiles_array


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


class GameData(object):
    def __init__(self):
        self.player_data = []
        self.character_data_list = {}
        self.prop_data_list = {}
        self.decoration_data_list = {}

        self.room_data_list = {}
        self.door_data_list = {}
        self.keyboard_manager_data_list = {}
        self.menu_data_list = {}
        self.overlay_data_list = {}
        self.temp_item_data_list = {}
        self.key_item_data_list = {}
        self.goal_data_list = {}
        self.outfit_data_list = {}

        self.spritesheet_list = {}

    def add_spritesheet(self, spritesheet_name, spritesheet_object):
        self.spritesheet_list[spritesheet_name] = spritesheet_object

    def add_player_data(self, player_object):
        self.player_data = player_object

    def add_character_data(self, character_name, character_object):
        self.character_data_list[character_name] = character_object

    def add_prop_data(self, prop_name, prop_object):
        self.prop_data_list[prop_name] = prop_object

    def add_decoration_data(self, decoration_name, decoration_object):
        self.decoration_data_list[decoration_name] = decoration_object

    def add_keyboard_manager_data(self, keyboard_manager_name, keyboard_manager_object):
        self.keyboard_manager_data_list[keyboard_manager_name] = keyboard_manager_object

    def add_room_data(self, room_name, room_object):
        self.room_data_list[room_name] = room_object

    def add_door_data(self, door_name, door_object):
        self.door_data_list[door_name] = door_object

    def add_temp_item_data(self, item_name, item_object):
        self.temp_item_data_list[item_name] = item_object

    def add_key_item_data(self, item_name, item_object):
        self.key_item_data_list[item_name] = item_object

    def add_menu_data(self, menu_name, menu_object):
        self.menu_data_list[menu_name] = menu_object

    def add_overlay_data(self, overlay_name, overlay_object):
        self.overlay_data_list[overlay_name] = overlay_object

    def add_goal_data(self, goal_name, goal_object):
        self.goal_data_list[goal_name] = goal_object

    def add_outfit_data(self, outfit_name, outfit_object):
        self.outfit_data_list[outfit_name] = outfit_object


class GameState(object):
    def __init__(self, game_controller):
        self.game_controller = game_controller  # type: GameController
        self.player_state = Player_Avatar(1, 1)  # type: Player_Avatar
        self.character_state_list = {}
        self.prop_state_list = {}
        self.decoration_state_list = {}

        self.new_game = True
        self.current_room = None
        self.camera = [0, 0]

        self.your_coins = 127
        self.your_seeds = 24
        self.total_seeds_found = 26

        self.day_of_summer = 12
        self.time_of_day = 14
        self.night_filter_current_alpha = 0

    def add_player_state(self, player_object):
        self.player_state = player_object

    def add_character_avatar(self, character_name, character_object):
        self.character_state_list[character_name] = character_object


class GameView(object):
    def __init__(self, game_controller, game_data):
        self.game_data = game_data  # type: GameData
        self.game_controller = game_controller  # type: GameController
        self.clock = pygame.time.Clock()
        self.resolution = (320, 320)
        self.FPS = 30
        self.square_size = [32, 32]
        self.base_locator_x = (self.resolution[0] / 2) /self.square_size[0]
        self.base_locator_y = (self.resolution[1] / 2) /self.square_size[1]
        self.screen = pygame.display.set_mode(self.resolution)
        self.font = "assets/fonts/PressStart.ttf"
        self.active_keyboard_manager = InGameKeyboardManager(self)  # type: KeyboardManager

        self.night_filter = pygame.Surface(pygame.Rect((0, 0, self.resolution[0], self.resolution[1])).size)
        self.sky_change_increments = 6
        self.fully_dark_hours = 4
        self.sky_change_degree = 15

        self.tile_set = TileSet("assets/tile_set/tile_set_1.png", 32, 32, 10, 10).load_tile_images()
        self.bg = TileMap("assets/tile_set/tile_map_1.csv", self.tile_set, 25).return_map()

        self.image = 1
        self.test_y = 50-12.5
        self.test_switch = 1

        self.image2 = 1
        self.test_y2 = 75-10
        self.test_switch2 = 1
        self.character_test = Spritesheet("player_base_spritesheet", "assets/spritesheets/test_run2.png", 25, 35)
        self.character_test2 = Spritesheet("player_base_spritesheet", "assets/spritesheets/test_run4.png", 25, 35)
    def tick(self):
        self.clock.tick(self.FPS)

    def set_active_keyboard_manager(self, active_manager):
        self.active_keyboard_manager = active_manager

    def draw_tester(self, screen):
        screen.blit(self.character_test.get_image(self.image, 0), [100-18, ((-(self.test_y2/32) + 1) * self.square_size[1]+self.test_y)])
        screen.blit(self.character_test2.get_image(self.image2, 0), [100 + 50 - 18, 100])

    def draw_player(self, screen):
        player_state = self.game_controller.get_player_state()
        self_x = (self.base_locator_x * self.square_size[0])
        self_y = ((self.base_locator_y * self.square_size[1]) - self.game_data.player_data.image_offset_y)
        screen.blit(self.game_data.spritesheet_list[player_state.spritesheet].get_image(player_state.cur_img[0], player_state.cur_img[1]), [self_x, self_y])

    def draw_bg(self):
        bg_x = (((self.game_controller.game.game_state.camera[0]) + 1) * self.square_size[0])
        bg_y = ((-(self.test_y2/32) + 1) * self.square_size[1])
        self.screen.blit(self.bg, (bg_x, bg_y))

    def draw_all(self):
        self.draw_bg()
        #self.draw_player(self.screen)
        self.draw_tester(self.screen)

    def parse_input_event(self, event):
        if event.type == pygame.QUIT:
            self.game_controller.close_game()

        elif event.type in [pygame.KEYDOWN, pygame.KEYUP]:
            self.active_keyboard_manager.parse_key_input(event.type, event.key)

        elif event.type in self.game_controller.timer_list:
            if event.type == self.game_controller.one_second_timer_id:
                print("1 second)")

            if event.type == self.game_controller.quarter_second_timer_id:
                if self.test_switch <= 40:
                    change = 1

                    if self.test_switch == 5:
                        self.image = 3

                    elif self.test_switch == 15:
                        self.image = 0

                    elif self.test_switch == 25:
                        self.image = 1

                    elif self.test_switch == 35:
                        self.image = 0

                    # if ((self.test_switch > 7) and (self.test_switch < 20) or ((self.test_switch > 27) and (self.test_switch < 40))):
                    self.test_y += change
                    self.test_switch += 1

                elif self.test_switch == 41:
                    self.test_switch = 1
                else:
                    self.test_switch += 1
                if self.test_y >= 700:
                    self.test_y = 25-10

            if event.type == self.game_controller.eighth_second_timer_id:
                change = 1
                if self.test_switch2 <= 50:
                    if self.test_switch2 == 5:
                        self.image2 = 3
                        self.test_y2 += change

                    elif self.test_switch2 == 30:
                        self.image2 = 1
                        self.test_y2 += change

                    else:
                        self.test_y2 += change

                    self.test_switch2 += 1

                elif self.test_switch2 == 51:
                    self.test_switch2 = 1
                    self.test_y2 += change

                if self.test_y2 >= 700:
                    self.test_y2 = 25-10

class InventoryManager(object):
    def __init__(self):
        pass


class UpdateManager(object):
    def __init__(self):
        pass


class KeyboardManager(object):
    def __init__(self, game_view):
        self.game_view = game_view

    def parse_key_input(self, event_type, key):
        if event_type == pygame.KEYDOWN:
            if key == pygame.K_RIGHT:
                self.key_direction_pressed(Direction.RIGHT)

            if key == pygame.K_LEFT:
                self.key_direction_pressed(Direction.LEFT)

            if key == pygame.K_DOWN:
                self.key_direction_pressed(Direction.DOWN)

            if key == pygame.K_UP:
                self.key_direction_pressed(Direction.UP)

            if key == pygame.K_RETURN:
                self.key_return_pressed()

            if key == pygame.K_SPACE:
                self.key_space_pressed()

            if key == pygame.K_LCTRL:
                self.key_control_pressed()

            if key == pygame.K_LSHIFT:
                self.key_lshift_pressed()

            if key == pygame.K_CAPSLOCK:
                self.key_caps_pressed()

        elif event_type == pygame.KEYUP:
            if key == pygame.K_RIGHT:
                self.key_direction_released(Direction.RIGHT)

            if key == pygame.K_LEFT:
                self.key_direction_released(Direction.LEFT)

            if key == pygame.K_DOWN:
                self.key_direction_released(Direction.DOWN)

            if key == pygame.K_UP:
                self.key_direction_released(Direction.UP)

            if key == pygame.K_RETURN:
                self.key_return_released()

            if key == pygame.K_SPACE:
                self.key_space_released()

            if key == pygame.K_LCTRL:
                self.key_control_released()

            if key == pygame.K_LSHIFT:
                self.key_lshift_released()

            if key == pygame.K_CAPSLOCK:
                self.key_caps_released()

    def key_direction_pressed(self, direction):
        if direction == Direction.RIGHT:
            pass

    def key_return_pressed(self):
        pass

    def key_space_pressed(self):
        pass

    def key_control_pressed(self):
        pass

    def key_lshift_pressed(self):
        pass

    def key_caps_pressed(self):
        pass

    def key_direction_released(self, direction):
        pass

    def key_return_released(self):
        pass

    def key_space_released(self):
        pass

    def key_control_released(self):
        pass

    def key_lshift_released(self):
        pass

    def key_caps_released(self):
        pass


class InGameKeyboardManager(KeyboardManager):
    def __init__(self, game_view):
        super().__init__(game_view)

    def parse_key_input(self, event_type, key):
        if event_type == pygame.KEYDOWN:
            if key == pygame.K_RIGHT:
                self.key_direction_pressed(Direction.RIGHT)

            if key == pygame.K_LEFT:
                self.key_direction_pressed(Direction.LEFT)

            if key == pygame.K_DOWN:
                self.key_direction_pressed(Direction.DOWN)

            if key == pygame.K_UP:
                self.key_direction_pressed(Direction.UP)

            if key == pygame.K_RETURN:
                self.key_return_pressed()

            if key == pygame.K_SPACE:
                self.key_space_pressed()

            if key == pygame.K_LCTRL:
                self.key_control_pressed()

            if key == pygame.K_LSHIFT:
                self.key_lshift_pressed()

            if key == pygame.K_CAPSLOCK:
                self.key_caps_pressed()

        elif event_type == pygame.KEYUP:
            if key == pygame.K_RIGHT:
                self.key_direction_released(Direction.RIGHT)

            if key == pygame.K_LEFT:
                self.key_direction_released(Direction.LEFT)

            if key == pygame.K_DOWN:
                self.key_direction_released(Direction.DOWN)

            if key == pygame.K_UP:
                self.key_direction_released(Direction.UP)

            if key == pygame.K_RETURN:
                self.key_return_released()

            if key == pygame.K_SPACE:
                self.key_space_released()

            if key == pygame.K_LCTRL:
                self.key_control_released()

            if key == pygame.K_LSHIFT:
                self.key_lshift_released()

            if key == pygame.K_CAPSLOCK:
                self.key_caps_released()

    def key_direction_pressed(self, direction):
        if direction == Direction.RIGHT:
            self.game_view.game_controller.move_right()

    def key_return_pressed(self):
        pass

    def key_space_pressed(self):
        pass

    def key_control_pressed(self):
        pass

    def key_lshift_pressed(self):
        pass

    def key_caps_pressed(self):
        pass

    def key_direction_released(self, direction):
        pass

    def key_return_released(self):
        pass

    def key_space_released(self):
        pass

    def key_control_released(self):
        pass

    def key_lshift_released(self):
        pass

    def key_caps_released(self):
        pass


class InMenuKeyboardManager(KeyboardManager):
    def __init__(self, game_view):
        super().__init__(game_view)

    def parse_key_input(self, event_type, key):
        if event_type == pygame.KEYDOWN:
            if key == pygame.K_RIGHT:
                self.key_direction_pressed(Direction.RIGHT)

            if key == pygame.K_LEFT:
                self.key_direction_pressed(Direction.LEFT)

            if key == pygame.K_DOWN:
                self.key_direction_pressed(Direction.DOWN)

            if key == pygame.K_UP:
                self.key_direction_pressed(Direction.UP)

            if key == pygame.K_RETURN:
                self.key_return_pressed()

            if key == pygame.K_SPACE:
                self.key_space_pressed()

            if key == pygame.K_LCTRL:
                self.key_control_pressed()

            if key == pygame.K_LSHIFT:
                self.key_lshift_pressed()

            if key == pygame.K_CAPSLOCK:
                self.key_caps_pressed()

        elif event_type == pygame.KEYUP:
            if key == pygame.K_RIGHT:
                self.key_direction_released(Direction.RIGHT)

            if key == pygame.K_LEFT:
                self.key_direction_released(Direction.LEFT)

            if key == pygame.K_DOWN:
                self.key_direction_released(Direction.DOWN)

            if key == pygame.K_UP:
                self.key_direction_released(Direction.UP)

            if key == pygame.K_RETURN:
                self.key_return_released()

            if key == pygame.K_SPACE:
                self.key_space_released()

            if key == pygame.K_LCTRL:
                self.key_control_released()

            if key == pygame.K_LSHIFT:
                self.key_lshift_released()

            if key == pygame.K_CAPSLOCK:
                self.key_caps_released()

    def key_direction_pressed(self, direction):
        if direction == Direction.RIGHT:
            self.game_view.game_controller.move_right()

    def key_return_pressed(self):
        pass

    def key_space_pressed(self):
        pass

    def key_control_pressed(self):
        pass

    def key_lshift_pressed(self):
        pass

    def key_caps_pressed(self):
        pass

    def key_direction_released(self, direction):
        pass

    def key_return_released(self):
        pass

    def key_space_released(self):
        pass

    def key_control_released(self):
        pass

    def key_lshift_released(self):
        pass

    def key_caps_released(self):
        pass