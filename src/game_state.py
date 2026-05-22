import copy
from feature_ghost_data_page import PlayerGhost, NpcGhost, PropGhost, HouseGhost, DecoGhost, BasketGhost, BirdGhost
from menu_ghosts_data_page import StatMenuGhost, SubMenuGhost, UseMenuGhost, SuppliesInventoryMenuGhost, KeyInventoryMenuGhost, ConversationOptionsMenuGhost, GameActionDialogueMenuGhost, SpecialMenuGhost, YesNoMenuGhost, ChatMenuGhost, AcquireMenuGhost
from input_manager_controller_page import *
from definitions import Direction, Types
from position_manager_state_page import Room, Door


class GameState(object):
    '''
    :type gv: GameView
    :type gc: GameController
    :type gd: GameData
    :type ms: MenuState
    '''
    def __init__(self, game_view, game_data, game_controller):
        self.gv = game_view
        self.gc = game_controller
        self.gd = game_data
        self.ms = MenuState(self)
        self.cc = ConditionChecker(self) # type:ConditionChecker
        self.ghost_classes = {"NPC": NpcGhost, "Prop": PropGhost, "House": HouseGhost, "Deco": DecoGhost, "Basket": BasketGhost, "Bird": BirdGhost}
        self.type_translator = {"NPC": Types.NPC, "Prop": Types.PROP, "Deco": Types.DECO, "House": Types.HOUSE, "Basket": Types.BASKET}
        self.sub_type_translator = {"None": None, "Basket": Types.BASKET, "Bird": Types.BIRD}
        self.direction_translations = {"Up": Direction.UP, "Down": Direction.DOWN, "Left": Direction.LEFT, "Right": Direction.RIGHT}

        self.selected_tool = "None"
        self.player_ghost = PlayerGhost(self, 1, 1)  # type: PlayerGhost
        self.feature_ghost_list = {}
        self.prop_ghost_list = {}
        self.deco_ghost_list = {}
        self.map_trigger_list = {}

        self.new_game = True
        self.current_room = "Staging_Area"
        self.current_player_elevation = 3

        self.your_coins = 127
        self.your_seeds = 24
        self.total_seeds_found = 26

        self.day_of_summer = 12
        self.hour_of_day = 1
        self.minute_of_hour = 0
        self.night_filter_current_alpha = 0
        self.current_inventory_dictionary = {}
        self.current_key_inventory_dictionary = {}
        self.current_animations_to_execute = []

    # region TRIGGERS
    def add_map_trigger(self, room_name, triggers_name, trigger_object):
        if room_name in self.map_trigger_list.keys():
            self.map_trigger_list[room_name][triggers_name] = trigger_object
        else:
            self.map_trigger_list[room_name] = {triggers_name: trigger_object}

    def remove_map_trigger(self, room_name, triggers_name):
        self.map_trigger_list[room_name].pop(triggers_name, None)

    #endregion

    # region FEATURE CONTROL
    def add_feature_ghost(self, npc_name, npc_object):
        self.feature_ghost_list[npc_name] = npc_object

    def add_deco_ghost(self, deco_name, deco_object):
        self.deco_ghost_list[deco_name] = deco_object

    def change_feature_ghost_facing(self, name, direction):
        self.get_feature_ghost(name).facing = direction

    def get_feature_animations_to_execute(self):
        to_execute = copy.copy(self.current_animations_to_execute)
        self.current_animations_to_execute = []
        return to_execute

    def get_feature_ghost(self, name):
        return self.feature_ghost_list[name]

    def get_deco_ghost(self, name):
        return self.deco_ghost_list[name]

    def get_all_feature_unique_names(self):
        key_list =[]
        for item in self.feature_ghost_list:
            key_list.append(item)
        return key_list

    def get_all_deco_unique_names(self):
        key_list =[]
        for item in self.deco_ghost_list:
            key_list.append(item)
        return key_list


    def get_feature_locations(self):
        feature_location_list = []
        deco_location_list = []

        npc_ghost_list = self.feature_ghost_list

        for npc in npc_ghost_list.keys():
            npc_ghost = self.get_feature_ghost(npc)
            if npc_ghost_list[npc].room == self.current_room:
                feature_location_list.append([npc, npc_ghost.y, npc_ghost.x])

        deco_ghost_list = self.deco_ghost_list

        for deco in deco_ghost_list.keys():
            deco_ghost = self.get_deco_ghost(deco)
            if deco_ghost_list[deco].room == self.current_room:
                deco_location_list.append([deco, deco_ghost.y, deco_ghost.x])

        player_location = [self.get_player_ghost().y, self.get_player_ghost().x]

        return player_location, feature_location_list, deco_location_list

    # endregion

    # region ROOM STUFF
    def get_current_room(self):
        return self.gv.game_data.room_data_list[self.current_room]

    def get_room(self, room_name):
        return self.gv.game_data.room_data_list[room_name]

    def set_room(self, room_name):
        self.current_room = room_name

    def get_list_of_feature_names_in_room(self, room_name):
        names_list =[]
        for item in self.feature_ghost_list.values():
            if item.room == room_name:
                names_list.append(item.name)
        return names_list

    def get_all_features_in_room(self, room_name):
        feature_list = []
        feature_list.append(self.get_player_ghost())
        for feature in self.feature_ghost_list.values():
            if feature.room == room_name:
                feature_list.append(feature)
        return feature_list
    # endregion

    # region inventory functions
    def get_item_quantity(self, item_name):
        item_dict = self.get_inventory_items("supplies_inventory_menu")
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

    def acquire_item(self, item, quantity):
        current_inventory = self.current_inventory_dictionary
        if item.NAME in current_inventory:
            current_inventory[item.NAME]["quantity"] += quantity
        else:
            current_inventory[item.NAME] = {"name": item.NAME, "quantity": quantity}

    def get_inventory_items(self, menu_name):
        result = None
        if menu_name == SuppliesInventoryMenuGhost.BASE:
            result = self.current_inventory_dictionary

        elif menu_name == KeyInventoryMenuGhost.BASE:
            result = self.current_key_inventory_dictionary
        return result

    # endregion

    # region PLAYER CONTROL
    def add_player_ghost(self, player_object):
        self.player_ghost = player_object

    def change_player_ghost_facing(self, direction):
        self.player_ghost.facing = direction

    def get_player_ghost_location(self):
        player_location = [self.get_player_ghost().x, self.get_player_ghost().y]
        return player_location

    def get_current_player_elevation(self):
        return self.current_player_elevation

    def set_player_elevation(self, new_elevation):
        self.current_player_elevation = new_elevation

    def get_player_ghost(self):
        return self.player_ghost
    # endregion

