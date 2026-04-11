import copy
import csv
import os

from feature_ghost_data_page import NpcGhost, TreeGhost, OldgodGhost
from input_manager_controller_page import *
from definitions import Direction, Types
from position_manager_state_page import Room2, PositionManager
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


class GameEvents(object):
    def __init__(self, game_controller):
        self.gc = game_controller  # type: GameController
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
                # self.gc.attempt_move_object("Cowboy", Direction.DOWN)
                # cowboy = self.gc.game_state.npc_ghost_list["Cowboy"]
                # self.gc.position_manager.move_feature(cowboy, self.gc.game_data.room_data_list[self.gc.game_state.current_room], Direction.DOWN)
                pass
            if event.type == self.fifth_second_timer_id:
                pass
            if event.type == self.twentieth_second_timer_id:
                self.gc.act_on_key_down_cue()
                self.gc.ask_animator_to_animate()

    def initiate_timers(self):
        twentieth_second_timer = self.twentieth_second_timer_id
        pygame.time.set_timer(twentieth_second_timer, 4)

        fifth_second_timer = self.fifth_second_timer_id
        pygame.time.set_timer(fifth_second_timer, 20)

        one_second_timer = self.one_second_timer_id
        pygame.time.set_timer(one_second_timer, 1000)

        five_second_timer = self.five_second_timer_id
        pygame.time.set_timer(five_second_timer, 5000)

        ten_second_timer = self.ten_second_timer_id
        pygame.time.set_timer(ten_second_timer, 10000)


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
        self.feature_animations_in_progress = []

    # region GAME CONTROLS
    def set_active_keyboard_manager(self, active_manager_id):
        self.active_keyboard_manager = self.game_view.game_data.keyboard_manager_data_list[active_manager_id]

    def close_game(self):
        self.game.game_running = False

    def load_feature(self, name, ghost_object, avatar_object):
        self.game_state.add_feature_ghost(name, ghost_object)
        self.game_view.add_feature_avatar(name, avatar_object)
    # endregion

    # region FEATURE MOVEMENT
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
            pass
        else:
            self.position_manager.update_feature_dictionary(object_name, target_cube_location)
            self.position_manager.update_locations(feature_room, object_name, current_cube_location, target_cube_location)


    def check_if_feature_already_animating(self, name):
        avatar = self.game_view.npc_avatar_list[name]
        return avatar.currently_animating

    def initiate_feature_movement(self, name, direction):
        self.game_state.change_feature_facing(name, direction)
        if self.position_manager.check_if_feature_can_move(self.game_state.get_feature_ghost(name), direction, self.game_view.game_data.room_data_list[self.game_state.current_room]):
            self.game_state.move_feature_avatar(name, direction)
            self.position_manager.move_feature_ghost(name, direction)

    def reset_feature_to_spawn(self, feature):
        chosen_feature = self.game_state.get_feature_ghost(feature)
        chosen_feature.reset_to_spawn()
    # endregion

    # region PLAYER ACTIONS
    def player_interact(self):
        full = self.position_manager.check_if_adjacent_tiles_full(self.game_state.get_player_ghost(), self.game_state.get_player_ghost().facing, self.game_state.get_current_room())
        if full:
            cube = self.position_manager.get_adjacent_tile(self.game_state.get_player_ghost(), self.game_state.get_player_ghost().facing, self.game_state.get_current_room())
            feature = self.game_state.get_feature_ghost(cube.object_filling)
            if feature.type == Types.NPC:
                self.talk_to_npc(cube.object_filling, self.game_state.get_player_ghost().facing)
            else:
                pass

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

        npc_talking_to_ghost = self.game_state.feature_ghost_list[npc_talking_to]
        npc_talking_to_avatar = self.game_view.npc_avatar_list[npc_talking_to]
        self.game_state.change_npc_facing(direction_to_turn, npc_talking_to)
        self.game_state.ms.post_notice("You talked to " + npc_talking_to_ghost.name)
        # self.menu_manager.set_conversation_menu(npc_talking_to_ghost.name, 11, npc_talking_to_avatar.face_image)
        # self.menu_manager.set_dialogue_menu("Something strange is going on around here, have you heard about the children disapearing? Their parents couldn't even remember their names...", npc_talking_to_ghost.name, 11, npc_talking_to_avatar.face_image)

    def act_on_key_down_cue(self):
        if not self.check_if_player_already_animating():
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

                self.initiate_player_movement(direction)

        for feature in self.game_state.get_feature_animations_to_execute():
            feature_name = feature[0]
            feature_direction = feature[1]
            if not self.check_if_feature_already_animating(feature_name):
                self.feature_animations_in_progress.append(feature_name)
                self.initiate_feature_movement(feature_name, feature_direction)

    def check_if_player_already_animating(self):
        return self.game_view.player_avatar.currently_animating

    def initiate_player_movement(self, direction):
        room = self.game_view.game_data.room_data_list[self.game_state.current_room]
        target_tile = self.position_manager.get_adjacent_tile(self.game_state.player_ghost, direction, room)
        door_status = self.position_manager.check_for_door(room.name, target_tile.x, target_tile.y)
        print(door_status)
        self.game_state.change_player_facing(direction)
        if self.position_manager.check_if_player_can_move(direction, self.game_state.player_ghost, room):
            if not door_status:
                self.game_state.move_player_avatar(direction)
                self.position_manager.nudge_player_ghost(direction)
            elif door_status:
                print("ping")
                self.go_through_door(room.name + "_" + str(target_tile.x) + "_" + str(target_tile.y))

    # endregion

    # region INVENTORY
    def get_stat_items(self):
        hour = self.game_state.hour_of_day
        minute = self.game_state.minute_of_hour

        stat_dict = {"seeds": str(self.game_state.your_seeds),
                     "Coins": str(self.game_state.your_coins),
                     "time": str(hour) + ":" + str(minute) + "0",
                     "day": str(self.game_state.day_of_summer),
                     "selected_tool": str(self.game_state.selected_tool)}

        return stat_dict
    # endregion

    def ask_animator_to_animate(self):
        if self.check_if_player_already_animating():
            self.game_view.animation_manager.perform_player_animation(self.game_view.player_avatar)

        for feature_name in self.feature_animations_in_progress:
            thing_avatar = self.game_state.get_npc_avatar(feature_name)
            wrap_up = False
            if self.check_if_feature_already_animating(feature_name):
                wrap_up = self.game_view.animation_manager.perform_feature_animation(thing_avatar)
            if wrap_up:
                self.feature_animations_in_progress.remove(feature_name)

    def import_NPCs_from_csv(self, filename):
        NPC_data = []
        with open(os.path.join(filename), mode='r', encoding='utf-8-sig') as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                NPC_data.append(list(row))
        for NPC in NPC_data:
            if NPC[0] == "NPC":
                test = NpcGhost(NPC[2], self.game_state, NPC[3], int(NPC[4]), int(NPC[5]), Direction.DOWN)
                self.game_state.add_feature_ghost(NPC[1], test)
            elif NPC[0] == "Tree":
                test = TreeGhost(NPC[2], self.game_state, NPC[3], int(NPC[4]), int(NPC[5]), Direction.DOWN)
                self.game_state.add_feature_ghost(NPC[1], test)
            elif NPC[0] == "Oldgod":
                test = OldgodGhost(NPC[2], self.game_state, NPC[3], int(NPC[4]), int(NPC[5]), Direction.DOWN)
                self.game_state.add_feature_ghost(NPC[1], test)

        return NPC_data

    def reset_room(self, room_name):
        room = self.game_state.get_room(room_name)
        for feature_ghost in self.game_state.get_all_features_in_room(room_name):
            feature_ghost.reset_to_spawn()
            avatar = self.game_view.get_npc_avatar(feature_ghost.name)
            avatar.reset_to_base(feature_ghost.facing)
        self.position_manager.clear_room_grid(room_name)

    def load_up_room(self, room_name):
        self.position_manager.fill_room_grid(room_name)
        self.game_state.set_room(room_name)

    def change_room(self, room_going_to):
        current_room = self.game_state.get_current_room()
        self.reset_room(current_room.name)
        self.load_up_room(room_going_to)

    def get_door(self, door_name):
        return self.game_data.door_data_list[door_name]

    def go_through_door(self, door_name):
        door = self.get_door(door_name)
        self.position_manager.move_player_ghost(door.room_to, door.x_to, door.y_to, 1)
        self.change_room(door.room_to)
        pass


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
            self.gc_input.game_state.ms.post_notice("Could not use " + item.NAME)
        elif successes > 0:
            self.gc_input.game_state.ms.post_notice("used " + str(successes) + " " + item.NAME + "(s)")

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
            self.gc_input.game_state.ms.post_notice("Could not use " + item.NAME)
        elif successes > 0:
            self.gc_input.game_state.ms.post_notice("used " + item.NAME)


class MenuManager(object):
    def __init__(self, gc_input):
        self.gc_input = gc_input  # type: GameController

    def activate_menu(self):
        pass

