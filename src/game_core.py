from enum import Enum

import pygame

from ghost_page import PlayerGhost
from menu_page import StartMenu
from player import Player_Avatar
from tile_map import TileMap, TileSet
from room_page import Room
from keyboard_manager_page import *
from avatar_page import PlayerAvatar
from definitions import Direction, GameSettings, Types


class Game(object):
    def __init__(self):
        self.game_running = True
        self.game_state = GameState()  # type: GameState
        self.game_data = GameData()  # type: GameData
        self.game_view = GameView(self.game_data)  # type: GameView

        self.game_controller = GameController(self, self.game_view, self.game_state)  # type: GameController


class GameController(object):
    def __init__(self, game, game_view, game_state):
        self.game = game  # type: Game
        self.game_view = game_view  # type: GameView
        self.game_state = game_state  # type: GameState

        self.five_second_timer_id = pygame.USEREVENT + 150
        self.ten_second_timer_id = pygame.USEREVENT + 151
        self.one_second_timer_id = pygame.USEREVENT + 152
        self.fifth_second_timer_id = pygame.USEREVENT + 153
        self.twentieth_second_timer_id = pygame.USEREVENT + 154
        self.timer_list = [self.one_second_timer_id, self.five_second_timer_id, self.ten_second_timer_id, self.fifth_second_timer_id, self.twentieth_second_timer_id]

        self.active_keyboard_manager = None
        self.key_down_queue = []
        self.position_manager = PositionManager(self)
        self.menu_manager = MenuManager(self)
        self.inventory_manager = InventoryManager(self)  # type:InventoryManager

    def parse_input_event(self, event):
        if event.type == pygame.QUIT:
            self.close_game()

        elif event.type in [pygame.KEYDOWN, pygame.KEYUP]:
            self.active_keyboard_manager.parse_key_input(event.type, event.key)

        elif event.type in self.timer_list:
            if event.type == self.one_second_timer_id:
                pass
            if event.type == self.fifth_second_timer_id:
                pass
            if event.type == self.twentieth_second_timer_id:
                if not self.game_view.game_data.player_avatar.currently_animating:
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

                        self.change_player_facing(direction)
                        if self.position_manager.check_if_player_can_move(direction, self.game_state.player_ghost, self.game_view.game_data.room_data_list[self.game_state.current_room]):
                            self.move_character_avatar(direction)
                            self.move_character_ghost(direction)

                if self.game_view.game_data.player_avatar.currently_animating:
                    self.perform_animation(self.game_view.game_data.player_avatar)

    def set_active_keyboard_manager(self, active_manager_id):
        self.active_keyboard_manager = self.game_view.game_data.keyboard_manager_data_list[active_manager_id]

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
        self.game_view.camera[0] = -(self.game_view.game_data.player_avatar.image_x - self.game_state.player_ghost.x) * 24
        self.game_view.camera[1] = -(self.game_view.game_data.player_avatar.image_y - self.game_state.player_ghost.y) * 24

    def close_game(self):
        self.game.game_running = False

    def get_player_state(self):
        return self.game_state.player_ghost

    def get_npc_ghost(self, name):
        return self.game_state.npc_ghost_list[name]

    def get_npc_avatar(self, name):
        return self.game_view.game_data.npc_avatar_list[name]

    def get_player_ghost(self):
        return self.game_state.player_ghost

    def get_player_avatar(self):
        return self.game_view.game_data.player_avatar

    def get_current_room(self):
        return self.game_view.game_data.room_data_list[self.game_state.current_room]

    def change_player_facing(self, direction):
        self.game_state.player_ghost.facing = direction
        self.game_view.game_data.player_avatar.face_character(direction)

    def change_npc_facing(self, direction, npc_name):
        self.get_npc_ghost(npc_name).facing = direction
        self.get_npc_avatar(npc_name).face_character(direction)

    def move_character_ghost(self, direction):
        if direction == Direction.DOWN:
            self.game_state.player_ghost.y += 1
        elif direction == Direction.UP:
            self.game_state.player_ghost.y -= 1
        elif direction == Direction.LEFT:
            self.game_state.player_ghost.x -= 1
        elif direction == Direction.RIGHT:
            self.game_state.player_ghost.x += 1

    def move_character_avatar(self, direction):
        if direction == Direction.DOWN:
            self.game_view.game_data.player_avatar.initiate_animation("walk_front")
        elif direction == Direction.UP:
            self.game_view.game_data.player_avatar.initiate_animation("walk_up")
        elif direction == Direction.LEFT:
            self.game_view.game_data.player_avatar.initiate_animation("walk_left")
        elif direction == Direction.RIGHT:
            self.game_view.game_data.player_avatar.initiate_animation("walk_right")

    def update_view(self):
        current_room = self.game_state.current_room
        drawables_list = self.get_current_drawables()
        self.game_view.draw_all(drawables_list, current_room)

        for menu in self.menu_manager.visible_menus:
            self.game_view.draw_menu(self.menu_manager.menu_data_list[menu])
        for menu in self.menu_manager.static_menus:
            self.game_view.draw_menu(self.menu_manager.menu_data_list[menu])

    def get_current_drawables(self):
        drawables_list = []

        npc_ghost_list = self.game_state.npc_ghost_list

        for npc in npc_ghost_list.keys():
            npc_ghost = self.get_npc_ghost(npc)
            npc_avatar = self.get_npc_avatar(npc)
            if npc_ghost_list[npc].room == self.game_state.current_room:
                drawables_list.append([npc_avatar, npc_ghost.y, npc_avatar.drawing_priority])

        drawables_list.append([self.get_player_avatar(), self.get_player_ghost().y, self.get_player_avatar().drawing_priority])

        drawing_order = sorted(drawables_list, key=lambda x: (x[1], x[2]))

        return drawing_order

    def perform_animation(self, animator):
        animation_result = (animator.animation_list[animator.current_animation].animate())
        animator.current_image_x = animation_result[2]
        animator.current_image_y = animation_result[3]
        self.game_view.camera[0] += animation_result[0]
        self.game_view.camera[1] += animation_result[1]
        complete = animation_result[4]
        if complete:
            animator.currently_animating = False
            animator.current_animation = None

    def talk_to_npc(self, npc_talking_to, player_direction):
        direction_to_turn = Direction.DOWN
        if player_direction == Direction.DOWN:
            direction_to_turn = Direction.UP
        elif player_direction == Direction.UP:
            direction_to_turn = Direction.DOWN
        elif player_direction == Direction.LEFT:
            direction_to_turn = Direction.RIGHT
        elif player_direction == Direction.RIGHT:
            direction_to_turn = Direction.LEFT

        npc_talking_to_ghost = self.game_state.npc_ghost_list[npc_talking_to]
        npc_talking_to_avatar = self.game_view.game_data.npc_avatar_list[npc_talking_to]
        self.change_npc_facing(direction_to_turn, npc_talking_to)
        self.post_notice("You talked to " + npc_talking_to_ghost.name)
        self.menu_manager.set_dialogue_menu("Something strange is going on around here, have you heard about the children disapearing? Their parents couldn't even remember their names...", npc_talking_to_ghost.name, 11)

    def player_interact(self):
        interact_tile = self.position_manager.check_adjacent_tile(self.get_player_ghost().facing, self.get_player_ghost(), self.get_current_room())
        full = interact_tile.is_full
        fill_type = interact_tile.filling_type
        fill_object = interact_tile.object_filling
        if fill_type == Types.NPC:
            self.talk_to_npc(fill_object, self.get_player_ghost().facing)
        if fill_type == Types.PROP:
            pass

    def post_notice(self, phrase):
        self.menu_manager.menu_data_list["game_action_dialogue_menu"].show_dialogue(phrase)


