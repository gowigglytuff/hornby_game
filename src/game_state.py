import copy
from ghost_page import PlayerGhost
from graphics import BuiltOverlay
from menu_ghosts import StatMenuGhost, SubMenuGhost, UseMenuGhost, SuppliesInventoryMenuGhost, KeyInventoryMenuGhost, ConversationOptionsMenuGhost, GameActionDialogueGhost, SpecialMenuGhost, YesNoMenuGhost
from keyboard_manager_page import *
from avatar_page import PlayerAvatar
from definitions import Direction, GameSettings, Types
from position_manager import Room2, PositionManager


class GameState(object):
    def __init__(self, game_view, game_data, game_controller):
        self.gv = game_view  # type: GameView
        self.gc = game_controller  # type: GameController
        self.gd = game_data  # type: GameData
        self.ms = MenuState(self)  # type: MenuState

        self.selected_tool = "None"
        self.player_ghost = PlayerGhost(self, 1, 1)  # type: PlayerGhost
        self.npc_ghost_list = {}
        self.prop_ghost_list = {}
        self.decoration_ghost_list = {}

        self.new_game = True
        self.current_room = "Basic_Room"

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
            "John": ["overworld", [3, 3, 3]]}
        self.menu_ghost_data_list = {}

    def add_menu_ghost(self, menu_ghost_name, menu_ghost_object):
        self.menu_ghost_data_list[menu_ghost_name] = menu_ghost_object

    def add_player_ghost(self, player_object):
        self.player_ghost = player_object

    def get_player_ghost(self):
        return self.player_ghost

    def get_player_avatar(self):
        return self.gd.player_avatar

    def change_player_facing(self, direction):
        self.player_ghost.facing = direction
        self.gv.game_data.player_avatar.face_character(direction)

    def move_player_ghost(self, direction):
        if direction == Direction.DOWN:
            self.player_ghost.y += 1
        elif direction == Direction.UP:
            self.player_ghost.y -= 1
        elif direction == Direction.LEFT:
            self.player_ghost.x -= 1
        elif direction == Direction.RIGHT:
            self.player_ghost.x += 1

    def move_player_avatar(self, direction):
        if direction == Direction.DOWN:
            self.gv.game_data.player_avatar.initiate_animation("walk_front")
        elif direction == Direction.UP:
            self.gv.game_data.player_avatar.initiate_animation("walk_up")
        elif direction == Direction.LEFT:
            self.gv.game_data.player_avatar.initiate_animation("walk_left")
        elif direction == Direction.RIGHT:
            self.gv.game_data.player_avatar.initiate_animation("walk_right")

    def add_npc_ghost(self, npc_name, npc_object):
        self.npc_ghost_list[npc_name] = npc_object

    def get_npc_ghost(self, name):
        return self.npc_ghost_list[name]

    def get_npc_avatar(self, name):
        return self.gv.game_data.npc_avatar_list[name]

    def change_npc_facing(self, direction, npc_name):
        self.get_npc_ghost(npc_name).facing = direction
        self.get_npc_avatar(npc_name).face_character(direction)

    def get_current_room(self):
        return self.gv.game_data.room_data_list[self.current_room]

    def update_view(self):
        current_room = self.current_room
        drawables_list = self.get_current_drawables()
        self.gv.draw_all(drawables_list, current_room)

        for menu in self.ms.static_menus:
            self.gv.draw_special_menu(menu, self.ms.menu_ghost_data_list[menu + "_ghost"].generate_text_print(), self.ms.menu_display_details[menu]["coordinates"][0], self.ms.menu_display_details[menu]["coordinates"][1])
        for menu in self.ms.visible_menus:
            if self.ms.menu_ghost_data_list[menu + "_ghost"].menu_type == "sub":
                sub_menu = self.ms.menu_ghost_data_list[menu + "_ghost"]
                self.gv.draw_sub_menu(menu, sub_menu.generate_text_print(), self.ms.menu_display_details[menu]["coordinates"][0], self.ms.menu_display_details[menu]["coordinates"][1])
            else:
                self.gv.draw_special_menu(menu, self.ms.menu_ghost_data_list[menu + "_ghost"].generate_text_print(), self.ms.menu_display_details[menu]["coordinates"][0], self.ms.menu_display_details[menu]["coordinates"][1])

    def get_current_drawables(self):
        drawables_list = []

        npc_ghost_list = self.npc_ghost_list

        for npc in npc_ghost_list.keys():
            npc_ghost = self.get_npc_ghost(npc)
            npc_avatar = self.get_npc_avatar(npc)
            if npc_ghost_list[npc].room == self.current_room:
                drawables_list.append([npc_avatar, npc_ghost.y, npc_avatar.drawing_priority])

        drawables_list.append([self.get_player_avatar(), self.get_player_ghost().y, self.get_player_avatar().drawing_priority])

        drawing_order = sorted(drawables_list, key=lambda x: (x[1], x[2]))

        return drawing_order

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

    def get_menu_items(self, menu_name):
        result = None
        if menu_name == "supplies_inventory_menu":
            result = self.current_inventory_dictionary

        elif menu_name == "key_inventory_menu":
            result = self.current_key_inventory_dictionary
        return result

    def acquire_item(self, item, quantity):
        current_inventory = self.current_inventory_dictionary
        if item.NAME in current_inventory:
            current_inventory[item.NAME]["quantity"] += quantity
        else:
            current_inventory[item.NAME] = {"name": item.NAME, "quantity": quantity}

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


