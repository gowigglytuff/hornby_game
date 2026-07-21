from typing import TYPE_CHECKING

import pygame

from animations_page_view_page import CameraPanAnimation
from definitions import Direction
from menu_ghosts_data_page import StartMenuGhost, QuizMenuGhost, OutfitMenuGhost, MapMenuGhost, GuideMenuGhost, MenuGhost, SceneDialogueMenuGhost
from scenes import Scene

if TYPE_CHECKING:
    from game_controller import GameController, DelayedTrigger


class KeyboardManager(object):
    def __init__(self, gc):
        self.gc = gc  # type: GameController

    def parse_key_input(self, event_type, key):
        if event_type == pygame.KEYDOWN:
            if key == pygame.K_RIGHT:
                pass

            if key == pygame.K_LEFT:
                pass
            if key == pygame.K_DOWN:
                pass
            if key == pygame.K_UP:
                pass
            if key == pygame.K_RETURN:
                self.key_return_pressed()

            if key == pygame.K_SPACE:
                self.key_space_pressed()

            if key == pygame.K_LCTRL:
                self.key_control_pressed()

            if key == pygame.K_TAB:
                self.key_tab_pressed()

            if key == pygame.K_LSHIFT:
                self.key_lshift_pressed()

            if key == pygame.K_CAPSLOCK:
                self.key_caps_pressed()

        elif event_type == pygame.KEYUP:
            if key == pygame.K_RIGHT:
                pass
            if key == pygame.K_LEFT:
                pass
            if key == pygame.K_DOWN:
                pass
            if key == pygame.K_UP:
                pass
            if key == pygame.K_RETURN:
                self.key_return_released()

            if key == pygame.K_SPACE:
                self.key_space_released()

            if key == pygame.K_LCTRL:
                self.key_control_released()

            if key == pygame.K_LSHIFT:
                self.key_lshift_released()

            if key == pygame.K_CAPSLOCK:
                self.key_caps_released()

    # region KEYS
    def key_return_pressed(self):
        pass

    def key_space_pressed(self):
        pass

    def key_control_pressed(self):
        pass

    def key_tab_pressed(self):
        pass

    def key_lshift_pressed(self):
        pass

    def key_alt_pressed(self):
        pass

    def key_alt_release(self):
        pass

    def key_caps_pressed(self):
        pass

    def key_direction_released(self, direction):
        pass

    def key_return_released(self):
        pass

    def key_space_released(self):
        pass

    def key_control_released(self):
        pass

    def key_lshift_released(self):
        pass

    def key_caps_released(self):
        pass
    # endregion