class PositionManager(object):
    def __init__(self, gc_input):
        self.gc_input = gc_input # type: GameController

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


class GameState(object):
    def __init__(self):
        self.player_ghost = PlayerGhost(self, 1, 1)  # type: PlayerGhost
        self.npc_ghost_list = {}
        self.prop_ghost_list = {}
        self.decoration_ghost_list = {}

        self.new_game = True
        self.current_room = "Basic_Room"
        self.current_inventory = {}

        self.your_coins = 127
        self.your_seeds = 24
        self.total_seeds_found = 26

        self.day_of_summer = 12
        self.time_of_day = 14
        self.night_filter_current_alpha = 0

    def add_player_ghost(self, player_object):
        self.player_ghost = player_object

    def add_npc_ghost(self, npc_name, npc_object):
        self.npc_ghost_list[npc_name] = npc_object


class GameView(object):
    def __init__(self, game_data):
        self.game_data = game_data  # type: GameData
        self.clock = pygame.time.Clock()
        self.resolution = GameSettings.RESOLUTION
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

        self.player_avatar = PlayerAvatar(self.base_locator_x, self.base_locator_y)

    def tick(self):
        self.clock.tick(self.FPS)

    def draw_npc(self, npc_name):
        camera_x = -self.camera[0]
        camera_y = -self.camera[1]
        chosen_npc_avatar = self.game_data.npc_avatar_list[npc_name]
        npc_loc_x = camera_x + (self.game_data.npc_avatar_list[npc_name].image_x - 1) * self.square_size[0]
        npc_loc_y = camera_y + (self.game_data.npc_avatar_list[npc_name].image_y - 1) * self.square_size[1] - chosen_npc_avatar.image_offset_y
        self.screen.blit(chosen_npc_avatar.spritesheet.get_image(chosen_npc_avatar.current_image_x, chosen_npc_avatar.current_image_y), (npc_loc_x, npc_loc_y))

    def draw_player(self):
        player = self.game_data.player_avatar
        play_loc_x = (player.image_x * self.square_size[0]) - self.square_size[0]
        play_loc_y = player.image_y * self.square_size[1] - (self.square_size[1] + player.image_offset_y)
        self.screen.blit(player.spritesheet.get_image(player.current_image_x, player.current_image_y), [play_loc_x, play_loc_y])

    def draw_bg(self, current_room):
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(0, 0, self.resolution[0], self.resolution[1]))
        camera_x = -self.camera[0]
        camera_y = -self.camera[1]
        room = self.game_data.room_data_list[current_room]
        for plot in room.plot_list.keys():
            selected_plot = room.plot_list[plot]
            plot_location_x = room.plot_size_x * (selected_plot.plot_x - 1) * self.square_size[0]
            plot_location_y = room.plot_size_y * (selected_plot.plot_y - 1) * self.square_size[1]
            self.screen.blit(selected_plot.background_map, (camera_x + plot_location_x, camera_y + plot_location_y))

    def draw_all(self, drawables_list, current_room):
        self.draw_bg(current_room)
        for drawable in drawables_list:

            if drawable[0].type == "Player":
                self.draw_player()
            elif drawable[0].type == "Npc":
                self.draw_npc(drawable[0].name)

    def draw_overlay(self, overlay):
        overlay_loc_x = overlay.x
        overlay_loc_y = overlay.y
        self.screen.blit(overlay.image, (overlay_loc_x, overlay_loc_y))

    def draw_menu_cursor(self, menu):
        my_font = pygame.font.Font(self.font, 10)
        item = my_font.render(menu.cursor, True, (0, 0, 0))
        self.screen.blit(item, (menu.x - 12, (menu.y+2 + menu.y_spacing) + (menu.cursor_at * menu.menu_spread)))

    def draw_menu2(self, menu):
        menu_loc_x = []
        menu_loc_y = []
        self.draw_overlay(menu.overlay)
        if menu.menu_type is not "static":
            self.draw_menu_cursor(menu)
        my_font = pygame.font.Font(self.font, menu.font_size)

        if menu.menu_header:
            item = my_font.render(menu.menu_header, True, (0, 0, 0))
            self.screen.blit(item, (menu.x, menu.y))

        for option in range(len(menu.get_menu_items_to_print())):
            print(option)
            item = my_font.render(menu.get_menu_items_to_print()[option], True, (0, 0, 0))
            self.screen.blit(item, (menu.x, menu.y + menu.y_spacing + (option * menu.menu_spread)))

    def draw_menu(self, menu):
        menu_loc_x = []
        menu_loc_y = []
        self.draw_overlay(menu.overlay)

        text_print_list = menu.generate_text_print()

        if menu.menu_type is not "static":
            self.draw_menu_cursor(menu)

        for menu_item in text_print_list:
            my_font = pygame.font.Font(self.font, menu_item.font_size)
            item = my_font.render(menu_item.text, True, (0, 0, 0))
            self.screen.blit(item, (menu_item.x, menu_item.y))


