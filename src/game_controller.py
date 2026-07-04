import copy
import csv
import os
import random
import time
from random import choice

from animations_page_view_page import CameraPanAnimation, Switch
from input_manager_controller_page import *
from definitions import Direction, Types, GameSettings, Mundane
from menu_ghosts_data_page import ConversationOptionsMenuGhost, StatMenuGhost, AcquireMenuGhost, SubMenuGhost, NumberSelectionMenuGhost, KeyInventoryMenuGhost, SuppliesInventoryMenuGhost, GameActionDialogueMenuGhost, ChatMenuGhost, MapMenuGhost, GalleryMenuGhost, PictureMenuGhost, GiftGivingMenuGhost, GuideMenuGhost
from position_manager_state_page import Room, PositionManager
from game_state import GameState, GameData
from game_view import GameView, OutfitManager
from scenes import Scene


class Game(object):
    def __init__(self):
        self.game_running = True
        self.gs = GameState(None, None, None)  # type: GameState
        self.game_data = GameData()  # type: GameData
        self.game_view = GameView(self.game_data, self.gs)  # type: GameView
        self.game_controller = GameController(self, self.game_view, self.gs, self.game_data)  # type: GameController
        self.gs.gc = self.game_controller
        self.gs.gv = self.game_view
        self.gs.gd = self.game_data
        self.gs.ms.gd = self.game_data
        self.game_events = GameEvents(self.game_controller)


