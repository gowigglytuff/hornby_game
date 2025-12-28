import copy
from enum import Enum

import pygame

from ghost_page import PlayerGhost
from graphics import BuiltOverlay
from player import Player_Avatar
from tile_map import TileMap, TileSet
from room_page import Room
from keyboard_manager_page import *
from avatar_page import PlayerAvatar
from definitions import Direction, GameSettings, Types
from position_manager import Room2, PositionManager


class Game(object):
    def __init__(self):
        self.game_running = True
        self.game_state = GameState()  # type: GameState
        self.game_data = GameData()  # type: GameData
        self.game_view = GameView(self.game_data, MenuDrawer(self))  # type: GameView

        self.game_controller = GameController(self, self.game_view, self.game_state)  # type: GameController


class GameController(object):
    def __init__(self, game, game_view, game_state):
        self.game = game  # type: Game
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
        pygame.time.set_timer(twentieth_second_timer, 2)

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

    def attempt_move_object(self, object_name, movement_direction):
        feature_loc_info = self.position_manager.get_feature_location(object_name)
        feature_room = feature_loc_info[0]
        current_cube_location = feature_loc_info[1]
        target_cube_location = copy.deepcopy(current_cube_location)

        if movement_direction == Direction.DOWN:
            target_cube_location[1] += 1
        elif movement_direction == Direction.UP:
            target_cube_location[1] -= 1
        elif movement_direction == Direction.LEFT:
            target_cube_location[0] -= 1
        elif movement_direction == Direction.RIGHT:
            target_cube_location[0] += 1

        target_location_fill_status = self.position_manager.check_location_full(feature_room, target_cube_location)

        if target_location_fill_status:
            # print("this location is full")
            pass
        else:
            # print("moving!")

            self.position_manager.update_feature_dictionary(object_name, target_cube_location)
            self.position_manager.update_locations("Room", object_name, target_cube_location, current_cube_location)
        # print(current_cube_location)
        # print(target_cube_location)

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

        for menu in self.menu_manager.static_menus:
            self.game_view.draw_menu(self.menu_manager.menu_data_list[menu])
        for menu in self.menu_manager.visible_menus:
            self.game_view.draw_special_menu(menu, self.menu_manager.menu_ghost_data_list[menu + "_ghost"].generate_text_print())

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
        self.menu_manager.set_conversation_menu(npc_talking_to_ghost.name, 11, npc_talking_to_avatar.face_image)
        # self.menu_manager.set_dialogue_menu("Something strange is going on around here, have you heard about the children disapearing? Their parents couldn't even remember their names...", npc_talking_to_ghost.name, 11, npc_talking_to_avatar.face_image)

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

    def build_overlay_image(self, name, x_size, y_size, header=None):
        image = BuiltOverlay(name, x_size, y_size, header=header).build_overlay()
        return image

    def get_item_info(self, item_name):
        image = self.inventory_manager.item_data_list[item_name].menu_image
        item_size_x = self.inventory_manager.item_data_list[item_name].image_size_x
        item_size_y = self.inventory_manager.item_data_list[item_name].image_size_y
        return [image, item_size_x, item_size_y]

    def get_key_item_info(self, item_name):
        image = self.inventory_manager.key_item_data_list[item_name].menu_image
        item_size_x = self.inventory_manager.key_item_data_list[item_name].image_size_x
        item_size_y = self.inventory_manager.key_item_data_list[item_name].image_size_y
        return [image, item_size_x, item_size_y]

    def get_stat_items(self):
        hour = self.game_state.hour_of_day
        minute = self.game_state.minute_of_hour

        stat_dict = {"seeds": str(self.game_state.your_seeds),
                     "Coins": str(self.game_state.your_coins),
                     "time": str(hour) + ":" + str(minute) + "0",
                     "day": str(self.game_state.day_of_summer),
                     "selected_tool": str(self.game_state.selected_tool)}

        return stat_dict


class GameState(object):
    def __init__(self):
        self.selected_tool = "None"
        self.player_ghost = PlayerGhost(self, 1, 1)  # type: PlayerGhost
        self.npc_ghost_list = {}
        self.prop_ghost_list = {}
        self.decoration_ghost_list = {}

        self.new_game = True
        self.current_room = "Basic_Room"
        self.menu_items_dict = {"inventory_menu":{}, "key_inventory_menu":{}}
        self.current_inventory = {}
        self.current_key_inventory = {}

        self.your_coins = 127
        self.your_seeds = 24
        self.total_seeds_found = 26

        self.day_of_summer = 12
        self.hour_of_day = 14
        self.minute_of_hour = 00
        self.night_filter_current_alpha = 0
        self.feature_location_dictionary = {
            "John": ["overworld", [3, 3, 3]]
        }

    def add_player_ghost(self, player_object):
        self.player_ghost = player_object

    def add_npc_ghost(self, npc_name, npc_object):
        self.npc_ghost_list[npc_name] = npc_object


