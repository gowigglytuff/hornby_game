from enum import Enum

import pygame
from tile_map import TileMap, TileSet


class Definitions(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4


class Game(object):
    def __init__(self):
        self.game_running = True
        self.game_controller = GameController(self)
        self.game_state = GameState(self.game_controller)
        self.game_date = GameData()
        self.position_manager = PositionManager()
        self.game_view = GameView(self.game_controller)
        self.inventory_manager = InventoryManager()  # type:InventoryManager

        self.keyboard_manager = KeyboardManager(self.game_view)


class GameController(object):
    def __init__(self, game):
        self.game = game  # type: Game

    def close_game(self):
        self.game.game_running = False


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

    def add_spreadsheet(self, spritesheet_name, spritesheet_object):
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
        self.player_state = []
        self.character_state_list = {}
        self.prop_state_list = {}
        self.decoration_state_list = {}

        self.new_game = True
        self.current_room = None
        self.camera = [-79, -79]

        self.your_coins = 127
        self.your_seeds = 24
        self.total_seeds_found = 26

        self.day_of_summer = 12
        self.time_of_day = 14
        self.night_filter_current_alpha = 0

    def add_character_avatar(self, character_name, character_object):
        self.character_state_list[character_name] = character_object


class GameView(object):
    def __init__(self, game_controller):
        self.game_controller = game_controller  # type: GameController
        self.clock = pygame.time.Clock()
        self.resolution = (320, 320)
        self.FPS = 30
        self.square_size = [32, 32]
        self.base_locator_x = self.resolution[0] / 2 - self.square_size[0] / 2
        self.base_locator_y = self.resolution[1] / 2 - self.square_size[1] / 2
        self.screen = pygame.display.set_mode(self.resolution)
        self.font = "assets/fonts/PressStart.ttf"
        self.active_keyboard_manager = KeyboardManager(self)  # type: KeyboardManager

        self.night_filter = pygame.Surface(pygame.Rect((0, 0, self.resolution[0], self.resolution[1])).size)
        self.sky_change_increments = 6
        self.fully_dark_hours = 4
        self.sky_change_degree = 15

        self.tile_set = TileSet("assets/tile_set/tile_set_1.png", 32, 32, 10, 10).load_tile_images()
        self.bg = TileMap("assets/tile_set/tile_map_1.csv", self.tile_set, 32).return_map()

        self.five_second_timer_id = pygame.USEREVENT + 150
        self.ten_second_timer_id = pygame.USEREVENT + 151
        self.one_second_timer_id = pygame.USEREVENT + 152

    def tick(self):
        self.clock.tick(self.FPS)

    def set_active_keyboard_manager(self, active_manager):
        self.active_keyboard_manager = active_manager

    def draw_all(self):
        self.screen.blit(self.bg, (0, 0))

    def initiate_timers(self):
        one_second_timer = self.one_second_timer_id
        pygame.time.set_timer(one_second_timer, 1000)

        five_second_timer = self.five_second_timer_id
        pygame.time.set_timer(five_second_timer, 5000)

        ten_second_timer = self.ten_second_timer_id
        pygame.time.set_timer(ten_second_timer, 10000)

    def parse_event(self, event):
        if event.type == pygame.QUIT:
            self.game_controller.close_game()

        if event.type in [self.five_second_timer_id, self.ten_second_timer_id, self.one_second_timer_id]:
            print(event)

        elif event.type in [pygame.KEYDOWN, pygame.KEYUP]:
            self.active_keyboard_manager.parse_key_input(event.type, event.key)


class InventoryManager(object):
    def __init__(self):
        pass


class PositionManager(object):
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
                self.key_direction_pressed(Definitions.RIGHT)

            if key == pygame.K_LEFT:
                self.key_direction_pressed(Definitions.LEFT)

            if key == pygame.K_DOWN:
                self.key_direction_pressed(Definitions.DOWN)

            if key == pygame.K_UP:
                self.key_direction_pressed(Definitions.UP)

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
                self.key_direction_released(Definitions.RIGHT)

            if key == pygame.K_LEFT:
                self.key_direction_released(Definitions.LEFT)

            if key == pygame.K_DOWN:
                self.key_direction_released(Definitions.DOWN)

            if key == pygame.K_UP:
                self.key_direction_released(Definitions.UP)

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