class GameEvents(object):
    def __init__(self, game_controller):
        self.gc = game_controller  # type: GameController
        self.previous_time = time.time()
        self.delta_time = 0
        self.timer_list = []
        self.event_dict = {.004: [self.gc.act_on_key_down_cue, self.gc.gs.act_on_action_queue, self.gc.game_view.animation_manager.ask_animator_to_animate, self.gc.game_view.animation_manager.ask_scene_to_animate, self.gc.check_if_run_held],
                            2: [self.gc.cowboy_action],
                           .25: [self.gc.game_view.switch_tile_frame],
                           .75: [self.gc.switch_flash],
                            1: [self.gc.gs.game_clock_pass_1_minute],
                           1: [self.gc.rotate_birds],
                           4: [self.gc.actor_event_popoff]}
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
        self.gs = game_state  # type: GameState
        self.game_data = game_data  # type: GameData

        self.active_keyboard_manager = None
        self.running_number = 1
        self.key_down_queue = []
        # self.held_keys = [pygame.K_x]
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
        self.rotation_number = 0

    # region GAME CONTROLS
    def set_active_keyboard_manager(self, active_manager_id):
        self.active_keyboard_manager = self.game_view.game_data.keyboard_manager_data_list[active_manager_id]

    def close_game(self):
        self.game.game_running = False

    def load_feature(self, unique_name, ghost_object, avatar_object):
        self.gs.add_feature_ghost(unique_name, ghost_object)
        self.game_view.add_feature_avatar(unique_name, avatar_object)
    # endregion

    def rotate_birds(self):
        direction = Direction.LEFT
        if self.rotation_number == 0:
            direction = Direction.LEFT
            self.rotation_number = 1
        elif self.rotation_number == 1:
            direction = Direction.UP
            self.rotation_number = 2
        elif self.rotation_number == 2:
            direction = Direction.RIGHT
            self.rotation_number = 3
        elif self.rotation_number == 3:
            direction = Direction.DOWN
            self.rotation_number = 0
        bird_list = ["Vulture", "Stellar_Jay", "Canada_Jay", "Towhee", "Warbler", "Mallard", "Crow", "Seagull", "Quail", "Pigeon", "Song_Sparrow", "Cormorant", "Jay"]
        birds_in_room = self.gs.get_all_features_in_room("Habitat_Room")
        birds_in_room = birds_in_room + self.gs.get_all_features_in_room("Staging_Area")
        for feature in birds_in_room:
            if feature.feature_subtype == Types.BIRD:
                if feature.species in bird_list:
                    self.gs.change_feature_facing(feature.unique_name, direction)

    def initiate_action(self, actor_ghost, action_object):
    # if not self.check_if
        self.gs.add_to_action_queue(actor_ghost.unique_name, action_object)

    def cowboy_action(self):
        unique_name = "Cowboy_6"
        if unique_name not in self.gs.action_queue.keys():
            ghost_object = self.gs.get_feature_ghost(unique_name)
            if not ghost_object.check_if_busy():
                self.initiate_action(ghost_object, Switch())


    # region ITEM USE METHODS (mermaid crown, ghost eye)
    def activate_mermaid_crown(self):
        self.clear_key_down_cue()
        self.gs.using_mermaid_crown = True
        self.gs.mermaid_crown_initiation = [self.gs.get_player_ghost_location()[0], self.gs.get_player_ghost_location()[1]]
        self.gs.mermaid_crown_counter = 0
        self.gs.update_accessible_terrains([1], [])

    def activate_ghost_eye(self):
        player_ghost = self.gs.get_player_ghost()
        self.clear_key_down_cue()
        self.gs.using_ghost_eye = True
        self.gs.ghost_eye_initiation = [self.gs.get_player_ghost_location()[0], self.gs.get_player_ghost_location()[1]]
        self.gs.ghost_eye_counter = 0
        self.gs.ghost_eye_initiation_facing = copy.copy(player_ghost.facing)
        husk_ghost = self.create_husk(self.gs.get_current_room(), player_ghost.x, player_ghost.y, player_ghost.facing, "green_shirt")
        self.gs.ghost_eye_husk_name = husk_ghost.unique_name
        self.outfit_manager.put_on_temporary_outfit("ghost_eye")
        self.set_active_keyboard_manager(GhostEyeKeyboardManager.ID)

    def create_husk(self, room_object, x, y, facing, outfit):
        feature_dict = {"species": "Husk", "display_name": "Husk", "function": "None", "spawn_room": room_object.room_name, "spawn_x": str(x), "spawn_y": str(y), "spawn_facing": Mundane.get_word_from_direction(facing), "spawn_active": "no"}
        ghost_install = self.gs.install_element(feature_dict)
        ghost_install.active = True
        return ghost_install

    def deactivate_ghost_eye(self):
        self.clear_key_down_cue()
        x_change = self.gs.get_player_ghost_location()[0]-self.gs.ghost_eye_initiation[0]
        y_change = self.gs.get_player_ghost_location()[1]-self.gs.ghost_eye_initiation[1]
        self.gs.change_player_facing(self.gs.ghost_eye_initiation_facing)
        direction_x = Direction.LEFT
        if x_change < 0:
            direction_x = Direction.RIGHT
        direction_y = Direction.UP
        if y_change < 0:
            direction_y = Direction.DOWN
        self.scene_manager.play_scene(Scene(self, [("animation", CameraPanAnimation(direction_x, x_change)), ("animation", CameraPanAnimation(direction_y, y_change)), ("action", "delete_husk"), ("action", "ghost_eye_followup")]))

    def execute_action_from_animator(self, action_name):
        if action_name == "delete_husk":
            husk = self.gs.get_feature_ghost(self.gs.ghost_eye_husk_name)
            self.position_manager.despawn_feature(husk.unique_name, self.gs.get_current_room())
        elif action_name == "ghost_eye_followup":
            self.outfit_manager.put_on_outfit(self.gs.revert_outfit)
            self.gs.change_player_facing(self.gs.ghost_eye_initiation_facing)
            self.gs.using_ghost_eye = False
            self.gs.ghost_eye_initiation = [0, 0]
            self.gs.ghost_eye_counter = 0
            self.set_active_keyboard_manager(InGameKeyboardManager.ID)


    def determine_mermaid_crown_end(self):
        if self.gs.using_mermaid_crown:
            if self.position_manager.get_tile_terrain(self.gs.get_current_room().room_name, self.gs.get_player_ghost_location()[0], self.gs.get_player_ghost_location()[1]) == 1:
                self.deactivate_mermaid_crown()
            else:
                self.cancel_mermaid_crown()

    def determine_ghost_eyes_end(self):
        if self.gs.using_ghost_eye:
            self.deactivate_ghost_eye()

    def deactivate_mermaid_crown(self):
        self.clear_key_down_cue()
        x_change = self.gs.get_player_ghost_location()[0]-self.gs.mermaid_crown_initiation[0]
        y_change = self.gs.get_player_ghost_location()[1]-self.gs.mermaid_crown_initiation[1]
        direction_x = Direction.LEFT
        if x_change < 0:
            direction_x = Direction.RIGHT
        direction_y = Direction.UP
        if y_change < 0:
            direction_y = Direction.DOWN
        self.scene_manager.play_scene(Scene(self, [("animation", CameraPanAnimation(direction_x, x_change)), ("animation", CameraPanAnimation(direction_y, y_change))]))
        self.gs.using_mermaid_crown = False
        self.gs.mermaid_crown_initiation = [0, 0]
        self.gs.mermaid_crown_counter = 0
        self.gs.update_accessible_terrains([], [1])
        self.outfit_manager.put_on_outfit(self.gs.revert_outfit)

    def cancel_mermaid_crown(self):
        self.outfit_manager.put_on_outfit(self.gs.revert_outfit)
        self.gs.using_mermaid_crown = False
        self.gs.mermaid_crown_initiation = [0, 0]
        self.gs.mermaid_crown_counter = 0
        self.gs.update_accessible_terrains([], [1])
    # endregion ( (

    # region SOUNDS
    def play_sound(self, queue_name):
        sound_name = self.gs.gd.sound_reference_dict[queue_name]
        self.gs.gd.get_sound(sound_name).play()
    # endregion

    # region text controls
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
    # endregion

    # region TOOL USE
    def check_if_pickaxe_worked(self):
        result = False
        player = self.gs.get_player_ghost()
        room = self.gs.get_current_room()
        cube = self.position_manager.get_adjacent_tile(player, player.facing, room)

        tile_name = room.room_name + "_" + str(cube.x) + "_" + str(cube.y)
        pickaxe_doors_list = self.gs.pickaxe_door_dict.keys()

        if player.facing == Direction.UP:
            if tile_name in pickaxe_doors_list:
                result = True

        return result

    def pickaxe_make_door(self):
        player = self.gs.get_player_ghost()
        room = self.gs.get_current_room()
        cube = self.position_manager.get_adjacent_tile(player, player.facing, room)

        tile_name = room.room_name + "_" + str(cube.x) + "_" + str(cube.y)
        pickaxe_dict_selection = self.gs.pickaxe_door_dict[tile_name]
        door_add_result_dict = self.position_manager.add_door(pickaxe_dict_selection[3], room.room_name, pickaxe_dict_selection[0], cube.x, cube.y, pickaxe_dict_selection[1], pickaxe_dict_selection[2])
        doorway1_ghost = door_add_result_dict["doorway1"]
        doormat1_ghost = door_add_result_dict["doormat1"]
        if doorway1_ghost is not None:
            doorway1_ghost.active = True
        if doormat1_ghost is not None:
            doormat1_ghost.active = True

        self.gs.pickaxe_door_dict.pop(tile_name)
        self.play_sound("pickaxe_success")

        self.gs.gc.menu_controller.post_notice("You found a door!")

    def use_selected_tool(self):
        if self.gs.selected_tool != "None":
            tool = self.inventory_manager.gc.gs.gd.key_item_data_list[self.gs.selected_tool]
            self.inventory_manager.use_key_item(tool)
        else:
            self.gs.gc.menu_controller.post_notice("There is nothing selected")
    # endregion

    def actor_event_popoff(self):
        feature_name = "Stellar_Jay_326"
        feature_ghost = self.gs.get_feature_ghost(feature_name)
        feature_avatar = self.gs.gv.get_feature_avatar(feature_name)
        if (feature_name in self.gs.feature_ghost_list.keys()) and feature_ghost.active:
            already_animating = self.check_if_feature_already_animating(feature_name)
            if not already_animating:
                if feature_avatar.option == 1:
                    feature_avatar.initiate_animation("up_down")
                    self.game_view.animation_manager.add_to_anim_in_progress(feature_name)
                    feature_avatar.option = 0
                elif feature_avatar.option == 0:
                    feature_avatar.initiate_animation("look_around")
                    self.game_view.animation_manager.add_to_anim_in_progress(feature_name)
                    feature_avatar.option = 1


        # feature = self.gs.get_feature_ghost("Pigeon_142")
        # if ("Pigeon_142" in self.gs.feature_ghost_list.keys()) and feature.active:
        #     self.move_feature_chaotically("Pigeon_142")
        pass

    # region INTERACT WITH OBJECTS (package, basket)
    def player_interact(self):
        player = self.gs.get_player_ghost()
        room = self.gs.get_current_room()
        full = self.position_manager.check_if_adjacent_tiles_full(player, player.facing, room)
        if full:
            cube = self.position_manager.get_adjacent_tile(player, player.facing, room)
            feature = self.gs.get_feature_ghost(cube.filling_unique_name)
            if feature.feature_type == Types.ACTOR:
                if not feature.check_if_busy():
                    if feature.feature_subtype == Types.BIRD:
                        self.gs.gc.menu_controller.post_notice("You shouldn't touch wild animals.")
                    else:
                        self.talk_to_character(cube.filling_unique_name, player.facing)
            elif feature.feature_type == Types.PROP:
                self.talk_to_prop(cube.filling_unique_name, player.facing)
            else:
                pass

    def talk_to_character(self, character_talking_to, player_direction):
        direction_to_turn = Direction.DOWN
        if player_direction == Direction.DOWN:
            direction_to_turn = Direction.UP
        elif player_direction == Direction.UP:
            direction_to_turn = Direction.DOWN
        elif player_direction == Direction.LEFT:
            direction_to_turn = Direction.RIGHT
        elif player_direction == Direction.RIGHT:
            direction_to_turn = Direction.LEFT

        character_talking_to_ghost = self.gs.feature_ghost_list[character_talking_to]
        character_talking_to_avatar = self.game_view.feature_avatar_list[character_talking_to]
        self.gs.change_feature_facing(character_talking_to, direction_to_turn)
        character_talking_to_ghost.currently_chatting = True
        self.gs.gc.menu_controller.post_notice("You talked to " + self.gs.get_feature_display_name(character_talking_to_ghost.unique_name))
        details = {"speaker_name": self.gs.get_feature_display_name(character_talking_to_ghost.unique_name),
                   "friendship_level": character_talking_to_ghost.friendship_level,
                   "face_image": character_talking_to_avatar.face_image,
                   "speaker_unique_name": character_talking_to_ghost.unique_name}

        self.gs.gc.menu_controller.set_menu(ConversationOptionsMenuGhost.BASE, details)

    def talk_to_prop(self, prop_talking_to, player_direction):
        prop_talking_to_ghost = self.gs.feature_ghost_list[prop_talking_to]
        prop_talking_to_avatar = self.game_view.feature_avatar_list[prop_talking_to]
        prop_talking_to_ghost.get_interacted_with()
        details = {}

    def snap_photo(self):
        facing = self.gs.get_player_ghost().facing
        if not self.check_if_player_already_animating():
            direction = Mundane.direction_feedback(facing, "left", "right", "up", "down")
            vector_x = Mundane.direction_feedback(facing, -1, 1, 0, 0)
            vector_y = Mundane.direction_feedback(facing, 0, 0, -1, 1)
            self.game_view.player_avatar.initiate_animation("snap_photo_" + direction)

            camera_range = 2
            pl = self.gs.get_player_ghost_location()
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
                ghost = self.gs.get_feature_ghost(result)
                self.gs.gc.menu_controller.post_notice("Snapped a pic of a " + ghost.display_name)
                gallery_menu = self.gs.ms.get_menu_ghost(GalleryMenuGhost.BASE)
                if ghost.feature_subtype == Types.BIRD and not gallery_menu.check_if_item_in_list("Bird", ghost.species) and not ghost.species == "Pigeon":
                    gallery_menu.add_to_item_list("Bird", ghost.species, ghost.display_name)
                    self.gs.gc.menu_controller.post_notice("Added " + ghost.display_name + " to gallery!")
                elif ghost.species == "Pigeon":
                    # TODO: START HERE
                    gallery_menu.add_to_item_list("Tree", ghost.species, ghost.display_name)
                elif ghost.feature_subtype == Types.TREE and not gallery_menu.check_if_item_in_list("Tree", ghost.species):
                    gallery_menu.add_to_item_list("Tree", ghost.species, ghost.display_name)
                    self.gs.gc.menu_controller.post_notice("Added " + ghost.display_name + " to gallery!")
            else:
                self.gs.gc.menu_controller.post_notice("There was nothing there")

    def pick_up_package(self, type, package_unique_name, room_name, package_items):

        room_object = self.gs.get_room(room_name)
        ghost = self.gs.get_feature_ghost(package_unique_name)
        ghost.spawn_active = False
        self.position_manager.despawn_feature(package_unique_name, room_object)
        item_type_result = None
        for item in package_items:
            if type == "Package":
                item_type_result = self.inventory_manager.get_key_or_temp_item(item, 1)
                self.menu_controller.post_notice("Added " + item + " to your bag.")
            if type == "Page":
                self.menu_controller.post_notice("Added " + item + " to your Guide.")
                self.inventory_manager.get_page(item)

    def look_in_basket(self, basket_unique_name, basket_items):
        if basket_items:
            ghost = self.gs.get_feature_ghost(basket_unique_name)
            self.menu_controller.post_notice("You looked in the " + ghost.species)
            details = {"item_list": basket_items, "basket_unique_name": basket_unique_name}
            self.menu_controller.set_menu(AcquireMenuGhost.BASE, details)
        else:
            self.menu_controller.post_notice("It appears to be empty.")

    def take_from_basket(self, basket_unique_name, name_item_taken):
        self.inventory_manager.get_key_or_temp_item(name_item_taken, 1)
        self.menu_controller.post_notice("You took the " + name_item_taken)
        ghost = self.gs.get_feature_ghost(basket_unique_name)
        ghost.function_items.remove(name_item_taken)
    # endregion

    # region FEATURE MOVEMENT
    def check_if_player_already_animating(self):
        return self.game_view.player_avatar.currently_animating

    def check_for_tile_transition(self, room_object, current_x, current_y, target_x, target_y):
        result = False
        current_tile_terrain = self.position_manager.get_tile_terrain(room_object.room_name, current_x, current_y)
        target_tile_terrain = self.position_manager.get_tile_terrain(room_object.room_name, target_x, target_y)
        if current_tile_terrain != target_tile_terrain:
            if target_tile_terrain == 1:
                self.outfit_manager.put_on_temporary_outfit("Mermaid")
            elif current_tile_terrain == 1:
                self.cancel_mermaid_crown()
        else:
            if target_tile_terrain != 1:
                if self.gs.using_mermaid_crown:
                    self.cancel_mermaid_crown()

    def initiate_player_movement(self, direction):
        room_object = self.game_view.game_data.room_data_list[self.gs.current_room]
        target_tile = self.position_manager.get_adjacent_tile(self.gs.player_ghost, direction, room_object)
        self.gs.change_player_facing(direction)
        move_status = self.position_manager.check_if_player_can_move(direction, self.gs.player_ghost, room_object)[0]
        door_status = self.position_manager.check_if_player_can_move(direction, self.gs.player_ghost, room_object)[1]
        if door_status:
            self.go_through_door(room_object.room_name + "_" + str(target_tile.x) + "_" + str(target_tile.y))
        elif not door_status:
            if move_status:
                player = self.gs.get_player_ghost()
                self.game_view.walk_player_avatar(direction)
                self.check_for_tile_transition(room_object, player.x, player.y, target_tile.x, target_tile.y)
                self.position_manager.move_ghost(player, room_object, room_object, player.x + Direction.get_vector_from_direction(direction)[0], player.y + Direction.get_vector_from_direction(direction)[1])
                self.player_moved_followup(player.x, player.y)
            else:
                pass

    def initiate_spirit_movement(self, direction):
        room_object = self.game_view.game_data.room_data_list[self.gs.current_room]
        target_tile = self.position_manager.get_adjacent_tile(self.gs.player_ghost, direction, room_object)
        self.gs.change_player_facing(direction)
        move_test = self.position_manager.check_if_spirit_can_move(direction, self.gs.player_ghost, room_object)
        if move_test:
            player = self.gs.get_player_ghost()
            self.game_view.walk_player_avatar(direction)
            self.position_manager.move_spirit_ghost(player, room_object, room_object, player.x + Direction.get_vector_from_direction(direction)[0], player.y + Direction.get_vector_from_direction(direction)[1])
            self.spirit_moved_followup(player.x, player.y)

    def spirit_moved_followup(self, player_x, player_y):
        self.trigger_manager.check_for_map_triggers(player_x, player_y)
        if self.gs.using_ghost_eye:
            self.gs.ghost_eye_counter += 1
            if self.gs.ghost_eye_counter == self.gs.ghost_eye_limit:
                self.deactivate_ghost_eye()


    def player_moved_followup(self, player_x, player_y):
        if self.gs.gc.position_manager.get_tile_terrain(self.gs.get_current_room().room_name, player_x, player_y) == 1:
            self.gs.gc.play_sound("mermaid_swim")
        self.trigger_manager.check_for_map_triggers(player_x, player_y)
        if self.gs.using_mermaid_crown:
            self.gs.mermaid_crown_counter += 1
            if self.gs.mermaid_crown_counter == self.gs.mermaid_crown_limit:
                self.deactivate_mermaid_crown()
        if self.gs.using_ghost_eye:
            self.gs.ghost_eye_counter += 1
            if self.gs.ghost_eye_counter == self.gs.ghost_eye_limit:
                self.deactivate_ghost_eye()

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
        feature_ghost = self.gs.get_feature_ghost(feature_unique_name)
        feature_avatar = self.game_view.get_feature_avatar(feature_unique_name)

        already_animating = self.check_if_feature_already_animating(feature_unique_name)
        doable = self.check_if_action_doable(feature_ghost, action_name)[0]
        direction = self.check_if_action_doable(feature_ghost, action_name)[1]
        vector = Direction.get_vector_from_direction(direction)
        room_object = self.gs.get_room(feature_ghost.spawn_room)
        if not already_animating:
            if doable:
                success = True
                feature_avatar.initiate_animation(action_name)
                self.game_view.animation_manager.add_to_anim_in_progress(feature_unique_name)
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
        room_object = self.gs.get_room(feature_ghost.spawn_room)
        can_move = self.position_manager.check_if_feature_can_move(feature_ghost, direction, room_object)
        return can_move, direction

    def get_avatar_class(self, avatar_type):
        return self.game_view.avatar_classes[avatar_type]

    def check_if_feature_already_animating(self, unique_name):
        avatar = self.game_view.get_feature_avatar(unique_name)
        ghost_object = self.gs.get_feature_ghost(unique_name)
        return ghost_object.currently_animating

    def reset_feature_to_spawn(self, feature):
        chosen_feature = self.gs.get_feature_ghost(feature)
        chosen_feature.reset_to_spawn()
    # endregion

    def update_view(self):
        current_room = self.gs.get_current_room().room_name
        drawables_list = self.game_view.get_drawables_list(self.gs.get_feature_locations()[0], self.gs.get_feature_locations()[1], self.game_view.get_independent_anim_locations())
        self.game_view.draw_all(drawables_list, current_room)

        self.menu_controller.update_stat_menus()
        for menu in (self.gs.ms.static_menus + self.gs.ms.visible_menus):
            ghost = self.gs.ms.menu_ghost_data_list[menu + "_ghost"]
            avatar_display_details = self.game_view.menu_avatar_data_list[menu + "_avatar"].menu_display_details
            self.game_view.draw_special_menu(menu, ghost.generate_menu_information_package(), avatar_display_details["coordinates"][0], avatar_display_details["coordinates"][1])

    # region INPUT EVENTS
    def clear_key_down_cue(self):
        self.key_down_queue = []

    def add_to_held_key(self, key):
        self.held_keys.append(key)

    def get_held_keys(self):
        return self.held_keys

    def check_if_run_held(self):
        held = self.get_held_keys()
        if pygame.K_x in held:
            self.running_number = 0
        else:
            self.running_number = 1

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
                    print(self.active_keyboard_manager.ID, InGameKeyboardManager.ID)
                if self.active_keyboard_manager.ID == InGameKeyboardManager.ID:
                    self.initiate_player_movement(direction)
                elif self.active_keyboard_manager.ID == GhostEyeKeyboardManager.ID:
                    self.initiate_spirit_movement(direction)

    # endregion

    # region IMPORT FUNCTIONS
    def import_classes_from_csv(self, filename):
        feature_data = self.process_features_from_csv(filename)
        for feature_dict in feature_data:
            self.gs.create_feature_ghost_class(feature_dict)

    def import_map_objects_from_csv(self, filename, room_name):
        map = []
        int_map = []
        with open(os.path.join(filename), mode='r', encoding='utf-8-sig') as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))
        for row in map:
            int_list = [int(i) for i in row]
            int_map.append(int_list)

        feature_reference_dict = {0: "Pine", 1: "Apple_Tree", 2: "Oak", 3: "Arbutus", 4: "Rock", 5: "Small_Rock", 6: "Small_Craig"}

        feature_list = []

        row_counter = 0
        for row in int_map:
            row_counter += 1
            item_counter = 0
            for item in row:
                item_counter += 1
                if item in feature_reference_dict.keys():
                    x = item_counter
                    y = row_counter
                    feature_list.append((x, y, feature_reference_dict[item]))

        feature_dict = {"species": 1, "display_name": 1, "function": "None", "spawn_room": 1, "spawn_x": 1, "spawn_y": 1, "spawn_facing": "Down", "spawn_active": "yes"}

        for item in feature_list:
            object_class = self.gs.gd.get_feature_class(item[2])
            spawn_facing = Direction.DOWN
            unique_name = item[2] + "_" + str(GameSettings.get_unique_ID())
            feature_ghost_object = object_class(self.gs, unique_name, "None", room_name, item[0], item[1],  spawn_facing, "yes")

            self.gs.add_feature_ghost(unique_name, feature_ghost_object)
            test = self.gs.get_feature_ghost(unique_name)

    def import_pages_from_csv(self, filename):
        feature_data = self.process_features_from_csv(filename)

        return feature_data

    def import_characters_from_csv(self, filename):
        feature_data = self.process_features_from_csv(filename)

        for feature_dict in feature_data:
            object_class = self.gs.gd.get_feature_class(feature_dict["species"])
            spawn_facing = self.gs.direction_translations[feature_dict["spawn_facing"]]
            unique_name = feature_dict["species"] + "_" + str(GameSettings.get_unique_ID())
            feature_ghost_object = object_class(self.gs, unique_name, feature_dict["function"], feature_dict["spawn_room"], int(feature_dict["spawn_x"]), int(feature_dict["spawn_y"]),  spawn_facing, feature_dict["spawn_active"])
            self.gs.add_feature_ghost(unique_name, feature_ghost_object)
            test = self.gs.get_feature_ghost(unique_name)

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

    # endregion

    # region ROOM MANAGEMENT
    def reset_room(self, room_name):
        room_object = self.gs.get_room(room_name)
        self.position_manager.despawn_all_room_elements(room_object)
        self.position_manager.clear_room_grid(room_name)
        self.trigger_manager.remove_all_triggers(room_object)

    def load_up_room(self, room_name):
        room_object = self.gs.get_room(room_name)
        self.position_manager.spawn_all_initial_room_elements(room_object)
        self.position_manager.add_player_to_grid(room_name)
        self.gs.set_room(room_name)

    def change_room(self, room_going_to):
        current_room = self.gs.get_current_room()
        self.reset_room(current_room.room_name)
        self.load_up_room(room_going_to)

    def get_door(self, door_name):
        return self.game_data.door_data_list[door_name]

    def go_through_door(self, door_name):
        player_object = self.gs.get_player_ghost()
        self.clear_key_down_cue()
        door = self.get_door(door_name)
        x_change = door.x_to - player_object.x
        y_change = door.y_to - player_object.y
        self.gs.change_player_facing(door.exit_direction)
        current_room_object = self.gs.get_room(door.room_from)
        new_room_object = self.gs.get_room(door.room_to)
        self.position_manager.move_ghost(player_object, current_room_object, new_room_object, door.x_to, door.y_to)
        self.position_manager.match_player_elevation_to_target(new_room_object, door.x_to, door.y_to)
        self.game_view.manually_update_camera(x_change, y_change)
        self.change_room(door.room_to)
        self.play_sound("go_through_door")
    # endregion

    # region TRIGGER MANAGEMENT


    def trigger_a_bird(self, unique_name, room, trigger):
        if room.room_name != "Aviary_Room":
            bird_ghost = self.gs.get_feature_ghost(unique_name)
            bird_avatar = self.game_view.get_feature_avatar(unique_name)

            check_trigger_result = bird_ghost.check_trigger_result(trigger)

            if check_trigger_result == "remove":
                self.game_view.trigger_independent_animation("disappear_animation", bird_ghost.unique_name + "_disappear_animation", bird_ghost.unique_name, room, bird_avatar.drawing_priority, bird_avatar.image_x, bird_avatar.image_y, bird_avatar.image_offset_x, bird_avatar.image_offset_y)
                self.position_manager.despawn_feature(unique_name, room)
            else:
                pass
    # endregion