class InGameKeyboardManager(KeyboardManager):
    ID = "InGame"

    def __init__(self, gc):
        super().__init__(gc)
        self.press_function_dict = {"up arrow": [],
                                    "down arrow": [],
                                    "right arrow": [],
                                    "left arrow": [],
                                    "return": [self.gc.clear_key_down_cue, self.gc.player_interact, self.gc.gs.produce_player_coords],
                                    "space": [self.gc.snap_photo],
                                    "a": [self.gc.activate_mermaid_crown],
                                    "s": [self.gc.activate_ghost_eye],
                                    "left ctrl": [self.gc.clear_key_down_cue, self.gc.menu_controller.set_start_menu],
                                    "left shift": [self.key_lshift_pressed],
                                    "escape": [],
                                    "tab": [self.gc.use_selected_tool],
                                    "caps lock": [self.gc.close_game]}
        self.release_function_dict = {"a": [self.gc.determine_mermaid_crown_end],
                                      "s": [self.gc.determine_ghost_eyes_end],
                                      "return": [],
                                      "space": [],
                                      "left ctrl": [],
                                      "left shift": [],
                                      "escape": [],
                                      "tab": [],
                                      "caps lock": []}


    def parse_key_input(self, event_type, key):
        if event_type == pygame.KEYDOWN:

            self.gc.add_to_held_key(key)

            if key in [pygame.K_DOWN, pygame.K_UP, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_z]:
                self.key_direction_pressed(key)
            else:
                if pygame.key.name(key) in self.press_function_dict.keys():
                    self.key_pressed(key)

        elif event_type == pygame.KEYUP:
            self.gc.remove_from_held_key(key)

            if key in [pygame.K_DOWN, pygame.K_UP, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_z]:
                self.key_direction_released(key)
            else:
                if pygame.key.name(key) in self.release_function_dict.keys():
                    self.key_released(key)


    def key_direction_pressed(self, key):
        self.gc.key_down_queue = key

    def key_pressed(self, key):
        for item in self.press_function_dict[pygame.key.name(key)]:
            item()

    def key_released(self, key):
        for item in self.release_function_dict[pygame.key.name(key)]:
            item()

    def key_lshift_pressed(self):
        # self.gc.game_view.trigger_independent_animation("bird_disappear_animation")
        # player = self.gc.game_view.get_player_avatar()
        # player.spritesheet = self.gc.game_view.outfit_manager.lab
        # self.gc.menu_controller.set_menu(GuideMenuGhost.BASE, None)
        # self.gc.scene_manager.pan_camera(Direction.DOWN, 5)
        # self.gc.activate_mermaid_crown()
        # self.gc.scene_manager.play_scene(Scene(self.gc, [CameraPanAnimation(Direction.LEFT, 5), CameraPanAnimation(Direction.UP, 5)]))
        # self.gc.gs.gv.player_perform_animation("up_down", None)

        # character_talking_to_avatar = self.gc.gs.gv.get_feature_avatar("Cowboy_2")
        #
        # details = {"speaker_name": "Jane",
        #            "friendship_level": 3,
        #            "face_image": character_talking_to_avatar.face_image,
        #            "speaker_unique_name": "Jane",
        #            "phrase": ["Hi there, I hope that you're having an amazing day!"]}
        #
        # self.gc.menu_controller.set_menu(SceneDialogueMenuGhost.BASE, details)

        # def condition(gc):
        #     result = False
        #     if gc.gs.cc.check_clock_time(1, 10, 1, 10):
        #         result = True
        #     return result
        #
        # def reaction(gc):
        #     print("it happened!")
        #
        # self.gc.game.game_events.add_delayed_trigger(condition, reaction)
        self.gc.scene_manager.initiate_scene("scene_1")

    def key_direction_released(self, key):
        if self.gc.key_down_queue == key:
            self.gc.key_down_queue = []


class GhostEyeKeyboardManager(KeyboardManager):
    ID = "GhostEye"

    def __init__(self, gc):
        super().__init__(gc)
        self.press_function_dict = {"up arrow": [],
                                    "down arrow": [],
                                    "right arrow": [],
                                    "left arrow": [],
                                    "return": [self.gc.clear_key_down_cue, self.gc.gs.produce_player_coords],
                                    "space": [],
                                    "a": [],
                                    "s": [],
                                    "left ctrl": [],
                                    "left shift": [],
                                    "escape": [],
                                    "tab": [],
                                    "caps lock": [self.gc.close_game]}
        self.release_function_dict = {"a": [],
                                      "s": [self.gc.determine_ghost_eyes_end],
                                      "return": [],
                                      "space": [],
                                      "left ctrl": [],
                                      "left shift": [],
                                      "escape": [],
                                      "tab": [],
                                      "caps lock": []}


    def parse_key_input(self, event_type, key):
        if event_type == pygame.KEYDOWN:

            self.gc.add_to_held_key(key)

            if key in [pygame.K_DOWN, pygame.K_UP, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_z]:
                self.key_direction_pressed(key)
            else:
                if pygame.key.name(key) in self.press_function_dict.keys():
                    self.key_pressed(key)

        elif event_type == pygame.KEYUP:
            self.gc.remove_from_held_key(key)

            if key in [pygame.K_DOWN, pygame.K_UP, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_z]:
                self.key_direction_released(key)
            else:
                if pygame.key.name(key) in self.release_function_dict.keys():
                    self.key_released(key)


    def key_direction_pressed(self, key):
        self.gc.key_down_queue = key

    def key_pressed(self, key):
        for item in self.press_function_dict[pygame.key.name(key)]:
            item()

    def key_released(self, key):
        for item in self.release_function_dict[pygame.key.name(key)]:
            item()

    def key_direction_released(self, key):
        if self.gc.key_down_queue == key:
            self.gc.key_down_queue = []