class GameView(object):
    def __init__(self, game_data, menu_drawer):
        self.game_data = game_data  # type: GameData
        self.menu_drawer = menu_drawer  # type: MenuDrawer
        self.clock = pygame.time.Clock()
        self.resolution = GameSettings.RESOLUTION
        self.FPS = 72
        self.square_size = [GameSettings.TILESIZE, GameSettings.TILESIZE]
        self.base_locator_x = ((self.resolution[0] - self.square_size[0]) / self.square_size[0]) / 2 + 1
        self.base_locator_y = ((self.resolution[1] - self.square_size[1]) / self.square_size[1]) / 2 + 1

        self.camera = [0, 0]
        self.screen = pygame.display.set_mode(self.resolution)
        self.font_file = "assets/fonts/PressStart.ttf"

        self.font_medium = pygame.font.Font(self.font_file, GameSettings.FONT_SIZE)


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

    def draw_menu(self, menu):
        overlay = self.game_data.overlay_data_list[menu.name + "_overlay"]
        text_print_list = menu.generate_text_print()
        img_print_list = menu.generate_image_print()
        menu_tester = self.compile_menu(text_print_list, img_print_list, overlay)
        self.screen.blit(menu_tester, (menu.x, menu.y))
        # print(menu.name)

    def draw_special_menu(self, menu_name, menu_info):

        menu_avatar = self.game_data.menu_avatar_data_list[menu_name + "_avatar"]
        menu_info = menu_info
        final_menu_text = menu_avatar.get_menu_text_drawing_instructions(menu_info)

        full_menu = self.compile_special_menu(final_menu_text, None, menu_avatar.overlay_image)
        self.screen.blit(full_menu, (menu_avatar.x, menu_avatar.y))

    def compile_special_menu(self, text_print_list, image_print_list, overlay):
        final_image = pygame.Surface((overlay.get_width(), overlay.get_height()))
        final_image.blit(overlay, [0, 0])
        # print("using compile")

        for item in text_print_list:
            my_font = pygame.font.Font(self.font_file, GameSettings.FONT_SIZE)
            item_text = my_font.render(item.text, True, (0, 0, 0))
            final_image.blit(item_text, [item.x, item.y])

        if image_print_list:
            for item in image_print_list:
                image = item.image
                final_image.blit(image, [item.x, item.y])

        return final_image

    def compile_menu(self, text_print_list, image_print_list, overlay):
        final_image = pygame.Surface((overlay.image.get_width(), overlay.image.get_height()))
        final_image.blit(overlay.image, [0, 0])
        for item in text_print_list:
            my_font = pygame.font.Font(self.font_file, GameSettings.FONT_SIZE)
            item_text = my_font.render(item.text, True, (0, 0, 0))
            final_image.blit(item_text, [item.x, item.y])

        if image_print_list:
            for item in image_print_list:
                image = item.image
                final_image.blit(image, [item.x, item.y])

        return final_image


class GameData(object):
    def __init__(self):
        self.menu_avatar_data_list = {}
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
        self.room_dictionary = {
            "overworld": Room2("overworld", 5, 5)
        }

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

    def add_menu_avatar(self, menu_avatar_name, menu_avatar_object):
        self.menu_avatar_data_list[menu_avatar_name] = menu_avatar_object


class InventoryManager(object):
    def __init__(self, gc_input):
        self.gc_input = gc_input  # type: GameController
        self.item_data_list = {}
        self.key_item_data_list = {}

    def install_key_item_data(self, item_name, item_object):
        self.key_item_data_list[item_name] = item_object

    def install_item_data(self, item_name, item_object):
        self.item_data_list[item_name] = item_object

    def get_item(self, item, quantity):
        current_inventory = self.gc_input.game_state.menu_items_dict["inventory_menu"]
        if item.NAME in current_inventory:
            current_inventory[item.NAME]["quantity"] += quantity
        else:
            current_inventory[item.NAME] = {"name": item.NAME, "quantity": quantity}

    def use_item(self, item, quantity_used):
        current_inventory = self.gc_input.game_state.menu_items_dict["inventory_menu"]
        successes = 0
        for x in range(quantity_used):
            # print(quantity_used)
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
        if quantity > self.gc_input.menu_manager.get_item_quantity(item.name):
            success = False
        if not self.item_data_list[item.NAME].use_requirements():
            success = False
        return success

    def check_if_can_use_key_item(self, item):
        success = True

        if not self.key_item_data_list[item.NAME].use_requirements():
            success = False
        return success

    def get_key_item(self, item):
        current_key_inventory = self.gc_input.game_state.current_key_inventory
        if item.NAME in current_key_inventory:
            pass
        else:
            current_key_inventory[item.NAME] = {"name": item.NAME}

    def use_key_item(self, item):
        current_key_inventory = self.gc_input.game_state.current_inventory
        successes = 0
        if self.check_if_can_use_key_item(item):
            self.key_item_data_list[item.NAME].item_use()
            successes += 1

        if successes == 0:
            self.gc_input.post_notice("Could not use " + item.NAME)
        elif successes > 0:
            self.gc_input.post_notice("used " + item.NAME)


