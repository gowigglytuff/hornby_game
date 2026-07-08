import copy
from random import choice

import feature_ghost_data_page
from feature_ghost_data_page import PlayerGhost
from menu_ghosts_data_page import StatMenuGhost, SubMenuGhost, SuppliesInventoryMenuGhost, KeyInventoryMenuGhost, ConversationOptionsMenuGhost, GameActionDialogueMenuGhost, ChatMenuGhost, AcquireMenuGhost, GalleryMenuGhost, GiftGivingMenuGhost
from input_manager_controller_page import *
from definitions import Direction, Types, GameSettings
from position_manager_state_page import Room, Door
if TYPE_CHECKING:
    from game_controller import GameController


class GameState(object):
    '''
    :type gv: GameView
    :type gc: GameController
    :type gd: GameData
    :type ms: MenuState
    '''
    def __init__(self, game_view, game_data, game_controller):
        self.gv = game_view
        self.gc = game_controller  # type: GameController
        self.gd = game_data  # type: GameData
        self.ms = MenuState(self)
        self.cc = ConditionChecker(self) # type:ConditionChecker
        self.ghost_classes = {}
        self.type_translator = {"Character": Types.CHARACTER, "Actor": Types.ACTOR, "Prop": Types.PROP, "Deco": Types.DECO}
        self.sub_type_translator = {"None": None, "Character": Types.CHARACTER, "Bird": Types.BIRD, "Tree": Types.TREE, "Prop": Types.PROP, "Deco": Types.DECO}
        self.direction_translations = {"Up": Direction.UP, "Down": Direction.DOWN, "Left": Direction.LEFT, "Right": Direction.RIGHT}

        self.selected_tool = "Pickaxe"
        self.player_ghost = PlayerGhost(self, 1, 3)  # type: PlayerGhost
        self.feature_ghost_list = {}
        # self.deco_ghost_list = {}
        self.current_outfit = "green_shirt"
        self.revert_outfit = "green_shirt"
        self.pickaxe_door_dict = {}

        self.new_game = True
        self.current_room = "Staging_Area"
        self.current_player_elevation = 3

        self.your_coins = 127
        self.bird_count = 1
        self.pigeon_count = 5
        self.total_seeds_found = 26
        self.held_pages = []
        self.accessible_terrains = [0]
        self.using_mermaid_crown = False
        self.using_ghost_eye = False
        self.mermaid_crown_initiation = [0,0]
        self.mermaid_crown_counter = 0
        self.mermaid_crown_limit = 20

        self.ghost_eye_initiation = [0,0]
        self.ghost_eye_initiation_facing = None
        self.ghost_eye_counter = 0
        self.ghost_eye_limit = 20
        self.ghost_eye_husk_name = None

        self.day_of_summer = 12
        self.hour_of_day = 1
        self.minute_of_hour = 0
        self.night_filter_current_alpha = 0
        self.current_inventory_dictionary = {}
        self.current_key_inventory_dictionary = {}
        self.current_animations_to_execute = []

        self.action_queue = {}

    def check_if_actor_busy(self):
        result = False
        return result

    def add_to_action_queue(self, item_name, item_action_object):
        self.action_queue[item_name] = item_action_object

    def remove_from_action_queue(self, item_name):
        item = self.action_queue.pop(item_name)
        item.reset()

    def act_on_action_queue(self):
        remove_list = []
        for actor_ghost_name in self.action_queue.keys():
            actor_ghost = self.get_feature_ghost(actor_ghost_name)
            # is_already_animating = self.gc.check_if_feature_already_animating(actor_ghost_name)
            is_already_animating = actor_ghost.check_if_busy()
            if not is_already_animating:
                action_object = self.action_queue[actor_ghost_name]
                actor_ghost = self.get_feature_ghost(actor_ghost_name)
                current_room = self.get_room(actor_ghost.spawn_room)
                current_move = action_object.movement_list[action_object.current_action]
                print("pow", current_move)
                direction = None
                if current_move[0] == -1:
                    direction = Direction.LEFT
                    action_type = "movement"
                elif current_move[0] == 1:
                    direction = Direction.RIGHT
                    action_type = "movement"
                elif current_move[1] == -1:
                    direction = Direction.UP
                    action_type = "movement"
                elif current_move[1] == 1:
                    direction = Direction.DOWN
                    action_type = "movement"
                else:
                    action_type = "stationary"
                can_move = True
                if action_type == "movement":
                    can_move = self.gc.position_manager.check_if_feature_can_move(actor_ghost, direction, current_room)
                if can_move:
                    self.execute_action_step(actor_ghost_name, action_object)
                    if action_object.check_if_complete():
                        action_object.reset()
                        remove_list.append(actor_ghost_name)
        for actor_ghost_name in remove_list:
                self.action_queue.pop(actor_ghost_name)

    def execute_action_step(self, actor_ghost_name, action_object):
        feature_avatar = self.gv.get_feature_avatar(actor_ghost_name)
        actor_ghost = self.get_feature_ghost(actor_ghost_name)

        current_move = action_object.movement_list[action_object.current_action]
        current_animation_name = action_object.animation_sequence[action_object.current_action]
        action_object.current_action += 1

        feature_avatar.initiate_animation(current_animation_name)
        actor_ghost.initiate_animation(current_animation_name)
        self.gv.animation_manager.add_to_anim_in_progress(actor_ghost.unique_name)

        target_x = actor_ghost.x + current_move[0]
        target_y = actor_ghost.y + current_move[1]

        current_room = self.get_room(actor_ghost.spawn_room)

        self.gc.position_manager.move_ghost(actor_ghost, current_room, current_room, target_x, target_y)


    def add_pickaxe_door_entry(self, entry_name, entry_object):
        self.pickaxe_door_dict[entry_name] = entry_object

    # region FEATURE CONTROL

    def install_element(self, feature_dict):
        ghost_install = self.install_element_ghost(feature_dict)
        self.gv.install_feature_avatar(ghost_install)

        return ghost_install

    def install_element_ghost(self, feature_dict):
        object_class = self.gd.get_feature_class(feature_dict["species"])
        spawn_facing = self.direction_translations[feature_dict["spawn_facing"]]
        unique_name = feature_dict["species"] + "_" + str(GameSettings.get_unique_ID())
        feature_ghost_object = object_class(self, unique_name, feature_dict["function"], feature_dict["spawn_room"], int(feature_dict["spawn_x"]), int(feature_dict["spawn_y"]), spawn_facing, feature_dict["spawn_active"])

        self.add_feature_ghost(unique_name, feature_ghost_object)
        test = self.get_feature_ghost(unique_name)

        return feature_ghost_object

    def create_feature_ghost_class(self, feature_dict):
        def class_init(self, gc_input, unique_name, function, spawn_room, spawn_x, spawn_y, spawn_facing, spawn_active):
            super(newclass, self).__init__(gc_input, unique_name, function, spawn_room, spawn_x, spawn_y, spawn_facing, spawn_active)
            self.gc_input = gc_input
            self.unique_name = unique_name
            self.function = function
            self.spawn_room = spawn_room
            self.spawn_x = spawn_x
            self.spawn_y = spawn_y
            self.spawn_facing = spawn_facing
            self.spawn_active = spawn_active
            self.species = feature_dict["species"]
            self.display_name = feature_dict["display_name"]
            self.figure_size_x = int(feature_dict["figure_size_x"])
            self.figure_size_y = int(feature_dict["figure_size_y"])
            self.base_size_x = int(feature_dict["base_size_x"])
            self.base_size_y = int(feature_dict["base_size_y"])
            if self.feature_subtype == Types.CHARACTER:
                self.base_phrase = feature_dict["base_phrase"]
                self.good_gift_phrase = feature_dict["good_gift_phrase"]
                self.bad_gift_phrase = feature_dict["bad_gift_phrase"]
                self.neutral_gift_phrase = feature_dict["neutral_gift_phrase"]
                self.bird_hint_phrase = feature_dict["bird_hint_phrase"]
                self.good_gift_list = feature_dict["good_gift_list"]
                self.bad_gift_list = feature_dict["bad_gift_list"]

            self.run_initialization()

        newclass = type(feature_dict["species"], (getattr(feature_ghost_data_page, feature_dict["feature_subtype"] + "Ghost"),), {"__init__": class_init})
        self.gd.add_feature_class(feature_dict["species"], newclass)

        return feature_dict

    def add_feature_ghost(self, feature_name, feature_object):
        self.feature_ghost_list[feature_name] = feature_object

    def change_feature_facing(self, name, direction):
        self.change_feature_ghost_facing(name, direction)
        self.gv.change_feature_avatar_facing(name, direction)

    def change_feature_ghost_facing(self, name, direction):
        self.get_feature_ghost(name).facing = direction

    def get_feature_ghost(self, name):
        return self.feature_ghost_list[name]

    def get_feature_display_name(self, feature_unique_nane):
        ghost = self.get_feature_ghost(feature_unique_nane)
        return ghost.display_name

    def get_all_feature_unique_names(self):
        key_list =[]
        for item in self.feature_ghost_list:
            key_list.append(item)
        return key_list

    def check_if_in_accessible_terrains(self, terrain):
        result = False
        if terrain in self.accessible_terrains:
            result = True
        return result

    def update_accessible_terrains(self, add_list, remove_list):
        for item in add_list:
            self.accessible_terrains.append(item)

        for item in remove_list:
            self.accessible_terrains.remove(item)

    def get_feature_locations(self):
        location_list = []

        ghost_list = self.feature_ghost_list

        for item in ghost_list.keys():
            item_ghost = self.get_feature_ghost(item)
            if ghost_list[item].spawn_room == self.current_room and item_ghost.active:
                location_list.append([item, item_ghost.y, item_ghost.x])

        player_location = [self.get_player_ghost().y, self.get_player_ghost().x]

        return player_location, location_list
    # endregion

    # region ROOM STUFF
    def get_current_room(self):
        return self.gv.game_data.room_data_list[self.current_room]

    def get_room(self, room_name):
        return self.gv.game_data.room_data_list[room_name]

    def set_room(self, room_name):
        self.current_room = room_name

    def get_all_features_in_room(self, room_name):
        feature_list = []
        feature_list.append(self.get_player_ghost())
        for item in self.feature_ghost_list.values():
            if item.spawn_room == room_name:
                feature_list.append(item)
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

    def acquire_item(self, item_name, quantity):
        item = self.gc.game_data.item_data_list[item_name]
        current_inventory = self.current_inventory_dictionary
        if item.NAME in current_inventory:
            current_inventory[item.NAME]["quantity"] += quantity
        else:
            current_inventory[item.NAME] = {"name": item.NAME, "quantity": quantity}

    def acquire_key_item(self, key_item_name):
        key_item = self.gc.game_data.key_item_data_list[key_item_name]
        current_inventory = self.current_key_inventory_dictionary
        if key_item.NAME in current_inventory:
            pass
        else:
            current_inventory[key_item.NAME] = {"name": key_item.NAME}

    def get_inventory_items(self, menu_name):
        result = None
        if menu_name == SuppliesInventoryMenuGhost.BASE:
            result = self.current_inventory_dictionary

        elif menu_name == KeyInventoryMenuGhost.BASE:
            result = self.current_key_inventory_dictionary
        return result

    # endregion

    def game_clock_pass_1_minute(self):
        if self.minute_of_hour < 59:
            self.minute_of_hour += 1
        else:
            self.minute_of_hour = 0
            if self.hour_of_day < 23:
                self.hour_of_day += 1
            else:
                self.hour_of_day = 0

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

    def produce_player_coords(self):
        print(self.player_ghost.x, self.player_ghost.y)

    def change_player_facing(self, direction):
        final_facing = direction
        current_facing = self.player_ghost.facing
        if direction == Direction.MATCH:
            final_facing = current_facing
        elif direction == Direction.SWITCH:
            if current_facing == Direction.DOWN:
                final_facing = Direction.UP
            elif current_facing == Direction.UP:
                final_facing = Direction.DOWN
            elif current_facing == Direction.LEFT:
                final_facing = Direction.RIGHT
            elif current_facing == Direction.RIGHT:
                final_facing = Direction.LEFT
        self.change_player_ghost_facing(final_facing)
        self.gv.player_avatar.face_character(final_facing)
    # endregion

