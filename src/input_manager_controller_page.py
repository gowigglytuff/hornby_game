from typing import TYPE_CHECKING

import pygame

from animations_page_view_page import CameraPanAnimation
from definitions import Direction
from menu_ghosts_data_page import StartMenuGhost, QuizMenuGhost, OutfitMenuGhost, MapMenuGhost, GuideMenuGhost
from scenes import Scene

if TYPE_CHECKING:
    from game_controller import GameController


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

    def parse_key_input(self, event_type, key):
        if event_type == pygame.KEYDOWN:

            self.gc.add_to_held_key(key)

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

            if key == pygame.K_a:
                self.key_a_pressed()

        elif event_type == pygame.KEYUP:
            self.gc.remove_from_held_key(key)

            if key in [pygame.K_DOWN, pygame.K_UP, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_z]:
                self.key_direction_released(key)

            if key == pygame.K_RETURN:
                self.key_return_released()

            if key == pygame.K_a:
                self.key_a_released()

            if key == pygame.K_SPACE:
                self.key_space_released()

            if key == pygame.K_LCTRL:
                self.key_control_released()

            if key == pygame.K_LSHIFT:
                self.key_lshift_released()

            if key == pygame.K_CAPSLOCK:
                self.key_caps_released()

    def key_direction_pressed(self, key):
        self.gc.key_down_queue = key

    def key_return_pressed(self):
        self.gc.clear_key_down_cue()
        self.gc.player_interact()
        print(self.gc.gs.player_ghost.x, self.gc.gs.player_ghost.y)
        # self.gc.attempt_move_object("John", Direction.DOWN)

    def key_space_pressed(self):
        self.gc.snap_photo()

    def key_a_pressed(self):
        self.gc.activate_mermaid_crown()

    def key_a_released(self):
        if self.gc.gs.using_mermaid_crown:
            if self.gc.position_manager.get_tile_terrain(self.gc.gs.get_current_room().room_name, self.gc.gs.get_player_ghost_location()[0], self.gc.gs.get_player_ghost_location()[1]) == 1:
                self.gc.deactivate_mermaid_crown()
            else:
                self.gc.cancel_mermaid_crown()

    def key_control_pressed(self):
        self.gc.clear_key_down_cue()
        self.gc.menu_controller.set_menu(StartMenuGhost.BASE, None)

    def key_escape_pressed(self):
        pass

    def key_lshift_pressed(self):
        # self.gc.game_view.trigger_independent_animation("bird_disappear_animation")
        # player = self.gc.game_view.get_player_avatar()
        # player.spritesheet = self.gc.game_view.outfit_manager.lab
        # self.gc.menu_controller.set_menu(GuideMenuGhost.BASE, None)
        # self.gc.scene_manager.pan_camera(Direction.DOWN, 5)
        # self.gc.activate_mermaid_crown()
        # self.gc.scene_manager.play_scene(Scene(self.gc, [CameraPanAnimation(Direction.LEFT, 5), CameraPanAnimation(Direction.UP, 5)]))
        pass

    def key_caps_pressed(self):
        self.gc.game.game_running = False

    def key_alt_pressed(self):
        pass

    def key_tab_pressed(self):
        self.gc.use_selected_tool()

    def key_alt_release(self):
        pass

    def key_direction_released(self, key):
        if self.gc.key_down_queue == key:
            self.gc.key_down_queue = []

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
        active_menu = self.gc.gs.ms.menu_ghost_data_list[self.gc.gs.ms.menu_stack[0] + "_ghost"]
        if event_type == pygame.KEYDOWN:

            self.gc.add_to_held_key(key)

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
                self.gc.menu_controller.exit_all_menus()

        elif event_type == pygame.KEYUP:

            self.gc.remove_from_held_key(key)

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
        active_menu = self.gc.gs.ms.menu_ghost_data_list[self.gc.gs.ms.menu_stack[0] + "_ghost"]
        active_menu.choose_option()

    def key_space_pressed(self):
        pass

    def key_control_pressed(self):
        self.gc.menu_controller.exit_all_menus()

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


class InSceneKeyboardManager(KeyboardManager):
    ID = "InScene"

    def __init__(self, game_view):
        super().__init__(game_view)

    def parse_key_input(self, event_type, key):
        # active_menu = self.gc.gs.ms.menu_ghost_data_list[self.gc.gs.ms.menu_stack[0] + "_ghost"]
        if event_type == pygame.KEYDOWN:

            self.gc.add_to_held_key(key)

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

            if key == pygame.K_LSHIFT:
                self.key_lshift_pressed()

            if key == pygame.K_CAPSLOCK:
                self.key_caps_pressed()

            if key == pygame.K_ESCAPE:
                pass

        elif event_type == pygame.KEYUP:

            self.gc.remove_from_held_key(key)

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
        pass

    def key_return_pressed(self):
        pass

    def key_space_pressed(self):
        pass

    def key_control_pressed(self):
        pass

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