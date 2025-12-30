import copy
from ghost_page import PlayerGhost
from graphics import BuiltOverlay
from menu_ghosts import StatMenuGhost, SubMenuGhost, UseMenuGhost, SuppliesInventoryMenuGhost, KeyInventoryMenuGhost, ConversationOptionsMenuGhost, GameActionDialogueGhost, SpecialMenuGhost, YesNoMenuGhost
from keyboard_manager_page import *
from avatar_page import PlayerAvatar
from definitions import Direction, GameSettings, Types
from position_manager import Room2, PositionManager
from game_state import GameState, GameData
from game_view import GameView, MenuDrawer


class Game(object):
    def __init__(self):
        self.game_running = True
        self.game_state = GameState(None, None, None)  # type: GameState
        self.game_data = GameData()  # type: GameData
        self.game_view = GameView(self.game_data, self.game_state, MenuDrawer(self))  # type: GameView
        self.game_controller = GameController(self, self.game_view, self.game_state, self.game_data)  # type: GameController
        self.game_state.gc = self.game_controller
        self.game_state.gv = self.game_view
        self.game_state.gd = self.game_data
        self.game_state.ms.gd = self.game_data
        self.game_events = GameEvents(self.game_controller)
        self.game_input = GameInput(self.game_controller)


class GameEvents(object):
    def __init__(self, game_controller):
        self.gc = game_controller
        self.five_second_timer_id = pygame.USEREVENT + 150
        self.ten_second_timer_id = pygame.USEREVENT + 151
        self.one_second_timer_id = pygame.USEREVENT + 152
        self.fifth_second_timer_id = pygame.USEREVENT + 153
        self.twentieth_second_timer_id = pygame.USEREVENT + 154
        self.timer_list = [self.one_second_timer_id, self.five_second_timer_id, self.ten_second_timer_id, self.fifth_second_timer_id, self.twentieth_second_timer_id]

    def parse_input_event(self, event):
        if event.type == pygame.QUIT:
            self.gc.close_game()

        elif event.type in [pygame.KEYDOWN, pygame.KEYUP]:
            self.gc.active_keyboard_manager.parse_key_input(event.type, event.key)

        elif event.type in self.timer_list:
            if event.type == self.one_second_timer_id:
                pass
            if event.type == self.fifth_second_timer_id:
                pass
            if event.type == self.twentieth_second_timer_id:
                if not self.gc.game_view.game_data.player_avatar.currently_animating:
                    direction = []
                    if self.gc.key_down_queue:
                        if self.gc.key_down_queue == pygame.K_DOWN:
                            direction = Direction.DOWN
                        elif self.gc.key_down_queue == pygame.K_UP:
                            direction = Direction.UP
                        elif self.gc.key_down_queue == pygame.K_RIGHT:
                            direction = Direction.RIGHT
                        elif self.gc.key_down_queue == pygame.K_LEFT:
                            direction = Direction.LEFT

                        self.gc.game_state.change_player_facing(direction)
                        if self.gc.position_manager.check_if_player_can_move(direction, self.gc.game_state.player_ghost, self.gc.game_view.game_data.room_data_list[self.gc.game_state.current_room]):
                            self.gc.game_state.move_player_avatar(direction)
                            self.gc.game_state.move_player_ghost(direction)

                if self.gc.game_view.game_data.player_avatar.currently_animating:
                    self.gc.game_state.perform_animation(self.gc.game_view.game_data.player_avatar)

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


class GameInput(object):
    def __init__(self, game_controller):
        self.gc = game_controller


