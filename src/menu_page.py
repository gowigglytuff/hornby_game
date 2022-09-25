import pygame

from definitions import GameSettings, Types
from spritesheet import Spritesheet


class Overlay(object):
    def __init__(self, name, x, y, image):
        self.x = x
        self.y = y
        self.name = name
        self.image = image.get_image(0, 0)


class MenuTemporary(object):
    NAME = "Menu_Temporary"

    def __init__(self, gc_input):
        super().__init__()
        self.gc_input = gc_input
        overlay_size_x = 150
        overlay_size_y = 400
        x = 100
        y = 100
        self.font_size = 10
        self.offset_x = 30
        self.offset_y = 20
        self.overlay = Overlay(self.NAME + "_overlay", x, y, Spritesheet(self.NAME + "_overlay" + "_spritesheet", "assets/spritesheets/menu_spritesheets/start_menu.png", overlay_size_x, overlay_size_y))
        self.x = x + self.offset_x
        self.y = y + self.offset_y
        self.menu_item_list = ["Bag", "Outfits", "Map", "Chore List", "Profile", "Save", "Options", "Vibes"]
        self.menu_item_list.append("Exit")
        self.menu_spread = 25
        self.cursor_at = 0
        self.y_spacing = 0
        self.name = self.NAME
        self.menu_type = "base"
        self.menu_header = None

    @property
    def size(self):
        return len(self.menu_item_list)

    # Same for most menus
    def cursor_down(self):
        if self.cursor_at == len(self.menu_item_list) -1:
            self.cursor_at = 0
        else:
            self.cursor_at += 1

    def cursor_up(self):
        if self.cursor_at == 0:
            self.cursor_at = len(self.menu_item_list) -1
        else:
            self.cursor_at -= 1

    def cursor_left(self):
        pass

    def cursor_right(self):
        pass

    def reset_cursor(self):
        self.cursor_at = 0

    def choose_option(self):
        self.do_option()

    def do_option(self):
        menu_selection = self.get_current_menu_item()

        if menu_selection == "Bag":
            pass

        elif menu_selection == "Key Items":
            pass
        elif menu_selection == "Chore List":
            pass

        elif menu_selection == "Profile":
            pass

        elif menu_selection == "Map":
            pass

        elif menu_selection == "Options":
            pass

        elif menu_selection == "Vibes":
            pass

        elif menu_selection == "Outfits":
            pass

        elif menu_selection == "Save":
            pass

        elif menu_selection == "Exit":
            self.gc_input.menu_manager.exit_all_menus()

        else:
            self.gc_input.menu_manager.exit_all_menus()

    def get_current_menu_item(self):
        menu_selection = self.menu_item_list[self.cursor_at]
        return menu_selection

    def update_menu_items_list(self):
        pass

    def get_menu_items_to_print(self):
        return self.menu_item_list

    def fill_out_menu_info(self, image_file):
        spritesheet_width = Spritesheet.get_w_h(image_file)[0]
        spritesheet_height = Spritesheet.get_w_h(image_file)[1]
        x = GameSettings.RESOLUTION[0] - spritesheet_width - 10
        y = GameSettings.RESOLUTION[1] - spritesheet_height - 300
        self.overlay = Overlay(self.NAME + "_overlay", x, y, Spritesheet(self.NAME + "_overlay" + "_spritesheet", image_file, spritesheet_width, spritesheet_height))
        self.x = x + self.offset_x
        self.y = y + self.offset_y
        if self.menu_header:
            self.y_spacing = 20


class StartMenu(MenuTemporary):
    NAME = "start_menu"

    def __init__(self, gc_input):
        super().__init__(gc_input)
        image_file = "assets/spritesheets/menu_spritesheets/start_menu.png"
        self.font_size = 10
        x = 100
        y = 100
        self.menu_item_list = ["Bag", "Outfits", "Map", "Chore List", "Profile", "Save", "Options", "Vibes"]
        self.menu_item_list.append("Exit")
        self.name = self.NAME
        self.menu_type = Types.BASE
        self.fill_out_menu_info(image_file)

    # Same for most menus
    def cursor_down(self):
        if self.cursor_at == len(self.menu_item_list) -1:
            self.cursor_at = 0
        else:
            self.cursor_at += 1

    def cursor_up(self):
        if self.cursor_at == 0:
            self.cursor_at = len(self.menu_item_list) -1
        else:
            self.cursor_at -= 1

    def cursor_left(self):
        pass

    def cursor_right(self):
        pass

    def reset_cursor(self):
        self.cursor_at = 0

    def choose_option(self):
        self.do_option()

    def do_option(self):
        menu_selection = self.get_current_menu_item()

        if menu_selection == "Bag":
            self.gc_input.menu_manager.set_menu(InventoryMenu.NAME)

        elif menu_selection == "Key Items":
            pass
        elif menu_selection == "Chore List":
            pass

        elif menu_selection == "Profile":
            pass

        elif menu_selection == "Map":
            pass

        elif menu_selection == "Options":
            pass

        elif menu_selection == "Vibes":
            pass

        elif menu_selection == "Outfits":
            pass

        elif menu_selection == "Save":
            pass

        elif menu_selection == "Exit":
            self.gc_input.menu_manager.exit_all_menus()

        else:
            self.gc_input.menu_manager.exit_all_menus()

    def get_current_menu_item(self):
        menu_selection = self.menu_item_list[self.cursor_at]
        return menu_selection

    def update_menu_items_list(self):
        pass