class MenuState(object):
    def __init__(self, gs_input):
        self.menu_ghost_data_list = {}
        self.gs = gs_input
        self.gc_input = self.gs.gc  # type: GameController
        self.menu_data_list = {}
        self.static_menus = [GameActionDialogueMenuGhost.BASE, SpecialMenuGhost.BASE, StatMenuGhost.BASE]
        self.active_menu = []
        self.menu_stack = []
        self.visible_menus = []
        self.start_menu_stack = [SuppliesInventoryMenuGhost.BASE, KeyInventoryMenuGhost.BASE]


    def add_menu_ghost(self, menu_ghost_name, menu_ghost_object):
        self.menu_ghost_data_list[menu_ghost_name] = menu_ghost_object

    def get_menu_ghost(self, menu_name):
        return self.menu_ghost_data_list[menu_name + "_ghost"]

    # region MENU DISPLAY LOGISTICS
    def get_menu_items(self, menu_name):
        result = None
        if menu_name == SuppliesInventoryMenuGhost.BASE:
            result = self.gs.current_inventory_dictionary

        elif menu_name == KeyInventoryMenuGhost.BASE:
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

        if menu_type == Types.BASE:
            selected_menu.update_menu_items_list(details)

        elif menu_type == Types.SUB:
            print("set it boss")
            selected_menu.set_master_menu(details["master_menu"])
            self.gs.gv.update_sub_menu_display_details(menu_name, details["master_menu"])

        if menu_name == ChatMenuGhost.BASE:
            selected_menu.set_current_phrase(details["phrase"])

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
            self.exit_menu(StartMenuGhost.BASE)
            self.set_menu(SuppliesInventoryMenuGhost.BASE, None)

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

    def conversation_options_menu_selection(self, item_selected):
        menu_selection = item_selected
        current_menu = self.get_menu_ghost(ConversationOptionsMenuGhost.BASE)
        selected_phrase = self.gs.get_feature_ghost(current_menu.speaker_unique_name).phrase

        if menu_selection == "Talk":
            details = {"speaker_name": current_menu.talking_to,
                        "friendship_level": current_menu.friendship,
                        "face_image": current_menu.face_image,
                        "speaker_unique_name": current_menu.speaker_unique_name,
                        "phrase": [selected_phrase]}
            self.exit_menu(ConversationOptionsMenuGhost.BASE)

            self.set_menu(ChatMenuGhost.BASE, details)

        elif menu_selection == "Give Gift":
            pass

        elif menu_selection == "Exit":
            self.exit_all_menus()

        else:
            self.exit_all_menus()

    def chat_menu_selection(self, item_selected):
        self.exit_all_menus()

    def post_notice(self, phrase):
        self.menu_ghost_data_list[GameActionDialogueMenuGhost.NAME].show_dialogue(phrase)
    # endregion