class InMenuKeyboardManager(KeyboardManager):
    ID = "InMenu"

    def __init__(self, game_view):
        super().__init__(game_view)
        self.press_function_dict = {"up": [self.gc.menu_controller.menu_cursor_up],
                                    "down": [self.gc.menu_controller.menu_cursor_down],
                                    "right": [self.gc.menu_controller.menu_cursor_right],
                                    "left": [self.gc.menu_controller.menu_cursor_left],
                                    "return": [self.gc.menu_controller.menu_choose_option],
                                    "space": [],
                                    "a": [],
                                    "s": [],
                                    "left ctrl": [self.gc.menu_controller.exit_all_menus],
                                    "left shift": [],
                                    "escape": [self.gc.menu_controller.exit_all_menus],
                                    "tab": [],
                                    "caps lock": []}
        self.release_function_dict = {"a": [],
                                      "s": [],
                                      "return": [],
                                      "space": [],
                                      "left ctrl": [],
                                      "left shift": [],
                                      "escape": [],
                                      "tab": [],
                                      "caps lock": []}

    def parse_key_input(self, event_type, key):
        if event_type == pygame.KEYDOWN:

            self.gc.add_to_held_key(key)

            if pygame.key.name(key) in self.press_function_dict.keys():
                self.key_pressed(key)

        elif event_type == pygame.KEYUP:
            self.gc.remove_from_held_key(key)

            if key in [pygame.K_DOWN, pygame.K_UP, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_z]:
                self.key_direction_released(key)
            else:
                if pygame.key.name(key) in self.release_function_dict.keys():
                    self.key_released(key)

    def key_pressed(self, key):
        for item in self.press_function_dict[pygame.key.name(key)]:
            item()

    def key_released(self, key):
        for item in self.release_function_dict[pygame.key.name(key)]:
            item()


class InSceneKeyboardManager(KeyboardManager):
    ID = "InScene"

    def __init__(self, game_view):
        super().__init__(game_view)
        self.press_function_dict = {"return": [],
                                    "space": [],
                                    "a": [],
                                    "s": [],
                                    "left ctrl": [],
                                    "left shift": [],
                                    "escape": [],
                                    "tab": [],
                                    "caps lock": []}
        self.release_function_dict = {"a": [],
                                      "s": [],
                                      "return": [],
                                      "space": [],
                                      "left ctrl": [],
                                      "left shift": [],
                                      "escape": [],
                                      "tab": [],
                                      "caps lock": []}

    def parse_key_input(self, event_type, key):
        # active_menu = self.gc.gs.ms.menu_ghost_data_list[self.gc.gs.ms.menu_stack[0] + "_ghost"]
        if event_type == pygame.KEYDOWN:

            self.gc.add_to_held_key(key)

            if pygame.key.name(key) in self.press_function_dict.keys():
                self.key_pressed(key)

        elif event_type == pygame.KEYUP:
            self.gc.remove_from_held_key(key)

            if pygame.key.name(key) in self.release_function_dict.keys():
                self.key_released(key)

    def key_pressed(self, key):
        for item in self.press_function_dict[pygame.key.name(key)]:
            item()

    def key_released(self, key):
        for item in self.release_function_dict[pygame.key.name(key)]:
            item()