class InventoryManager(object):
    def __init__(self, gc):
        self.gc = gc  # type: GameController

    def get_key_or_temp_item(self, item_name, quantity):
        item_type = None
        item_list = self.gc.game_data.item_data_list
        key_item_list = self.gc.game_data.key_item_data_list
        if item_name in key_item_list.keys():
            self.gc.gs.acquire_key_item(item_name)
            item_type = "Key Item"
            self.gc.play_sound("acquire_key_item")
        elif item_name in item_list.keys():
            self.gc.gs.acquire_item(item_name, quantity)
            item_type = "Item"
        return item_type

    def fetch_page(self, page_name):
        return self.gc.gs.gd.bird_page_data_list[page_name]

    def get_page(self, page_name):
        self.gc.gs.held_pages.append(page_name)

    def get_item(self, item_name, quantity):
        item = self.gc.game_data.item_data_list[item_name]
        current_inventory = self.gc.gs.ms.get_menu_items_list("supplies_inventory_menu")
        if item.NAME in current_inventory:
            current_inventory[item.NAME]["quantity"] += quantity
        else:
            current_inventory[item.NAME] = {"name": item.NAME, "quantity": quantity}

    def use_item(self, item, quantity_used):
        current_inventory = self.gc.gs.ms.get_menu_items_list("supplies_inventory_menu")
        successes = 0
        for x in range(quantity_used):
            if self.check_if_can_use_item(item, quantity_used):
                successes += 1
                self.gc.gs.gd.item_data_list[item.NAME].item_use()
                current_inventory[item.NAME]["quantity"] -= 1
        if current_inventory[item.NAME]["quantity"] == 0:
            current_inventory.pop(item.NAME)

        if successes == 0:
            self.gc.gs.gc.menu_controller.post_notice("Could not use " + item.NAME)
        elif successes > 0:
            self.gc.gs.gc.menu_controller.post_notice("used " + str(successes) + " " + item.NAME + "(s)")

    def get_quantity_of_item(self, item_name):
        current_inventory = self.gc.gs.ms.get_menu_items_list("supplies_inventory_menu")
        quantity = current_inventory[item_name]["quantity"]
        return quantity

    def remove_item(self, item, quantity_removed):
        current_inventory = self.gc.gs.ms.get_menu_items_list("supplies_inventory_menu")
        if quantity_removed <= self.gc.gs.get_item_quantity(item.name):
            current_inventory[item.NAME]["quantity"] -= quantity_removed
        if current_inventory[item.NAME]["quantity"] == 0:
            current_inventory.pop(item.NAME)

    def check_if_can_use_item(self, item, quantity):
        success = True
        if quantity > self.gc.gs.get_item_quantity(item.name):
            success = False
        if not self.gc.gs.gd.item_data_list[item.NAME].use_requirements_met():
            success = False
        return success

    def check_if_can_use_key_item(self, item, details):
        chosen_item = self.gc.gs.gd.key_item_data_list[item.NAME]
        success = False
        message = None
        if chosen_item.use_requirements_met(details):
            success = True
            message = chosen_item.get_success_message(details)
        else:
            message = chosen_item.get_failure_message(details)
        return success, message

    def get_key_item(self, key_item):
        current_key_inventory = self.gc.gs.ms.get_menu_items_list("key_inventory_menu")
        if key_item.NAME in current_key_inventory:
            pass
        else:
            current_key_inventory[key_item.NAME] = {"name": key_item.NAME}

    def use_key_item(self, item):
        current_key_inventory = self.gc.gs.ms.get_menu_items_list("key_inventory_menu")
        successes = 0

        room = self.gc.gs.get_current_room()
        player = self.gc.gs.get_player_ghost()
        cube = room.access_adjacent_cube(player, player.facing)
        if not self.gc.position_manager.check_rooms_edges(player, player.facing, room):
            details = {"room": room, "cube": cube, "adjacent_tile_filling": cube.filling_unique_name, "filling_type": cube.filling_type, "filling_subtype": cube.filling_subtype, "adjacent_tile_terrain": self.gc.position_manager.get_tile_terrain(room.room_name, cube.x, cube.y)}
        else:
            details = {"room": room, "cube": cube, "adjacent_tile_filling": None, "filling_type": None, "filling_subtype": None, "adjacent_tile_terrain": None}

        result = self.check_if_can_use_key_item(item, details)[0]
        message = self.check_if_can_use_key_item(item, details)[1]

        if result:
            self.gc.gs.gd.key_item_data_list[item.NAME].item_use(details)
            successes += 1

        self.gc.gs.gc.menu_controller.post_notice(message)