class ConditionChecker(object):
    def __init__(self, gs_input):
        self.gs = gs_input #type: GameState
        self.gc_input = self.gs.gc  # type: GameController

    def check_player_on_tile(self, room_name, coords_list):
        result = False
        pl = self.gs.player_ghost
        if room_name == self.gs.current_room:
            for tile in coords_list:
                if pl.x == tile[0] and pl.y == tile[1]:
                    result = True
        else:
            pass

        return result

    def check_clock_time(self, hour_from, minute_from, hour_to, minute_to):
        result = False
        if self.gs.hour_of_day >= hour_from and self.gs.hour_of_day <= hour_to:
            if (self.gs.hour_of_day == hour_to and self.gs.minute_of_hour <= minute_to and self.gs.minute_of_hour >= minute_from):
                result = True
            elif (self.gs.hour_of_day > hour_from and self.gs.hour_of_day < hour_to):
                result = True
            else:
                pass
        else:
            pass

        return result

    def check_if_word_in_posted_notice(self, source_word):
        result = False
        items = self.gs.ms.menu_ghost_data_list[GameActionDialogueMenuGhost.NAME].menu_item_list
        for phrase in items:
            for match_word in phrase.split():
                if source_word == str(match_word):
                    result = True

        return result


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

    def add_door_data(self, door_type, room_from, room_to, door_from_x, door_from_y, door_to_x, door_to_y):
        if door_type == "Ladder":
            # Door 1
            door1_name = room_from + "_" + str(door_from_x) + "_" + str(door_from_y)
            door1_object = Door(room_from, room_to, door_from_x, door_from_y, door_to_x, door_to_y, Direction.MATCH)
            self.door_data_list[door1_name] = door1_object

            # Door 2
            door2_name = room_to + "_" + str(door_to_x) + "_" + str(door_to_y)
            door2_object = Door(room_to, room_from, door_to_x, door_to_y, door_from_x, door_from_y, Direction.MATCH)
            self.door_data_list[door2_name] = door2_object

        elif door_type == "Passage":
            # Door 1
            door1_name = room_from + "_" + str(door_from_x) + "_" + str(door_from_y)
            door1_object = Door(room_from, room_to, door_from_x, door_from_y, door_to_x, door_to_y-1, Direction.MATCH)
            self.door_data_list[door1_name] = door1_object

            # Door 2
            door2_name = room_to + "_" + str(door_to_x) + "_" + str(door_to_y)
            door2_object = Door(room_to, room_from, door_to_x, door_to_y, door_from_x, door_from_y+1, Direction.MATCH)
            self.door_data_list[door2_name] = door2_object

    def add_temp_item_data(self, item_name, item_object):
        self.temp_item_data_list[item_name] = item_object

    def add_overlay_data(self, overlay_name, overlay_object):
        self.overlay_data_list[overlay_name] = overlay_object

    def add_goal_data(self, goal_name, goal_object):
        self.goal_data_list[goal_name] = goal_object

    def add_outfit_data(self, outfit_name, outfit_object):
        self.outfit_data_list[outfit_name] = outfit_object