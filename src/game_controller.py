import copy
import csv
import os
import random
from random import choice

from animations_page_view_page import CameraPanAnimation
from input_manager_controller_page import *
from definitions import Direction, Types, GameSettings, Mundane
from menu_ghosts_data_page import ConversationOptionsMenuGhost, StatMenuGhost, AcquireMenuGhost, SubMenuGhost, NumberSelectionMenuGhost, KeyInventoryMenuGhost, SuppliesInventoryMenuGhost, GameActionDialogueMenuGhost, ChatMenuGhost, MapMenuGhost, GalleryMenuGhost, PictureMenuGhost, GiftGivingMenuGhost, GuideMenuGhost
from position_manager_state_page import Room, PositionManager
from game_state import GameState, GameData
from game_view import GameView, OutfitManager


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
        self.timer_list = []
        self.event_dict = {.004: [self.gc.act_on_key_down_cue, self.gc.ask_animator_to_animate, self.gc.ask_scene_to_animate],
                            .167: [self.gc.npc_event_popoff],
                           .25: [self.gc.switch_tile_frame],
                           .75: [self.gc.switch_flash],
                            1: [self.gc.game_clock_pass_1_minute]}
        self.setup_timers()



    def setup_timers(self):
        userevent_numbers = 200

        for timer in self.event_dict.keys():
            event_name = str(timer) + "_second_timer_id"
            setattr(self, event_name, pygame.USEREVENT + userevent_numbers)

            new_timer = getattr(self, event_name)

            self.timer_list.append(new_timer)
            userevent_numbers += 1

            one_second_equiv = 1000
            timer_equiv = timer * one_second_equiv
            pygame.time.set_timer(new_timer, int(timer_equiv))

    def parse_input_event(self, event):
        if event.type == pygame.QUIT:
            self.gc.close_game()

        elif event.type in [pygame.KEYDOWN, pygame.KEYUP]:
            self.gc.active_keyboard_manager.parse_key_input(event.type, event.key)

        elif event.type in self.timer_list:
            for timer in self.event_dict.keys():
                if event.type == getattr(self, str(timer) + "_second_timer_id"):
                    for popoff in self.event_dict[timer]:
                        popoff()