class MenuState(object):
    def __init__(self, gs_input):
        self.menu_avatar_data_list = {}
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
        self.menu_display_details = {"start_menu": {"default_width": 32, "default_height": None, "align_x": "right", "align_y": "center", "coordinates": [0, 0]},
                                     "stat_menu": {"default_width": None, "default_height": None, "align_x": "right", "align_y": "top", "coordinates": [0, 0]},
                                     "special_menu": {"default_width": None, "default_height": None, "align_x": "left", "align_y": "top", "coordinates": [0, 0]},
                                     "supplies_inventory_menu": {"default_width": 34, "default_height": None, "align_x": "right", "align_y": "center", "coordinates": [0, 0]},
                                     "key_inventory_menu": {"default_width": 34, "default_height": None, "align_x": "right", "align_y": "center", "coordinates": [0, 0]},
                                     "conversation_options_menu": {"default_width": 34, "default_height": None, "align_x": "right", "align_y": "center", "coordinates": [0, 0]},
                                     "game_action_dialogue_menu": {"default_width": 70, "default_height": 23, "align_x": "right", "align_y": "bottom", "coordinates": [0, 0]},
                                     "use_menu": {"default_width": 20, "default_height": None, "align_x": "right", "align_y": "bottom", "coordinates": [0, 0]},
                                     "yes_no_menu": {"default_width": 20, "default_height": None, "align_x": "right", "align_y": "bottom", "coordinates": [0, 0]},
                                     "sub_menu": {"default_width": 20, "default_height": None, "align_x": "right", "align_y": "bottom", "coordinates": [0, 0]}}

    def set_menu_display_coordinates(self, name):
        for item in self.menu_display_details:
            menu_avatar = self.menu_avatar_data_list[name + "_avatar"]
            x_instruction = self.menu_display_details[name]["align_x"]
            y_instruction = self.menu_display_details[name]["align_y"]
            x = 0
            y = 0

            if x_instruction == "center":
                x = GameSettings.RESOLUTION[0] / 2 - menu_avatar.spritesheet_width / 2
            elif x_instruction == "left":
                x = 0 + GameSettings.RESOLUTION[0] / GameSettings.MENUEDGE
            elif x_instruction == "right":
                x = GameSettings.RESOLUTION[0] - menu_avatar.spritesheet_width - GameSettings.RESOLUTION[0] / GameSettings.MENUEDGE
            else:
                x = x_instruction

            if y_instruction == "center":
                y = GameSettings.RESOLUTION[1] / 2 - menu_avatar.spritesheet_height / 2
            elif y_instruction == "top":
                y = 0 + GameSettings.RESOLUTION[1] / GameSettings.MENUEDGE
            elif y_instruction == "bottom":
                y = GameSettings.RESOLUTION[1] - menu_avatar.spritesheet_height - GameSettings.RESOLUTION[1] / GameSettings.MENUEDGE
            else:
                y = y_instruction

            self.menu_display_details[name]["coordinates"][0] = x
            self.menu_display_details[name]["coordinates"][1] = y

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

    def add_menu_ghost(self, menu_ghost_name, menu_ghost_object):
        self.menu_ghost_data_list[menu_ghost_name] = menu_ghost_object

    def add_menu_avatar(self, menu_avatar_name, menu_avatar_object):
        self.menu_avatar_data_list[menu_avatar_name] = menu_avatar_object

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
        self.room_dictionary = {
            "overworld": Room2("overworld", 5, 5),
            "Basic_Room": Room2("Basic_Room", 5, 5)}
        self.menu_load_list = [SpecialMenuGhost, StatMenuGhost, StartMenuGhost, SubMenuGhost, YesNoMenuGhost, UseMenuGhost, SuppliesInventoryMenuGhost, KeyInventoryMenuGhost, ConversationOptionsMenuGhost, GameActionDialogueGhost]
        self.item_data_list = {}
        self.key_item_data_list = {}

    def install_key_item_data(self, item_name, item_object):
        self.key_item_data_list[item_name] = item_object

    def install_item_data(self, item_name, item_object):
        self.item_data_list[item_name] = item_object

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

    def build_overlay_image(self, name, x_size, y_size, header=None):
        image = BuiltOverlay(name, x_size, y_size, header=header).build_overlay()
        return image