class GameController(object):
    def __init__(self, game, game_view, game_state, game_data):
        self.game = game  # type: Game
        self.game = game  # type: Game
        self.game_view = game_view  # type: GameView
        self.game_state = game_state  # type: GameState
        self.game_data = game_data # type: GameData

        self.active_keyboard_manager = None
        self.key_down_queue = []
        self.position_manager = PositionManager(self)  # type:PositionManager
        self.menu_manager = MenuManager(self)  # type:MenuManager
        self.inventory_manager = InventoryManager(self)  # type:InventoryManager

    def set_active_keyboard_manager(self, active_manager_id):
        self.active_keyboard_manager = self.game_view.game_data.keyboard_manager_data_list[active_manager_id]

    def close_game(self):
        self.game.game_running = False

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
        self.game_state.change_npc_facing(direction_to_turn, npc_talking_to)
        self.menu_manager.post_notice("You talked to " + npc_talking_to_ghost.name)
        # self.menu_manager.set_conversation_menu(npc_talking_to_ghost.name, 11, npc_talking_to_avatar.face_image)
        # self.menu_manager.set_dialogue_menu("Something strange is going on around here, have you heard about the children disapearing? Their parents couldn't even remember their names...", npc_talking_to_ghost.name, 11, npc_talking_to_avatar.face_image)

    def player_interact(self):
        interact_tile = self.position_manager.check_adjacent_tile(self.game_state.get_player_ghost().facing, self.game_state.get_player_ghost(), self.game_state.get_current_room())
        full = interact_tile.is_full
        fill_type = interact_tile.filling_type
        fill_object = interact_tile.object_filling
        if fill_type == Types.NPC:
            self.talk_to_npc(fill_object, self.game_state.get_player_ghost().facing)
        if fill_type == Types.PROP:
            pass

    def get_stat_items(self):
        hour = self.game_state.hour_of_day
        minute = self.game_state.minute_of_hour

        stat_dict = {"seeds": str(self.game_state.your_seeds),
                     "Coins": str(self.game_state.your_coins),
                     "time": str(hour) + ":" + str(minute) + "0",
                     "day": str(self.game_state.day_of_summer),
                     "selected_tool": str(self.game_state.selected_tool)}

        return stat_dict


class InventoryManager(object):
    def __init__(self, gc_input):
        self.gc_input = gc_input  # type: GameController

    def get_item(self, item, quantity):
        current_inventory = self.gc_input.game_state.ms.get_menu_items_list("supplies_inventory_menu")
        if item.NAME in current_inventory:
            current_inventory[item.NAME]["quantity"] += quantity
        else:
            current_inventory[item.NAME] = {"name": item.NAME, "quantity": quantity}

    def use_item(self, item, quantity_used):
        current_inventory = self.gc_input.game_state.ms.get_menu_items_list("supplies_inventory_menu")
        successes = 0
        for x in range(quantity_used):
            if self.check_if_can_use_item(item, quantity_used):
                successes += 1
                self.gc_input.game_state.gd.item_data_list[item.NAME].item_use()
                current_inventory[item.NAME]["quantity"] -= 1
        if current_inventory[item.NAME]["quantity"] == 0:
            current_inventory.pop(item.NAME)

        if successes == 0:
            self.gc_input.menu_manager.post_notice("Could not use " + item.NAME)
        elif successes > 0:
            self.gc_input.menu_manager.post_notice("used " + str(successes) + " " + item.NAME + "(s)")

    def check_if_can_use_item(self, item, quantity):
        success = True
        if quantity > self.gc_input.game_state.get_item_quantity(item.name):
            success = False
        if not self.gc_input.game_state.gd.item_data_list[item.NAME].use_requirements():
            success = False
        return success

    def check_if_can_use_key_item(self, item):
        success = True

        if not self.gc_input.game_state.gd.key_item_data_list[item.NAME].use_requirements():
            success = False
        return success

    def get_key_item(self, item):
        current_key_inventory = self.gc_input.game_state.ms.get_menu_items_list("key_inventory_menu")
        if item.NAME in current_key_inventory:
            pass
        else:
            current_key_inventory[item.NAME] = {"name": item.NAME}

    def use_key_item(self, item):
        current_key_inventory = self.gc_input.game_state.ms.get_menu_items_list("key_inventory_menu")
        successes = 0
        if self.check_if_can_use_key_item(item):
            self.gc_input.game_state.gd.key_item_data_list[item.NAME].item_use()
            successes += 1

        if successes == 0:
            self.gc_input.menu_manager.post_notice("Could not use " + item.NAME)
        elif successes > 0:
            self.gc_input.menu_manager.post_notice("used " + item.NAME)


