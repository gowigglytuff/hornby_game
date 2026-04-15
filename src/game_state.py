import copy
from feature_ghost_data_page import PlayerGhost
from graphics import BuiltOverlay
from menu_ghosts_data_page import StatMenuGhost, SubMenuGhost, UseMenuGhost, SuppliesInventoryMenuGhost, KeyInventoryMenuGhost, ConversationOptionsMenuGhost, GameActionDialogueGhost, SpecialMenuGhost, YesNoMenuGhost
from input_manager_controller_page import *
from feature_avatar_view_page import PlayerAvatar
from definitions import Direction, GameSettings, Types
from position_manager_state_page import Room2, PositionManager, NewBasicRoom


class GameState(object):
    def __init__(self, game_view, game_data, game_controller):
        self.gv = game_view  # type: GameView
        self.gc = game_controller  # type: GameController
        self.gd = game_data  # type: GameData
        self.ms = MenuState(self)  # type: MenuState

        self.selected_tool = "None"
        self.player_ghost = PlayerGhost(self, 1, 1)  # type: PlayerGhost
        self.feature_ghost_list = {}
        self.prop_ghost_list = {}
        self.decoration_ghost_list = {}
        self.unique_idea_generator = 10000

        self.new_game = True
        self.current_room = "Ringside"
        self.current_player_elevation = 3

        self.your_coins = 127
        self.your_seeds = 24
        self.total_seeds_found = 26

        self.day_of_summer = 12
        self.hour_of_day = 14
        self.minute_of_hour = 00
        self.night_filter_current_alpha = 0
        self.current_inventory_dictionary = {}
        self.current_key_inventory_dictionary = {}
        self.feature_location_dictionary = {
            "John": ["overworld", [3, 3, 3]],
            "Cowboy": ["New_Basic_Room", [5, 2, 1]]}
        self.menu_ghost_data_list = {}
        self.current_animations_to_execute = []

    def add_menu_ghost(self, menu_ghost_name, menu_ghost_object):
        self.menu_ghost_data_list[menu_ghost_name] = menu_ghost_object

    def add_player_ghost(self, player_object):
        self.player_ghost = player_object

    def add_feature_ghost(self, npc_name, npc_object):
        self.feature_ghost_list[npc_name] = npc_object

    def generate_unique_id(self):
        unique_id = copy.copy(self.unique_idea_generator)
        self.unique_idea_generator += 1
        return unique_id

    def get_all_features_in_room(self, room_name):
        feature_list = []
        feature_list.append(self.get_player_ghost())
        for feature in self.feature_ghost_list.values():
            if feature.room == room_name:
                feature_list.append(feature)
        return feature_listL


    # region GETTERS
    def get_feature_animations_to_execute(self):
        to_execute = copy.copy(self.current_animations_to_execute)
        self.current_animations_to_execute = []
        return to_execute

    def get_player_ghost(self):
        return self.player_ghost

    def get_player_avatar(self):
        return self.gv.player_avatar

    def get_feature_ghost(self, name):
        return self.feature_ghost_list[name]

    def get_npc_avatar(self, name):
        return self.gv.npc_avatar_list[name]

    def get_current_room(self):
        return self.gv.game_data.room_data_list[self.current_room]

    def get_room(self, room_name):
        return self.gv.game_data.room_data_list[room_name]

    def get_item_quantity(self, item_name):
        item_dict = self.get_menu_items("supplies_inventory_menu")
        return item_dict[item_name]["quantity"]

    def get_item_info(self, item_name):
        image = self.gd.item_data_list[item_name].menu_image
        item_size_x = self.gd.item_data_list[item_name].image_size_x
        item_size_y = self.gd.item_data_list[item_name].image_size_y
        return [image, item_size_x, item_size_y]

    def get_key_item_info(self, item_name):
        image = self.gd.key_item_data_list[item_name].menu_image
        item_size_x = self.gd.key_item_data_list[item_name].image_size_x
        item_size_y = self.gd.key_item_data_list[item_name].image_size_y
        return [image, item_size_x, item_size_y]

    def get_list_of_feature_names_in_room(self, room_name):
        names_list =[]
        for item in self.feature_ghost_list.values():
            if item.room == room_name:
                names_list.append(item.name)
        return names_list

    def get_menu_items(self, menu_name):
        result = None
        if menu_name == "supplies_inventory_menu":
            result = self.current_inventory_dictionary

        elif menu_name == "key_inventory_menu":
            result = self.current_key_inventory_dictionary
        return result

    def get_feature_locations(self):
        location_list = []

        npc_ghost_list = self.feature_ghost_list

        for npc in npc_ghost_list.keys():
            npc_ghost = self.get_feature_ghost(npc)
            npc_avatar = self.get_npc_avatar(npc)
            if npc_ghost_list[npc].room == self.current_room:
                location_list.append([npc, npc_ghost.y, npc_ghost.x])

        player_location = [self.get_player_ghost().y, self.get_player_ghost().x]

        return player_location, location_list

    def get_player_location(self):
        player_location = [self.get_player_ghost().x, self.get_player_ghost().y]
        return player_location

    def get_current_player_elevation(self):
        return self.current_player_elevation

    def set_player_elevation(self, new_elevation):
        self.current_player_elevation = new_elevation
    # endregion

    # region PLAYER CONTROL
    def change_player_facing(self, direction):
        self.player_ghost.facing = direction
        self.gv.player_avatar.face_character(direction)

    def move_player_avatar(self, direction):
        if direction == Direction.DOWN:
            self.gv.player_avatar.initiate_animation("walk_front")
        elif direction == Direction.UP:
            self.gv.player_avatar.initiate_animation("walk_up")
        elif direction == Direction.LEFT:
            self.gv.player_avatar.initiate_animation("walk_left")
        elif direction == Direction.RIGHT:
            self.gv.player_avatar.initiate_animation("walk_right")
    # endregion

    # region FEATURE CONTROL
    def change_feature_facing(self, name, direction):
        self.get_feature_ghost(name).facing = direction
        self.get_npc_avatar(name).face_feature(direction)

    def move_feature_avatar(self, name, direction):
        feature_avatar = self.gv.npc_avatar_list[name]
        if direction == Direction.DOWN:
            feature_avatar.initiate_animation("walk_front")
        elif direction == Direction.UP:
            feature_avatar.initiate_animation("walk_up")
        elif direction == Direction.LEFT:
            feature_avatar.initiate_animation("walk_left")
        elif direction == Direction.RIGHT:
            feature_avatar.initiate_animation("walk_right")

    def change_npc_facing(self, direction, npc_name):
        self.get_feature_ghost(npc_name).facing = direction
        self.get_npc_avatar(npc_name).face_feature(direction)

    def perform_animation(self, animator):
        animation_result = (animator.animation_list[animator.current_animation].animate())
        animator.current_image_x = animation_result[2]
        animator.current_image_y = animation_result[3]
        self.gv.camera[0] += animation_result[0]
        self.gv.camera[1] += animation_result[1]
        complete = animation_result[4]
        if complete:
            animator.currently_animating = False
            animator.current_animation = None
    # endregion

    def set_room(self, room_name):
        self.current_room = room_name

    def update_view(self):
        current_room = self.current_room
        drawables_list = self.gv.get_drawables_list(self.get_feature_locations()[0], self.get_feature_locations()[1])
        self.gv.draw_all(drawables_list, current_room)

        for menu in self.ms.static_menus:
            self.gv.draw_special_menu(menu, self.ms.menu_ghost_data_list[menu + "_ghost"].generate_text_print(), self.gv.menu_display_details[menu]["coordinates"][0], self.gv.menu_display_details[menu]["coordinates"][1])
        for menu in self.ms.visible_menus:
            if self.ms.menu_ghost_data_list[menu + "_ghost"].menu_type == "sub":
                sub_menu = self.ms.menu_ghost_data_list[menu + "_ghost"]
                self.gv.draw_sub_menu(menu, sub_menu.generate_text_print(), self.gv.menu_display_details[menu]["coordinates"][0], self.gv.menu_display_details[menu]["coordinates"][1])
            else:
                self.gv.draw_special_menu(menu, self.ms.menu_ghost_data_list[menu + "_ghost"].generate_text_print(), self.gv.menu_display_details[menu]["coordinates"][0], self.gv.menu_display_details[menu]["coordinates"][1])

    def acquire_item(self, item, quantity):
        current_inventory = self.current_inventory_dictionary
        if item.NAME in current_inventory:
            current_inventory[item.NAME]["quantity"] += quantity
        else:
            current_inventory[item.NAME] = {"name": item.NAME, "quantity": quantity}


