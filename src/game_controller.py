import copy
import csv
import os
import random

from input_manager_controller_page import *
from definitions import Direction, Types, GameSettings
from menu_ghosts_data_page import ConversationOptionsMenuGhost, SpecialMenuGhost, StatMenuGhost, AcquireMenuGhost, SubMenuGhost, YesNoMenuGhost, KeyInventoryMenuGhost, SuppliesInventoryMenuGhost, UseMenuGhost, GameActionDialogueMenuGhost, ChatMenuGhost
from position_manager_state_page import Room, PositionManager
from game_state import GameState, GameData
from game_view import GameView


class Game(object):
    def __init__(self):
        self.game_running = True
        self.game_state = GameState(None, None, None)  # type: GameState
        self.game_data = GameData()  # type: GameData
        self.game_view = GameView(self.game_data, self.game_state)  # type: GameView
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
        self.two_second_timer_id = pygame.USEREVENT + 157
        self.one_second_timer_id = pygame.USEREVENT + 152
        self.half_second_timer_id = pygame.USEREVENT + 155
        self.quarter_second_timer_id = pygame.USEREVENT + 156
        self.fifth_second_timer_id = pygame.USEREVENT + 153
        self.twentieth_second_timer_id = pygame.USEREVENT + 154
        self.timer_list = [self.two_second_timer_id, self.one_second_timer_id, self.half_second_timer_id, self.five_second_timer_id, self.ten_second_timer_id, self.fifth_second_timer_id, self.twentieth_second_timer_id, self.quarter_second_timer_id]

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
            if event.type == self.ten_second_timer_id:
                pass
            if event.type == self.five_second_timer_id:
                pass
            if event.type == self.two_second_timer_id:
                for npc in self.gc.game_state.feature_ghost_list.values():
                    print(npc)
                    if npc.feature_subtype == Types.BIRD:
                        chance = random.randint(1, 3)
                        if chance == 1:
                            avatar = self.gc.game_view.get_npc_avatar(npc.unique_name)
                            avatar.initiate_animation("deedle")
                            self.gc.feature_animations_in_progress.append(avatar.unique_name)


            if event.type == self.quarter_second_timer_id:
                self.gc.switch_tile_frame()
                self.gc.game_clock_pass_1_minute()
            if event.type == self.twentieth_second_timer_id:
                self.gc.act_on_key_down_cue()
                self.gc.ask_animator_to_animate()


    def initiate_timers(self):
        twentieth_second_timer = self.twentieth_second_timer_id
        pygame.time.set_timer(twentieth_second_timer, 4)

        fifth_second_timer = self.fifth_second_timer_id
        pygame.time.set_timer(fifth_second_timer, 20)

        quarter_second_timer = self.quarter_second_timer_id
        pygame.time.set_timer(quarter_second_timer, 500)

        half_second_timer = self.half_second_timer_id
        pygame.time.set_timer(half_second_timer, 500)

        one_second_timer = self.one_second_timer_id
        pygame.time.set_timer(one_second_timer, 1000)

        five_second_timer = self.five_second_timer_id
        pygame.time.set_timer(five_second_timer, 5000)

        ten_second_timer = self.ten_second_timer_id
        pygame.time.set_timer(ten_second_timer, 10000)

        two_second_timer = self.two_second_timer_id
        pygame.time.set_timer(two_second_timer, 2000)