class GameData(object):
    def __init__(self):
        self.player_avatar = None
        self.npc_avatar_list = {}
        self.prop_avatar_list = {}
        self.decoration_data_list = {}

        self.room_data_list = {}
        self.door_data_list = {}
        self.keyboard_manager_data_list = {}
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

    def add_player_avatar(self, player_object):
        self.player_avatar = player_object

    def add_character_avatar(self, character_name, character_object):
        self.npc_avatar_list[character_name] = character_object

    def add_prop_data(self, prop_name, prop_object):
        self.prop_avatar_list[prop_name] = prop_object

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

    def add_overlay_data(self, overlay_name, overlay_object):
        self.overlay_data_list[overlay_name] = overlay_object

    def add_goal_data(self, goal_name, goal_object):
        self.goal_data_list[goal_name] = goal_object

    def add_outfit_data(self, outfit_name, outfit_object):
        self.outfit_data_list[outfit_name] = outfit_object


class InventoryManager(object):
    def __init__(self, gc_input):
        self.gc_input = gc_input  # type: GameController
        self.item_data_list = {}

    def install_item_data(self, item_name, item_object):
        self.item_data_list[item_name] = item_object

    def get_item(self, item, quantity):
        current_inventory = self.gc_input.game_state.current_inventory
        if item.NAME in current_inventory:
            current_inventory[item.NAME]["quantity"] += quantity
        else:
            current_inventory[item.NAME] = {"name": item.NAME, "quantity": quantity}

    def use_item(self, item, quantity_used):
        current_inventory = self.gc_input.game_state.current_inventory
        successes = 0
        for x in range(quantity_used):
            if self.check_if_can_use_item(item, quantity_used):
                successes += 1
                self.item_data_list[item.NAME].item_use()
                current_inventory[item.NAME]["quantity"] -= 1
        if current_inventory[item.NAME]["quantity"] == 0:
            current_inventory.pop(item.NAME)

        if successes == 0:
            self.gc_input.post_notice("Could not use " + item.NAME)
        elif successes > 0:
            self.gc_input.post_notice("used " + str(successes) + " " + item.NAME + "(s)")

    def check_if_can_use_item(self, item, quantity):
        success = True
        if not self.item_data_list[item.NAME].use_requirements():
            success = False
        return success