class GameController(object):

    def __init__(self, game, game_view, game_state, game_data):
        self.game = game  # type: Game
        self.game = game  # type: Game
        self.game_view = game_view  # type: GameView
        self.game_state = game_state  # type: GameState
        self.game_data = game_data  # type: GameData

        self.active_keyboard_manager = None
        self.key_down_queue = []
        self.held_keys = []
        self.position_manager = PositionManager(self)  # type:PositionManager
        self.menu_controller = MenuController(self)  # type:MenuController
        self.trigger_manager = TriggerManager(self) # type: TriggerManager
        self.inventory_manager = InventoryManager(self)  # type:InventoryManager
        self.outfit_manager = OutfitManager(self) # type: OutfitManager
        self.scene_manager = SceneManager(self)     # SceneManager
        self.feature_animations_in_progress = []
        self.scene_animations_in_progress = []
        self.move_counter = 0
        self.flashing_currently = False
    # region GAME CONTROLS
    def set_active_keyboard_manager(self, active_manager_id):
        self.active_keyboard_manager = self.game_view.game_data.keyboard_manager_data_list[active_manager_id]

    def close_game(self):
        self.game.game_running = False

    def load_feature(self, unique_name, ghost_object, avatar_object):
        self.game_state.add_feature_ghost(unique_name, ghost_object)
        self.game_view.add_npc_avatar(unique_name, avatar_object)
    # endregion


    def play_sound(self, sound_name):
        pygame.mixer.Sound("assets/sound_effects/splash.mp3").play()

    def switch_flash(self):
        if self.flashing_currently:
            self.flashing_currently = False
        else:
            self.flashing_currently = True

    def make_flashing_text(self, text):
        result = text

        if self.flashing_currently:
            result = ""

        return result

    def use_selected_tool(self):
        if self.game_state.selected_tool != "None":
            tool = self.inventory_manager.gc_input.game_state.gd.key_item_data_list[self.game_state.selected_tool]
            self.inventory_manager.use_key_item(tool)
        else:
            self.game_state.gc.menu_controller.post_notice("There is nothing selected")

    def npc_event_popoff(self):
        feature = self.game_state.get_feature_ghost("Pigeon_44")
        if ("Pigeon_44" in self.game_state.feature_ghost_list.keys()) and feature.active:
            self.move_feature_chaotically("Pigeon_44")
        pass

    def get_feature_display_name(self, feature_unique_nane):
        ghost = self.game_state.get_feature_ghost(feature_unique_nane)
        return ghost.display_name

    def pick_up_package(self, type, package_unique_name, room_name, package_items):
        self.menu_controller.post_notice("You picked up the package")
        room_object = self.game_state.get_room(room_name)
        ghost = self.game_state.get_feature_ghost(package_unique_name)
        ghost.spawn_active = False
        self.position_manager.despawn_feature(package_unique_name, room_object)
        for item in package_items:
            if type == "Package":
                self.inventory_manager.get_key_or_temp_item(item, 1)
            if type == "Page":
                self.inventory_manager.get_page(item)

    def look_in_basket(self, basket_unique_name, basket_items):
        if basket_items:
            print("I'm testing this out", basket_items)
            ghost = self.game_state.get_feature_ghost(basket_unique_name)
            self.menu_controller.post_notice("You looked in the " + ghost.species)
            details = {"item_list": basket_items, "basket_unique_name": basket_unique_name}
            self.menu_controller.set_menu(AcquireMenuGhost.BASE, details)
        else:
            self.menu_controller.post_notice("It appears to be empty.")

    def take_from_basket(self, basket_unique_name, name_item_taken):
        self.inventory_manager.get_key_or_temp_item(name_item_taken, 1)
        self.menu_controller.post_notice("You took the " + name_item_taken)
        ghost = self.game_state.get_feature_ghost(basket_unique_name)
        ghost.function_items.remove(name_item_taken)

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

    def add_to_anim_in_progress(self, feature_unique_name):
        self.scene_animations_in_progress.append(feature_unique_name)

    def add_to_scene_anim_in_progress(self, scene_animation_name):
        self.scene_animations_in_progress.append(scene_animation_name)

    def move_feature_chaotically(self, feature_unique_name):
        already_animating = self.check_if_feature_already_animating(feature_unique_name)
        if not already_animating:
            complete = False
            while not complete:
                movements = ["walk_front", "walk_left", "walk_right", "walk_up"]
                if movements:
                    chosen_movement = movements.pop(random.choice(range(len(movements))))
                    complete = self.attempt_feature_action(feature_unique_name, chosen_movement)
                else:
                    complete = True

    def attempt_feature_action(self, feature_unique_name, action_name):
        success = False
        feature_ghost = self.game_state.get_feature_ghost(feature_unique_name)
        feature_avatar = self.game_view.get_npc_avatar(feature_unique_name)

        already_animating = self.check_if_feature_already_animating(feature_unique_name)
        doable = self.check_if_action_doable(feature_ghost, action_name)[0]
        direction = self.check_if_action_doable(feature_ghost, action_name)[1]
        vector = Direction.get_vector_from_direction(direction)
        room_object = self.game_state.get_room(feature_ghost.room)
        if not already_animating:
            if doable:
                success = True
                feature_avatar.initiate_animation(action_name)
                self.add_to_anim_in_progress(feature_unique_name)
                self.position_manager.move_ghost(feature_ghost, room_object, room_object, feature_ghost.x + vector[0], feature_ghost.y + vector[1])
        return success


    def check_if_action_doable(self, feature_ghost, action_name):
        direction = None
        if action_name == "walk_front":
            direction = Direction.DOWN
        elif action_name == "walk_left":
            direction = Direction.LEFT
        elif action_name == "walk_right":
            direction = Direction.RIGHT
        elif action_name == "walk_up":
            direction = Direction.UP
        room_object = self.game_state.get_room(feature_ghost.room)
        can_move = self.position_manager.check_if_feature_can_move(feature_ghost, direction, room_object)
        return can_move, direction

    def get_avatar_class(self, avatar_type):
        return self.game_view.avatar_classes[avatar_type]

    def check_if_feature_already_animating(self, name):
        avatar = self.game_view.get_npc_avatar(name)
        return avatar.currently_animating

    def reset_feature_to_spawn(self, feature):
        chosen_feature = self.game_state.get_feature_ghost(feature)
        chosen_feature.reset_to_spawn()
    # endregion

    def update_view(self):
        current_room = self.game_state.get_current_room().room_name
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
            feature = self.game_state.get_feature_ghost(cube.filling_unique_name)
            if feature.feature_type == Types.NPC:
                if feature.feature_subtype == Types.BIRD:
                    self.game_state.gc.menu_controller.post_notice("You shouldn't touch wild animals.")
                else:
                    self.talk_to_npc(cube.filling_unique_name, player.facing)
            if feature.feature_type == Types.PROP:
                self.talk_to_prop(cube.filling_unique_name, player.facing)
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
        self.game_state.gc.menu_controller.post_notice("You talked to " + self.get_feature_display_name(npc_talking_to_ghost.unique_name))
        details = {"speaker_name": self.get_feature_display_name(npc_talking_to_ghost.unique_name),
                   "friendship_level": npc_talking_to_ghost.friendship_level,
                   "face_image": npc_talking_to_avatar.face_image,
                   "speaker_unique_name": npc_talking_to_ghost.unique_name}

        self.game_state.gc.menu_controller.set_menu(ConversationOptionsMenuGhost.BASE, details)
        # self.menu_manager.set_dialogue_menu("Something strange is going on around here, have you heard about the children disapearing? Their parents couldn't even remember their names...", npc_talking_to_ghost.name, 11, npc_talking_to_avatar.face_image)

    def talk_to_prop(self, prop_talking_to, player_direction):
        prop_talking_to_ghost = self.game_state.feature_ghost_list[prop_talking_to]
        prop_talking_to_avatar = self.game_view.feature_avatar_list[prop_talking_to]
        self.game_state.gc.menu_controller.post_notice("You talked to " + prop_talking_to_ghost.species)
        prop_talking_to_ghost.get_interacted_with()
        details = {}

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

    def check_if_player_already_animating(self):
        return self.game_view.player_avatar.currently_animating

    def check_for_tile_transition(self, room_object, current_x, current_y, target_x, target_y):
        result = False
        current_tile_terrain = self.position_manager.get_tile_terrain(room_object.room_name, current_x, current_y)
        target_tile_terrain = self.position_manager.get_tile_terrain(room_object.room_name, target_x, target_y)
        if current_tile_terrain != target_tile_terrain:
            result = True
        print("terrainchecking,", result)

        if result:
            if target_tile_terrain == 1:
                print("water")
                self.outfit_manager.put_on_temporary_outfit("Mermaid")
            elif current_tile_terrain == 1:
                self.outfit_manager.put_on_outfit(self.game_state.revert_outfit)

    def initiate_player_movement(self, direction):
        room_object = self.game_view.game_data.room_data_list[self.game_state.current_room]
        target_tile = self.position_manager.get_adjacent_tile(self.game_state.player_ghost, direction, room_object)
        self.change_player_facing(direction)
        move_status = self.position_manager.check_if_player_can_move(direction, self.game_state.player_ghost, room_object)[0]
        door_status = self.position_manager.check_if_player_can_move(direction, self.game_state.player_ghost, room_object)[1]
        if door_status:
            self.go_through_door(room_object.room_name + "_" + str(target_tile.x) + "_" + str(target_tile.y))
        elif not door_status:
            if move_status:
                player = self.game_state.get_player_ghost()
                self.game_view.walk_player_avatar(direction)
                print(player.x, player.y, target_tile.x, target_tile.y)
                self.check_for_tile_transition(room_object, player.x, player.y, target_tile.x, target_tile.y)
                self.position_manager.move_ghost(player, room_object, room_object, player.x + Direction.get_vector_from_direction(direction)[0], player.y + Direction.get_vector_from_direction(direction)[1])
                self.player_moved_followup(player.x, player.y)
            else:
                pass

    # endregionj

    def snap_photo(self):
        facing = self.game_state.get_player_ghost().facing
        if not self.check_if_player_already_animating():
            direction = Mundane.direction_feedback(facing, "left", "right", "up", "down")
            vector_x = Mundane.direction_feedback(facing, -1, 1, 0, 0)
            vector_y = Mundane.direction_feedback(facing, 0, 0, -1, 1)
            self.game_view.player_avatar.initiate_animation("snap_photo_" + direction)

            camera_range = 2
            pl = self.game_state.get_player_ghost_location()
            success = False
            check_x = pl[0] + vector_x
            check_y = pl[1] + vector_y
            result = None
            for x in range(camera_range): #TODO: make this so it can't go out of the room range
                if success:
                    break
                cube = self.position_manager.access_cube(check_x, check_y)
                result = cube.filling_unique_name
                if cube.filling_unique_name:
                    success = True
                check_x += vector_x
                check_y += vector_y

            if success:
                ghost = self.game_state.get_feature_ghost(result)
                self.game_state.gc.menu_controller.post_notice("Snapped a pic of a " + ghost.display_name)
                gallery_menu = self.game_state.ms.get_menu_ghost(GalleryMenuGhost.BASE)
                if ghost.feature_subtype == Types.BIRD and not gallery_menu.check_if_item_in_list("Bird", ghost.species) and not ghost.species == "Pigeon":
                    gallery_menu.add_to_item_list("Bird", ghost.species, ghost.display_name)
                    self.game_state.gc.menu_controller.post_notice("Added " + ghost.display_name + " to gallery!")
                elif ghost.species == "Pigeon":
                    # TODO: START HERE
                    gallery_menu.add_to_item_list("Tree", ghost.species, ghost.display_name)
                elif ghost.feature_subtype == Types.TREE and not gallery_menu.check_if_item_in_list("Tree", ghost.species):
                    gallery_menu.add_to_item_list("Tree", ghost.species, ghost.display_name)
                    self.game_state.gc.menu_controller.post_notice("Added " + ghost.display_name + " to gallery!")
            else:
                self.game_state.gc.menu_controller.post_notice("There was nothing there")

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
        display_hour = 0
        display_minute = 0
        if hour < 10:
            display_hour = "0" + str(hour)
        else:
            display_hour = str(hour)

        if minute < 10:
            display_minute = "0" + str(minute)
        else:
            display_minute = str(minute)
        final_time = display_hour + ":" + display_minute
        return final_time

    def get_stat_items(self):
        hour = self.game_state.hour_of_day
        minute = self.game_state.minute_of_hour

        stat_dict = {"Birds": str(self.game_state.bird_count),
                     "Pigeons": str(self.game_state.pigeon_count),
                     "time": self.get_game_time_string(),
                     "day": str(self.game_state.day_of_summer),
                     "selected_tool": str(self.game_state.selected_tool)}

        return stat_dict

    def update_stat_menus(self):
        for menu in self.game_state.ms.static_menus:
            ghost = self.game_state.ms.get_menu_ghost(menu)
            ghost.prepare_menu_for_display()

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
        for animation_name in self.game_view.animation_manager.active_independent_animations.keys():
            animation = self.game_view.animation_manager.active_independent_animations[animation_name].animate()
            if animation[4]:
                complete_animation_names.append(animation_name)
        for item in complete_animation_names:
            self.game_view.complete_independent_animation(item)

    def ask_scene_to_animate(self):
        for scene_animation in self.scene_animations_in_progress:
            wrap_up = self.game_view.animation_manager.perform_scene_animation(scene_animation)
            if wrap_up:
                self.scene_animations_in_progress.remove(scene_animation)
                self.scene_manager.scene_end_character_movements({})

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

    def import_features_from_csv(self, filename):
        feature_data = self.process_features_from_csv(filename)

        for feature_dict in feature_data:
            feature_type = self.game_state.type_translator[feature_dict["type"]]
            feature_subtype = self.game_state.sub_type_translator[feature_dict["subtype"]]
            unique_name = feature_dict["species"] + "_" + str(GameSettings.get_unique_ID())
            feature_ghost_object = self.game_state.ghost_classes[feature_dict["subtype"]](feature_type, feature_subtype, feature_dict["species"], unique_name, feature_dict["display_name"], feature_dict["function"], self.game_state, feature_dict["room"], int(feature_dict["x"]), int(feature_dict["y"]),
                                                              self.game_state.direction_translations[feature_dict["direction"]], int(feature_dict["base_size_x"]),
                                                              int(feature_dict["base_size_y"]), int(feature_dict["figure_size_x"]), int(feature_dict["figure_size_y"]), feature_dict["spawn_active"], str(feature_dict["phrase"]))
            if feature_subtype == Types.DECO:
                self.game_state.add_deco_ghost(unique_name, feature_ghost_object)
            else:
                self.game_state.add_feature_ghost(unique_name, feature_ghost_object)

    def import_pages_from_csv(self, filename):
        feature_data = self.process_features_from_csv(filename)

        return feature_data

        # for feature_dict in feature_data:
        #     feature_type = self.game_state.type_translator[feature_dict["type"]]
        #     feature_subtype = self.game_state.sub_type_translator[feature_dict["subtype"]]
        #     unique_name = feature_dict["species"] + "_" + str(GameSettings.get_unique_ID())
        #     feature_ghost_object = self.game_state.ghost_classes[feature_dict["subtype"]](feature_type, feature_subtype, feature_dict["species"], unique_name, feature_dict["display_name"], feature_dict["function"], self.game_state, feature_dict["room"], int(feature_dict["x"]), int(feature_dict["y"]),
        #                                                       self.game_state.direction_translations[feature_dict["direction"]], int(feature_dict["base_size_x"]),
        #                                                       int(feature_dict["base_size_y"]), int(feature_dict["figure_size_x"]), int(feature_dict["figure_size_y"]), feature_dict["spawn_active"], str(feature_dict["phrase"]))
        #     if feature_subtype == Types.DECO:
        #         self.game_state.add_deco_ghost(unique_name, feature_ghost_object)
        #     else:
        #         self.game_state.add_feature_ghost(unique_name, feature_ghost_object)

    def import_npcs_from_csv(self, filename):
        feature_data = self.process_features_from_csv(filename)

        for feature_dict in feature_data:
            feature_type = self.game_state.type_translator[feature_dict["type"]]
            feature_subtype = self.game_state.sub_type_translator[feature_dict["subtype"]]
            unique_name = feature_dict["species"] + "_" + str(GameSettings.get_unique_ID())
            feature_ghost_object = self.game_state.ghost_classes[feature_dict["subtype"]](feature_type,
                                                                                          feature_subtype,
                                                                                          feature_dict["species"],
                                                                                          unique_name,
                                                                                          feature_dict["display_name"],
                                                                                          feature_dict["function"],
                                                                                          self.game_state,
                                                                                          feature_dict["room"],
                                                                                          int(feature_dict["x"]),
                                                                                          int(feature_dict["y"]),
                                                                                          self.game_state.direction_translations[feature_dict["direction"]],
                                                                                          int(feature_dict["base_size_x"]),
                                                                                          int(feature_dict["base_size_y"]),
                                                                                          int(feature_dict["figure_size_x"]),
                                                                                          int(feature_dict["figure_size_y"]),
                                                                                          feature_dict["spawn_active"],
                                                                                          str(feature_dict["base_phrase"]),
                                                                                          str(feature_dict["good_gift_phrase"]),
                                                                                          str(feature_dict["bad_gift_phrase"]),
                                                                                          str(feature_dict["neutral_gift_phrase"]),
                                                                                          str(feature_dict["bird_hint_phrase"]))
            if feature_subtype == Types.DECO:
                self.game_state.add_deco_ghost(unique_name, feature_ghost_object)
            else:
                self.game_state.add_feature_ghost(unique_name, feature_ghost_object)


    def process_features_from_csv(self, filename):
        feature_data = []
        with open(os.path.join(filename), mode='r', encoding='utf-8-sig') as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                dict = {}
                for item in row:
                    index = row.index(item)
                    if Mundane.is_even(index):
                        dict[item] = row[index + 1]
                feature_data.append(dict)
        return feature_data

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
        room_object = self.game_state.get_room(room_name)
        self.position_manager.despawn_all_room_features(room_object)
        self.position_manager.clear_room_grid(room_name)
        self.trigger_manager.remove_all_triggers(room_object)

    def load_up_room(self, room_name):
        room_object = self.game_state.get_room(room_name)
        self.position_manager.spawn_all_initial_room_features(room_object)
        self.position_manager.add_player_to_grid(room_name)
        self.game_state.set_room(room_name)

    def change_room(self, room_going_to):
        current_room = self.game_state.get_current_room()
        self.reset_room(current_room.room_name)
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
        if self.game_state.gc.position_manager.get_tile_terrain(self.game_state.get_current_room().room_name, player_x, player_y) == 1:
            self.game_state.gc.play_sound("splash")
        self.check_for_map_triggers(player_x, player_y)
        pass

    def check_for_map_triggers(self, player_x, player_y):
        room = self.game_state.get_current_room()
        triggers = copy.copy(self.trigger_manager.check_for_triggers(room, player_x, player_y))
        for trigger in triggers:
            self.trigger_a_bird(trigger[0], room, trigger[1])

    def trigger_a_bird(self, unique_name, room, trigger):
        if room.room_name != "Aviary_Room":
            bird_ghost = self.game_state.get_feature_ghost(unique_name)
            bird_avatar = self.game_view.get_npc_avatar(unique_name)

            check_trigger_result = bird_ghost.check_trigger_result(trigger)

            if check_trigger_result == "remove":
                self.game_view.trigger_independent_animation("disappear_animation", bird_ghost.unique_name + "_disappear_animation", bird_ghost.unique_name, room, bird_avatar.drawing_priority, bird_avatar.image_x, bird_avatar.image_y, bird_avatar.image_offset_x, bird_avatar.image_offset_y)
                self.position_manager.despawn_feature(unique_name, room)
            else:
                pass


