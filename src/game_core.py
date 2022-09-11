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
        self.fifth_second_timer_id = pygame.USEREVENT + 153
        self.twentieth_second_timer_id = pygame.USEREVENT + 154
        self.timer_list = [self.one_second_timer_id, self.five_second_timer_id, self.ten_second_timer_id, self.fifth_second_timer_id, self.twentieth_second_timer_id]

    def parse_timer_event(self, event):
        if event.type in [self.five_second_timer_id, self.ten_second_timer_id, self.one_second_timer_id, self.twentieth_second_timer_id]:
            pass

    def initiate_timers(self):
        twentieth_second_timer = self.twentieth_second_timer_id
        pygame.time.set_timer(twentieth_second_timer, 7)

        fifth_second_timer = self.fifth_second_timer_id
        pygame.time.set_timer(fifth_second_timer, 20)

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
        self.animation_list = {}

        self.spritesheet_list = {}

    def add_spritesheet(self, spritesheet_name, spritesheet_object):
        self.spritesheet_list[spritesheet_name] = spritesheet_object

    def add_animation(self, animation_name, animation_object):
        self.animation_list[animation_name] = animation_object

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
        self.resolution = (312, 312)
        self.FPS = 72
        self.square_size = [24, 24]
        self.base_locator_x = ((self.resolution[0] - self.square_size[0]) / 2)
        self.base_locator_y = ((self.resolution[1] - self.square_size[1]) / 2)

        self.camera = [0, 0]
        self.screen = pygame.display.set_mode(self.resolution)
        self.font = "assets/fonts/PressStart.ttf"
        self.active_keyboard_manager = InGameKeyboardManager(self)  # type: KeyboardManager

        self.night_filter = pygame.Surface(pygame.Rect((0, 0, self.resolution[0], self.resolution[1])).size)
        self.sky_change_increments = 6
        self.fully_dark_hours = 4
        self.sky_change_degree = 15

        self.tile_set = TileSet("assets/tile_set/tile_set_1.png", self.square_size[0], self.square_size[1], 10, 10).load_tile_images()
        self.bg = TileMap("assets/tile_set/tile_map_1.csv", self.tile_set, self.square_size[0]).return_map()

        self.image = 1
        self.test_y = 0
        self.test_x = 0
        self.test_switch = 1

        self.direction = Direction.DOWN
        self.image1 = 0
        self.image2 = 1
        self.offset_y = 36/2
        self.test_y2 = 0
        self.test_x2 = 0

        self.test_switch2 = 0
        self.character_test = Spritesheet("player_base_spritesheet", "assets/spritesheets/player1.png", 24, 36)
        self.character_test2 = Spritesheet("player_base_spritesheet", "assets/spritesheets/player1.png", 24, 36)

        self.character = PlayerImage(self, 5, 5)

        self.key_down_queue = []

    def tick(self):
        self.clock.tick(self.FPS)

    def set_active_keyboard_manager(self, active_manager):
        self.active_keyboard_manager = active_manager

    def draw_tester(self, screen):
        screen.blit(self.character_test.get_image(self.image, 0), [24*4, ((-(self.camera[1]/self.square_size[1]) + 1) * self.square_size[1] + self.test_y)])

    def draw_player(self, screen):
        screen.blit(self.character.spritesheet.get_image(self.character.current_image_x, self.character.current_image_y), [self.character.image_x * self.square_size[0], self.character.image_y*self.square_size[1]-self.offset_y])

    def draw_bg(self):
        bg_x = ((-(self.camera[0]/self.square_size[0])) * self.square_size[0])
        bg_y = ((-(self.camera[1]/self.square_size[1])) * self.square_size[1])
        self.screen.blit(self.bg, (bg_x, bg_y))

    def draw_all(self):
        self.draw_bg()
        self.draw_player(self.screen)
        self.draw_tester(self.screen)

    def parse_input_event(self, event):
        if event.type == pygame.QUIT:
            self.game_controller.close_game()

        elif event.type in [pygame.KEYDOWN, pygame.KEYUP]:
            # self.active_keyboard_manager.parse_key_input(event.type, event.key)
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_DOWN, pygame.K_UP, pygame.K_RIGHT, pygame.K_LEFT]:
                    self.key_down_queue = event.key

            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_DOWN, pygame.K_UP, pygame.K_RIGHT, pygame.K_LEFT]:
                    if self.key_down_queue == event.key:
                        self.key_down_queue = []

        elif event.type in self.game_controller.timer_list:
            if event.type == self.game_controller.one_second_timer_id:
                pass

            if event.type == self.game_controller.fifth_second_timer_id:
                if self.test_switch <= 24:
                    change = 1

                    if self.test_switch == 2:
                        self.image = 3

                    elif self.test_switch == 8:
                        self.image = 0

                    elif self.test_switch == 14:
                        self.image = 1

                    elif self.test_switch == 20:
                        self.image = 0

                    # if ((self.test_switch > 7) and (self.test_switch < 20) or ((self.test_switch > 27) and (self.test_switch < 40))):
                    self.test_y += change
                    self.test_switch += 1

                elif self.test_switch == 25:
                    self.test_switch = 1
                else:
                    self.test_switch += 1
                if self.test_y >= 700:
                    self.test_y = 24-10

            if event.type == self.game_controller.twentieth_second_timer_id:
                if not self.character.currently_animating:
                    if self.key_down_queue == pygame.K_DOWN:
                        self.character.initiate_animation("walk_front")

                    elif self.key_down_queue == pygame.K_UP:
                        self.character.initiate_animation("walk_up")

                    elif self.key_down_queue == pygame.K_RIGHT:
                        self.character.initiate_animation("walk_right")

                    elif self.key_down_queue == pygame.K_LEFT:
                        self.character.initiate_animation("walk_left")

                if self.character.currently_animating:
                    self.character.perform_animation()


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