class MenuManager(object):
    def __init__(self, gc_input):
        self.gc_input = gc_input  # type: GameController
        self.menu_data_list = {}
        self.static_menus = ["game_action_dialogue_menu"]  #
        self.active_menu = []
        self.menu_stack = []
        self.visible_menus = []

    def install_menu_data(self, menu_name, menu_object):
        self.menu_data_list[menu_name] = menu_object

    def add_menu_to_stack(self, menu_to_add):
        self.menu_stack.insert(0, menu_to_add)
        self.add_menu_to_visible(menu_to_add)

    def add_menu_to_visible(self, menu_to_add):
        chosen_menu = self.menu_data_list[menu_to_add]
        self.visible_menus.insert(0, menu_to_add)
        if chosen_menu.menu_type == Types.BASE:
            for menu in self.visible_menus:
                if (menu != menu_to_add) and (chosen_menu.menu_type == Types.BASE):
                    self.visible_menus.remove(menu)

    def deactivate_menu(self, menu_to_deactivate):
        self.menu_stack.remove(menu_to_deactivate)
        if menu_to_deactivate in self.visible_menus:
            self.visible_menus.remove(menu_to_deactivate)

        if len(self.menu_stack) == 0:
            self.gc_input.set_active_keyboard_manager(InGameKeyboardManager.ID)

    def set_menu(self, menu_name):
        selected_menu = self.menu_data_list[menu_name]
        selected_menu.update_menu_items_list()
        self.gc_input.set_active_keyboard_manager(InMenuKeyboardManager.ID)
        selected_menu.gc_input.menu_manager.add_menu_to_stack(menu_name)

    def set_dialogue_menu(self, phrases, speaker_name, friendship_level):
        selected_menu = self.menu_data_list["character_dialogue"]
        selected_menu.update_menu_items_list(phrases, speaker_name, friendship_level)
        self.gc_input.set_active_keyboard_manager(InMenuKeyboardManager.ID)
        selected_menu.gc_input.menu_manager.add_menu_to_stack("character_dialogue")

    def exit_menu(self, menu_name):
        selected_menu = self.menu_data_list[menu_name]
        selected_menu.reset_cursor()
        self.gc_input.menu_manager.deactivate_menu(menu_name)

    def exit_all_menus(self):
        list = []
        for x in self.menu_stack:
            list.append(x)
        for item in list:
            self.exit_menu(item)

    def get_item_quantity(self, item_name):
        return self.gc_input.game_state.current_inventory[item_name]["quantity"]