class MenuManager(object):
    def __init__(self, gc_input):
        self.menu_ghost_data_list = {}
        self.gc_input = gc_input  # type: GameController
        self.menu_data_list = {}
        self.static_menus = ["game_action_dialogue_menu"]
        self.active_menu = []
        self.menu_stack = []
        self.visible_menus = ["special_menu", "stat_menu"]
        self.other_menus = ["special_menu_ghost", "stat_menu"]
        self.start_menu_stack = ["inventory_menu", "key_inventory_menu"]

    def get_menu_items_list(self, menu_name):
        items_list = self.gc_input.game_state.menu_items_dict[menu_name]

    def install_menu_data(self, menu_name, menu_object):
        self.menu_data_list[menu_name] = menu_object

    def add_menu_ghost(self, menu_ghost_name, menu_ghost_object):
        self.menu_ghost_data_list[menu_ghost_name] = menu_ghost_object

    def add_menu_to_stack(self, menu_to_add):
        self.menu_stack.insert(0, menu_to_add)
        self.add_menu_to_visible(menu_to_add)

    def add_menu_to_visible(self, menu_to_add):
        chosen_menu = self.menu_ghost_data_list[menu_to_add + "_ghost"]
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
        selected_menu = self.menu_ghost_data_list[menu_name + "_ghost"]
        selected_menu.update_menu_items_list()
        self.gc_input.set_active_keyboard_manager(InMenuKeyboardManager.ID)
        selected_menu.gc_input.menu_manager.add_menu_to_stack(menu_name)

    def set_sub_menu(self, menu_name, master_menu):
        selected_menu = self.menu_data_list[menu_name]
        selected_menu.update_menu_items_list(master_menu)
        self.gc_input.set_active_keyboard_manager(InMenuKeyboardManager.ID)
        selected_menu.gc_input.menu_manager.add_menu_to_stack(menu_name)

    def set_dialogue_menu(self, phrases, speaker_name, friendship_level, face_image):
        selected_menu = self.menu_data_list["character_dialogue"]
        selected_menu.update_menu_items_list(phrases, speaker_name, friendship_level, face_image)
        self.gc_input.set_active_keyboard_manager(InMenuKeyboardManager.ID)
        selected_menu.gc_input.menu_manager.add_menu_to_stack("character_dialogue")

    def set_conversation_menu(self, speaker_name, friendship_level, face_image):
        selected_menu = self.menu_data_list["conversation_options_menu"]
        selected_menu.update_menu_items_list(speaker_name, friendship_level, face_image)
        self.gc_input.set_active_keyboard_manager(InMenuKeyboardManager.ID)
        selected_menu.gc_input.menu_manager.add_menu_to_stack("conversation_options_menu")

    def exit_menu(self, menu_name):
        selected_menu = self.menu_ghost_data_list[menu_name + "_ghost"]
        selected_menu.reset_cursor()
        self.gc_input.menu_manager.deactivate_menu(menu_name)

    def exit_all_menus(self):
        list = []
        for x in self.menu_stack:
            list.append(x)
        for item in list:
            self.exit_menu(item)

    def get_item_quantity(self, item_name):
        # for item in self.gc_input.game_state.current_inventory:
        #     print(item)
        return self.gc_input.game_state.current_inventory[item_name]["quantity"]

    def next_menu(self, current_menu):
        total_number_menus = len(self.start_menu_stack)
        print(total_number_menus)
        current_menu_index = self.start_menu_stack.index(current_menu)
        self.exit_menu(self.start_menu_stack[current_menu_index])
        next_menu = self.start_menu_stack[current_menu_index + 1]
        if current_menu_index == (total_number_menus - 1):
            next_menu = self.start_menu_stack[0]
        else:
            pass
        self.set_menu(next_menu)

    def previous_menu(self, current_menu):
        total_number_menus = len(self.start_menu_stack)
        current_menu_index = self.start_menu_stack.index(current_menu)
        self.exit_menu(self.start_menu_stack[current_menu_index])
        previous_menu = self.start_menu_stack[current_menu_index-1]
        if current_menu_index == 0:
            previous_menu = self.start_menu_stack[total_number_menus - 1]
        else:
            pass
        self.set_menu(previous_menu)

    def start_menu_selection(self, item_selected):
        menu_selection = item_selected
        if menu_selection == "Bag":
            self.exit_menu("start_menu")
            self.set_menu("inventory_menu")

        elif menu_selection == "Key Items":
            pass

        elif menu_selection == "Chore List":
            pass

        elif menu_selection == "Profile":
            pass

        elif menu_selection == "Map":
            pass

        elif menu_selection == "Options":
            pass

        elif menu_selection == "Vibes":
            pass

        elif menu_selection == "Outfits":
            pass

        elif menu_selection == "Save":
            pass

        elif menu_selection == "Exit":
            self.gc_input.menu_manager.exit_all_menus()

        else:
            self.gc_input.menu_manager.exit_all_menus()


class MenuDrawer(object):
    def __init__(self, gv_input):
        self.font_size = GameSettings.FONT_SIZE
        print("using this")