class TriggerManager(object):
    def __init__(self, gc):
        self.gc = gc
        self.trigger_list = {}

    def setup_trigger_list(self):
        for room in self.gc.game_data.room_data_list.values():
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

    def check_for_map_triggers(self, player_x, player_y):
        room = self.gc.gs.get_current_room()
        triggers = copy.copy(self.check_for_triggers(room, player_x, player_y))
        for trigger in triggers:
            self.gc.trigger_a_bird(trigger[0], room, trigger[1])

    def check_for_triggers(self, room_object, x, y):
        return self.trigger_list[room_object.room_name][x, y]


class MenuController(object):
    def __init__(self, gc):
        self.gc = gc  # type: GameController
        self.menu_load_list = [StatMenuGhost, AcquireMenuGhost, StartMenuGhost, SubMenuGhost, NumberSelectionMenuGhost,
                               SuppliesInventoryMenuGhost, KeyInventoryMenuGhost, ConversationOptionsMenuGhost,
                               GameActionDialogueMenuGhost, GuideMenuGhost, QuizMenuGhost, ChatMenuGhost, GalleryMenuGhost, OutfitMenuGhost, MapMenuGhost, PictureMenuGhost, GiftGivingMenuGhost]

    def menu_cursor_down(self):
        active_menu = self.gc.gs.ms.menu_ghost_data_list[self.gc.gs.ms.menu_stack[0] + "_ghost"]
        active_menu.cursor_down()

    def menu_cursor_up(self):
        active_menu = self.gc.gs.ms.menu_ghost_data_list[self.gc.gs.ms.menu_stack[0] + "_ghost"]
        active_menu.cursor_up()

    def menu_cursor_left(self):
        active_menu = self.gc.gs.ms.menu_ghost_data_list[self.gc.gs.ms.menu_stack[0] + "_ghost"]
        active_menu.cursor_left()

    def menu_cursor_right(self):
        active_menu = self.gc.gs.ms.menu_ghost_data_list[self.gc.gs.ms.menu_stack[0] + "_ghost"]
        active_menu.cursor_right()

    def menu_choose_option(self):
        active_menu = self.gc.gs.ms.menu_ghost_data_list[self.gc.gs.ms.menu_stack[0] + "_ghost"]
        active_menu.choose_option()

    def activate_menu(self):
        pass

    def get_game_time_string(self):
        hour = self.gc.gs.hour_of_day
        minute = self.gc.gs.minute_of_hour
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

    def update_stat_menus(self):
        for menu in self.gc.gs.ms.static_menus:
            ghost = self.gc.gs.ms.get_menu_ghost(menu)
            ghost.prepare_menu_for_display()

    def get_stat_items(self):
        hour = self.gc.gs.hour_of_day
        minute = self.gc.gs.minute_of_hour

        stat_dict = {"Birds": str(self.gc.gs.bird_count),
                     "Pigeons": str(self.gc.gs.pigeon_count),
                     "time": self.gc.menu_controller.get_game_time_string(),
                     "day": str(self.gc.gs.day_of_summer),
                     "selected_tool": str(self.gc.gs.selected_tool)}

        return stat_dict

    def gift_menu_selection(self, sub_menu_selection, chosen_item_name, details):
        if sub_menu_selection == "Yes":
            chosen_item = self.gc.gs.gd.item_data_list[chosen_item_name]
            speaker = self.gc.gs.get_feature_ghost(details["speaker_unique_name"])

            self.gc.inventory_manager.remove_item(chosen_item, 1)
            self.gc.menu_controller.post_notice("You gave " + speaker.display_name + " a " + chosen_item.name)

            details["phrase"] = [speaker.receive_gift(chosen_item_name)]
            details["friendship_level"] = Mundane.get_friendship_hearts(speaker.friendship_level)
            self.gc.menu_controller.exit_all_menus()
            speaker.currently_chatting = True
            self.gc.menu_controller.set_menu(ChatMenuGhost.BASE, details)

        else:
            self.gc.menu_controller.exit_all_menus()

    def inventory_menu_selection(self, inventory_menu_object, sub_menu_selection, chosen_item_name):
        chosen_item = self.gc.inventory_manager.gc.gs.gd.item_data_list[chosen_item_name]

        if not inventory_menu_object.action_doing:
            if sub_menu_selection == "Use":
                inventory_menu_object.action_doing = "Use"
                self.post_notice("Use how many " + chosen_item.name + "(s)?")
                self.gc.menu_controller.set_menu(NumberSelectionMenuGhost.BASE, {"master_menu": inventory_menu_object.BASE, "max_number": self.gc.inventory_manager.get_quantity_of_item(chosen_item.name), "min_number": 1})

            elif sub_menu_selection == "Toss":
                inventory_menu_object.action_doing = "Toss"
                self.post_notice("Toss how many " + chosen_item.name + "(s)?")
                self.gc.menu_controller.set_menu(NumberSelectionMenuGhost.BASE, {"master_menu": inventory_menu_object.BASE, "max_number": self.gc.inventory_manager.get_quantity_of_item(chosen_item.name), "min_number": 1})

            elif sub_menu_selection == "Cancel":
                self.gc.menu_controller.exit_all_menus()
        else:
            if inventory_menu_object.action_doing == "Use":
                self.gc.inventory_manager.use_item(chosen_item, sub_menu_selection)

            elif inventory_menu_object.action_doing == "Toss":
                self.toss_item(chosen_item, sub_menu_selection)

            inventory_menu_object.action_doing = None
            self.gc.menu_controller.exit_all_menus()

    def toss_item(self, item, number_to_toss):
        self.gc.inventory_manager.remove_item(item, number_to_toss)
        self.post_notice("You tossed " + str(number_to_toss) + " " + item.name + "(s)")

    def start_menu_selection(self, item_selected):
        menu_selection = item_selected
        if menu_selection == "Bag":
            self.gc.menu_controller.exit_menu(StartMenuGhost.BASE)
            self.gc.menu_controller.set_menu(SuppliesInventoryMenuGhost.BASE, None)

        elif menu_selection == "Guide":
            self.gc.menu_controller.exit_menu(StartMenuGhost.BASE)
            self.gc.menu_controller.set_menu(GuideMenuGhost.BASE, None)

        elif menu_selection == "Profile":
            pass

        elif menu_selection == "Map":
            self.gc.menu_controller.exit_menu(StartMenuGhost.BASE)
            self.gc.menu_controller.set_menu(MapMenuGhost.BASE, None)

        elif menu_selection == "Options":
            pass

        elif menu_selection == "Gallery":
            self.gc.menu_controller.exit_menu(StartMenuGhost.BASE)
            self.gc.menu_controller.set_menu(GalleryMenuGhost.BASE, None)

        elif menu_selection == "Records":
            pass

        elif menu_selection == "Outfits":
            self.gc.menu_controller.exit_menu(StartMenuGhost.BASE)
            self.gc.menu_controller.set_menu(OutfitMenuGhost.BASE, None)

        elif menu_selection == "Save":
            pass

        elif menu_selection == "Exit":
            self.gc.menu_controller.exit_all_menus()

        else:
            self.gc.menu_controller.exit_all_menus()

    def conversation_options_menu_selection(self, item_selected):
        menu_selection = item_selected
        current_menu = self.gc.gs.ms.get_menu_ghost(ConversationOptionsMenuGhost.BASE)
        phrase_list = ["base_phrase", "good_gift_phrase", "bad_gift_phrase", "neutral_gift_phrase", "bird_hint_phrase"]
        selected_phrase = copy.copy(getattr(self.gc.gs.get_feature_ghost(current_menu.speaker_unique_name), choice(phrase_list)))
        # selected_phrase = self.gs.get_feature_ghost(current_menu.speaker_unique_name).base_phrase
        details = {"speaker_name": copy.copy(current_menu.talking_to),
                   "friendship_level": copy.copy(current_menu.friendship),
                   "face_image": copy.copy(current_menu.face_image),
                   "speaker_unique_name": copy.copy(current_menu.speaker_unique_name),
                   "phrase": [selected_phrase]}

        if menu_selection == "Talk":
            self.gc.menu_controller.exit_menu(ConversationOptionsMenuGhost.BASE)
            self.gc.gs.get_feature_ghost(details["speaker_unique_name"]).currently_chatting = True
            self.gc.menu_controller.set_menu(ChatMenuGhost.BASE, details)

        elif menu_selection == "Give Gift":
            details["master_menu"] = current_menu.BASE
            # self.gc.menu_controller.exit_menu(ConversationOptionsMenuGhost.BASE)
            self.gc.menu_controller.set_menu(GiftGivingMenuGhost.BASE, details)

        elif menu_selection == "Exit":
            self.gc.menu_controller.exit_all_menus()

        else:
            self.gc.menu_controller.exit_all_menus()

    def chat_menu_selection(self, item_selected):
        self.gc.menu_controller.exit_all_menus()

    def post_notice(self, phrase):
        self.gc.gs.ms.get_menu_ghost(GameActionDialogueMenuGhost.BASE).show_dialogue(phrase)

    def set_start_menu(self):
        self.set_menu(StartMenuGhost.BASE, None)

    def set_menu(self, menu_name, details):
        selected_menu = self.gc.gs.ms.get_menu_ghost(menu_name)
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
            self.gc.game_view.update_sub_menu_display_details(menu_name, details["master_menu"], information_from_ghost)

        if menu_name == ChatMenuGhost.BASE:
            selected_menu.set_current_phrase(details["phrase"])

        self.gc.set_active_keyboard_manager(InMenuKeyboardManager.ID)
        selected_menu.gc.gs.ms.add_menu_to_stack(menu_name)

    def next_menu(self, current_menu):
        total_number_menus = len(self.gc.gs.ms.start_menu_stack)
        current_menu_index = self.gc.gs.ms.start_menu_stack.index(current_menu)
        self.exit_menu(self.gc.gs.ms.start_menu_stack[current_menu_index])
        next_menu = self.gc.gs.ms.start_menu_stack[0]
        if current_menu_index != (total_number_menus - 1):
            next_menu = self.gc.gs.ms.start_menu_stack[current_menu_index + 1]
        else:
            pass
        self.set_menu(next_menu, None)

    def previous_menu(self, current_menu):
        total_number_menus = len(self.gc.gs.ms.start_menu_stack)
        current_menu_index = self.gc.gs.ms.start_menu_stack.index(current_menu)
        self.exit_menu(self.gc.gs.ms.start_menu_stack[current_menu_index])
        previous_menu = self.gc.gs.ms.start_menu_stack[current_menu_index-1]
        if current_menu_index == 0:
            previous_menu = self.gc.gs.ms.start_menu_stack[total_number_menus - 1]
        else:
            pass
        self.set_menu(previous_menu, None)

    def exit_menu(self, menu_name):
        selected_menu = self.gc.gs.ms.get_menu_ghost(menu_name)
        if menu_name in ["conversation_options_menu", "chat_menu"]:

            print("cool")
        selected_menu.reset_elements()
        self.gc.gs.ms.deactivate_menu(menu_name)


    def exit_all_menus(self):
        list = []
        for x in self.gc.gs.ms.menu_stack:
            list.append(x)
        for item in list:
            self.exit_menu(item)

    def resize_sub_menu(self):
        pass