class InventoryManager(object):
    def __init__(self, gc_input):
        self.gc_input = gc_input  # type: GameController

    def get_key_or_temp_item(self, item_name, quantity):
        item_list = self.gc_input.game_data.item_data_list
        key_item_list = self.gc_input.game_data.key_item_data_list
        if item_name in key_item_list.keys():
            self.get_key_item(item_name)
        elif item_name in item_list.keys():
            self.get_item(item_name, quantity)

    def fetch_page(self, page_name):
        return self.gc_input.game_state.gd.bird_page_data_list[page_name]

    def get_page(self, page_name):
        self.gc_input.game_state.held_pages.append(page_name)

    def get_item(self, item_name, quantity):
        item = self.gc_input.game_data.item_data_list[item_name]
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
            self.gc_input.game_state.gc.menu_controller.post_notice("Could not use " + item.NAME)
        elif successes > 0:
            self.gc_input.game_state.gc.menu_controller.post_notice("used " + str(successes) + " " + item.NAME + "(s)")

    def get_quantity_of_item(self, item_name):
        current_inventory = self.gc_input.game_state.ms.get_menu_items_list("supplies_inventory_menu")
        quantity = current_inventory[item_name]["quantity"]
        return quantity

    def remove_item(self, item, quantity_removed):
        current_inventory = self.gc_input.game_state.ms.get_menu_items_list("supplies_inventory_menu")
        if quantity_removed <= self.gc_input.game_state.get_item_quantity(item.name):
            current_inventory[item.NAME]["quantity"] -= quantity_removed
        if current_inventory[item.NAME]["quantity"] == 0:
            current_inventory.pop(item.NAME)

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
        details = {"room": room, "cube": cube, "adjacent_tile_filling": cube.filling_unique_name, "filling_type": cube.filling_type, "filling_subtype": cube.filling_subtype}

        result = self.check_if_can_use_key_item(item, details)[0]
        message = self.check_if_can_use_key_item(item, details)[1]

        if result:
            self.gc_input.game_state.gd.key_item_data_list[item.NAME].item_use(details)
            successes += 1

        self.gc_input.game_state.gc.menu_controller.post_notice(message)