class MenuState(object):
    def __init__(self, gs_input):
        self.menu_ghost_data_list = {}
        self.gs = gs_input
        self.gc_input = self.gs.gc  # type: GameController
        self.menu_data_list = {}
        self.static_menus = ["game_action_dialogue_menu", "special_menu", "stat_menu"]
        self.active_menu = []
        self.menu_stack = []
        self.visible_menus = []
        self.other_menus = ["special_menu_ghost", "stat_menu"]
        self.start_menu_stack = ["supplies_inventory_menu", "key_inventory_menu"]

    def add_menu_ghost(self, menu_ghost_name, menu_ghost_object):
        self.menu_ghost_data_list[menu_ghost_name] = menu_ghost_object

    def get_menu_ghost(self, menu_name):
        return self.menu_ghost_data_list[menu_name + "_ghost"]

    # region MENU DISPLAY LOGISTICS
    def get_menu_items(self, menu_name):
        result = None
        if menu_name == "supplies_inventory_menu":
            result = self.gs.current_inventory_dictionary

        elif menu_name == "key_inventory_menu":
            result = self.gs.current_key_inventory_dictionary
        return result

    def get_menu_items_list(self, menu_name):
        items_list = self.get_menu_items(menu_name)
        return items_list

    def add_menu_to_stack(self, menu_to_add):
        self.menu_stack.insert(0, menu_to_add)
        self.add_menu_to_visible(menu_to_add)

    def add_menu_to_visible(self, menu_to_add):
        chosen_menu = self.get_menu_ghost(menu_to_add)
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
            self.gs.gc.set_active_keyboard_manager(InGameKeyboardManager.ID)
    # endregion

    # region MENU NAVIGATION
    def set_menu(self, menu_name, details):
        selected_menu = self.get_menu_ghost(menu_name)
        menu_type = selected_menu.menu_type

        if menu_type == "base":
            selected_menu.update_menu_items_list()

        if menu_type == "sub":
            selected_menu.set_master_menu(details["master_menu"])
            self.gs.gv.update_sub_menu_display_details(menu_name, details["master_menu"])

        if menu_type == "dialogue":
            selected_menu.update_menu_items_list(details["phrases"], details["speaker_name"], details["friendship_level"], details["friendship_level"])

        if menu_type == "conversation":
            selected_menu.update_menu_items_list()
            # selected_menu.update_menu_items_list(details["speaker_name"], details["friendship_level"], details["face_image"])

        self.gs.gc.set_active_keyboard_manager(InMenuKeyboardManager.ID)
        selected_menu.gc_input.game_state.ms.add_menu_to_stack(menu_name)

    def next_menu(self, current_menu):
        total_number_menus = len(self.start_menu_stack)
        current_menu_index = self.start_menu_stack.index(current_menu)
        self.exit_menu(self.start_menu_stack[current_menu_index])
        next_menu = self.start_menu_stack[0]
        if current_menu_index != (total_number_menus - 1):
            next_menu = self.start_menu_stack[current_menu_index + 1]
        else:
            pass
        self.set_menu(next_menu, None)

    def previous_menu(self, current_menu):
        total_number_menus = len(self.start_menu_stack)
        current_menu_index = self.start_menu_stack.index(current_menu)
        self.exit_menu(self.start_menu_stack[current_menu_index])
        previous_menu = self.start_menu_stack[current_menu_index-1]
        if current_menu_index == 0:
            previous_menu = self.start_menu_stack[total_number_menus - 1]
        else:
            pass
        self.set_menu(previous_menu, None)

    def exit_menu(self, menu_name):
        selected_menu = self.menu_ghost_data_list[menu_name + "_ghost"]
        selected_menu.reset_cursor()
        self.deactivate_menu(menu_name)

    def exit_all_menus(self):
        list = []
        for x in self.menu_stack:
            list.append(x)
        for item in list:
            self.exit_menu(item)

    # endregion

    # region MENU SELECTION RESULTS
    def start_menu_selection(self, item_selected):
        menu_selection = item_selected
        if menu_selection == "Bag":
            self.exit_menu("start_menu")
            self.set_menu("supplies_inventory_menu", None)

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
            self.exit_all_menus()

        else:
            self.exit_all_menus()

    def post_notice(self, phrase):
        self.menu_ghost_data_list["game_action_dialogue_menu_ghost"].show_dialogue(phrase)
    # endregion