class MenuState(object):
    def __init__(self, gs_input):
        self.menu_ghost_data_list = {}
        self.gs = gs_input
        self.gc = self.gs.gc  # type: GameController
        self.menu_data_list = {}
        self.static_menus = [GameActionDialogueMenuGhost.BASE, StatMenuGhost.BASE]
        # self.static_menus = [GameActionDialogueMenuGhost.BASE, SpecialMenuGhost.BASE, StatMenuGhost.BASE]
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
        else:
            print(chosen_menu.BASE)

    def deactivate_menu(self, menu_to_deactivate):
        self.menu_stack.remove(menu_to_deactivate)
        if menu_to_deactivate in self.visible_menus:
            self.visible_menus.remove(menu_to_deactivate)

        if len(self.menu_stack) == 0:
            self.gs.gc.set_active_keyboard_manager(InGameKeyboardManager.ID)
    # endregion

class ConditionChecker(object):
    def __init__(self, gs_input):
        self.gs = gs_input #type: GameState
        self.gc = self.gs.gc  # type: GameController

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
        if not hour_from:
            if minute_to >= self.gs.minute_of_hour >= minute_from:
                result = True
        elif not minute_from:
            if hour_to >= self.gs.hour_of_day >= hour_from:
                result = True
        elif hour_from <= self.gs.hour_of_day <= hour_to:
            if self.gs.hour_of_day == hour_to and minute_to >= self.gs.minute_of_hour >= minute_from:
                result = True
            elif hour_from < self.gs.hour_of_day < hour_to:
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
        self.bird_master_list = ["Meadowlark", "Nuthatch", "Crow", "Tanager", "Starling", "Saw-whet_Owl", "Barred_Owl", "Great_Horned_Owl", 'Nighthawk',
                "Blackbird", "Junko", "Flycatcher", "Wood_Peewee", "Thrush", "Robin", "Goldfinch", "Cormorant", "Seagull", "Coot", "Green_Heron",
                "Kingfisher", "Redwing_Blackbird", "Mallard", "Murrelet", "Harlequin_Duck"]

        self.feature_class_dict = {}
        self.sound_dict = {}
        self.terrain_dict = {0: "soil",
                             1: "water",
                             2: "mud",
                             3: "wall"}
        self.sound_reference_dict = {}
        self.action_dict = {}
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
        self.bird_page_data_list = {}

    def get_terrain_number_or_word(self, number, word):
        word_result = None
        number_result = None
        if number is not None:
            word_result = self.terrain_dict[number]

        if word is not None:
            number_result = next(k for k, v in self.terrain_dict.items() if v == word)

        return number_result, word_result

    def add_feature_class(self, item_name, item_object):
        self.feature_class_dict[item_name] = item_object

    def add_action(self, item_name, item_object):
        self.action_dict[item_name] = item_object

    def get_action(self, item_name):
        return self.feature_class_dict[item_name]

    def get_feature_class(self, item_name):
        return self.feature_class_dict[item_name]

    def add_sound_reference(self, item_name, item_object):
        self.sound_reference_dict[item_name] = item_object

    def get_sound(self, item_name):
        return self.sound_dict[item_name]

    def add_sound_object(self, item_name, item_object):
        self.sound_dict[item_name] = item_object

    def add_key_item_data(self, item_name, item_object):
        self.key_item_data_list[item_name] = item_object

    def add_bird_page_data(self, page_name, page_object):
        self.bird_page_data_list[page_name] = page_object

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


class Action(object):
    def __init__(self, direction):
        self.direction = direction
        self.y_change = 0
        self.x_change = 0

        self.vector = 1
        self.changing_variable = self.x_change

        if self.direction == Direction.UP:
            self.y_change = -1

        elif self.direction == Direction.LEFT:
            self.x_change = -1

        elif self.direction == Direction.DOWN:
            self.y_change = 1

        elif self.direction == Direction.RIGHT:
            self.x_change = 1

    def animate(self):
        pass