class TriggerManager(object):
    def __init__(self, gc_input):
        self.gc_input = gc_input
        self.trigger_list = {}

    def setup_trigger_list(self):
        for room in self.gc_input.game_data.room_data_list.values():
            self.trigger_list[room.room_name] = {}
            for tile in room.return_list_all_cubes():
                self.trigger_list[room.room_name][(tile.x, tile.y)] = []

    def add_triggers(self, room_object, trigger_dict):
        for key in trigger_dict.keys():
            if self.check_if_coord_outside_room(key, room_object):
                pass
            else:
                coords = (key[0], key[1])
                self.trigger_list[room_object.room_name][coords].append(trigger_dict[key])

    def check_if_coord_outside_room(self, coords, room_object):
        outside = False
        if (coords[0] > room_object.x_size) or coords[0] < 1 or (coords[1] > room_object.y_size) or coords[1] < 1:
            outside = True
        else:
            pass
        return outside

    def update_features_triggers(self, room_object, feature_ghost):
        remove_trigger_list = copy.copy(feature_ghost.trigger_list)
        self.remove_triggers(room_object, feature_ghost)
        add_trigger_list = feature_ghost.produce_trigger_list()
        self.add_triggers(room_object, add_trigger_list)

    def print_all_triggers(self, room_object):
        print(self.trigger_list[room_object.room_name])

    def remove_all_triggers(self, room_object):
        for tile in self.trigger_list[room_object.room_name]:
            self.trigger_list[room_object.room_name][tile].clear()

    def remove_triggers(self, room_object, feature_ghost):
        tracker = 0
        for existing_trigger in self.trigger_list[room_object.room_name].values():
            for trigger in existing_trigger:
                if trigger[0] == feature_ghost.unique_name:
                    existing_trigger.pop(existing_trigger.index(trigger))
                    tracker +=1


    def check_for_triggers(self, room_object, x, y):
        return self.trigger_list[room_object.room_name][x, y]


