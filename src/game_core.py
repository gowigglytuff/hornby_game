from enum import Enum

import pygame

from ghost_page import PlayerGhost
from player import Player_Avatar
from tile_map import TileMap, TileSet
from room_page import Room
from keyboard_manager_page import *
from avatar_page import PlayerAvatar
from definitions import Direction, GameSettings


class Game(object):
    def __init__(self):
        self.game_running = True
        self.game_controller = GameController(self) #type: GameController
        self.game_state = GameState(self.game_controller)
        self.game_data = GameData() #type: GameData
        self.game_view = GameView(self.game_controller, self.game_data)
        self.inventory_manager = InventoryManager()  # type:InventoryManager


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


class GameController(object):
    def __init__(self, game):
        self.game = game  # type: Game

        self.five_second_timer_id = pygame.USEREVENT + 150
        self.ten_second_timer_id = pygame.USEREVENT + 151
        self.one_second_timer_id = pygame.USEREVENT + 152
        self.fifth_second_timer_id = pygame.USEREVENT + 153
        self.twentieth_second_timer_id = pygame.USEREVENT + 154
        self.timer_list = [self.one_second_timer_id, self.five_second_timer_id, self.ten_second_timer_id, self.fifth_second_timer_id, self.twentieth_second_timer_id]

        self.active_keyboard_manager = InGameKeyboardManager(self, Direction)  # type: KeyboardManager
        self.key_down_queue = []
        self.position_manager = PositionManager(self)

    def parse_input_event(self, event):
        if event.type == pygame.QUIT:
            self.close_game()

        elif event.type in [pygame.KEYDOWN, pygame.KEYUP]:
            if event.key == pygame.K_RETURN:
                self.position_manager.check_adjacent_tile(Direction.UP, self.game.game_state.player_ghost, self.game.game_data.room_data_list[self.game.game_state.current_room])
            self.active_keyboard_manager.parse_key_input(event.type, event.key)

        elif event.type in self.timer_list:
            if event.type == self.one_second_timer_id:
                pass
            if event.type == self.fifth_second_timer_id:
                pass
            if event.type == self.twentieth_second_timer_id:
                if not self.game.game_view.character_avatar.currently_animating:
                    direction = []
                    if self.key_down_queue:
                        if self.key_down_queue == pygame.K_DOWN:
                            direction = Direction.DOWN
                        elif self.key_down_queue == pygame.K_UP:
                            direction = Direction.UP
                        elif self.key_down_queue == pygame.K_RIGHT:
                            direction = Direction.RIGHT
                        elif self.key_down_queue == pygame.K_LEFT:
                            direction = Direction.LEFT

                        self.change_character_facing(direction)
                        if self.position_manager.check_if_player_can_move(direction, self.game.game_state.player_ghost, self.game.game_data.room_data_list[self.game.game_state.current_room]):
                            self.move_character_avatar(direction)
                            self.move_character_ghost(direction)

                if self.game.game_view.character_avatar.currently_animating:
                    self.game.game_view.character_avatar.perform_animation()

    def set_active_keyboard_manager(self, active_manager):
        self.active_keyboard_manager = active_manager

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

    def set_camera(self):
        self.game.game_view.camera[0] = -(self.game.game_view.character_avatar.image_x - self.game.game_state.player_ghost.x) * 24
        self.game.game_view.camera[1] = -(self.game.game_view.character_avatar.image_y - self.game.game_state.player_ghost.y) * 24

    def close_game(self):
        self.game.game_running = False

    def get_player_state(self):
        return self.game.game_state.player_ghost

    def change_character_facing(self, direction):
        self.game.game_state.player_ghost.facing = direction
        self.game.game_view.character_avatar.face_character(direction)

    def move_character_ghost(self, direction):
        if direction == Direction.DOWN:
            self.game.game_state.player_ghost.y += 1
        elif direction == Direction.UP:
            self.game.game_state.player_ghost.y -= 1
        elif direction == Direction.LEFT:
            self.game.game_state.player_ghost.x -= 1
        elif direction == Direction.RIGHT:
            self.game.game_state.player_ghost.x += 1

    def move_character_avatar(self, direction):
        if direction == Direction.DOWN:
            self.game.game_view.character_avatar.initiate_animation("walk_front")
        elif direction == Direction.UP:
            self.game.game_view.character_avatar.initiate_animation("walk_up")
        elif direction == Direction.LEFT:
            self.game.game_view.character_avatar.initiate_animation("walk_left")
        elif direction == Direction.RIGHT:
            self.game.game_view.character_avatar.initiate_animation("walk_right")


