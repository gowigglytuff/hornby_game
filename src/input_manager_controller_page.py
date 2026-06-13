from typing import TYPE_CHECKING

import pygame

from definitions import Direction
from menu_ghosts_data_page import StartMenuGhost, QuizMenuGhost, OutfitMenuGhost, MapMenuGhost, GuideMenuGhost

if TYPE_CHECKING:
    from game_controller import GameController


class KeyboardManager(object):
    def __init__(self, gc_input):
        self.gc_input = gc_input  # type: GameController

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

    def __init__(self, gc_input):
        super().__init__(gc_input)

    def parse_key_input(self, event_type, key):
        if event_type == pygame.KEYDOWN:

            self.gc_input.add_to_held_key(key)

            if key in [pygame.K_DOWN, pygame.K_UP, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_z]:
                self.key_direction_pressed(key)

            if key == pygame.K_RETURN:

                self.key_return_pressed()

            if key == pygame.K_SPACE:
                self.key_space_pressed()

            if key == pygame.K_LCTRL:
                self.key_control_pressed()

            if key == pygame.K_LSHIFT:
                self.key_lshift_pressed()

            if key == pygame.K_CAPSLOCK:
                self.key_caps_pressed()

            if key == pygame.K_CAPSLOCK:
                self.key_caps_pressed()

            if key == pygame.K_TAB:
                self.key_tab_pressed()

            if key == pygame.K_ESCAPE:
                self.key_escape_pressed()

        elif event_type == pygame.KEYUP:
            self.gc_input.remove_from_held_key(key)

            if key in [pygame.K_DOWN, pygame.K_UP, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_z]:
                self.key_direction_released(key)

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

    def key_direction_pressed(self, key):
        self.gc_input.key_down_queue = key

    def key_return_pressed(self):
        self.gc_input.clear_key_down_cue()
        self.gc_input.player_interact()
        print(self.gc_input.game_state.player_ghost.x, self.gc_input.game_state.player_ghost.y)
        # self.gc_input.attempt_move_object("John", Direction.DOWN)

    def key_space_pressed(self):
        self.gc_input.snap_photo()

    def key_control_pressed(self):
        self.gc_input.clear_key_down_cue()
        self.gc_input.menu_controller.set_menu(StartMenuGhost.BASE, None)

    def key_escape_pressed(self):
        pass

    def key_lshift_pressed(self):
        # self.gc_input.game_view.trigger_independent_animation("bird_disappear_animation")
        # player = self.gc_input.game_view.get_player_avatar()
        # player.spritesheet = self.gc_input.game_view.outfit_manager.lab
        self.gc_input.menu_controller.set_menu(GuideMenuGhost.BASE, None)

    def key_caps_pressed(self):
        self.gc_input.game.game_running = False

    def key_alt_pressed(self):
        pass

    def key_tab_pressed(self):
        self.gc_input.use_selected_tool()

    def key_alt_release(self):
        pass

    def key_direction_released(self, key):
        if self.gc_input.key_down_queue == key:
            self.gc_input.key_down_queue = []

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


class InMenuKeyboardManager(KeyboardManager):
    ID = "InMenu"

    def __init__(self, game_view):
        super().__init__(game_view)

    def parse_key_input(self, event_type, key):
        active_menu = self.gc_input.game_state.ms.menu_ghost_data_list[self.gc_input.game_state.ms.menu_stack[0] + "_ghost"]
        if event_type == pygame.KEYDOWN:

            self.gc_input.add_to_held_key(key)

            if key == pygame.K_RIGHT:
                active_menu.cursor_right()

            if key == pygame.K_LEFT:
                active_menu.cursor_left()

            if key == pygame.K_DOWN:
                active_menu.cursor_down()

            if key == pygame.K_UP:
                active_menu.cursor_up()

            if key == pygame.K_RETURN:
                self.key_return_pressed()

            if key == pygame.K_SPACE:
                self.key_space_pressed()

            if key == pygame.K_LCTRL:
                self.key_control_pressed()

            if key == pygame.K_LSHIFT:
                self.key_lshift_pressed()

            if key == pygame.K_CAPSLOCK:
                self.key_caps_pressed()

            if key == pygame.K_ESCAPE:
                self.gc_input.menu_controller.exit_all_menus()

        elif event_type == pygame.KEYUP:

            self.gc_input.remove_from_held_key(key)

            if key == pygame.K_RIGHT:
                self.key_direction_released(Direction.RIGHT)

            if key == pygame.K_LEFT:
                self.key_direction_released(Direction.LEFT)

            if key == pygame.K_DOWN:
                self.key_direction_released(Direction.DOWN)

            if key == pygame.K_UP:
                self.key_direction_released(Direction.UP)

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

    def key_direction_pressed(self, direction):
        if direction == Direction.RIGHT:
            self.game_view.game_controller.move_right()

    def key_return_pressed(self):
        active_menu = self.gc_input.game_state.ms.menu_ghost_data_list[self.gc_input.game_state.ms.menu_stack[0] + "_ghost"]
        active_menu.choose_option()

    def key_space_pressed(self):
        pass

    def key_control_pressed(self):
        self.gc_input.menu_controller.exit_all_menus()

    def key_lshift_pressed(self):
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