class MenuController(object):
    def __init__(self, gc_input):
        self.gc_input = gc_input  # type: GameController
        self.menu_load_list = [StatMenuGhost, AcquireMenuGhost, StartMenuGhost, SubMenuGhost, NumberSelectionMenuGhost,
                               SuppliesInventoryMenuGhost, KeyInventoryMenuGhost, ConversationOptionsMenuGhost,
                               GameActionDialogueMenuGhost, GuideMenuGhost, QuizMenuGhost, ChatMenuGhost, GalleryMenuGhost, OutfitMenuGhost, MapMenuGhost, PictureMenuGhost, GiftGivingMenuGhost]

    def activate_menu(self):
        pass

    def gift_menu_selection(self, sub_menu_selection, chosen_item_name, details):
        if sub_menu_selection == "Yes":
            chosen_item = self.gc_input.game_state.gd.item_data_list[chosen_item_name]
            speaker = self.gc_input.game_state.get_feature_ghost(details["speaker_unique_name"])

            self.gc_input.inventory_manager.remove_item(chosen_item, 1)
            self.gc_input.menu_controller.post_notice("You gave " + speaker.display_name + " a " + chosen_item.name)

            details["phrase"] = [speaker.receive_gift(chosen_item_name)]
            details["friendship_level"] = Mundane.get_friendship_hearts(speaker.friendship_level)
            self.gc_input.menu_controller.exit_all_menus()
            self.gc_input.menu_controller.set_menu(ChatMenuGhost.BASE, details)

        else:
            self.gc_input.menu_controller.exit_all_menus()

    def inventory_menu_selection(self, inventory_menu_object, sub_menu_selection, chosen_item_name):
        chosen_item = self.gc_input.inventory_manager.gc_input.game_state.gd.item_data_list[chosen_item_name]

        if not inventory_menu_object.action_doing:
            if sub_menu_selection == "Use":
                inventory_menu_object.action_doing = "Use"
                self.post_notice("Use how many " + chosen_item.name + "(s)?")
                self.gc_input.menu_controller.set_menu(NumberSelectionMenuGhost.BASE, {"master_menu": inventory_menu_object.BASE, "max_number": self.gc_input.inventory_manager.get_quantity_of_item(chosen_item.name), "min_number": 1})

            elif sub_menu_selection == "Toss":
                inventory_menu_object.action_doing = "Toss"
                self.post_notice("Toss how many " + chosen_item.name + "(s)?")
                self.gc_input.menu_controller.set_menu(NumberSelectionMenuGhost.BASE, {"master_menu": inventory_menu_object.BASE, "max_number": self.gc_input.inventory_manager.get_quantity_of_item(chosen_item.name), "min_number": 1})

            elif sub_menu_selection == "Cancel":
                self.gc_input.menu_controller.exit_all_menus()
        else:
            if inventory_menu_object.action_doing == "Use":
                self.gc_input.inventory_manager.use_item(chosen_item, sub_menu_selection)

            elif inventory_menu_object.action_doing == "Toss":
                self.toss_item(chosen_item, sub_menu_selection)

            inventory_menu_object.action_doing = None
            self.gc_input.menu_controller.exit_all_menus()

    def toss_item(self, item, number_to_toss):
        self.gc_input.inventory_manager.remove_item(item, number_to_toss)
        self.post_notice("You tossed " + str(number_to_toss) + " " + item.name + "(s)")

    def start_menu_selection(self, item_selected):
        menu_selection = item_selected
        if menu_selection == "Bag":
            self.gc_input.menu_controller.exit_menu(StartMenuGhost.BASE)
            self.gc_input.menu_controller.set_menu(SuppliesInventoryMenuGhost.BASE, None)

        elif menu_selection == "Guide":
            self.gc_input.menu_controller.exit_menu(StartMenuGhost.BASE)
            self.gc_input.menu_controller.set_menu(GuideMenuGhost.BASE, None)

        elif menu_selection == "Profile":
            pass

        elif menu_selection == "Map":
            self.gc_input.menu_controller.exit_menu(StartMenuGhost.BASE)
            self.gc_input.menu_controller.set_menu(MapMenuGhost.BASE, None)

        elif menu_selection == "Options":
            pass

        elif menu_selection == "Gallery":
            self.gc_input.menu_controller.exit_menu(StartMenuGhost.BASE)
            self.gc_input.menu_controller.set_menu(GalleryMenuGhost.BASE, None)

        elif menu_selection == "Records":
            pass

        elif menu_selection == "Outfits":
            self.gc_input.menu_controller.exit_menu(StartMenuGhost.BASE)
            self.gc_input.menu_controller.set_menu(OutfitMenuGhost.BASE, None)

        elif menu_selection == "Save":
            pass

        elif menu_selection == "Exit":
            self.gc_input.menu_controller.exit_all_menus()

        else:
            self.gc_input.menu_controller.exit_all_menus()

    def conversation_options_menu_selection(self, item_selected):
        menu_selection = item_selected
        current_menu = self.gc_input.game_state.ms.get_menu_ghost(ConversationOptionsMenuGhost.BASE)
        phrase_list = ["base_phrase", "good_gift_phrase", "bad_gift_phrase", "neutral_gift_phrase", "bird_hint_phrase"]
        selected_phrase = getattr(self.gc_input.game_state.get_feature_ghost(current_menu.speaker_unique_name), choice(phrase_list))
        # selected_phrase = self.gs.get_feature_ghost(current_menu.speaker_unique_name).base_phrase
        details = {"speaker_name": current_menu.talking_to,
                   "friendship_level": current_menu.friendship,
                   "face_image": current_menu.face_image,
                   "speaker_unique_name": current_menu.speaker_unique_name,
                   "phrase": [selected_phrase]}

        if menu_selection == "Talk":
            self.gc_input.menu_controller.set_menu(ChatMenuGhost.BASE, details)

        elif menu_selection == "Give Gift":
            details["master_menu"] = current_menu.BASE
            # self.gc_input.menu_controller.exit_menu(ConversationOptionsMenuGhost.BASE)

            self.gc_input.menu_controller.set_menu(GiftGivingMenuGhost.BASE, details)

        elif menu_selection == "Exit":
            self.gc_input.menu_controller.exit_all_menus()

        else:
            self.gc_input.menu_controller.exit_all_menus()

    def chat_menu_selection(self, item_selected):
        self.gc_input.menu_controller.exit_all_menus()

    def post_notice(self, phrase):
        self.gc_input.game_state.ms.get_menu_ghost(GameActionDialogueMenuGhost.BASE).show_dialogue(phrase)

    def set_menu(self, menu_name, details):
        selected_menu = self.gc_input.game_state.ms.get_menu_ghost(menu_name)
        menu_type = selected_menu.menu_type

        if menu_type == Types.BASE:
            selected_menu.prepare_menu_for_display(details)

        elif menu_type == Types.SECONDARY:
            selected_menu.set_master_menu(details["master_menu"])
            selected_menu.prepare_menu_for_display(details)

        elif menu_type == Types.SUB:
            selected_menu.set_master_menu(details["master_menu"])
            selected_menu.prepare_menu_for_display(details)
            information_from_ghost = selected_menu.generate_menu_information_package()
            self.gc_input.game_view.update_sub_menu_display_details(menu_name, details["master_menu"], information_from_ghost)

        if menu_name == ChatMenuGhost.BASE:
            selected_menu.set_current_phrase(details["phrase"])

        self.gc_input.set_active_keyboard_manager(InMenuKeyboardManager.ID)
        selected_menu.gc_input.game_state.ms.add_menu_to_stack(menu_name)

    def next_menu(self, current_menu):
        total_number_menus = len(self.gc_input.game_state.ms.start_menu_stack)
        current_menu_index = self.gc_input.game_state.ms.start_menu_stack.index(current_menu)
        self.exit_menu(self.gc_input.game_state.ms.start_menu_stack[current_menu_index])
        next_menu = self.gc_input.game_state.ms.start_menu_stack[0]
        if current_menu_index != (total_number_menus - 1):
            next_menu = self.gc_input.game_state.ms.start_menu_stack[current_menu_index + 1]
        else:
            pass
        self.set_menu(next_menu, None)

    def previous_menu(self, current_menu):
        total_number_menus = len(self.gc_input.game_state.ms.start_menu_stack)
        current_menu_index = self.gc_input.game_state.ms.start_menu_stack.index(current_menu)
        self.exit_menu(self.gc_input.game_state.ms.start_menu_stack[current_menu_index])
        previous_menu = self.gc_input.game_state.ms.start_menu_stack[current_menu_index-1]
        if current_menu_index == 0:
            previous_menu = self.gc_input.game_state.ms.start_menu_stack[total_number_menus - 1]
        else:
            pass
        self.set_menu(previous_menu, None)

    def exit_menu(self, menu_name):
        selected_menu = self.gc_input.game_state.ms.get_menu_ghost(menu_name)
        selected_menu.reset_elements()
        self.gc_input.game_state.ms.deactivate_menu(menu_name)

    def exit_all_menus(self):
        list = []
        for x in self.gc_input.game_state.ms.menu_stack:
            list.append(x)
        for item in list:
            self.exit_menu(item)

    def resize_sub_menu(self):
        pass