class PlayerImage:
    def __init__(self, game_view, image_x, image_y):
        self.game_view = game_view  # type: GameView
        self.spritesheet = Spritesheet("player_base_spritesheet", "assets/spritesheets/player.png", 24, 36)
        self.current_image_x = 0
        self.current_image_y = 0
        self.image_x = image_x
        self.image_y = image_y
        self.animation_list = {"walk_front": WalkAnimation(self, Direction.DOWN),
                               "walk_left": WalkAnimation(self, Direction.LEFT),
                               "walk_right": WalkAnimation(self, Direction.RIGHT),
                               "walk_up": WalkAnimation(self, Direction.UP)}
        self.animation_frame = 0
        self.currently_animating = False
        self.current_animation = None

    def initiate_animation(self, animation_name):
        self.current_animation = animation_name
        self.currently_animating = True

    def perform_animation(self):
        animation_result = (self.animation_list[self.current_animation].animate())
        self.current_image_x = animation_result[2]
        self.current_image_y = animation_result[3]
        self.game_view.camera[0] += animation_result[0]
        self.game_view.camera[1] += animation_result[1]
        complete = animation_result[4]
        if complete:
            self.currently_animating = False
            self.current_animation = None

class Animation(object):
    def __init__(self, game_view, direction):
        self.game_view = game_view
        self.total_distance = 0
        self.direction = direction
        self.current_frame = 0
        self.frequency = 0

        self.complete = False

        self.y_change = 0
        self.x_change = 0
        self.current_image_x = 0
        self.current_image_y = 0
        self.vector = 1
        self.changing_variable = self.x_change
        if self.direction == Direction.UP:
            self.vector = -1
            self.changing_variable = self.y_change
            self.current_image_y = 1

        elif self.direction == Direction.LEFT:
            self.vector = -1
            self.current_image_y = 2

        elif self.direction == Direction.DOWN:
            self.current_image_y = 0
            self.changing_variable = self.y_change

        elif self.direction == Direction.RIGHT:
            self.current_image_y = 3

    def animate(self):
        pass

class WalkAnimation(Animation):
    def __init__(self, game_view, direction):
        super().__init__(game_view, direction)
        self.foot = "left"
        self.current_image_x = 0
        self.current_image_y = 0

        self.x_vector = 0
        self.y_vector = 0

        self.changing_variable = self.x_change
        self.set_directions()

    def set_directions(self):
        if self.direction == Direction.UP:
            self.y_vector = -1
            self.x_vector = 0
            self.changing_variable = self.y_change
            self.current_image_y = 1
        elif self.direction == Direction.LEFT:
            self.y_vector = 0
            self.x_vector = -1
            self.current_image_y = 3
        elif self.direction == Direction.DOWN:
            self.y_vector = 1
            self.x_vector = 0
            self.current_image_y = 0
            self.changing_variable = self.y_change
        elif self.direction == Direction.RIGHT:
            self.y_vector = 0
            self.x_vector = 1
            self.current_image_y = 2

    def animate(self):
        if self.current_frame <= 23:
            if self.current_frame == 0:
                if self.foot == "left":
                    self.current_image_x = 3
                elif self.foot == "right":
                    self.current_image_x = 1

            elif self.current_frame == 23:
                self.current_frame = 0
                self.current_image_x = 0
                self.complete = True

            self.current_frame += 1
        return self.result()

    def reset(self):
        self.current_frame = 0
        self.switch_foot()
        self.complete = False

    def switch_foot(self):
        if self.foot == "left":
            self.foot = "right"
        elif self.foot == "right":
            self.foot = "left"

    def result(self):
        y_change = self.y_vector
        x_change = self.x_vector
        sheet_x = self.current_image_x
        sheet_y = self.current_image_y
        complete = self.complete
        if self.complete:
            self.reset()

        return x_change, y_change, sheet_x, sheet_y, complete