# Menus' from Start Menu
class InventoryMenu(MenuTemporary):
    NAME = "inventory_menu"

    def __init__(self, gc_input):
        super().__init__(gc_input)
        image_file = "assets/spritesheets/menu_spritesheets/inventory_menu.png"
        self.font_size = 10
        self.menu_header = "<   ITEMS   >"
        self.max_length = 14
        self.menu_type = Types.BASE
        self.menu_item_list = []
        self.currently_displayed_items = []
        self.list_shifts = 0
        self.fill_out_menu_info(image_file)

    def get_menu_items_to_print(self):
        menu_length_calc = 0
        if self.size >= self.max_length:
            menu_length_calc = self.max_length
        elif self.size < self.max_length:
            menu_length_calc = self.size

        printable_item_list = []

        for option in range(menu_length_calc):
            item = self.currently_displayed_items[option]
            if item == "Exit":
                printable_item_list.append(self.currently_displayed_items[option])

            else:
                available_spaces = 13
                item_word_length = len(item)
                quantity = str(self.gc_input.menu_manager.get_item_quantity(item))
                quantity_word_length = len(quantity)
                total_length = item_word_length + quantity_word_length
                number_of_spaces = available_spaces - total_length
                spaces_str = ""
                for x in range(number_of_spaces):
                    spaces_str = spaces_str + " "
                final_item = item + spaces_str + "x" + quantity
                printable_item_list.append(final_item)

        print(printable_item_list)
        return printable_item_list

    def update_menu_items_list(self):
        keys_list = []
        for item in self.gc_input.game_state.current_inventory:
            keys_list.append(item)
        self.menu_item_list = keys_list
        self.menu_item_list.append("Exit")
        self.update_currently_displayed()

    def update_currently_displayed(self):
        self.currently_displayed_items = []
        if self.size <= self.max_length:
            for item in range(self.size):
                self.currently_displayed_items.append(self.menu_item_list[item + self.list_shifts])
        else:
            for item in range(self.max_length):
                self.currently_displayed_items.append(self.menu_item_list[item + self.list_shifts])

    def choose_option(self):
        chosen_item_name = self.get_current_menu_item()
        if chosen_item_name == "Exit":
            self.gc_input.menu_manager.exit_all_menus()
        else:
            chosen_item = self.gc_input.inventory_manager.item_data_list[chosen_item_name]
            self.gc_input.inventory_manager.use_item(chosen_item, 3)
            self.gc_input.menu_manager.exit_all_menus()

    def do_option(self, choice=None):
        menu_selection = choice

        if menu_selection == "Use":
            pass

        elif menu_selection == "Toss":
            pass

        elif menu_selection == "Exit":
            self.gc_input.menu_manager.exit_all_menus()

    def cursor_left(self):
        self.exit_menu()
        self.gd_input.menu_list[KeyInventoryMenu.NAME].set_menu()

    def cursor_right(self):
        self.exit_menu()
        self.gd_input.menu_list[KeyInventoryMenu.NAME].set_menu()


    def cursor_down(self):

        if self.size > 1:
            if (self.cursor_at + self.list_shifts) < self.size - 1:
                if self.size > self.max_length:
                    if self.cursor_at == self.max_length - 1:
                        self.list_shifts += 1
                        self.update_currently_displayed()
                    elif self.cursor_at < self.max_length - 1:
                        self.cursor_at += 1
                    else:
                        pass

                elif self.max_length >= self.size > self.cursor_at:
                    self.cursor_at += 1

    def cursor_up(self):
        if (self.cursor_at + self.list_shifts) > 0:
            if self.cursor_at == 0 and self.list_shifts > 0:
                self.list_shifts -= 1
                self.update_currently_displayed()
            elif self.cursor_at > 0:
                self.cursor_at -= 1
            else:
                pass

    def get_current_menu_item(self):
        menu_selection = self.currently_displayed_items[self.cursor_at]
        return menu_selection

    def reset_cursor(self):
        self.cursor_at = 0
        self.list_shifts = 0


class GameActionDialogue(object):
    NAME = "game_action_dialogue_menu"

    def __init__(self, gc_input):
        image_file = "assets/spritesheets/menu_spritesheets/game_action_dialogue_menu.png"
        self.gc_input = gc_input
        self.font_size = 7
        self.offset_x = 10
        self.offset_y = 20
        self.name = self.NAME
        self.menu_item_list = ["This is the game dialouge box!"]
        self.menu_spread = 17
        self.cursor_at = 0
        self.y_spacing = 0
        self.menu_type = "static"
        self.menu_header = None
        self.fill_out_menu_info(image_file)

    def fill_out_menu_info(self, image_file):
        spritesheet_width = Spritesheet.get_w_h(image_file)[0]
        spritesheet_height = Spritesheet.get_w_h(image_file)[1]
        x = GameSettings.RESOLUTION[0] - spritesheet_width - 10
        y = GameSettings.RESOLUTION[1] - spritesheet_height - 10
        self.overlay = Overlay(self.NAME + "_overlay", x, y, Spritesheet(self.NAME + "_overlay" + "_spritesheet", image_file, spritesheet_width, spritesheet_height))
        self.x = x + self.offset_x
        self.y = y + self.offset_y
        if self.menu_header:
            self.y_spacing = 20

    @property
    def size(self):
        return len(self.menu_item_list)

    def show_dialogue(self, phrase):
        if len(self.menu_item_list) >= 4:
            del self.menu_item_list[0]
        self.menu_item_list.append(phrase)

    def get_menu_items_to_print(self):
        return self.menu_item_list