class SceneManager(object): #TODO: Work on this mess!!
    def __init__(self, gc):
        self.gc = gc
        self.scene_list = {}
        self.animation_list = {"pan_left_5": CameraPanAnimation(Direction.LEFT, 5),
                               "pan_up_5": CameraPanAnimation(Direction.LEFT, 5)}
        self.player_movement_x = 0
        self.player_movement_y = 0
        self.current_scene = None

    def play_scene(self, scene_object):
        self.scene_list["play"] = scene_object
        self.gc.set_active_keyboard_manager(InSceneKeyboardManager.ID)
        self.current_scene = "play"
        self.continue_scene({"x_move": 0, "y_move": 0})

    def continue_scene(self, previous_follow_up):
        self.scene_list[self.current_scene].total_player_x_movement += previous_follow_up["x_move"]
        self.scene_list[self.current_scene].total_player_y_movement += previous_follow_up["y_move"]
        next_action, complete = self.scene_list[self.current_scene].return_current_action()
        if complete:
            self.scene_end_character_movements({"x_move": self.scene_list[self.current_scene].total_player_x_movement,
                                                "y_move": self.scene_list[self.current_scene].total_player_y_movement})
            self.end_scene()
        else:
            if next_action[0] == "animation":
                self.gc.game_view.animation_manager.add_to_scene_anim_in_progress(next_action[1])
            elif next_action[0] == "action":
                self.gc.execute_action_from_animator(next_action[1])
                self.continue_scene({"x_move": 0, "y_move": 0})

    def end_scene(self):
        self.gc.set_active_keyboard_manager(InGameKeyboardManager.ID)
        self.current_scene = None


    def pan_camera(self, direction, number_of_tiles):
        if direction == Direction.LEFT:
            self.animation_list["pan_left_5"].set_animation(direction, number_of_tiles)
            self.gc.game_view.animation_manager.add_to_scene_anim_in_progress("pan_left_5")
            self.player_movement_x = number_of_tiles
        if direction == Direction.UP:
            self.animation_list["pan_up_5"].set_animation(direction, number_of_tiles)
            self.gc.game_view.animation_manager.add_to_scene_anim_in_progress("pan_up_5")
            self.player_movement_y = number_of_tiles


    def blank_out_character(self, character_name):
        pass

    def scene_end_character_movements(self, movement_dict):
        player_object = self.gc.gs.get_player_ghost()
        x_change = player_object.x - movement_dict["x_move"]
        y_change = player_object.y - movement_dict["y_move"]
        # self.change_player_facing(door.exit_direction)
        current_room_object = self.gc.gs.get_current_room()
        self.gc.position_manager.move_ghost(player_object, current_room_object, current_room_object, x_change, y_change)
        self.gc.position_manager.match_player_elevation_to_target(current_room_object, x_change, y_change)
        # self.gc.game_view.manually_update_camera(x_change, y_change)