class GameData(object):
    def __init__(self):
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
            "overworld": Room2("overworld", 5, 5),
            "Ringside": Room2("Ringside", 5, 5)}
        self.menu_load_list = [SpecialMenuGhost, StatMenuGhost, StartMenuGhost, SubMenuGhost, YesNoMenuGhost, UseMenuGhost, SuppliesInventoryMenuGhost, KeyInventoryMenuGhost, ConversationOptionsMenuGhost, GameActionDialogueGhost]
        self.item_data_list = {}
        self.key_item_data_list = {}

    def add_key_item_data(self, item_name, item_object):
        self.key_item_data_list[item_name] = item_object

    def add_item_data(self, item_name, item_object):
        self.item_data_list[item_name] = item_object

    def add_spritesheet(self, spritesheet_name, spritesheet_object):
        self.spritesheet_list[spritesheet_name] = spritesheet_object

    def add_animation(self, animation_name, animation_object):
        self.animation_list[animation_name] = animation_object

    def add_keyboard_manager_data(self, keyboard_manager_name, keyboard_manager_object):
        self.keyboard_manager_data_list[keyboard_manager_name] = keyboard_manager_object

    def add_room_data(self, room_name, room_object):
        self.room_data_list[room_name] = room_object

    def add_door_data(self, door_name, door_object):
        self.door_data_list[door_name] = door_object

    def add_temp_item_data(self, item_name, item_object):
        self.temp_item_data_list[item_name] = item_object

    def add_overlay_data(self, overlay_name, overlay_object):
        self.overlay_data_list[overlay_name] = overlay_object

    def add_goal_data(self, goal_name, goal_object):
        self.goal_data_list[goal_name] = goal_object

    def add_outfit_data(self, outfit_name, outfit_object):
        self.outfit_data_list[outfit_name] = outfit_object