class GameController(object):

    def __init__(self, game, game_view, game_state, game_data):
        self.game = game  # type: Game
        self.game = game  # type: Game
        self.game_view = game_view  # type: GameView
        self.game_state = game_state  # type: GameState
        self.game_data = game_data # type: GameData

        self.active_keyboard_manager = None
        self.key_down_queue = []
        self.held_keys = []
        self.position_manager = PositionManager(self)  # type:PositionManager
        self.menu_manager = MenuManager(self)  # type:MenuManager
        self.inventory_manager = InventoryManager(self)  # type:InventoryManager
        self.feature_animations_in_progress = []
        self.move_counter = 0
    # region GAME CONTROLS
    def set_active_keyboard_manager(self, active_manager_id):
        self.active_keyboard_manager = self.game_view.game_data.keyboard_manager_data_list[active_manager_id]

    def close_game(self):
        self.game.game_running = False

    def load_feature(self, unique_name, ghost_object, avatar_object):
        self.game_state.add_feature_ghost(unique_name, ghost_object)
        self.game_view.add_npc_avatar(unique_name, avatar_object)
    # endregion

    def switch_tile_frame(self):
        ref = self.game_view.tile_frame
        if ref == 1:
            self.game_view.tile_frame = 2
        elif ref == 0:
            self.game_view.tile_frame = 1
        elif ref == 2:
            self.game_view.tile_frame = 3
        elif ref == 3:
            self.game_view.tile_frame = 0
    # region FEATURE MOVEMENT

    def get_avatar_class(self, avatar_type):
        return self.game_view.avatar_classes[avatar_type]

    def check_if_feature_already_animating(self, name):
        avatar = self.game_view.feature_avatar_list[name]
        return avatar.currently_animating

    def initiate_feature_movement(self, name, direction):
        self.change_feature_facing(name, direction)
        if self.position_manager.check_if_feature_can_move(self.game_state.get_feature_ghost(name), direction, self.game_view.game_data.room_data_list[self.game_state.current_room]):
            self.game_view.walk_feature_avatar(name, direction)
            self.position_manager.move_feature_ghost(name, direction)

    def reset_feature_to_spawn(self, feature):
        chosen_feature = self.game_state.get_feature_ghost(feature)
        chosen_feature.reset_to_spawn()
    # endregion

    def update_view(self):
        current_room = self.game_state.get_current_room().name
        drawables_list = self.game_view.get_drawables_list(self.game_state.get_feature_locations()[0], self.game_state.get_feature_locations()[1], self.game_state.get_feature_locations()[2], self.game_view.get_independent_anim_locations())
        self.game_view.draw_all(drawables_list, current_room)

        self.update_stat_menus()
        for menu in (self.game_state.ms.static_menus + self.game_state.ms.visible_menus):
            ghost = self.game_state.ms.menu_ghost_data_list[menu + "_ghost"]
            avatar_display_details = self.game_view.menu_avatar_data_list[menu + "_avatar"].menu_display_details
            self.game_view.draw_special_menu(menu, ghost.generate_menu_information_package(), avatar_display_details["coordinates"][0], avatar_display_details["coordinates"][1])

    # region PLAYER ACTIONS
    def player_interact(self):
        player = self.game_state.get_player_ghost()
        room = self.game_state.get_current_room()
        full = self.position_manager.check_if_adjacent_tiles_full(player, player.facing, room)
        if full:
            cube = self.position_manager.get_adjacent_tile(player, player.facing, room)
            feature = self.game_state.get_feature_ghost(cube.object_filling)
            print(feature.feature_type)
            if feature.feature_type == Types.NPC:
                self.talk_to_npc(cube.object_filling, player.facing)
            if feature.feature_type == Types.PROP:
                self.talk_to_prop(cube.object_filling, player.facing)
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
        npc_talking_to_avatar = self.game_view.feature_avatar_list[npc_talking_to]
        self.change_feature_facing(npc_talking_to, direction_to_turn)
        self.game_state.ms.post_notice("You talked to " + npc_talking_to_ghost.name)
        details = {"speaker_name": npc_talking_to_ghost.name,
                   "friendship_level": 3,
                   "face_image": npc_talking_to_avatar.face_image,
                   "speaker_unique_name": npc_talking_to_ghost.unique_name}

        self.game_state.ms.set_menu(ConversationOptionsMenuGhost.BASE, details)
        # self.menu_manager.set_dialogue_menu("Something strange is going on around here, have you heard about the children disapearing? Their parents couldn't even remember their names...", npc_talking_to_ghost.name, 11, npc_talking_to_avatar.face_image)

    def talk_to_prop(self, prop_talking_to, player_direction):
        prop_talking_to_ghost = self.game_state.feature_ghost_list[prop_talking_to]
        prop_talking_to_avatar = self.game_view.feature_avatar_list[prop_talking_to]
        self.game_state.ms.post_notice("You talked to " + prop_talking_to_ghost.name)
        prop_talking_to_ghost.get_interacted_with()
        details = {}
        # self.game_state.ms.set_menu(ConversationOptionsMenuGhost.BASE, details)

    def clear_key_down_cue(self):
        self.key_down_queue = []

    def add_to_held_key(self, key):
        self.held_keys.append(key)

    def get_held_keys(self):
        return self.held_keys

    def remove_from_held_key(self, key):
        self.held_keys.remove(key)

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
        room_object = self.game_view.game_data.room_data_list[self.game_state.current_room]
        target_tile = self.position_manager.get_adjacent_tile(self.game_state.player_ghost, direction, room_object)
        self.change_player_facing(direction)
        move_status = self.position_manager.check_if_player_can_move(direction, self.game_state.player_ghost, room_object)[0]
        door_status = self.position_manager.check_if_player_can_move(direction, self.game_state.player_ghost, room_object)[1]
        if door_status:
            self.go_through_door(room_object.name + "_" + str(target_tile.x) + "_" + str(target_tile.y))
        elif not door_status:
            if move_status:
                player = self.game_state.get_player_ghost()
                self.game_view.walk_player_avatar(direction)
                self.position_manager.nudge_ghost(player, room_object, direction)
                self.player_moved_followup(player.x, player.y)
            else:
                pass

    # endregionj

    def snap_photo(self):
        facing = self.game_state.get_player_ghost().facing
        if not self.check_if_player_already_animating():
            direction = "up"
            vector_x = 0
            vector_y = 0
            if facing == Direction.DOWN:
                direction = "down"
                vector_y = 1
            elif facing == Direction.UP:
                direction = "up"
                vector_y = -1
            elif facing == Direction.LEFT:
                direction = "left"
                vector_x = -1
            elif facing == Direction.RIGHT:
                direction = "right"
                vector_x = 1
            self.game_view.player_avatar.initiate_animation("snap_photo_" + direction)

            camera_range = 3
            pl = self.game_state.get_player_ghost_location()
            success = False
            check_x = pl[0] + vector_x
            check_y = pl[1] + vector_y
            result = None
            for x in range(camera_range): #TODO: make this so it can't go out of the room range
                if success:
                    break
                cube = self.position_manager.access_cube(check_x, check_y)
                result = cube.object_filling
                if cube.object_filling:
                    success = True
                check_x += vector_x
                check_y += vector_y

            if success:
                ghost = self.game_state.get_feature_ghost(result)
                self.game_state.ms.post_notice("Snapped a pic of a " + ghost.name)

            else:
                self.game_state.ms.post_notice("There was nothing there")

    def game_clock_pass_1_minute(self):
        if self.game_state.minute_of_hour < 59:
            self.game_state.minute_of_hour += 1
        else:
            self.game_state.minute_of_hour = 0
            if self.game_state.hour_of_day < 23:
                self.game_state.hour_of_day += 1
            else:
                self.game_state.hour_of_day = 0

    def get_game_time_string(self):
        hour = self.game_state.hour_of_day
        minute = self.game_state.minute_of_hour
        print_hour = 0
        print_minute = 0
        if hour < 10:
            print_hour = "0" + str(hour)
        else:
            print_hour = str(hour)

        if minute < 10:
            print_minute = "0" + str(minute)
        else:
            print_minute = str(minute)
        final_time = print_hour + ":" + print_minute
        return final_time

    def get_stat_items(self):
        hour = self.game_state.hour_of_day
        minute = self.game_state.minute_of_hour

        stat_dict = {"seeds": str(self.game_state.your_seeds),
                     "Coins": str(self.game_state.your_coins),
                     "time": self.get_game_time_string(),
                     "day": str(self.game_state.day_of_summer),
                     "selected_tool": str(self.game_state.selected_tool)}

        return stat_dict

    def update_stat_menus(self):
        for menu in self.game_state.ms.static_menus:
            ghost = self.game_state.ms.get_menu_ghost(menu)
            ghost.update_menu_items_list()

    def ask_animator_to_animate(self):
        if self.check_if_player_already_animating():
            self.game_view.animation_manager.perform_player_animation(self.game_view.player_avatar)

        for feature_name in self.feature_animations_in_progress:
            thing_avatar = self.game_view.get_npc_avatar(feature_name)
            wrap_up = False
            if self.check_if_feature_already_animating(feature_name):
                wrap_up = self.game_view.animation_manager.perform_feature_animation(thing_avatar)
            if wrap_up:
                self.feature_animations_in_progress.remove(feature_name)

        # independent animations
        complete_animation_names = []
        for animation_name in self.game_view.active_independent_animations.keys():
            animation = self.game_view.active_independent_animations[animation_name].animate()
            if animation[4]:
                complete_animation_names.append(animation_name)
        for item in complete_animation_names:
            self.game_view.complete_independent_animation(item)

    def change_feature_facing(self, name, direction):
        self.game_state.change_feature_ghost_facing(name, direction)
        self.game_view.change_feature_avatar_facing(name, direction)

    def change_player_facing(self, direction):
        final_facing = direction
        current_facing = self.game_state.player_ghost.facing
        if direction == Direction.MATCH:
            if current_facing == Direction.DOWN:
                final_facing = Direction.DOWN
            elif current_facing == Direction.UP:
                final_facing = Direction.UP
            elif current_facing == Direction.LEFT:
                final_facing = Direction.LEFT
            elif current_facing == Direction.RIGHT:
                final_facing = Direction.RIGHT
        elif direction == Direction.SWITCH:
            if current_facing == Direction.DOWN:
                final_facing = Direction.UP
            elif current_facing == Direction.UP:
                final_facing = Direction.DOWN
            elif current_facing == Direction.LEFT:
                final_facing = Direction.RIGHT
            elif current_facing == Direction.RIGHT:
                final_facing = Direction.LEFT
        self.game_state.change_player_ghost_facing(final_facing)
        self.game_view.player_avatar.face_character(final_facing)

    def import_NPCs_from_csv(self, filename):
        NPC_data = []
        with open(os.path.join(filename), mode='r', encoding='utf-8-sig') as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                NPC_data.append(list(row))
        for Feature in NPC_data:
            feature_type = self.game_state.type_translator[Feature[0]]
            feature_subtype = self.game_state.sub_type_translator[Feature[10]]
            unique_name = Feature[1] + "_" + str(GameSettings.get_unique_ID())
            if feature_type == Types.NPC:
                if feature_subtype == Types.BIRD:
                    test = self.game_state.ghost_classes["Bird"](Feature[1], self.game_state, Feature[2], int(Feature[3]), int(Feature[4]),
                                                                self.game_state.direction_translations[Feature[5]], feature_type, int(Feature[7]),
                                                                int(Feature[8]), unique_name, str(Feature[9]), feature_subtype)
                    self.game_state.add_feature_ghost(unique_name, test)

                    # produce initial triggers
                    triggers_object = test.produce_map_trigger(int(Feature[3]), int(Feature[4]))
                    print(unique_name, triggers_object.coords_list)
                    self.game_state.add_map_trigger(Feature[2], triggers_object.triggers_name, triggers_object)

                else:
                    test = self.game_state.ghost_classes["NPC"](Feature[1], self.game_state, Feature[2], int(Feature[3]), int(Feature[4]),
                                                                self.game_state.direction_translations[Feature[5]], feature_type, int(Feature[7]),
                                                                int(Feature[8]), unique_name, str(Feature[9]), feature_subtype)
                    self.game_state.add_feature_ghost(unique_name, test)
            if feature_type == Types.PROP:
                if feature_subtype == Types.BASKET:
                    test = self.game_state.ghost_classes["Basket"](Feature[1], self.game_state, Feature[2], int(Feature[3]), int(Feature[4]),
                                                                self.game_state.direction_translations[Feature[5]], feature_type, int(Feature[7]),
                                                                int(Feature[8]), unique_name, str(Feature[9]), feature_subtype)
                else:
                    test = self.game_state.ghost_classes["Prop"](Feature[1], self.game_state, Feature[2], int(Feature[3]), int(Feature[4]),
                                                                 self.game_state.direction_translations[Feature[5]], feature_type, int(Feature[7]),
                                                                 int(Feature[8]), unique_name, str(Feature[9]), feature_subtype)
                self.game_state.add_feature_ghost(unique_name, test)
            if feature_type == Types.HOUSE:
                test = self.game_state.ghost_classes["House"](Feature[1], self.game_state, Feature[2], int(Feature[3]), int(Feature[4]),
                                                            self.game_state.direction_translations[Feature[5]], feature_type, int(Feature[7]),
                                                            int(Feature[8]), unique_name, str(Feature[9]), feature_subtype)
                self.game_state.add_feature_ghost(unique_name, test)
            if feature_type == Types.DECO:
                test = self.game_state.ghost_classes["Deco"](Feature[1], self.game_state, Feature[2], int(Feature[3]), int(Feature[4]),
                                                              self.game_state.direction_translations[Feature[5]], feature_type, int(Feature[7]),
                                                              int(Feature[8]), unique_name, str(Feature[9]), feature_subtype)
                self.game_state.add_feature_ghost(unique_name, test)

        return NPC_data

    def import_decos_from_csv(self, filename):
        deco_data = []
        with open(os.path.join(filename), mode='r', encoding='utf-8-sig') as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                deco_data.append(list(row))
        for Feature in deco_data:
            feature_type = self.game_state.type_translator[Feature[0]]
            feature_subtype = self.game_state.sub_type_translator[Feature[10]]
            unique_name = Feature[1] + "_" + str(GameSettings.get_unique_ID())
            if feature_type == Types.DECO:
                test = self.game_state.ghost_classes["Deco"](Feature[1], self.game_state, Feature[2], int(Feature[3]), int(Feature[4]),
                                                             self.game_state.direction_translations[Feature[5]], Feature[6], int(Feature[7]),
                                                             int(Feature[8]), unique_name, str(Feature[9]), feature_subtype)
                self.game_state.add_deco_ghost(unique_name, test)

        return deco_data

    def reset_room(self, room_name):
        room = self.game_state.get_room(room_name)
        for feature_ghost in self.game_state.get_all_features_in_room(room_name):
            if feature_ghost.feature_type == "Player":
                pass
            else:
                feature_ghost.reset_to_spawn()
                avatar = self.game_view.get_npc_avatar(feature_ghost.unique_name)
                avatar.reset_to_base()
        self.position_manager.clear_room_grid(room_name)

    def load_up_room(self, room_name):
        self.position_manager.fill_room_grid(room_name)
        self.position_manager.add_player_to_grid(room_name)
        self.game_state.set_room(room_name)

    def change_room(self, room_going_to):
        current_room = self.game_state.get_current_room()
        self.reset_room(current_room.name)
        self.load_up_room(room_going_to)

    def get_door(self, door_name):
        return self.game_data.door_data_list[door_name]

    def go_through_door(self, door_name):
        player_object = self.game_state.get_player_ghost()
        self.clear_key_down_cue()
        door = self.get_door(door_name)
        x_change = door.x_to - player_object.x
        y_change = door.y_to - player_object.y
        self.change_player_facing(door.exit_direction)
        current_room_object = self.game_state.get_room(door.room_from)
        new_room_object = self.game_state.get_room(door.room_to)
        self.position_manager.move_ghost(player_object, current_room_object, new_room_object, door.x_to, door.y_to)
        self.position_manager.match_player_elevation_to_target(new_room_object, door.x_to, door.y_to)
        self.game_view.manually_update_camera(x_change, y_change)
        self.change_room(door.room_to)
        pygame.mixer.Sound("assets/sound_effects/popping_sound.mp3").play()

    def player_moved_followup(self, player_x, player_y):
        self.check_for_map_triggers(player_x, player_y)
        pass

    def check_for_map_triggers(self, player_x, player_y):
        room = self.game_state.get_current_room()
        if room.name in self.game_state.map_trigger_list.keys():
            fetch_list = self.game_state.map_trigger_list[self.game_state.get_current_room().name]
            birds_to_trigger = []
            for map_trigger in fetch_list.values():
                for x in map_trigger.coords_list:
                    if x[0] == player_x and x[1] == player_y:
                        triggered_feature_name = map_trigger.trigger_owner_unique_name
                        birds_to_trigger.append(triggered_feature_name)
            for bird_unique_name in birds_to_trigger:
                self.trigger_a_bird(bird_unique_name, room)

    def trigger_a_bird(self, unique_name, room):
        bird_ghost = self.game_state.get_feature_ghost(unique_name)
        bird_avatar = self.game_view.get_npc_avatar(unique_name)
        print(unique_name)
        self.game_state.remove_map_trigger(room.name, unique_name)
        self.position_manager.remove_feature_from_map(unique_name, room)
        self.game_view.trigger_independent_animation("disappear_animation", bird_ghost.unique_name + "_disappear_animation", bird_ghost.unique_name, room, bird_avatar.drawing_priority, bird_avatar.image_x, bird_avatar.image_y, bird_avatar.image_offset_x, bird_avatar.image_offset_y)


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
        if not self.gc_input.game_state.gd.item_data_list[item.NAME].use_requirements_met():
            success = False
        return success

    def check_if_can_use_key_item(self, item, details):
        chosen_item = self.gc_input.game_state.gd.key_item_data_list[item.NAME]
        success = False
        message = None
        if chosen_item.use_requirements_met(details):
            success = True
            message = chosen_item.get_success_message(details)
        else:
            message = chosen_item.get_failure_message(details)
        return success, message

    def get_key_item(self, item):
        current_key_inventory = self.gc_input.game_state.ms.get_menu_items_list("key_inventory_menu")
        if item.NAME in current_key_inventory:
            pass
        else:
            current_key_inventory[item.NAME] = {"name": item.NAME}

    def use_key_item(self, item):
        current_key_inventory = self.gc_input.game_state.ms.get_menu_items_list("key_inventory_menu")
        successes = 0

        room = self.gc_input.game_state.get_current_room()
        player = self.gc_input.game_state.get_player_ghost()
        cube = room.access_adjacent_cube(player, player.facing)
        details = {"room": room, "cube": cube, "adjacent_tile_filling": cube.object_filling, "filling_type": cube.filling_type}
        print("it was filled with", cube.object_filling)

        result = self.check_if_can_use_key_item(item, details)[0]
        message = self.check_if_can_use_key_item(item, details)[1]

        if result:
            self.gc_input.game_state.gd.key_item_data_list[item.NAME].item_use(details)
            successes += 1

        self.gc_input.game_state.ms.post_notice(message)



class MenuManager(object):
    def __init__(self, gc_input):
        self.gc_input = gc_input  # type: GameController
        self.menu_load_list = [SpecialMenuGhost, StatMenuGhost, AcquireMenuGhost, StartMenuGhost, SubMenuGhost, YesNoMenuGhost,
                               UseMenuGhost, SuppliesInventoryMenuGhost, KeyInventoryMenuGhost, ConversationOptionsMenuGhost,
                               GameActionDialogueMenuGhost, QuizMenuGhost, ChatMenuGhost]

    def activate_menu(self):
        pass