class MenuManager(object):
    def __init__(self, gc_input):
        self.gc_input = gc_input  # type: GameController

    def deactivate_menu(self, menu_to_deactivate):
        self.gc_input.game_state.ms.menu_stack.remove(menu_to_deactivate)
        if menu_to_deactivate in self.gc_input.game_state.ms.visible_menus:
            self.gc_input.game_state.ms.visible_menus.remove(menu_to_deactivate)

        if len(self.gc_input.game_state.ms.menu_stack) == 0:
            self.gc_input.set_active_keyboard_manager(InGameKeyboardManager.ID)

    def set_menu(self, menu_name):
        selected_menu = self.gc_input.game_state.ms.menu_ghost_data_list[menu_name + "_ghost"]
        selected_menu.update_menu_items_list()
        self.gc_input.set_active_keyboard_manager(InMenuKeyboardManager.ID)
        selected_menu.gc_input.game_state.ms.add_menu_to_stack(menu_name)

    def set_sub_menu(self, menu_name, master_menu):
        selected_menu = self.gc_input.game_state.ms.menu_ghost_data_list[menu_name + "_ghost"]
        selected_menu.set_master_menu(master_menu)
        selected_menu_avatar = self.gc_input.game_state.ms.menu_avatar_data_list[menu_name + "_avatar"]
        self.gc_input.game_state.ms.menu_display_details[menu_name]["coordinates"][0] = self.gc_input.game_state.ms.menu_display_details[master_menu]["coordinates"][0] - selected_menu_avatar.spritesheet_width - 5
        self.gc_input.game_state.ms.menu_display_details[menu_name]["coordinates"][1] = self.gc_input.game_state.ms.menu_display_details[master_menu]["coordinates"][1]
        self.gc_input.set_active_keyboard_manager(InMenuKeyboardManager.ID)
        selected_menu.gc_input.game_state.ms.add_menu_to_stack(menu_name)

    def set_dialogue_menu(self, phrases, speaker_name, friendship_level, face_image):
        selected_menu = self.gc_input.game_state.ms.menu_data_list["character_dialogue"]
        selected_menu.update_menu_items_list(phrases, speaker_name, friendship_level, face_image)
        self.gc_input.set_active_keyboard_manager(InMenuKeyboardManager.ID)
        selected_menu.gc_input.game_state.ms.add_menu_to_stack("character_dialogue")

    def set_conversation_menu(self, speaker_name, friendship_level, face_image):
        selected_menu = self.gc_input.game_state.ms.menu_data_list["conversation_options_menu"]
        selected_menu.update_menu_items_list(speaker_name, friendship_level, face_image)
        self.gc_input.set_active_keyboard_manager(InMenuKeyboardManager.ID)
        selected_menu.gc_input.game_state.ms.add_menu_to_stack("conversation_options_menu")

    def exit_menu(self, menu_name):
        selected_menu = self.gc_input.game_state.ms.menu_ghost_data_list[menu_name + "_ghost"]
        selected_menu.reset_cursor()
        self.gc_input.menu_manager.deactivate_menu(menu_name)

    def exit_all_menus(self):
        list = []
        for x in self.gc_input.game_state.ms.menu_stack:
            list.append(x)
        for item in list:
            self.exit_menu(item)

    def next_menu(self, current_menu):
        total_number_menus = len(self.gc_input.game_state.ms.start_menu_stack)
        print(total_number_menus)
        current_menu_index = self.gc_input.game_state.ms.start_menu_stack.index(current_menu)
        self.exit_menu(self.gc_input.game_state.ms.start_menu_stack[current_menu_index])
        next_menu = self.gc_input.game_state.ms.start_menu_stack[0]
        if current_menu_index != (total_number_menus - 1):
            next_menu = self.gc_input.game_state.ms.start_menu_stack[current_menu_index + 1]
        else:
            pass
        self.set_menu(next_menu)

    def previous_menu(self, current_menu):
        total_number_menus = len(self.gc_input.game_state.ms.start_menu_stack)
        current_menu_index = self.gc_input.game_state.ms.start_menu_stack.index(current_menu)
        self.exit_menu(self.gc_input.game_state.ms.start_menu_stack[current_menu_index])
        previous_menu = self.gc_input.game_state.ms.start_menu_stack[current_menu_index-1]
        if current_menu_index == 0:
            previous_menu = self.gc_input.game_state.ms.start_menu_stack[total_number_menus - 1]
        else:
            pass
        self.set_menu(previous_menu)

    def start_menu_selection(self, item_selected):
        menu_selection = item_selected
        if menu_selection == "Bag":
            self.exit_menu("start_menu")
            self.set_menu("supplies_inventory_menu")

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

    def post_notice(self, phrase):
        self.gc_input.game_state.ms.menu_ghost_data_list["game_action_dialogue_menu_ghost"].show_dialogue(phrase)