class SceneManager(object): #TODO: Work on this mess!!
    def __init__(self, gc_input):
        self.gc_input = gc_input
        self.scene_list = {}
        self.animation_list = {"pan_down_3": CameraPanAnimation()}
        self.player_movement_x = 0
        self.player_movement_y = 0

    def play_scene(self):
        self.gc_input.set_active_keyboard_manager(InSceneKeyboardManager.ID)

    def end_scene(self):
        self.gc_input.set_active_keyboard_manager(InGameKeyboardManager.ID)

    def pan_camera(self, direction, number_of_tiles):
        self.animation_list["pan_down_3"].set_animation(direction, number_of_tiles)
        self.player_movement_x = number_of_tiles
        self.gc_input.add_to_scene_anim_in_progress("pan_down_3")

    def blank_out_character(self, character_name):
        pass

    def scene_end_character_movements(self, movement_dict):
        movement_dict = {"player": [self.player_movement_x, self.player_movement_y]}
        player_object = self.gc_input.game_state.get_player_ghost()
        x_change = player_object.x - movement_dict["player"][0]
        y_change = player_object.y - movement_dict["player"][1]
        # self.change_player_facing(door.exit_direction)
        current_room_object = self.gc_input.game_state.get_current_room()
        self.gc_input.position_manager.move_ghost(player_object, current_room_object, current_room_object, x_change, y_change)
        self.gc_input.position_manager.match_player_elevation_to_target(current_room_object, x_change, y_change)
        # self.gc_input.game_view.manually_update_camera(x_change, y_change)
