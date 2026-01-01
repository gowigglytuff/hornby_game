import pygame

import position_manager
from definitions import Direction
from menu_ghosts import StartMenuGhost
from position_manager import Room2


class KeyboardManager(object):
    """
    :type gc_input: GameController
    """

    def __init__(self, gc_input):
        self.gc_input = gc_input

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


class InGameKeyboardManager(KeyboardManager):
    ID = "InGame"

    def __init__(self, gc_input):
        super().__init__(gc_input)

    def parse_key_input(self, event_type, key):
        if event_type == pygame.KEYDOWN:
            if key in [pygame.K_DOWN, pygame.K_UP, pygame.K_RIGHT, pygame.K_LEFT]:
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

            if key == pygame.K_ESCAPE:
                self.key_escape_pressed()

        elif event_type == pygame.KEYUP:
            if key in [pygame.K_DOWN, pygame.K_UP, pygame.K_RIGHT, pygame.K_LEFT]:
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
        self.gc_input.player_interact()
        # self.gc_input.attempt_move_object("John", Direction.DOWN)

    def key_space_pressed(self):
        self.gc_input.inventory_manager.use_item(self.gc_input.game_state.gd.inventory_manager.item_data_list["Cheese"], 2)

    def key_control_pressed(self):
        self.gc_input.game_state.ms.set_menu(StartMenuGhost.BASE, None)

    def key_escape_pressed(self):
        pass

    def key_lshift_pressed(self):
        pass

    def key_caps_pressed(self):
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
                self.gc_input.game_state.ms.exit_all_menus()

        elif event_type == pygame.KEYUP:
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
        self.gc_input.game_state.ms.exit_all_menus()

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