class PositionManager(object):
    def __init__(self, gc_input):
        self.gc_input = gc_input

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


class GameState(object):
    def __init__(self, game_controller):
        self.game_controller = game_controller  # type: GameController
        self.player_ghost = PlayerGhost(self, 1, 1)  # type: PlayerGhost
        self.character_ghost_list = {}
        self.prop_ghost_list = {}
        self.decoration_ghost_list = {}

        self.new_game = True
        self.current_room = "Basic_Room"

        self.your_coins = 127
        self.your_seeds = 24
        self.total_seeds_found = 26

        self.day_of_summer = 12
        self.time_of_day = 14
        self.night_filter_current_alpha = 0

    def add_player_state(self, player_object):
        self.player_ghost = player_object

    def add_character_avatar(self, character_name, character_object):
        self.character_state_list[character_name] = character_object


class GameView(object):
    def __init__(self, game_controller, game_data):
        self.game_data = game_data  # type: GameData
        self.game_controller = game_controller  # type: GameController
        self.clock = pygame.time.Clock()
        self.resolution = (312*2, 312*2)
        self.FPS = 72
        self.square_size = [GameSettings.TILESIZE, GameSettings.TILESIZE]
        self.base_locator_x = ((self.resolution[0]-self.square_size[0])/self.square_size[0])/2 + 1
        self.base_locator_y = ((self.resolution[1]-self.square_size[1])/self.square_size[1])/2 + 1

        self.camera = [0, 0]
        self.screen = pygame.display.set_mode(self.resolution)
        self.font = "assets/fonts/PressStart.ttf"

        self.night_filter = pygame.Surface(pygame.Rect((0, 0, self.resolution[0], self.resolution[1])).size)
        self.sky_change_increments = 6
        self.fully_dark_hours = 4
        self.sky_change_degree = 15

        self.character_avatar = PlayerAvatar(self, self.base_locator_x, self.base_locator_y)

    def tick(self):
        self.clock.tick(self.FPS)

    def draw_player(self, screen):
        player = self.character_avatar
        play_loc_x = (player.image_x * self.square_size[0]) - self.square_size[0]
        play_loc_y = player.image_y * self.square_size[1] - (self.square_size[1] + player.image_offset_y)
        screen.blit(player.spritesheet.get_image(player.current_image_x, player.current_image_y), [play_loc_x, play_loc_y])

    def draw_bg(self):
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(0, 0, self.resolution[0], self.resolution[1]))
        camera_x = -self.camera[0]
        camera_y = -self.camera[1]
        room = self.game_data.room_data_list[self.game_controller.game.game_state.current_room]
        for plot in room.plot_list.keys():
            selected_plot = room.plot_list[plot]
            plot_location_x = room.plot_size_x * (selected_plot.plot_x - 1) * self.square_size[0]
            plot_location_y = room.plot_size_y * (selected_plot.plot_y - 1) * self.square_size[1]
            self.screen.blit(selected_plot.background_map, (camera_x + plot_location_x, camera_y + plot_location_y))

    def draw_all(self):
        self.draw_bg()
        self.draw_player(self.screen)


class InventoryManager(object):
    def __init__(self):
        pass


class UpdateManager(object):
    def __init__(self):
        pass