class ListMenu(object):  # TODO: Work on this!!
    BASE = "every_menu_base"
    NAME = BASE + "_ghost"

    def __init__(self, gc_input):
        super().__init__()
        self.gc_input = gc_input

        self.menu_header = "<Goodies>"
        self.menu_item_list = ["Poop", "Pee", "Dragon Eggs", "Weasel Toe"]
        self.menu_images_list = []
        self.additional_information = []
        self.menu_type = "base"

        self.cursor = "-"
        self.current_select = 0
        self.name = self.NAME

    def get_menu_items_to_print(self):
        return self.menu_item_list

    def get_current_menu_item(self):
        menu_selection = self.menu_item_list[self.current_select]
        return menu_selection

    def choose_option(self):
        self.do_option()

    def do_option(self):
        menu_selection = self.get_current_menu_item()

    def send_menu_state(self):
        source = self.get_menu_items_to_print().copy()
        current_select = self.current_select
        text_print_list = []

        for item in range(len(source)):
            text_print_list.append(source[item])

        menu_information = {"header": self.menu_header,
                            "text_print_list": text_print_list,
                            "current_select": current_select}

        return menu_information

    def update_menu_items_list(self):
        pass

    def next_menu_item(self):
        if self.current_select == len(self.menu_item_list) - 1:
            self.current_select = 0
        else:
            self.current_select += 1

    def previous_menu_item(self):
        if self.current_select == 0:
            self.current_select = len(self.menu_item_list) - 1
        else:
            self.current_select -= 1

    def reset_current_select(self):
        self.current_select = 0
        self.current_select = 0

    @property
    def size(self):
        return len(self.menu_item_list)