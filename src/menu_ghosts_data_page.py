import copy
import math
import random
import shutil
import textwrap

import pygame

from definitions import GameSettings, Types, Mundane
from game_view import Outfit
from menu_avatars_view_page import ListMenuAvatar, SuppliesMenuAvatar, KeyInventoryMenuAvatar, TreasuresInventoryMenuAvatar, GiftGivingMenuAvatar, AcquireMenuAvatar, SellerMenuAvatar, ChattingMenuAvatar, StatMenuAvatar, GameActionDialogueMenuAvatar, GuideMenuAvatar, GalleryMenuAvatar, NumberSelectionMenuAvatar, SubMenuAvatar, TextInputMenuAvatar, ImageMenuAvatar, BasketMenuAvatar, DeveloperMenuAvatar, CharacterAssemblyMenuAvatar, GameModeStatMenuAvatar, ClickListMenuAvatar, \
    CharacterSpritesheetViewMenu
from spritesheet import Spritesheet
from text_input import get_input


class MenuInformation(object):
    def __init__(self, header, text_display_list, cursor_image, cursor_at, menu_specific_details_dict):
        self.header = header
        self.text_display_list = text_display_list
        self.cursor_image = cursor_image
        self.cursor_at = cursor_at
        self.menu_specific_details_dict = menu_specific_details_dict


class MenuGhost(object):
    BASE = "menu_base"
    NAME = BASE + "_ghost"

    def __init__(self, gc):
        super().__init__()
        self.gc = gc

        self.menu_header = "<Goodies>"
        self.menu_item_list = ["Poop", "Pee", "Dragon Eggs", "Weasel Toe"]
        self.menu_images_list = []
        self.additional_information = []
        self.menu_type = Types.BASE
        self.text_entry_boxes = {}
        self.currently_selected_text_entry_box = None
        self.master_menu = None

        self.cursor = "-"
        self.cursor_at = [0, 0]
        self.name = self.NAME
        self.button_list = {}

    def once_set_actions(self):
        pass

    def get_menu_items_to_display(self):
        return self.menu_item_list

    def choose_option(self):
        self.do_option()

    def get_current_menu_item(self):
        menu_selection = self.menu_item_list[self.cursor_at[1]]
        return menu_selection

    def do_option(self):
        menu_selection = self.get_current_menu_item()

    def key_letter(self, letter):
        pass

    def erase_letter(self):
        pass

    def generate_menu_information_package(self):
        source = self.get_menu_items_to_display().copy()
        cursor_at = self.cursor_at
        cursor_image = self.cursor
        text_display_list = []

        for item in range(len(source)):
            text_display_list.append(source[item])

        menu_specific = {"header": self.menu_header,
                        "text_display_list": text_display_list,
                        "cursor_image": cursor_image,
                        "cursor_at": cursor_at}

        menu_information = MenuInformation(self.menu_header, text_display_list, cursor_image, cursor_at, menu_specific)
        return menu_information

    def generate_image_display(self):
        image_display_list = {}
        for image in range(len(self.menu_images_list)):
            image_display_list["Item_" + str(image)] = self.menu_images_list[image]
        return image_display_list

    def update_currently_displayed(self):
        pass

    def prepare_menu_for_display(self, details):
        pass

    def cursor_down(self):
        if self.cursor_at[1] == len(self.menu_item_list) -1:
            self.cursor_at[1] = 0
        else:
            self.cursor_at[1] += 1

    def cursor_up(self):
        if self.cursor_at[1] == 0:
            self.cursor_at[1] = len(self.menu_item_list) -1
        else:
            self.cursor_at[1] -= 1

    def cursor_left(self):
        pass

    def cursor_right(self):
        pass

    def reset_elements(self):
        self.cursor_at[0] = 0
        self.cursor_at[1] = 0

    def set_master_menu(self, master_menu):
        self.master_menu = master_menu

    @property
    def size(self):
        return len(self.menu_item_list)

    def set_current_text_entry_box(self, box_name):
        self.gc.menu_controller.set_current_text_entry_box(box_name)

    def unset_text_entry_box_followup(self):
        pass

    def get_current_text_box(self):
        return self.text_entry_boxes[self.currently_selected_text_entry_box]

    def push_menu_button(self, button_name):
        button = self.button_list[button_name]
        button.get_pressed()


class StatMenuGhost(MenuGhost):
    BASE = "stat_menu"
    NAME = BASE + "_ghost"
    AVATAR = StatMenuAvatar

    def __init__(self, gc):
        super().__init__(gc)
        self.menu_header = None

        self.menu_item_list = []
        self.menu_images_list = []
        self.cursor = None
        self.prepare_menu_for_display()
        self.menu_type = Types.STATIC

    def prepare_menu_for_display(self):
        stat_dict = self.gc.menu_controller.get_stat_items()
        self.menu_item_list = ["Day:" + stat_dict["day"], "Time:" + stat_dict["time"], "Select: " + stat_dict["selected_tool"]]

    def get_current_menu_item(self):
        menu_selection = self.menu_item_list[self.cursor_at[1]]
        return menu_selection

    def generate_menu_information_package(self):
        self.prepare_menu_for_display()
        source = self.get_menu_items_to_display().copy()
        cursor_at = self.cursor_at
        cursor_image = self.cursor
        text_display_list = []

        for item in range(len(source)):
            text_display_list.append(source[item])

        menu_specific = {"header": self.menu_header,
                        "text_display_list": text_display_list,
                        "cursor_image": cursor_image,
                        "cursor_at": cursor_at}

        menu_information = MenuInformation(self.menu_header, text_display_list, cursor_image, cursor_at, menu_specific)
        return menu_information


class GameModeStatMenuGhost(StatMenuGhost):
    BASE = "game_mode_stat_menu"
    NAME = BASE + "_ghost"
    AVATAR = GameModeStatMenuAvatar

    def __init__(self, gc):
        super().__init__(gc)
        self.menu_header = None

        self.menu_item_list = []
        self.menu_images_list = []
        self.cursor = None
        self.prepare_menu_for_display()
        self.menu_type = Types.STATIC

    def prepare_menu_for_display(self):
        stat_dict = self.gc.menu_controller.get_stat_mode_items()
        if stat_dict['mode'] == "builder":
            instructions = ["Mode: [LCtrl",
                            "MapMenu: [LShift]",
                            "MoveCam: [Dir]",
                            "Show Names: [c]",
                            "View Window: [v]",
                            "ExitGame: [Caps]"]
        else:
            instructions = ["Mode: [RCtrl]",
                            "Move: [Dir]",
                            "Interact: [Enter]",
                            "Photo: [Space]",
                            "Start: [LCtrl]",
                            "Swim: Hold [A]",
                            "Tool: [Tab]",
                            "MoveCam: H[LShift] + [Dir]",
                            "View Window: [v]",
                            "Test: [RShift]",
                            "Assembly: [1]",
                            "SwapPlayer: [2]",
                            "ExitGame: [Caps]"]

        self.menu_item_list = [f"Game Mode: {stat_dict['mode']}"] + instructions


class StartMenuGhost(MenuGhost):
    BASE = "start_menu"
    NAME = BASE + "_ghost"
    AVATAR = ListMenuAvatar

    def __init__(self, gc):
        super().__init__(gc)
        self.menu_header = None
        self.menu_item_list = ["Bag", "Outfits", "Map", "Gallery", "Guide", "Speak", "Save", "Options", "Vibes"]
        self.menu_item_list.append("Exit")
        self.menu_images_list = []
        self.cursor = "-"
        self.prepare_menu_for_display(None)

    def do_option(self, choice=None):
        menu_selection = self.get_current_menu_item()
        if choice is not None:
            menu_selection = choice
        self.gc.menu_controller.start_menu_selection(menu_selection)


class DeveloperMenuGhost(MenuGhost):
    BASE = "developer_menu"
    NAME = BASE + "_ghost"
    AVATAR = DeveloperMenuAvatar

    def __init__(self, gc):
        super().__init__(gc)
        self.menu_header = None
        self.menu_item_list = []
        self.menu_item_list.append("Exit")
        self.menu_images_list = []
        self.cursor = None
        # self.prepare_menu_for_display()

    def prepare_menu_for_display(self):
        stat_dict = self.gc.menu_controller.get_developer_items()
        self.menu_item_list = ["Room: " + stat_dict["Room"], "Player:" + stat_dict["Player"], "Image: " + stat_dict["Image"],
                               "Camera: " + stat_dict["Camera"]]

    def get_current_menu_item(self):
        menu_selection = self.menu_item_list[self.cursor_at[1]]
        return menu_selection

    def generate_menu_information_package(self):
        self.prepare_menu_for_display()
        source = self.get_menu_items_to_display().copy()
        cursor_at = self.cursor_at
        cursor_image = self.cursor
        text_display_list = []

        for item in range(len(source)):
            text_display_list.append(source[item])

        menu_specific = {"header": self.menu_header,
                        "text_display_list": text_display_list,
                        "cursor_image": cursor_image,
                        "cursor_at": cursor_at}

        menu_information = MenuInformation(self.menu_header, text_display_list, cursor_image, cursor_at, menu_specific)
        return menu_information


class WordsMenuGhost(MenuGhost):
    BASE = "words_menu"
    NAME = BASE + "_ghost"
    AVATAR = ListMenuAvatar

    def __init__(self, gc):
        super().__init__(gc)
        self.menu_header = None
        self.stored_words = ['"hello"', '"kazzam"', '"balloon"', '"poof"']
        self.menu_item_list = []
        self.currently_displayed_items = []
        self.menu_item_list.append("Exit")
        self.menu_images_list = []
        self.cursor = "-"
        self.max_displayed_items = 6
        self.shifts = 0
        self.prepare_menu_for_display(None)

    def prepare_menu_for_display(self, details):
        self.menu_item_list = copy.copy(self.stored_words)
        self.menu_item_list.sort()
        self.menu_item_list.append("Exit")
        self.menu_item_list.insert(0, "New Word")

    def choose_option(self):
        chosen_item_name = self.get_current_menu_item()
        if chosen_item_name == "Exit":
            self.gc.menu_controller.exit_all_menus()
        elif chosen_item_name == "New Word":
            self.gc.menu_controller.set_menu(TextInputMenuGhost.BASE, {"master_menu": WordsMenuGhost.BASE})
        else:
            self.gc.menu_controller.set_menu(SubMenuGhost.BASE, {"master_menu": self.BASE, "menu_items_list": ["Speak", "Whisper", "Shout", "Delete", "Cancel"]})

    def do_option(self, choice=None):
        sub_menu_selection = choice
        chosen_item_name = self.get_current_menu_item()

        if sub_menu_selection == "Cancel":
            self.gc.menu_controller.exit_all_menus()
        elif sub_menu_selection == "New Word":
            self.gc.menu_controller.set_menu(TextInputMenuGhost.BASE, {"master_menu": WordsMenuGhost.BASE})
        else:
            if sub_menu_selection in ["Speak", "Shout", "Whisper"]:
                word_fixed = chosen_item_name[1:-1]
                self.gc.player_speak(sub_menu_selection, word_fixed)
                self.gc.menu_controller.exit_all_menus()
            elif sub_menu_selection == "Delete":
                self.stored_words.remove(chosen_item_name)
                self.prepare_menu_for_display(None)
            else:
                self.stored_words.append('"' + sub_menu_selection + '"')
                self.prepare_menu_for_display(None)


class InventoryMenuGhost(MenuGhost):
    BASE = "inventory_menu"
    NAME = BASE + "_ghost"

    def __init__(self, gc):
        super().__init__(gc)
        self.menu_header = None
        self.menu_item_list = []
        self.menu_header = "<   ITEMS   >"
        self.menu_images_list = []
        self.cursor = "-"
        self.shifts = 0
        self.max_displayed_items = 14
        self.currently_displayed_items = []
        self.prepare_menu_for_display(None)
        self.update_currently_displayed()
        self.action_doing = None

    def reset_elements(self):
        super().reset_elements()
        self.action_doing = None
        self.shifts = 0

    def get_current_menu_item(self):
        menu_selection = self.menu_item_list[self.cursor_at[1]+self.shifts]
        return menu_selection

    def cursor_down(self):
        if self.size > 1:
            if self.cursor_at[1] < len(self.menu_item_list) -1:
                self.cursor_at[1] += 1
            else:
                self.cursor_at[1] = 0

    def cursor_up(self):
        if self.cursor_at[1] > 0:
            self.cursor_at[1] -= 1
        else:
            self.cursor_at[1] = len(self.menu_item_list) -1

    def cursor_left(self):
        self.gc.menu_controller.previous_menu(self.BASE)

    def cursor_right(self):
        self.gc.menu_controller.next_menu(self.BASE)

    def prepare_menu_for_display(self, details):
        keys_list = []
        current_inventory = self.gc.gs.get_inventory_items(self.BASE)
        if current_inventory:
            for item in current_inventory:
                keys_list.append(item)
            self.menu_item_list = keys_list
            self.menu_item_list.append("Exit")
            self.update_currently_displayed()

    def get_menu_items_to_display(self):
        displayable_item_list = []

        for item in self.menu_item_list:
            displayable_item_list.append(item)

        return displayable_item_list

    def update_currently_displayed(self):
        self.currently_displayed_items = []
        if self.size <= self.max_displayed_items:
            for item in range(self.size):
                self.currently_displayed_items.append(self.menu_item_list[item + self.shifts])
        else:
            for item in range(self.max_displayed_items):
                self.currently_displayed_items.append(self.menu_item_list[item + self.shifts])

    def choose_option(self):
        chosen_item_name = self.get_current_menu_item()
        if chosen_item_name == "Exit":
            self.gc.menu_controller.exit_all_menus()
        else:
            self.gc.menu_controller.set_menu(SubMenuGhost.BASE, {"master_menu": self.BASE, "menu_items_list": ["Use", "Toss", "Cancel"]})

    def do_option(self, choice=None):
        sub_menu_selection = choice
        chosen_item_name = self.get_current_menu_item()
        self.gc.menu_controller.inventory_menu_selection(self, sub_menu_selection, chosen_item_name)


class SuppliesInventoryMenuGhost(InventoryMenuGhost):
    BASE = "supplies_inventory_menu"
    NAME = BASE + "_ghost"
    AVATAR = SuppliesMenuAvatar

    def __init__(self, gc):
        super().__init__(gc)
        self.menu_header = None
        self.menu_item_list = []
        self.menu_header = "<   ITEMS   >"
        self.menu_images_list = []
        self.cursor = "-"
        self.shifts = 0
        self.max_displayed_items = 14
        self.currently_displayed_items = []
        self.prepare_menu_for_display(None)
        self.update_currently_displayed()

    def generate_menu_information_package(self):
        source = self.get_menu_items_to_display().copy()
        cursor_at = self.cursor_at
        cursor_image = self.cursor
        text_display_list = source

        menu_specific = {"header": self.menu_header,
                        "text_display_list": source,
                        "cursor_image": cursor_image,
                        "cursor_at": cursor_at}

        menu_information = MenuInformation(self.menu_header, text_display_list, cursor_image, cursor_at, menu_specific)
        return menu_information

    def get_menu_items_to_display(self):
        displayable_item_list = []

        for item in self.menu_item_list:
            if item == "Exit":
                displayable_item_list.append((item, "0"))

            else:
                quantity = str(self.gc.gs.get_item_quantity(item))
                displayable_item_list.append((item, quantity))

        return displayable_item_list


class GiftGivingMenuGhost(InventoryMenuGhost):
    BASE = "gift_giving_menu"
    NAME = BASE + "_ghost"
    AVATAR = GiftGivingMenuAvatar

    def __init__(self, gc):
        super().__init__(gc)
        self.menu_header = None
        self.menu_item_list = []
        self.menu_header = "    ITEMS    "
        self.menu_images_list = []
        self.cursor = "-"
        self.shifts = 0
        self.menu_type = Types.SECONDARY
        self.max_displayed_items = 14
        self.currently_displayed_items = []
        self.prepare_menu_for_display(None)
        self.update_currently_displayed()
        self.details = None

    def prepare_menu_for_display(self, details):
        self.details = details
        self.refresh_menu_items()

    def refresh_menu_items(self):
        keys_list = []
        current_inventory = self.gc.gs.get_inventory_items(SuppliesInventoryMenuGhost.BASE)
        for item in current_inventory:
            keys_list.append(item)
        self.menu_item_list = keys_list
        self.menu_item_list.append("Exit")

    def get_menu_items_to_display(self):
        self.refresh_menu_items()
        displayable_item_list = []

        for item in self.menu_item_list:
            if item == "Exit":
                displayable_item_list.append((item, "0"))

            else:
                quantity = str(self.gc.gs.get_item_quantity(item))
                displayable_item_list.append((item, quantity))

        return displayable_item_list

    def cursor_left(self):
        pass

    def cursor_right(self):
        pass

    def set_master_menu(self, master_menu):
        self.master_menu = master_menu

    def choose_option(self):
        chosen_item_name = self.get_current_menu_item()
        if chosen_item_name == "Exit":
            self.gc.menu_controller.exit_all_menus()
        else:
            self.gc.menu_controller.post_notice("Give this item?")
            self.gc.menu_controller.set_menu(SubMenuGhost.BASE, {"master_menu": self.BASE, "menu_items_list": ["Yes", "No"]})

    def do_option(self, choice=None):
        sub_menu_selection = choice
        chosen_item_name = self.get_current_menu_item()
        details = self.details
        self.gc.menu_controller.gift_menu_selection(sub_menu_selection, chosen_item_name, details)


class BasketMenuGhost(MenuGhost):
    BASE = "basket_menu"
    NAME = BASE + "_ghost"
    AVATAR = BasketMenuAvatar

    def __init__(self, gc):
        super().__init__(gc)
        self.menu_header = None
        self.menu_item_list = ["Take Something", "Leave Something"]
        self.menu_item_list.append("Exit")
        self.menu_images_list = []
        self.cursor = "-"
        self.details = {}

    def prepare_menu_for_display(self, details):
        self.details = details

    def do_option(self, choice=None):
        menu_selection = self.get_current_menu_item()
        if menu_selection == "Take Something":
            if self.details["item_list"]:
                self.gc.menu_controller.post_notice("What would you like to take?")
                details = copy.copy(self.details)
                self.gc.menu_controller.set_menu(AcquireMenuGhost.BASE, details)
            else:
                self.gc.menu_controller.post_notice("It appears to be empty.")
                self.gc.menu_controller.exit_all_menus()
        elif menu_selection == "Leave Something":
            details = self.details
            self.gc.menu_controller.set_menu(DepositMenuGhost.BASE, details)
        elif menu_selection == "Exit":
            self.gc.menu_controller.exit_all_menus()


class AcquireMenuGhost(MenuGhost): #TODO: Work on this
    BASE = "acquire_menu"
    NAME = BASE + "_ghost"
    AVATAR = AcquireMenuAvatar

    def __init__(self, gc):
        super().__init__(gc)
        self.menu_header = "CONTENTS"
        self.menu_item_list = ["Cheese", "Spoon", "Match"]
        self.menu_item_list.append("Exit")
        self.menu_images_list = []
        self.cursor = "-"

    def prepare_menu_for_display(self, details):
        self.menu_item_list = details["item_list"]
        self.current_basket = details["basket_unique_name"]
        self.menu_item_list.append("Exit")
        self.generate_menu_information_package()

    def generate_menu_information_package(self):
        source = self.get_menu_items_to_display().copy()
        cursor_at = self.cursor_at
        cursor_image = self.cursor
        text_display_list = []

        for item in range(len(source)):
            text_display_list.append(source[item])

        menu_specific = {"header": self.menu_header,
                         "text_display_list": text_display_list,
                         "cursor_image": cursor_image,
                         "cursor_at": cursor_at}

        menu_information = MenuInformation(self.menu_header, text_display_list, cursor_image, cursor_at, menu_specific)
        return menu_information

    def do_option(self, choice):
        menu_selection = self.get_current_menu_item()
        if choice == "Yes":
            self.gc.menu_controller.exit_all_menus()
            self.gc.take_from_basket(self.current_basket, menu_selection)
        if choice == "No":
            pass
        else:
            self.gc.menu_controller.exit_all_menus()

    def choose_option(self):
        chosen_item_name = self.get_current_menu_item()
        if chosen_item_name == "Exit":
            self.gc.menu_controller.exit_all_menus()
        else:
            self.gc.menu_controller.post_notice("Do you want to take the " + chosen_item_name + "?")
            self.gc.menu_controller.set_menu(SubMenuGhost.BASE, {"master_menu": self.BASE, "menu_items_list": ["Yes", "No"]})


class DepositMenuGhost(SuppliesInventoryMenuGhost):
    BASE = "deposit_menu"
    NAME = BASE + "_ghost"
    AVATAR = SuppliesMenuAvatar

    def __init__(self, gc):
        super().__init__(gc)
        self.menu_type = Types.BASE

    def choose_option(self):
        chosen_item_name = self.get_current_menu_item()
        if chosen_item_name == "Exit":
            self.gc.menu_controller.exit_all_menus()
        else:
            self.gc.menu_controller.post_notice("Leave this item?")
            self.gc.menu_controller.set_menu(SubMenuGhost.BASE, {"master_menu": self.BASE, "menu_items_list": ["Yes", "No"]})

    def do_option(self, choice): #TODO: Finish this
        menu_selection = self.get_current_menu_item()
        if choice == "Yes":
            self.gc.menu_controller.exit_all_menus()
            self.gc.deposit_in_basket(self.current_basket, menu_selection)
        if choice == "No":
            pass
        else:
            self.gc.menu_controller.exit_all_menus()

    def prepare_menu_for_display(self, details):
        if details:
            self.current_basket = details["basket_unique_name"]
        keys_list = []
        current_inventory = self.gc.gs.get_inventory_items(SuppliesInventoryMenuGhost.BASE)
        if current_inventory:
            for item in current_inventory:
                keys_list.append(item)
            self.menu_item_list = keys_list
            self.menu_item_list.append("Exit")
            self.update_currently_displayed()

    def cursor_left(self):
        pass

    def cursor_right(self):
        pass


class KeyInventoryMenuGhost(InventoryMenuGhost):
    BASE = "key_inventory_menu"
    NAME = BASE + "_ghost"
    AVATAR = KeyInventoryMenuAvatar

    def __init__(self, gc):
        super().__init__(gc)
        self.menu_header = None
        self.menu_item_list = []
        self.menu_header = "< KEY ITEMS >"
        self.menu_images_list = []
        self.cursor = "-"
        self.shifts = 0
        self.max_displayed_items = 14
        self.currently_displayed_items = []
        self.prepare_menu_for_display(None)
        self.update_currently_displayed()

    def choose_option(self):
        chosen_item_name = self.get_current_menu_item()
        if chosen_item_name == "Exit":
            self.gc.menu_controller.exit_all_menus()
        else:
            self.gc.menu_controller.set_menu(SubMenuGhost.BASE, {"master_menu": self.BASE, "menu_items_list": ["Use", "Toss", "Select", "Cancel"]})

    def do_option(self, choice=None):
        sub_menu_selection = choice
        chosen_item_name = self.get_current_menu_item()

        if sub_menu_selection == "Use":
            chosen_item = self.gc.inventory_manager.gc.gs.gd.key_item_data_list[chosen_item_name]
            if chosen_item.use_type == "continuous":
                self.gc.gs.selected_tool = chosen_item_name
            else:
                self.gc.inventory_manager.use_key_item(chosen_item)
            self.prepare_menu_for_display(None)
            self.gc.menu_controller.exit_all_menus()

        elif sub_menu_selection == "Toss":
            self.gc.menu_controller.exit_all_menus()

        elif sub_menu_selection == "Select":
            self.gc.gs.selected_tool = chosen_item_name
            self.gc.menu_controller.exit_all_menus()

        elif sub_menu_selection == "Cancel":
            self.gc.menu_controller.exit_all_menus()


class TreasureInventoryMenuGhost(InventoryMenuGhost):
    BASE = "treasure_inventory_menu"
    NAME = BASE + "_ghost"
    AVATAR = TreasuresInventoryMenuAvatar

    def __init__(self, gc):
        super().__init__(gc)
        self.menu_header = None
        self.menu_item_list = []
        self.menu_header = "< TREASURES >"
        self.menu_images_list = []
        self.cursor = "-"
        self.shifts = 0
        self.max_displayed_items = 14
        self.currently_displayed_items = []
        self.prepare_menu_for_display(None)
        self.update_currently_displayed()

    def choose_option(self):
        chosen_item_name = self.get_current_menu_item()
        if chosen_item_name == "Exit":
            self.gc.menu_controller.exit_all_menus()
        else:
            self.gc.menu_controller.set_menu(SubMenuGhost.BASE, {"master_menu": self.BASE, "menu_items_list": ["Use", "Toss", "Select", "Cancel"]})

    def do_option(self, choice=None):
        sub_menu_selection = choice
        chosen_item_name = self.get_current_menu_item()

        if sub_menu_selection == "Use":
            chosen_item = self.gc.inventory_manager.gc.gs.gd.treasure_item_data_list[chosen_item_name]
            if chosen_item.use_type == "continuous":
                self.gc.gs.selected_tool = chosen_item_name
            else:
                self.gc.inventory_manager.use_treasure_item(chosen_item)
            self.prepare_menu_for_display(None)
            self.gc.menu_controller.exit_all_menus()

        elif sub_menu_selection == "Toss":
            self.gc.menu_controller.exit_all_menus()

        elif sub_menu_selection == "Select":
            self.gc.gs.selected_tool = chosen_item_name
            self.gc.menu_controller.exit_all_menus()

        elif sub_menu_selection == "Cancel":
            self.gc.menu_controller.exit_all_menus()


class ConversationOptionsMenuGhost(MenuGhost):
    BASE = "conversation_options_menu"
    NAME = BASE + "_ghost"
    AVATAR = ChattingMenuAvatar

    def __init__(self, gc):
        super().__init__(gc)
        self.menu_header = None
        self.menu_type = Types.BASE
        self.menu_item_list = ["Talk", "Give Gift", "Exit"]
        self.menu_images_list = []
        self.cursor = "-"
        self.shifts = 0
        self.max_displayed_items = 14
        self.currently_displayed_items = []
        self.talking_to = None
        self.friendship = None
        self.face_image = None
        self.actor_type = None
        self.speaker_unique_name = None
        self.update_currently_displayed()

    def cursor_down(self):
        if self.size > 1:
            if (self.cursor_at[1] + self.shifts) < self.size - 1:
                if self.size > self.max_displayed_items:
                    if self.cursor_at[1] == self.max_displayed_items - 1:
                        self.shifts += 1
                        self.update_currently_displayed()
                    elif self.cursor_at[1] < self.max_displayed_items - 1:
                        self.cursor_at[1] += 1
                    else:
                        pass

                elif self.max_displayed_items >= self.size > self.cursor_at[1]:
                    self.cursor_at[1] += 1

    def cursor_up(self):
        if (self.cursor_at[1] + self.shifts) > 0:
            if self.cursor_at[1] == 0 and self.shifts > 0:
                self.shifts -= 1
                self.update_currently_displayed()
            elif self.cursor_at[1] > 0:
                self.cursor_at[1] -= 1
            else:
                pass

    def update_currently_displayed(self):
        self.currently_displayed_items = []
        if self.size <= self.max_displayed_items:
            for item in range(self.size):
                self.currently_displayed_items.append(self.menu_item_list[item + self.shifts])
        else:
            for item in range(self.max_displayed_items):
                self.currently_displayed_items.append(self.menu_item_list[item + self.shifts])

    def prepare_menu_for_display(self, details):
        self.talking_to = details["speaker_name"]
        self.friendship = self.get_friendship(int(details["friendship_level"]))
        self.face_image = details["face_image"]
        self.speaker_unique_name = details["speaker_unique_name"]
        self.actor_type = details["actor_type"]

    def generate_menu_information_package(self):
        source = self.get_menu_items_to_display().copy()
        cursor_at = self.cursor_at
        cursor_image = self.cursor
        text_display_list = []

        for item in range(len(source)):
            text_display_list.append(source[item])

        menu_specific = {"friendship_level": self.friendship,
                         "face_image": self.face_image,
                         "speaker_name": self.talking_to,
                         "actor_type": self.actor_type}

        menu_information = MenuInformation(self.menu_header, text_display_list, cursor_image, cursor_at, menu_specific)
        return menu_information

    def do_option(self):
        menu_selection = self.get_current_menu_item()
        self.gc.menu_controller.conversation_options_menu_selection(menu_selection)

    def get_friendship(self, friendship):
        friendship_counter = " - - - - "
        if friendship == 0:
            friendship_counter = " - - - - "
        # elif friendship == 1:
        #     friendship_counter = " \u2665 - - - "
        # elif friendship == 2:
        #     friendship_counter = " \u2665 \u2665 - - "
        # elif friendship == 3:
        #     friendship_counter = " \u2665 \u2665 \u2665 - "
        # elif friendship >= 4:
        #     friendship_counter = " \u2665 \u2665 \u2665 \u2665 "
        elif 5 >= friendship >= 1 :
            friendship_counter = " \u2665 - - - "
        elif 10 >= friendship >= 6:
            friendship_counter = " \u2665 \u2665 - - "
        elif 15 >= friendship >= 11:
            friendship_counter = " \u2665 \u2665 \u2665 - "
        elif friendship >= 16:
            friendship_counter = " \u2665 \u2665 \u2665 \u2665 "
        return friendship_counter

    def reset_elements(self):
        speaker_ghost = self.gc.gs.get_feature_ghost(self.speaker_unique_name)
        speaker_ghost.currently_chatting = False
        self.cursor_at[0] = 0
        self.cursor_at[1] = 0


class SellerOptionsMenuGhost(MenuGhost):
    BASE = "seller_options_menu"
    NAME = BASE + "_ghost"
    AVATAR = ChattingMenuAvatar

    def __init__(self, gc):
        super().__init__(gc)
        self.menu_header = None
        self.menu_type = Types.BASE
        self.menu_item_list = ["Buy", "Sell", "Exit"]
        self.menu_images_list = []
        self.cursor = "-"
        self.shifts = 0
        self.max_displayed_items = 14
        self.currently_displayed_items = []
        self.talking_to = None
        self.friendship = None
        self.face_image = None
        self.actor_type = None
        self.speaker_unique_name = None

    def cursor_down(self):
        if self.size > 1:
            if (self.cursor_at[1] + self.shifts) < self.size - 1:
                if self.size > self.max_displayed_items:
                    if self.cursor_at[1] == self.max_displayed_items - 1:
                        self.shifts += 1
                        self.update_currently_displayed()
                    elif self.cursor_at[1] < self.max_displayed_items - 1:
                        self.cursor_at[1] += 1
                    else:
                        pass

                elif self.max_displayed_items >= self.size > self.cursor_at[1]:
                    self.cursor_at[1] += 1

    def cursor_up(self):
        if (self.cursor_at[1] + self.shifts) > 0:
            if self.cursor_at[1] == 0 and self.shifts > 0:
                self.shifts -= 1
                self.update_currently_displayed()
            elif self.cursor_at[1] > 0:
                self.cursor_at[1] -= 1
            else:
                pass

    def prepare_menu_for_display(self, details):
        self.talking_to = details["speaker_name"]
        self.friendship = None,
        self.face_image = details["face_image"]
        self.speaker_unique_name = details["speaker_unique_name"]
        self.actor_type = details["actor_type"]

    def generate_menu_information_package(self):
        source = self.get_menu_items_to_display().copy()
        cursor_at = self.cursor_at
        cursor_image = self.cursor
        text_display_list = []

        for item in range(len(source)):
            text_display_list.append(source[item])

        menu_specific = {"friendship_level": self.friendship,
                         "face_image": self.face_image,
                         "speaker_name": self.talking_to,
                         "actor_type": self.actor_type}

        menu_information = MenuInformation(self.menu_header, text_display_list, cursor_image, cursor_at, menu_specific)
        return menu_information

    def do_option(self):
        menu_selection = self.get_current_menu_item()
        self.gc.menu_controller.seller_options_menu_selection(menu_selection)


    def reset_elements(self):
        speaker_ghost = self.gc.gs.get_feature_ghost(self.speaker_unique_name)
        speaker_ghost.currently_chatting = False
        self.cursor_at[0] = 0
        self.cursor_at[1] = 0


class SellerMenuGhost(MenuGhost):
    BASE = "seller_menu"
    NAME = BASE + "_ghost"
    AVATAR = SellerMenuAvatar

    def __init__(self, gc):
        super().__init__(gc)
        self.menu_header = "FOR SALE"
        self.menu_item_list = []
        self.menu_images_list = []
        self.cursor = "-"
        self.menu_prices = {}
        self.current_purchase_cost = 0
        # self.prepare_menu_for_display(None)

    def prepare_menu_for_display(self, details):
        self.menu_item_list = copy.copy(details["seller_items"])
        self.menu_item_list.sort()
        self.menu_prices = copy.copy(details["seller_item_prices"])
        self.menu_item_list.append("Exit")

    def choose_option(self):
        chosen_item_name = self.get_current_menu_item()
        if chosen_item_name == "Exit":
            self.gc.menu_controller.exit_all_menus()
        else:
            self.gc.menu_controller.post_notice("How many would you like to buy?")
            self.gc.menu_controller.set_menu(NumberSelectionMenuGhost.BASE, {"master_menu": self.BASE, "max_number": 99, "min_number": 1})

    def do_option(self, choice):
        menu_selection = self.get_current_menu_item()
        if choice == "Yes":
            self.gc.menu_controller.post_notice("Added the " + menu_selection + "(s) to your bag")
            self.gc.gs.spend_money(self.current_purchase_cost)
            print("money remaining", self.gc.gs.money_in_pocket)
        elif choice == "No":
            pass
        else:
            menu_selection = self.get_current_menu_item()
            price = self.menu_prices[menu_selection]
            total_cost = price * choice
            self.current_purchase_cost = total_cost
            self.gc.menu_controller.post_notice("That will be $" + str(total_cost))
            if self.gc.gs.check_if_have_enough_money(total_cost):
                self.gc.menu_controller.post_notice("Proceed with purchase?")
                self.gc.menu_controller.set_menu(SubMenuGhost.BASE, {"master_menu": self.BASE, "menu_items_list": ["Yes", "No"]})
            else:
                self.gc.menu_controller.post_notice("You do not have enough money...")

    def generate_menu_information_package(self):
        source = self.get_menu_items_to_display().copy()
        cursor_at = self.cursor_at
        cursor_image = self.cursor
        text_display_list = source

        menu_specific = {"header": self.menu_header,
                        "text_display_list": source,
                        "cursor_image": cursor_image,
                        "cursor_at": cursor_at}

        menu_information = MenuInformation(self.menu_header, text_display_list, cursor_image, cursor_at, menu_specific)
        return menu_information

    def get_menu_items_to_display(self):
        displayable_item_list = []

        for item in self.menu_item_list:
            if item == "Exit":
                displayable_item_list.append((item, "0"))

            else:
                price = str(self.menu_prices[item])
                displayable_item_list.append((item, price))

        return displayable_item_list


class SellItemMenuGhost(SuppliesInventoryMenuGhost):
    BASE = "sell_item_menu"
    NAME = BASE + "_ghost"
    AVATAR = SellerMenuAvatar

    def __init__(self, gc):
        super().__init__(gc)
        self.menu_type = Types.BASE
        self.menu_header = "SELL?"
        self.current_sell_quantity = 0

    def choose_option(self):
        chosen_item_name = self.get_current_menu_item()
        if chosen_item_name == "Exit":
            self.gc.menu_controller.exit_all_menus()
        else:
            self.gc.menu_controller.post_notice("How many would you like to sell?")
            self.gc.menu_controller.set_menu(NumberSelectionMenuGhost.BASE, {"master_menu": self.BASE, "max_number": 99, "min_number": 1})


    def do_option(self, choice):
        menu_selection = self.get_current_menu_item()
        menu_prices = self.gc.inventory_manager.price_list
        chosen_item = self.gc.gs.gd.item_data_list[menu_selection]
        if choice == "Yes":
            self.gc.menu_controller.post_notice("You sold the " + menu_selection +"(s).")
            self.gc.inventory_manager.remove_item(chosen_item, self.current_sell_quantity)
            self.prepare_menu_for_display(None)
        elif choice == "No":
            pass
        else:
            menu_selection = self.get_current_menu_item()
            price = menu_prices[menu_selection]
            total_cost = price * choice
            self.current_sell_quantity = choice
            self.current_purchase_cost = total_cost
            self.gc.menu_controller.post_notice("Sell " + str(choice) + " " + menu_selection + " for $" + str(total_cost) + "?")
            self.gc.menu_controller.set_menu(SubMenuGhost.BASE, {"master_menu": self.BASE, "menu_items_list": ["Yes", "No"]})

    def prepare_menu_for_display(self, details):
        keys_list = []
        current_inventory = self.gc.gs.get_inventory_items(SuppliesInventoryMenuGhost.BASE)
        if current_inventory:
            for item in current_inventory:
                keys_list.append(item)
            self.menu_item_list = keys_list
            self.menu_item_list.append("Exit")
            self.update_currently_displayed()

    def cursor_left(self):
        pass

    def cursor_right(self):
        pass

    def generate_menu_information_package(self):
        source = self.get_menu_items_to_display().copy()
        cursor_at = self.cursor_at
        cursor_image = self.cursor
        text_display_list = source

        menu_specific = {"header": self.menu_header,
                        "text_display_list": source,
                        "cursor_image": cursor_image,
                        "cursor_at": cursor_at}

        menu_information = MenuInformation(self.menu_header, text_display_list, cursor_image, cursor_at, menu_specific)
        return menu_information

    def get_menu_items_to_display(self):
        displayable_item_list = []

        menu_prices = self.gc.inventory_manager.price_list

        for item in self.menu_item_list:
            if item == "Exit":
                displayable_item_list.append((item, "0"))

            else:
                price = str(menu_prices[item])
                displayable_item_list.append((item, price))

        return displayable_item_list


class ChatMenuGhost(MenuGhost):
    BASE = "chat_menu"
    NAME = BASE + "_ghost"
    AVATAR = ChattingMenuAvatar

    def __init__(self, gc):
        super().__init__(gc)
        self.menu_header = None
        self.menu_type = Types.BASE
        self.menu_item_list = []
        self.menu_images_list = []
        self.cursor = None
        self.shifts = 0
        self.max_displayed_items = 14
        self.currently_displayed_items = []
        self.talking_to = None
        self.friendship = 0
        self.face_image = None
        self.phrase = None
        self.actor_type = None
        self.update_currently_displayed()
        self.speaking_queue = []
        self.current_phrase = []


    def update_currently_displayed(self):
        self.currently_displayed_items = []
        if self.size <= self.max_displayed_items:
            for item in range(self.size):
                self.currently_displayed_items.append(self.menu_item_list[item + self.shifts])
        else:
            for item in range(self.max_displayed_items):
                self.currently_displayed_items.append(self.menu_item_list[item + self.shifts])

    def prepare_menu_for_display(self, details):
        self.talking_to = details["speaker_name"]
        self.friendship = details["friendship_level"]
        self.face_image = details["face_image"]
        self.actor_type = details["actor_type"]
        self.speaker_unique_name = details["speaker_unique_name"]
        self.menu_item_list = details["phrase"]
        self.follow_up = details["follow_up"]

    def generate_menu_information_package(self):
        source = self.get_menu_items_to_display().copy()
        cursor_at = self.cursor_at
        cursor_image = self.cursor
        text_display_list = []

        for item in range(len(source)):
            text_display_list.append(source[item])

        menu_specific = {"friendship_level": self.friendship,
                         "face_image": self.face_image,
                         "speaker_name": self.talking_to,
                         "actor_type": self.actor_type}

        menu_information = MenuInformation(self.menu_header, text_display_list, cursor_image, cursor_at, menu_specific)
        return menu_information

    def do_option(self):
        self.set_speaking_queue()

    def set_current_phrase(self, phrases):
        self.current_phrase = textwrap.wrap(phrases[0], width=20)
        self.set_speaking_queue()

    def set_speaking_queue(self):
        phrase_counter = 0
        self.menu_item_list = []
        if len(self.current_phrase) > 2:
            for line in range(3):
                self.menu_item_list.append(self.current_phrase.pop(0))

        elif (len(self.current_phrase) <= 2) and (len(self.current_phrase) > 0):
            for line in range(len(self.current_phrase)):
                self.menu_item_list.append(self.current_phrase.pop(0))

        elif len(self.current_phrase) == 0:
            menu_selection = None
            self.gc.menu_controller.chat_menu_selection(menu_selection, self.follow_up)

    def reset_elements(self):
        speaker_ghost = self.gc.gs.get_feature_ghost(self.speaker_unique_name)
        speaker_ghost.currently_chatting = False
        self.cursor_at[0] = 0
        self.cursor_at[1] = 0


class OutfitMenuGhost(MenuGhost):
    BASE = "outfit_menu"
    NAME = BASE + "_ghost"
    AVATAR = GalleryMenuAvatar

    def __init__(self, gc):
        super().__init__(gc)
        self.menu_header = None
        self.menu_type = Types.BASE
        self.menu_item_list = []
        self.menu_images_list = []
        self.cursor = "-"
        self.shifts = 0
        self.max_displayed_items = 14
        self.currently_displayed_items = []
        self.update_currently_displayed()
        self.current_outfits_list = []
        self.selected_outfit = Outfit(gc.gs.gv, "green_shirt", "Green Shirt", 32, 48)
        self.is_last_outfit = False
        self.is_first_outfit = False
        self.outfit_number = 0

    def update_currently_displayed(self):
        self.currently_displayed_items = []
        if self.size <= self.max_displayed_items:
            for item in range(self.size):
                self.currently_displayed_items.append(self.menu_item_list[item + self.shifts])
        else:
            for item in range(self.max_displayed_items):
                self.currently_displayed_items.append(self.menu_item_list[item + self.shifts])

    def prepare_menu_for_display(self, details):
        self.current_outfits_list = self.gc.outfit_manager.get_acquired_outfits()
        self.make_main_outfit(0)

    def generate_menu_information_package(self):
        source = self.get_menu_items_to_display().copy()
        cursor_at = self.cursor_at
        cursor_image = self.cursor
        text_display_list = []

        for item in range(len(source)):
            text_display_list.append(source[item])

        is_first_outfit = self.is_first_outfit
        is_last_outfit = self.is_last_outfit
        image = self.selected_outfit.spritesheet
        image_choice = image.get_image(0, 0)

        menu_specific = {"menu_title": "OUTFITS",
                         "item_name": self.selected_outfit.display_name,
                         "is_first_item": is_first_outfit,
                         "is_last_item": is_last_outfit,
                         "item_image": image_choice}

        menu_information = MenuInformation(self.menu_header, text_display_list, cursor_image, cursor_at, menu_specific)
        return menu_information

    def do_option(self):
        self.gc.outfit_manager.put_on_outfit(self.selected_outfit.file_name)
        self.gc.menu_controller.exit_all_menus()


    def cursor_left(self):
        length = len(self.current_outfits_list)
        if 0 < self.outfit_number:
            new_number = self.outfit_number - 1
            self.make_main_outfit(new_number)
        else:
            pass

    def cursor_right(self):
        length = len(self.current_outfits_list)
        if (length - 1) > self.outfit_number:
            new_number = self.outfit_number + 1
            self.make_main_outfit(new_number)
        else:
            pass

    def make_main_outfit(self, number):
        self.outfit_number = number
        # outfit_keys = self.outfit_list.keys()
        # sorted_keys = sorted(outfit_keys)
        # self.selected_outfit = sorted_keys[number]

        self.selected_outfit = self.current_outfits_list[number]

        length = len(self.current_outfits_list)
        if number == (length - 1):
            self.is_last_outfit = True
        else:
            self.is_last_outfit = False
        if number == 0:
            self.is_first_outfit = True
        else:
            self.is_first_outfit = False


class GalleryMenuGhost(MenuGhost):
    BASE = "gallery_menu"
    NAME = BASE + "_ghost"
    AVATAR = GalleryMenuAvatar

    def __init__(self, gc):
        super().__init__(gc)
        self.menu_header = None
        self.menu_type = Types.BASE
        self.menu_item_list = []
        self.menu_images_list = []
        self.cursor = "-"
        self.shifts = 0
        self.max_displayed_items = 14
        self.currently_displayed_items = []
        self.galleries = ["Tree", "Bird", "Pigeon"]
        # self.update_currently_displayed()
        self.Tree_item_list = {"Arbutus": ["Arbutus", "Arbutus"]}
        self.Bird_item_list = {"Robin": ["Robin", "Robin"],
                          "Tanager": ["Tanager", "Tanager"],
                          "Blackbird": ["Blackbird", "Blackbird"],
                          "Mallard": ["Mallard", "Mallard"]}

        self.Pigeon_item_list = {"Pigeon 1": ["Pigeon 1", "Pigeon 1"],
                          "Pigeon 2": ["Pigeon 2", "Pigeon 2"],
                          "Pigeon 3": ["Pigeon 3", "Pigeon 3"],
                          "Pigeon 4": ["Pigeon 4", "Pigeon 4"]}
        for item in self.galleries:
            setattr(self, "selected_" + item, "default")
            setattr(self, "is_last_" + item, False)
            setattr(self, "is_first_" + item, True)
            setattr(self, item + "_number", 0)
            setattr(self, item + "_number", 0)
        self.prepare_menu_for_display(None)

        self.current_gallery = "Bird"

    def check_if_item_in_list(self, list_type, item_name):
        result = False
        for item in getattr(self, list_type + "_item_list").keys():
            if item_name == item:
                result = True
        return result

    def add_to_item_list(self, list_type, species, display_name):
        getattr(self, list_type + "_item_list")[species] = [species, display_name]

    def prepare_menu_for_display(self, details):
        for item in self.galleries:
            self.make_main_item(item, 0)

    def get_pigeon_image(self, pigeon_name):
        image = Spritesheet("Player_base_spritesheet", "assets/spritesheets/special_spritesheets/Pigeon_special_spritesheet.png", 32, 48)
        image_choice = image.get_image(0, 0)
        if pigeon_name == "Pigeon 1":
            image_choice = image.get_image(0, 0)
        elif pigeon_name == "Pigeon 2":
            image_choice = image.get_image(1, 0)
        elif pigeon_name == "Pigeon 3":
            image_choice = image.get_image(2, 0)
        elif pigeon_name == "Pigeon 4":
            image_choice = image.get_image(3, 0)
        return image_choice

    def generate_menu_information_package(self):
        source = self.get_menu_items_to_display().copy()
        cursor_at = self.cursor_at
        cursor_image = self.cursor
        text_display_list = []

        for item in range(len(source)):
            text_display_list.append(source[item])

        sprite_code = getattr(self, "selected_" + self.current_gallery)

        is_first_item = getattr(self, "is_first_" + self.current_gallery)
        is_last_item = getattr(self, "is_last_" + self.current_gallery)

        spritesheet_file_name = None
        if self.current_gallery == "Tree":
            spritesheet_file_name = "prop_spritesheets"
        elif self.current_gallery == "Bird" or self.current_gallery == "Pigeon":
            spritesheet_file_name = "bird_spritesheets"

        if getattr(self, "selected_" + self.current_gallery) in ["Pigeon 1", "Pigeon 2", "Pigeon 3", "Pigeon 4"]:
            image_choice = self.get_pigeon_image(getattr(self, "selected_" + self.current_gallery))
        else:
            image = Spritesheet("Player_base_spritesheet", "assets/spritesheets/feature_spritesheets/" + spritesheet_file_name + "/" + sprite_code + "_spritesheet.png", 32, 64)
            image_choice = image.get_image(0, 0)

        menu_specific = {"menu_title": "GALLERY",
                         "item_name": getattr(self, self.current_gallery + "_item_list")[getattr(self, "selected_" + self.current_gallery)][1],
                         "is_first_item": is_first_item,
                         "is_last_item": is_last_item,
                         "item_image": image_choice}

        menu_information = MenuInformation(self.menu_header, text_display_list, cursor_image, cursor_at, menu_specific)
        return menu_information

    def do_option(self):
        details = {"image": "Crow"}
        self.gc.menu_controller.set_menu(PictureMenuGhost.BASE, details)

    def cursor_left(self):
        getattr(self, self.current_gallery + "_number")
        if 0 < getattr(self, self.current_gallery + "_number"):
            new_number = getattr(self, self.current_gallery + "_number") - 1
            self.make_main_item(self.current_gallery, new_number)

    def cursor_right(self):
        length = len(getattr(self, self.current_gallery + "_item_list"))
        if (length - 1) > getattr(self, self.current_gallery + "_number"):
            new_number = getattr(self, self.current_gallery + "_number") + 1
            self.make_main_item(self.current_gallery, new_number)

    def cursor_up(self):
        current_number = self.galleries.index(self.current_gallery)
        if current_number > 0:
            self.current_gallery = self.galleries[current_number-1]
        else:
            pass

    def cursor_down(self):
        current_number = self.galleries.index(self.current_gallery)
        if current_number < len(self.galleries)-1:
            self.current_gallery = self.galleries[current_number+1]
        else:
            pass

    def make_main_item(self, list_type, number):
        setattr(self, list_type + "_number", number)
        list_keys = getattr(self, list_type + "_item_list").keys()
        sorted_keys = sorted(list_keys)
        setattr(self, "selected_" + list_type, sorted_keys[number])

        length = len(sorted_keys)
        if number == (length - 1):
            setattr(self, "is_last_" + list_type, True)
        else:
            setattr(self, "is_last_" + list_type, False)
        if number == 0:
            setattr(self, "is_first_" + list_type, True)
        else:
            setattr(self, "is_first_" + list_type, False)


class MapMenuGhost(MenuGhost):
    BASE = "map_menu"
    NAME = BASE + "_ghost"
    AVATAR = ImageMenuAvatar

    def __init__(self, gc):
        super().__init__(gc)
        self.menu_header = None
        self.menu_type = Types.BASE
        self.menu_item_list = []
        image = Spritesheet("Hornby_map_spritesheet", "assets/spritesheets/map_spritesheets/Hornby_map" + "_spritesheet.png",  256, 160)
        image_choice = image.get_image(0, 0)
        self.menu_images_list = [image_choice]
        self.cursor = None
        self.shifts = 0
        self.max_displayed_items = 14
        self.currently_displayed_items = []

    def prepare_menu_for_display(self, details):
        pass

    def generate_menu_information_package(self):
        # setting up text box
        image_pass_list = []
        for image in self.menu_images_list:
            passer = ComponentPass(image, None)
            image_pass_list.append(passer)

        menu_specific = {"image_passes": image_pass_list}

        menu_information = MenuInformation(self.menu_header, None, None, None, menu_specific)
        return menu_information

    def do_option(self):
        self.gc.menu_controller.exit_all_menus()


class PictureMenuGhost(MenuGhost):
    BASE = "picture_menu"
    NAME = BASE + "_ghost"
    AVATAR = ImageMenuAvatar

    def __init__(self, gc):
        super().__init__(gc)
        self.menu_header = None
        self.menu_type = Types.BASE
        self.menu_item_list = []
        self.image_name = "Tanager"
        image = Spritesheet("picture_spritesheet", "assets/spritesheets/irl_images/" + self.image_name + "_image.png",  256, 160)
        image_choice = image.get_image(0, 0)
        self.menu_images_list = [image_choice]
        self.cursor = "-"
        self.shifts = 0
        self.max_displayed_items = 14
        self.currently_displayed_items = []

    def prepare_menu_for_display(self, details):
        self.image_name = details["image"]

    def generate_menu_information_package(self):
        # setting up text box
        image_pass_list = []
        for image in self.menu_images_list:
            passer = ComponentPass(image, None)
            image_pass_list.append(passer)

        menu_specific = {"image_passes": image_pass_list}

        menu_information = MenuInformation(self.menu_header, None, None, None, menu_specific)
        return menu_information

    def do_option(self):
        self.gc.menu_controller.exit_all_menus()


class GameActionDialogueMenuGhost(MenuGhost):
    BASE = "game_action_dialogue_menu"
    NAME = BASE + "_ghost"
    AVATAR = GameActionDialogueMenuAvatar

    def __init__(self, gc):
        super().__init__(gc)

        self.gc = gc

        self.menu_header = None
        self.menu_item_list = ["This is the game dialouge box!"]
        self.menu_images_list = []
        self.additional_information = []
        self.menu_type = Types.STATIC

        self.cursor = None
        self.cursor_at = [0, 0]
        self.name = self.NAME

    @property
    def size(self):
        return len(self.menu_item_list)

    def show_dialogue(self, phrase):
        if len(self.menu_item_list) >= 4:
            del self.menu_item_list[0]
        self.menu_item_list.append(phrase)

    def generate_image_display(self):
        image_display_list = []
        return image_display_list

    def prepare_menu_for_display(self):
        pass


class SubMenuGhost(MenuGhost):
    BASE = "sub_menu"
    NAME = BASE + "_ghost"
    AVATAR = SubMenuAvatar

    def __init__(self, gc):
        super().__init__(gc)
        self.menu_item_list = ["Yes", "No"]
        self.master_menu = None
        self.menu_type = Types.SUB
        self.menu_header = None

    def choose_option(self):
        self.do_option()

    def set_master_menu(self, master_menu):
        self.master_menu = master_menu

    def prepare_menu_for_display(self, details):
        self.menu_item_list = details["menu_items_list"]

    def do_option(self, choice=None):
        menu_selection = choice
        chosen_item_name = self.get_current_menu_item()
        self.gc.menu_controller.exit_menu(self.BASE)
        self.gc.gs.ms.get_menu_ghost(self.master_menu).do_option(chosen_item_name)


class NumberSelectionMenuGhost(MenuGhost):
    BASE = "number_selection_menu"
    NAME = BASE + "_ghost"
    AVATAR = NumberSelectionMenuAvatar

    def __init__(self, gc):
        super().__init__(gc)
        self.menu_item_list = []
        self.master_menu = None
        self.menu_type = Types.SUB
        self.menu_header = None
        self.max_number = 1
        self.min_number = 0
        self.current_number = 0

    def reset_elements(self):
        self.max_number = 1
        self.min_number = 0
        self.current_number = 0

    def choose_option(self):
        self.do_option()

    def set_master_menu(self, master_menu):
        self.master_menu = master_menu

    def cursor_left(self):
        if self.current_number > self.min_number:
            self.current_number -= 1

    def cursor_right(self):
        if self.current_number < self.max_number:
            self.current_number += 1

    def prepare_menu_for_display(self, details):
        self.max_number = details["max_number"]
        self.min_number = details["min_number"]
        self.current_number = self.min_number
        self.menu_item_list = [str(0)]

    def get_current_menu_item(self):
        menu_selection = self.current_number
        return menu_selection

    def do_option(self, choice=None):
        chosen_number = self.get_current_menu_item()
        self.gc.menu_controller.exit_menu(self.BASE)
        self.gc.gs.ms.get_menu_ghost(self.master_menu).do_option(chosen_number)

    def generate_menu_information_package(self):
        source = self.get_menu_items_to_display().copy()
        cursor_at = self.cursor_at
        cursor_image = self.cursor

        final_text = Mundane.number_to_string_leading_zeros(self.current_number, 4)

        if self.current_number > self.min_number:
            final_text = "< " + final_text
        else:
            final_text = "  " + final_text

        if self.current_number < self.max_number:
            final_text = final_text + " >"

        text_display_list = [final_text]

        menu_specific = {"number_to_display": text_display_list}

        menu_information = MenuInformation(self.menu_header, text_display_list, cursor_image, cursor_at, menu_specific)
        return menu_information


class TextInputMenuGhost(MenuGhost):
    BASE = "text_input_menu"
    NAME = BASE + "_ghost"
    AVATAR = TextInputMenuAvatar

    def __init__(self, gc):
        super().__init__(gc)
        self.menu_item_list = []
        self.master_menu = None
        self.menu_type = Types.SUB
        self.menu_header = None
        self.current_text = ""
        self.max_text_length = 8
        self.text_entry_boxes = {"input_box_1": TextEntryBoxGhost(self.gc, "input_box_1")}
        self.setup_buttons_list()

    def once_set_actions(self):
        self.gc.menu_controller.set_current_text_entry_box("input_box_1")

    def unset_text_entry_box_followup(self):
        self.choose_option()

    def reset_elements(self):
        self.current_text = ""

    def prepare_menu_for_display(self, details):
        self.current_text = ""
        self.menu_item_list = self.current_text

    def do_option(self, choice=None):
        chosen_word = self.text_entry_boxes["input_box_1"].current_text
        if len(chosen_word) <= 2:
            print("that's not long enough!")
        else:
            self.gc.menu_controller.exit_menu(self.BASE)
            self.gc.gs.ms.get_menu_ghost(self.master_menu).do_option(chosen_word)

    def generate_menu_information_package(self):
        text_boxes_list = []
        for index, text_box in enumerate(self.text_entry_boxes.keys()):
            text_box_object = self.text_entry_boxes[text_box]
            passer_box = ComponentPass(text_box_object.final_surface, text_box_object.name)
            text_boxes_list.append(passer_box)

        menu_specific = {"textbox_passes": text_boxes_list}

        menu_information = MenuInformation(self.menu_header, None, None, None, menu_specific)
        return menu_information

    def setup_buttons_list(self):
        input_box_1_button = ButtonGhost(self.gc, "input_box_1", self.BASE, "set_current_text_entry_box", "input_box_1")
        self.button_list["input_box_1"] = input_box_1_button


class GuideMenuGhost(MenuGhost):
    BASE = "guide_menu"
    NAME = BASE + "_ghost"
    AVATAR = GuideMenuAvatar

    def __init__(self, gc):
        super().__init__(gc)
        self.menu_header = None
        self.menu_type = Types.BASE
        self.menu_item_list = []
        self.menu_images_list = []
        self.cursor = "-"
        self.shifts = 0
        self.max_displayed_items = 14
        self.currently_displayed_items = []
        bird_list = copy.copy(self.gc.gs.gd.bird_master_list)
        self.master_birds_list = sorted(bird_list)
        if not Mundane.is_even(len(self.master_birds_list)):
            self.master_birds_list.append(None)
        self.current_page = 0
        self.total_pages = math.ceil(len(self.master_birds_list)/2)

    def cursor_left(self):
        if self.current_page > 1:
            self.current_page -= 2

    def cursor_right(self):
        if self.current_page < len(self.master_birds_list) - 2:
            self.current_page += 2

    def prepare_menu_for_display(self, details):
        pass

    def check_if_have_panel(self, name):
        result = False
        if name in self.gc.gs.held_pages:
            result = True
        # if name:
        #     if top_or_bottom == "top":
        #         bottom_panel_list = ["Meadowlark", "Starling", "Saw-whet Owl", "Barred Owl", "Great Horned Owl", 'Nighthawk',
        #                 "Blackbird", "Junko", "Flycatcher", "Wood Peewee", "Thrush", "Robin",  "Cormorant", "Seagull", "Coot",
        #                 "Kingfisher", "Murrelet", "Harlequin Duck"]
        #         if name in bottom_panel_list:
        #             result = True
        #     if top_or_bottom == "bottom":
        #         top_panel_list = ["Meadowlark", "Crow", "Tanager", "Starling", "Saw-whet_Owl", "Barred_Owl", "Great_Horned_Owl", 'Nighthawk',
        #                              "Blackbird", "Junko", "Flycatcher", "Robin", "Goldfinch", "Cormorant", "Seagull", "Coot", "Green_Heron",
        #                              "Kingfisher", "Mallard", "Murrelet", 'Eurasian_Wigeon', "Harlequin_Duck", "Wood Peewee"]
        #         if name in top_panel_list:
        #             result = True
        # else:
        #     pass

        return result

    def generate_menu_information_package(self):
        cursor_at = self.cursor_at
        cursor_image = self.cursor
        text_display_list = []

        bird1 = self.master_birds_list[self.current_page]
        bird2 = self.master_birds_list[self.current_page + 1]
        bird1_page_top = None
        bird1_page_bottom = None
        bird2_page_top = None
        bird2_page_bottom = None

        if not bird1:
            panel1 = False
            panel2 = False
        else:
            panel1 = self.check_if_have_panel(bird1 + "top")
            panel2 = self.check_if_have_panel(bird1 + "bottom")
            if panel1:
                bird1_page_top = self.gc.inventory_manager.fetch_page(bird1 + "top")
            if panel2:
                bird1_page_bottom = self.gc.inventory_manager.fetch_page(bird1 + "bottom")

        if not bird2:
            panel3 = False
            panel4 = False
        else:
            panel3 = self.check_if_have_panel(bird2 + "top")
            panel4 = self.check_if_have_panel(bird2 + "bottom")
            if panel3:
                bird2_page_top = self.gc.inventory_manager.fetch_page(bird2 + "top")
            if panel4:
                bird2_page_bottom = self.gc.inventory_manager.fetch_page(bird2 + "bottom")

        if panel1:
            image1 = True
            # bird_ghost = self.gc.gs.gd.get_feature_ghost(self.master_birds_list[self.current_page])
            text_display_list.append(self.master_birds_list[self.current_page])
            text_display_list.append("Colour: " + bird1_page_top.colour)
            text_display_list.append("Size: " + bird1_page_top.size)
            text_display_list.append("Call: " + bird1_page_top.call)
        else:
            image1 = False
            text_display_list.append(" ")
            text_display_list.append(" ")
            text_display_list.append(" ")
            text_display_list.append(" ")

        if panel2:
            image2 = True
            description = textwrap.wrap(bird1_page_bottom.approach, width=15)
            text_display_list.append(description)
        else:
            image2 = False
            text_display_list.append([" "])

        if panel3:
            image3 = True
            text_display_list.append(self.master_birds_list[self.current_page + 1])
            text_display_list.append("Colour: " + bird2_page_top.colour)
            text_display_list.append("Size: " + bird2_page_top.size)
            text_display_list.append("Call: " + bird2_page_top.call)
        else:
            image3 = False
            text_display_list.append(" ")
            text_display_list.append(" ")
            text_display_list.append(" ")
            text_display_list.append(" ")

        if panel4:
            image4 = True
            description = textwrap.wrap(bird1_page_bottom.approach, width=15)
            text_display_list.append(description)
        else:
            image4 = False
            text_display_list.append([" "])

        on_first_page = True
        on_last_page = True

        if self.current_page > 1:
            on_first_page = False
        else:
            on_first_page = True

        if self.current_page < len(self.master_birds_list) - 2:
            on_last_page = False
        else:
            on_last_page = True

        if not on_first_page:
            text_display_list.append("<")
        else:
            text_display_list.append("")

        if not on_last_page:
            text_display_list.append(">")
        else:
            text_display_list.append("")

        page_left = self.current_page + 1
        page_right = page_left + 1

        menu_specific = {"image": [image1, image2, image3, image4], "page_left": page_left, "page_right": page_right}



        menu_information = MenuInformation(self.menu_header, text_display_list, cursor_image, cursor_at, menu_specific)
        return menu_information

    def do_option(self):
        self.gc.menu_controller.exit_all_menus()

    def reset_elements(self):
        self.current_page = 0


class SceneDialogueMenuGhost(MenuGhost):
    BASE = "scene_dialogue_menu"
    NAME = BASE + "_ghost"
    AVATAR = ChattingMenuAvatar

    def __init__(self, gc):
        super().__init__(gc)
        self.menu_header = None
        self.menu_type = Types.BASE
        self.menu_item_list = []
        self.menu_images_list = []
        self.cursor = " "
        self.shifts = 0
        self.max_displayed_items = 14
        self.currently_displayed_items = []
        self.talking_to = None
        self.friendship = 0
        self.face_image = None
        self.actor_type = None
        self.phrase = None
        self.update_currently_displayed()
        self.speaking_queue = []
        self.current_phrase = []


    def update_currently_displayed(self):
        self.currently_displayed_items = []
        if self.size <= self.max_displayed_items:
            for item in range(self.size):
                self.currently_displayed_items.append(self.menu_item_list[item + self.shifts])
        else:
            for item in range(self.max_displayed_items):
                self.currently_displayed_items.append(self.menu_item_list[item + self.shifts])

    def prepare_menu_for_display(self, details):
        self.talking_to = details["speaker_name"]
        self.friendship = details["friendship_level"]
        self.face_image = details["face_image"]
        self.actor_type = details["actor_type"]
        self.speaker_unique_name = details["speaker_unique_name"]
        self.menu_item_list = details["phrase"]

    def generate_menu_information_package(self):
        source = self.get_menu_items_to_display().copy()
        cursor_at = self.cursor_at
        cursor_image = self.cursor
        text_display_list = []

        for item in range(len(source)):
            text_display_list.append(source[item])

        menu_specific = {"friendship_level": self.friendship,
                         "face_image": self.face_image,
                         "speaker_name": self.talking_to,
                         "actor_type": self.actor_type}

        menu_information = MenuInformation(self.menu_header, text_display_list, cursor_image, cursor_at, menu_specific)
        return menu_information

    def do_option(self):
        self.set_speaking_queue()

    def set_current_phrase(self, phrases):
        self.current_phrase = textwrap.wrap(phrases[0], width=20)
        self.set_speaking_queue()

    def set_speaking_queue(self):
        phrase_counter = 0
        self.menu_item_list = []
        if len(self.current_phrase) > 2:
            for line in range(3):
                self.menu_item_list.append(self.current_phrase.pop(0))

        elif (len(self.current_phrase) <= 2) and (len(self.current_phrase) > 0):
            for line in range(len(self.current_phrase)):
                self.menu_item_list.append(self.current_phrase.pop(0))

        elif len(self.current_phrase) == 0:
            menu_selection = None
            self.gc.menu_controller.scene_menu_selection(menu_selection)

    def reset_elements(self):
        pass


# Builder menus

class CharacterAssemblyMenuGhost(MenuGhost):
    BASE = "character_assembly_menu"
    NAME = BASE + "_ghost"
    AVATAR = CharacterAssemblyMenuAvatar

    def __init__(self, gc):
        super().__init__(gc)
        self.menu_header = None
        self.menu_type = Types.BASE
        self.menu_item_list = []
        self.menu_images_list = []
        self.cursor = "-"
        self.shifts = 0
        self.max_displayed_items = 14
        self.currently_displayed_items = []

        self.text_entry_boxes = {"assembly_box_1": TextEntryBoxGhost(self.gc, "assembly_box_1")}
        self.currently_selected_text_entry_box = None
        self.button_list = {}
        self.arrow_list = ["<", ">"]

        self.legs_counter = 0
        self.torso_counter = 0
        self.hair_counter = 0
        self.eyes_counter = 0
        self.head_counter = 0
        self.mouth_counter = 0
        self.parts_list = ["head", "torso", "eyes", "hair", "mouth", "legs"]
        self.current_part = "torso"
        self.selected_head = 1
        self.selected_eyes = 1
        self.selected_hair = 1
        self.selected_torso = 1
        self.selected_legs = 1
        self.selected_mouth = 1
        self.mouth_list = {"front": {},
                          "back": {},
                          "right": {}}
        self.hair_list = {"front": {},
                          "back": {},
                          "right": {}}
        self.head_list = {"front": {},
                          "back": {},
                          "right": {}}
        self.eyes_list = {"front": {},
                          "back": {},
                          "right": {}}
        self.torso_list = {"front": {"frame_1": {},
                                     "frame_2": {}},
                           "back": {"frame_1": {},
                                     "frame_2": {}},
                           "right": {"frame_1": {},
                                     "frame_2": {},
                                     "frame_4": {}}}
        self.legs_list = {"front": {"frame_1": {},
                                    "frame_2": {}},
                          "back": {"frame_1": {},
                                    "frame_2": {}},
                          "right": {"frame_1": {},
                                    "frame_2": {},
                                    "frame_4": {}}}
        self.process_all_parts()
        self.bg_pink = (255, 145, 211)
        self.skin_base = (236, 214, 184)
        self.skin_base_2 = (155, 146, 134)
        self.primary_colour = (204, 204, 204)
        self.secondary_colour = (106, 106, 106)

        dark_red = (141, 43, 41)
        light_red = (255, 0, 0)

        dark_orange = (199, 101, 0)
        light_orange = (255, 167, 0)

        dark_yellow = (159, 138, 0)
        light_yellow = (255, 255, 0)

        light_green = (0, 255, 0)
        dark_green = (23, 119, 16)

        light_blue = (128, 197, 213)
        dark_blue = (48, 59, 156)

        teal = (0, 128, 128)

        lavender = (191, 140, 181)
        purple = (153, 39, 155)

        white = (255, 255, 255)
        black = (46, 46, 46)

        light_pink = (255, 146, 222)
        dark_pink = (217, 0, 152)
        magenta = (255, 0, 255)


        skin_2 = (246, 231, 218)
        skin_3 = (240, 213, 190)
        skin_4 = (229, 188, 155)
        skin_5 = (214, 161, 124)
        skin_6 = (197, 139, 96)
        skin_7 = (169, 111, 73)
        skin_8 = (139, 88, 60)
        skin_9 = (112, 67, 47)
        skin_10 = (82, 49, 36)

        self.selected_torso_colour = copy.copy(self.primary_colour)
        self.selected_legs_colour = copy.copy(self.primary_colour)
        self.selected_hair_colour = copy.copy(self.primary_colour)
        self.selected_head_colour = copy.copy(self.primary_colour)
        self.selected_mouth_colour = copy.copy(self.primary_colour)
        self.selected_eyes_colour = copy.copy(self.primary_colour)

        self.selected_torso_secondary_colour = copy.copy(self.secondary_colour)
        self.selected_legs_secondary_colour = copy.copy(self.secondary_colour)
        self.selected_hair_secondary_colour = copy.copy(self.secondary_colour)
        self.selected_head_secondary_colour = copy.copy(self.secondary_colour)
        self.selected_mouth_secondary_colour = copy.copy(self.secondary_colour)
        self.selected_eyes_secondary_colour = copy.copy(self.secondary_colour)
        self.primary_squares_list = []
        self.secondary_squares_list = []
        self.skin_tone_options = [skin_2, skin_3, skin_4, skin_5, skin_6, skin_7, skin_8, skin_9, skin_10]
        self.fun_colours = [white, black, dark_red, light_red, dark_orange, light_orange, light_yellow, dark_yellow, light_blue, dark_blue, light_green, teal, dark_green, lavender, purple, light_pink, dark_pink, magenta]
        self.colour_options = [self.primary_colour, self.secondary_colour] + self.skin_tone_options + self.fun_colours
        self.colour_buttons_list_primary = {}
        self.colour_buttons_list_secondary = {}
        self.final_front_frame_1 = self.assemble_front_1()
        self.final_front_frame_2 = self.assemble_front_2()
        self.final_front_frame_3 = self.assemble_front_1()
        self.final_front_frame_4 = self.assemble_front_4()
        self.final_back_frame_1 = self.assemble_back_1()
        self.final_back_frame_2 = self.assemble_back_2()
        self.final_back_frame_3 = self.assemble_back_1()
        self.final_back_frame_4 = self.assemble_back_4()
        self.final_right_frame_1 = self.assemble_right_1()
        self.final_right_frame_2 = self.assemble_right_2()
        self.final_right_frame_3 = self.assemble_right_1()
        self.final_right_frame_4 = self.assemble_right_4()
        self.final_left_frame_1 = self.assemble_left_1()
        self.final_left_frame_2 = self.assemble_left_2()
        self.final_left_frame_3 = self.assemble_left_1()
        self.final_left_frame_4 = self.assemble_left_4()
        self.setup_buttons_list()

        self.prepare_menu_for_display(None)

    def generate_menu_information_package(self):
        source = self.get_menu_items_to_display().copy()
        cursor_at = self.cursor_at
        cursor_image = self.cursor
        text_display_list = []

        for item in range(len(source)):
            text_display_list.append(source[item])

        # setting up parts selection list
        parts_pass_list = []
        for item in self.parts_list:
            passer = ComponentPass(item, item + "_change_button")
            if item != self.current_part:
                passer.lowlight_text()
            parts_pass_list.append(passer)

        # setting up arrows
        left_arrow_pass = ComponentPass(self.arrow_list[0], "left_arrow_button")
        right_arrow_pass = ComponentPass(self.arrow_list[1], "right_arrow_button")

        # setting up sprites
        frame_list = [self.final_front_frame_1, self.final_front_frame_2, self.final_front_frame_3, self.final_front_frame_4,
                       self.final_back_frame_1, self.final_back_frame_2, self.final_back_frame_3, self.final_back_frame_4,
                       self.final_left_frame_1, self.final_left_frame_2, self.final_left_frame_3, self.final_left_frame_4,
                       self.final_right_frame_1, self.final_right_frame_2, self.final_right_frame_3, self.final_right_frame_4]
        frame_passer_list = []
        for item in frame_list:
            passer = ComponentPass(item, None)
            frame_passer_list.append(passer)

        # setting up colour squares
        self.setup_colour_select_images()

        primary_square_pass_list = []
        for index, square in enumerate(self.primary_squares_list):
            passer = ComponentPass(square, "button_primary_" + str(index))
            primary_square_pass_list.append(passer)

        secondary_square_pass_list = []
        for index, square in enumerate(self.secondary_squares_list):
            passer = ComponentPass(square, "button_secondary_" + str(index))
            secondary_square_pass_list.append(passer)

        current_attributes_colour_primary = getattr(self, "selected_" + self.current_part + "_colour")
        primary_colour_index = self.colour_options.index(current_attributes_colour_primary)

        current_attributes_colour_secondary = getattr(self, "selected_" + self.current_part + "_secondary_colour")
        secondary_colour_index = self.colour_options.index(current_attributes_colour_secondary)

        # setting up text box
        text_boxes_list = []
        for index, text_box in enumerate(self.text_entry_boxes.keys()):
            text_box_object = self.text_entry_boxes[text_box]
            passer_box = ComponentPass(text_box_object.final_surface, text_box_object.name)
            text_boxes_list.append(passer_box)

        header = [ComponentPass("ASSEMBLE", None)]

        menu_specific = {"parts_passes": parts_pass_list,
                         "arrow_passes": [left_arrow_pass, right_arrow_pass],
                         "spritesheet_passes": frame_passer_list,
                         "primarycolour_passes": primary_square_pass_list,
                         "secondarycolour_passes": secondary_square_pass_list,
                         "textbox_dict": text_boxes_list,
                         "header_passes": header}

        menu_information = MenuInformation(self.menu_header, text_display_list, cursor_image, cursor_at, menu_specific)
        return menu_information

    def setup_buttons_list(self):
        button_count = 0
        for item in self.colour_options:
            # primary colour
            button_name = "button_primary_" + str(button_count)
            button = ButtonGhost(self.gc, button_name, self.BASE, "select_primary_colour", {"colour": item})
            self.colour_buttons_list_primary[button_name] = button
            self.button_list[button_name] = button

            # secondary colour
            button_name = "button_secondary_" + str(button_count)
            button = ButtonGhost(self.gc, button_name, self.BASE, "select_secondary_colour", {"colour": item})
            self.colour_buttons_list_secondary[button_name] = button
            self.button_list[button_name] = button
            button_count += 1

        # setup other buttons
        for item in self.parts_list:
            part_change_button = ButtonGhost(self.gc, item + "_change_button", self.BASE, "select_current_part", {"selected_part": item})
            self.button_list[item + "_change_button"] = part_change_button

        left_arrow_button = ButtonGhost(self.gc, "left_arrow_button", self.BASE, "cursor_left", {})
        self.button_list["left_arrow_button"] = left_arrow_button

        right_arrow_button = ButtonGhost(self.gc, "right_arrow_button", self.BASE, "cursor_right", {})
        self.button_list["right_arrow_button"] = right_arrow_button

        assembly_box_1_button = ButtonGhost(self.gc, "assembly_box_1", self.BASE, "set_current_text_entry_box", "assembly_box_1")
        self.button_list["assembly_box_1"] = assembly_box_1_button

    def process_all_parts(self):
        legs_files = Mundane.get_file_names_from_directory("assets/character_assembly/legs")
        for file in legs_files:
            self.process_legs_sheet(file)

        torso_files = Mundane.get_file_names_from_directory("assets/character_assembly/torso")
        for file in torso_files:
            self.process_torso_sheet(file)

        hair_files = Mundane.get_file_names_from_directory("assets/character_assembly/hair")
        for file in hair_files:
            self.process_hair_sheet(file)

        head_files = Mundane.get_file_names_from_directory("assets/character_assembly/head")
        for file in head_files:
            self.process_head_sheet(file)

        eyes_files = Mundane.get_file_names_from_directory("assets/character_assembly/eyes")
        for file in eyes_files:
            self.process_eyes_sheet(file)

        mouth_files = Mundane.get_file_names_from_directory("assets/character_assembly/mouth")
        for file in mouth_files:
            self.process_mouth_sheet(file)

    def process_legs_sheet(self, file_name):
        self.legs_counter += 1
        load_file = pygame.image.load("assets/character_assembly/legs/" + file_name).convert_alpha()
        self.legs_list["front"]["frame_1"][self.legs_counter] = load_file.subsurface((0, 0, 32, 48)).copy()
        self.legs_list["front"]["frame_2"][self.legs_counter] = load_file.subsurface((32, 0, 32, 48)).copy()
        self.legs_list["back"]["frame_1"][self.legs_counter] = load_file.subsurface((64, 0, 32, 48)).copy()
        self.legs_list["back"]["frame_2"][self.legs_counter] = load_file.subsurface((96, 0, 32, 48)).copy()
        self.legs_list["right"]["frame_1"][self.legs_counter] = load_file.subsurface((0, 48, 32, 48)).copy()
        self.legs_list["right"]["frame_2"][self.legs_counter] = load_file.subsurface((32, 48, 32, 48)).copy()
        self.legs_list["right"]["frame_4"][self.legs_counter] = load_file.subsurface((64, 48, 32, 48)).copy()

    def process_torso_sheet(self, file_name):
        self.torso_counter += 1
        load_file = pygame.image.load("assets/character_assembly/torso/" + file_name).convert_alpha()
        self.torso_list["front"]["frame_1"][self.torso_counter] = load_file.subsurface((0, 0, 32, 48)).copy()
        self.torso_list["front"]["frame_2"][self.torso_counter] = load_file.subsurface((32, 0, 32, 48)).copy()
        self.torso_list["back"]["frame_1"][self.torso_counter] = load_file.subsurface((64, 0, 32, 48)).copy()
        self.torso_list["back"]["frame_2"][self.torso_counter] = load_file.subsurface((96, 0, 32, 48)).copy()
        self.torso_list["right"]["frame_1"][self.torso_counter] = load_file.subsurface((0, 48, 32, 48)).copy()
        self.torso_list["right"]["frame_2"][self.torso_counter] = load_file.subsurface((32, 48, 32, 48)).copy()
        self.torso_list["right"]["frame_4"][self.torso_counter] = load_file.subsurface((64, 48, 32, 48)).copy()

    def process_hair_sheet(self, file_name):
        self.hair_counter += 1
        load_file = pygame.image.load("assets/character_assembly/hair/" + file_name).convert_alpha()
        self.hair_list["front"][self.hair_counter] = load_file.subsurface((0, 0, 32, 48)).copy()
        self.hair_list["back"][self.hair_counter] = load_file.subsurface((32, 0, 32, 48)).copy()
        self.hair_list["right"][self.hair_counter] = load_file.subsurface((64, 0, 32, 48)).copy()

    def process_head_sheet(self, file_name):
        self.head_counter += 1
        load_file = pygame.image.load("assets/character_assembly/head/" + file_name).convert_alpha()
        self.head_list["front"][self.head_counter] = load_file.subsurface((0, 0, 32, 48)).copy()
        self.head_list["back"][self.head_counter] = load_file.subsurface((32, 0, 32, 48)).copy()
        self.head_list["right"][self.head_counter] = load_file.subsurface((64, 0, 32, 48)).copy()

    def process_eyes_sheet(self, file_name):
        self.eyes_counter += 1
        load_file = pygame.image.load("assets/character_assembly/eyes/" + file_name).convert_alpha()
        self.eyes_list["front"][self.eyes_counter] = load_file.subsurface((0, 0, 32, 48)).copy()
        self.eyes_list["back"][self.eyes_counter] = load_file.subsurface((32, 0, 32, 48)).copy()
        self.eyes_list["right"][self.eyes_counter] = load_file.subsurface((64, 0, 32, 48)).copy()

    def process_mouth_sheet(self, file_name):
        self.mouth_counter += 1
        load_file = pygame.image.load("assets/character_assembly/mouth/" + file_name).convert_alpha()
        self.mouth_list["front"][self.mouth_counter] = load_file.subsurface((0, 0, 32, 48)).copy()
        self.mouth_list["back"][self.mouth_counter] = load_file.subsurface((32, 0, 32, 48)).copy()
        self.mouth_list["right"][self.mouth_counter] = load_file.subsurface((64, 0, 32, 48)).copy()

    def check_if_item_in_list(self, list_type, item_name):
        result = False
        for item in getattr(self, list_type + "_item_list").keys():
            if item_name == item:
                result = True
        return result

    def add_to_item_list(self, list_type, species, display_name):
        getattr(self, list_type + "_item_list")[species] = [species, display_name]

    def setup_colour_select_images(self):
        square_number = 0
        square_xy = 12
        spacing = 2
        square_offset = 15
        base_border_colour = (0, 0, 0)
        border_thickness = 2
        highlight_colour = (212, 212, 83)

        current_attributes_colour_primary = getattr(self, "selected_" + self.current_part + "_colour")
        primary_colour_index = self.colour_options.index(current_attributes_colour_primary)

        current_attributes_colour_secondary = getattr(self, "selected_" + self.current_part + "_secondary_colour")
        secondary_colour_index = self.colour_options.index(current_attributes_colour_secondary)

        primary_colour_squares = self.colour_buttons_list_primary.values()

        self.primary_squares_list = []
        for square_colour in primary_colour_squares:
            if square_number == primary_colour_index:
                border_colour = highlight_colour
            else:
                border_colour = base_border_colour
            boarder_square = pygame.Surface((square_xy, square_xy), pygame.SRCALPHA)
            boarder_square.fill(border_colour)

            colour_square_xy = (square_xy - border_thickness, square_xy - border_thickness)
            square_surface = pygame.Surface(colour_square_xy, pygame.SRCALPHA)
            square_surface.fill(square_colour.details["colour"])
            boarder_square.blit(square_surface, (border_thickness - 1, border_thickness - 1))
            self.primary_squares_list.append(boarder_square)
            square_number += 1

        secondary_colour_squares = self.colour_buttons_list_secondary.values()
        square_number = 0

        self.secondary_squares_list = []
        for square_colour in secondary_colour_squares:
            if square_number == secondary_colour_index:
                border_colour = highlight_colour
            else:
                border_colour = base_border_colour
            boarder_square = pygame.Surface((square_xy, square_xy), pygame.SRCALPHA)
            boarder_square.fill(border_colour)

            colour_square_xy = (square_xy - border_thickness, square_xy - border_thickness)
            square_surface = pygame.Surface(colour_square_xy, pygame.SRCALPHA)
            square_surface.fill(square_colour.details["colour"])
            boarder_square.blit(square_surface, (border_thickness - 1, border_thickness - 1))
            self.secondary_squares_list.append(boarder_square)
            square_number += 1

    def select_primary_colour(self, details):
        new_colour = details["colour"]
        setattr(self, "selected_" + self.current_part + "_colour", new_colour)

        self.perform_assemblies()

    def select_secondary_colour(self, details):
        new_colour = details["colour"]
        setattr(self, "selected_" + self.current_part + "_secondary_colour", new_colour)

        self.perform_assemblies()

    def select_current_part(self, details):
        self.current_part = details["selected_part"]
        current_number = self.parts_list.index(self.current_part)

    def prepare_menu_for_display(self, details):
        pass

    def do_option(self):
        if self.currently_selected_text_entry_box is not None:
            self.gc.menu_controller.unset_current_text_entry_box()
        else:
            pass

    def erase_letter(self):
        if self.currently_selected_text_entry_box is not None:
            self.text_entry_boxes[self.currently_selected_text_entry_box].erase_letter()
        else:
            pass

    def key_letter(self, letter):
        if self.currently_selected_text_entry_box is None:
            if letter == "a":
                relevant_number = getattr(self, "selected_" + self.current_part)
                current_list = getattr(self, self.current_part + "_list")
                selected_colour = getattr(self, "selected_" + self.current_part + "_colour")

                current_index = self.colour_options.index(selected_colour)

                new_colour = []
                if current_index == self.colour_options[0]:
                    new_colour = len(self.colour_options) - 1
                else:
                    new_colour = self.colour_options[current_index - 1]
                setattr(self, "selected_" + self.current_part + "_colour", new_colour)

                self.perform_assemblies()
            elif letter == "s":
                relevant_number = getattr(self, "selected_" + self.current_part)
                current_list = getattr(self, self.current_part + "_list")
                selected_colour = getattr(self, "selected_" + self.current_part + "_colour")

                current_index = self.colour_options.index(selected_colour)

                new_colour = []
                if current_index == len(self.colour_options) - 1:
                    new_colour = self.colour_options[0]
                else:
                    new_colour = self.colour_options[current_index + 1]
                setattr(self, "selected_" + self.current_part + "_colour", new_colour)

                self.perform_assemblies()
            elif letter == "q":
                relevant_number = getattr(self, "selected_" + self.current_part)
                current_list = getattr(self, self.current_part + "_list")
                selected_colour = getattr(self, "selected_" + self.current_part + "_secondary_colour")

                current_index = self.colour_options.index(selected_colour)

                new_colour = []
                if current_index == self.colour_options[0]:
                    new_colour = len(self.colour_options) - 1
                else:
                    new_colour = self.colour_options[current_index - 1]
                setattr(self, "selected_" + self.current_part + "_secondary_colour", new_colour)

                self.perform_assemblies()
            elif letter == "w":
                relevant_number = getattr(self, "selected_" + self.current_part)
                current_list = getattr(self, self.current_part + "_list")
                selected_colour = getattr(self, "selected_" + self.current_part + "_secondary_colour")

                current_index = self.colour_options.index(selected_colour)

                new_colour = []
                if current_index == len(self.colour_options) - 1:
                    new_colour = self.colour_options[0]
                else:
                    new_colour = self.colour_options[current_index + 1]
                setattr(self, "selected_" + self.current_part + "_secondary_colour", new_colour)

                self.perform_assemblies()
            elif letter == "z":
                name = self.text_entry_boxes["assembly_box_1"].current_text
                self.print_spritesheet_to_png(name)
            elif letter == "x":
                self.gc.menu_controller.set_current_text_entry_box("assembly_box_1")
            else:
                pass
        else:
            self.text_entry_boxes[self.currently_selected_text_entry_box].add_letter(letter)

    def print_spritesheet_to_png(self, name):
        final_surface = pygame.Surface((128, 192))
        final_surface.fill(self.bg_pink)

        self.x_counter = 0
        self.y_counter = 0

        def get_x_addition():
            if self.x_counter == 4:
                self.x_counter = 0
                self.y_counter += 1
            result = 0 + copy.copy(self.x_counter)
            self.x_counter += 1

            return result * 32

        front_frame_1 = self.final_front_frame_1
        front_frame_2 = self.final_front_frame_2
        front_frame_3 = self.final_front_frame_3
        front_frame_4 = self.final_front_frame_4
        back_frame_1 = self.final_back_frame_1
        back_frame_2 = self.final_back_frame_2
        back_frame_3 = self.final_back_frame_3
        back_frame_4 = self.final_back_frame_4
        right_frame_1 = self.final_right_frame_1
        right_frame_2 = self.final_right_frame_2
        right_frame_3 = self.final_right_frame_3
        right_frame_4 = self.final_right_frame_4
        left_frame_1 = self.final_left_frame_1
        left_frame_2 = self.final_left_frame_2
        left_frame_3 = self.final_left_frame_3
        left_frame_4 = self.final_left_frame_4
        final_images = [front_frame_1, front_frame_2, front_frame_3, front_frame_4,
                        back_frame_1, back_frame_2, back_frame_3, back_frame_4,
                        right_frame_1, right_frame_2, right_frame_3, right_frame_4,
                        left_frame_1, left_frame_2, left_frame_3, left_frame_4]

        for image in final_images:
            final_surface.blit(image, (get_x_addition(), self.y_counter * 48))

        if name != "":
            pygame.image.save(final_surface, "assets/character_assembly/assembled_images/" + name + "_image.png")
        else:
            number = random.randint(10000, 99999)
            pygame.image.save(final_surface, "assets/character_assembly/assembled_images/" + str(number) + "_image.png")

    def perform_assemblies(self):
        setattr(self, "final_front_frame_1", self.assemble_front_1())
        setattr(self, "final_front_frame_2", self.assemble_front_2())
        setattr(self, "final_front_frame_3", self.assemble_front_1())
        setattr(self, "final_front_frame_4", self.assemble_front_4())
        setattr(self, "final_back_frame_1", self.assemble_back_1())
        setattr(self, "final_back_frame_2", self.assemble_back_2())
        setattr(self, "final_back_frame_3", self.assemble_back_1())
        setattr(self, "final_back_frame_4", self.assemble_back_4())
        setattr(self, "final_right_frame_1", self.assemble_right_1())
        setattr(self, "final_right_frame_2", self.assemble_right_2())
        setattr(self, "final_right_frame_3", self.assemble_right_1())
        setattr(self, "final_right_frame_4", self.assemble_right_4())
        setattr(self, "final_left_frame_1", self.assemble_left_1())
        setattr(self, "final_left_frame_2", self.assemble_left_2())
        setattr(self, "final_left_frame_3", self.assemble_left_1())
        setattr(self, "final_left_frame_4", self.assemble_left_4())

    def assemble_front_1(self):
        hair_image = self.change_colour(self.hair_list["front"][self.selected_hair], "front", "frame_1", self.selected_hair_colour, self.selected_hair_secondary_colour)
        hair_image.set_colorkey(self.bg_pink)
        head_image = self.change_colour(self.head_list["front"][self.selected_head], "front", "frame_1", self.selected_head_colour, self.selected_head_secondary_colour)
        head_image.set_colorkey(self.bg_pink)
        mouth_image = self.mouth_list["front"][self.selected_mouth]
        mouth_image.set_colorkey(self.bg_pink)
        eyes_image = self.eyes_list["front"][self.selected_eyes]
        eyes_image.set_colorkey(self.bg_pink)
        torso_image = self.change_colour(self.torso_list["front"]["frame_1"][self.selected_torso], "front", "frame_1", self.selected_torso_colour, self.selected_torso_secondary_colour)
        torso_image.set_colorkey(self.bg_pink)
        legs_image = self.change_colour(self.legs_list["front"]["frame_1"][self.selected_legs], "front", "frame_1", self.selected_legs_colour, self.selected_legs_secondary_colour)
        legs_image.blit(torso_image, (0, 0))
        legs_image.blit(head_image, (0, 0))
        legs_image.blit(mouth_image, (0, 0))
        legs_image.blit(eyes_image, (0, 0))
        legs_image.blit(hair_image, (0, 0))
        final_image = self.change_skin_colour(legs_image, self.selected_head_colour, self.selected_head_secondary_colour)
        return final_image

    def assemble_front_2(self):
        hair_image = self.change_colour(self.hair_list["front"][self.selected_hair], "front", "frame_2", self.selected_hair_colour, self.selected_hair_secondary_colour)
        hair_image.set_colorkey(self.bg_pink)
        head_image = self.change_colour(self.head_list["front"][self.selected_head], "front", "frame_1", self.selected_head_colour, self.selected_head_secondary_colour)
        head_image.set_colorkey(self.bg_pink)
        mouth_image = self.mouth_list["front"][self.selected_mouth]
        mouth_image.set_colorkey(self.bg_pink)
        eyes_image = self.eyes_list["front"][self.selected_eyes]
        eyes_image.set_colorkey(self.bg_pink)
        torso_image = self.change_colour(self.torso_list["front"]["frame_2"][self.selected_torso], "front", "frame_2", self.selected_torso_colour, self.selected_torso_secondary_colour)
        torso_image.set_colorkey(self.bg_pink)
        legs_image = self.change_colour(self.legs_list["front"]["frame_2"][self.selected_legs], "front", "frame_2", self.selected_legs_colour, self.selected_legs_secondary_colour)
        legs_image.blit(torso_image, (0, 0))
        legs_image.blit(head_image, (0, 1))
        legs_image.blit(mouth_image, (0, 1))
        legs_image.blit(eyes_image, (0, 1))
        legs_image.blit(hair_image, (0, 1))
        final_image = self.change_skin_colour(legs_image, self.selected_head_colour, self.selected_head_secondary_colour)
        return final_image

    def assemble_front_4(self):
        hair_image = self.change_colour(self.hair_list["front"][self.selected_hair], "front", "frame_2", self.selected_hair_colour, self.selected_hair_secondary_colour)
        hair_image.set_colorkey(self.bg_pink)
        head_image = self.change_colour(self.head_list["front"][self.selected_head], "front", "frame_1", self.selected_head_colour, self.selected_head_secondary_colour)
        head_image.set_colorkey(self.bg_pink)
        mouth_image = self.mouth_list["front"][self.selected_mouth]
        mouth_image.set_colorkey(self.bg_pink)
        eyes_image = self.eyes_list["front"][self.selected_eyes]
        eyes_image.set_colorkey(self.bg_pink)
        torso_image = self.change_colour(self.torso_list["front"]["frame_2"][self.selected_torso], "front", "frame_2", self.selected_torso_colour, self.selected_torso_secondary_colour)
        torso_image = pygame.transform.flip(torso_image, True, False)
        torso_image.set_colorkey(self.bg_pink)
        legs_image = self.change_colour(self.legs_list["front"]["frame_2"][self.selected_legs], "front", "frame_2", self.selected_legs_colour, self.selected_legs_secondary_colour)
        legs_image = pygame.transform.flip(legs_image, True, False)
        legs_image.set_colorkey(self.bg_pink)
        legs_image.blit(torso_image, (0, 0))
        legs_image.blit(head_image, (0, 0))
        legs_image.blit(mouth_image, (0, 0))
        legs_image.blit(eyes_image, (0, 0))
        legs_image.blit(hair_image, (0, 0))
        final_image = self.change_skin_colour(legs_image, self.selected_head_colour, self.selected_head_secondary_colour)
        return final_image

    def assemble_back_1(self):
        hair_image = self.change_colour(self.hair_list["back"][self.selected_hair], "back", "frame_1",self.selected_hair_colour, self.selected_hair_secondary_colour)
        hair_image.set_colorkey(self.bg_pink)
        head_image = self.change_colour(self.head_list["back"][self.selected_head], "front", "frame_1", self.selected_head_colour, self.selected_head_secondary_colour)
        head_image.set_colorkey(self.bg_pink)
        torso_image = self.change_colour(self.torso_list["back"]["frame_1"][self.selected_torso], "back", "frame_1", self.selected_torso_colour, self.selected_torso_secondary_colour)
        torso_image.set_colorkey(self.bg_pink)
        legs_image = self.change_colour(self.legs_list["back"]["frame_1"][self.selected_legs], "back", "frame_1", self.selected_legs_colour, self.selected_legs_secondary_colour)
        legs_image.blit(torso_image, (0, 0))
        legs_image.blit(head_image, (0, 0))
        legs_image.blit(hair_image, (0, 0))
        final_image = self.change_skin_colour(legs_image, self.selected_head_colour, self.selected_head_secondary_colour)
        return final_image

    def assemble_back_2(self):
        hair_image = self.change_colour(self.hair_list["back"][self.selected_hair], "back", "frame_2", self.selected_hair_colour, self.selected_hair_secondary_colour)
        hair_image.set_colorkey(self.bg_pink)
        head_image = self.change_colour(self.head_list["back"][self.selected_head], "front", "frame_1", self.selected_head_colour, self.selected_head_secondary_colour)
        head_image.set_colorkey(self.bg_pink)
        torso_image = self.change_colour(self.torso_list["back"]["frame_2"][self.selected_torso], "back", "frame_2", self.selected_torso_colour, self.selected_torso_secondary_colour)
        torso_image.set_colorkey(self.bg_pink)
        legs_image = self.change_colour(self.legs_list["back"]["frame_2"][self.selected_legs], "back", "frame_2", self.selected_legs_colour, self.selected_legs_secondary_colour)
        legs_image.blit(head_image, (0, 1))
        legs_image.blit(torso_image, (0, 0))
        legs_image.blit(hair_image, (0, 1))
        final_image = self.change_skin_colour(legs_image, self.selected_head_colour, self.selected_head_secondary_colour)
        return final_image

    def assemble_back_4(self):
        hair_image = self.change_colour(self.hair_list["back"][self.selected_hair], "back", "frame_2", self.selected_hair_colour, self.selected_hair_secondary_colour)
        hair_image.set_colorkey(self.bg_pink)
        head_image = self.change_colour(self.head_list["back"][self.selected_head], "front", "frame_1", self.selected_head_colour, self.selected_head_secondary_colour)
        head_image.set_colorkey(self.bg_pink)
        torso_image = self.change_colour(self.torso_list["back"]["frame_2"][self.selected_torso], "back", "frame_2", self.selected_torso_colour, self.selected_torso_secondary_colour)
        torso_image = pygame.transform.flip(torso_image, True, False)
        torso_image.set_colorkey(self.bg_pink)
        legs_image = self.change_colour(self.legs_list["back"]["frame_2"][self.selected_legs], "back", "frame_2", self.selected_legs_colour, self.selected_legs_secondary_colour)
        legs_image = pygame.transform.flip(legs_image, True, False)
        legs_image.set_colorkey(self.bg_pink)
        legs_image.blit(head_image, (0, 0))
        legs_image.blit(torso_image, (0, 0))
        legs_image.blit(hair_image, (0, 0))
        final_image = self.change_skin_colour(legs_image, self.selected_head_colour, self.selected_head_secondary_colour)
        return final_image

    def assemble_right_1(self):
        hair_image = self.change_colour(self.hair_list["right"][self.selected_hair], "right", "frame_1", self.selected_hair_colour, self.selected_hair_secondary_colour)
        hair_image.set_colorkey(self.bg_pink)
        head_image = self.change_colour(self.head_list["right"][self.selected_head], "front", "frame_1", self.selected_head_colour, self.selected_head_secondary_colour)
        head_image.set_colorkey(self.bg_pink)
        mouth_image = self.mouth_list["right"][self.selected_mouth]
        mouth_image.set_colorkey(self.bg_pink)
        eyes_image = self.eyes_list["right"][self.selected_eyes]
        eyes_image.set_colorkey(self.bg_pink)
        torso_image = self.change_colour(self.torso_list["right"]["frame_1"][self.selected_torso], "right", "frame_1", self.selected_torso_colour, self.selected_torso_secondary_colour)
        torso_image.set_colorkey(self.bg_pink)
        legs_image = self.change_colour(self.legs_list["right"]["frame_1"][self.selected_legs], "right", "frame_1", self.selected_legs_colour, self.selected_legs_secondary_colour)
        legs_image.blit(torso_image, (0, 0))
        legs_image.blit(head_image, (0, 0))
        legs_image.blit(mouth_image, (0, 0))
        legs_image.blit(eyes_image, (0, 0))
        legs_image.blit(hair_image, (0, 0))
        final_image = self.change_skin_colour(legs_image, self.selected_head_colour, self.selected_head_secondary_colour)
        return final_image

    def assemble_right_2(self):
        hair_image = self.change_colour(self.hair_list["right"][self.selected_hair], "right", "frame_2", self.selected_hair_colour, self.selected_hair_secondary_colour)
        hair_image.set_colorkey(self.bg_pink)
        head_image = self.change_colour(self.head_list["right"][self.selected_head], "front", "frame_1", self.selected_head_colour, self.selected_head_secondary_colour)
        head_image.set_colorkey(self.bg_pink)
        mouth_image = self.mouth_list["right"][self.selected_mouth]
        mouth_image.set_colorkey(self.bg_pink)
        eyes_image = self.eyes_list["right"][self.selected_eyes]
        eyes_image.set_colorkey(self.bg_pink)
        torso_image = self.change_colour(self.torso_list["right"]["frame_2"][self.selected_torso], "right", "frame_2", self.selected_torso_colour, self.selected_torso_secondary_colour)
        torso_image.set_colorkey(self.bg_pink)
        legs_image = self.change_colour(self.legs_list["right"]["frame_2"][self.selected_legs], "right", "frame_2", self.selected_legs_colour, self.selected_legs_secondary_colour)
        legs_image.blit(torso_image, (0, 0))
        legs_image.blit(head_image, (1, 1))
        legs_image.blit(mouth_image, (1, 1))
        legs_image.blit(eyes_image, (1, 1))
        legs_image.blit(hair_image, (1, 1))
        final_image = self.change_skin_colour(legs_image, self.selected_head_colour, self.selected_head_secondary_colour)
        return final_image

    def assemble_right_4(self):
        hair_image = self.change_colour(self.hair_list["right"][self.selected_hair], "right", "frame_4", self.selected_hair_colour, self.selected_hair_secondary_colour)
        hair_image.set_colorkey(self.bg_pink)
        head_image = self.change_colour(self.head_list["right"][self.selected_head], "front", "frame_1", self.selected_head_colour, self.selected_head_secondary_colour)
        head_image.set_colorkey(self.bg_pink)
        mouth_image = self.mouth_list["right"][self.selected_mouth]
        mouth_image.set_colorkey(self.bg_pink)
        eyes_image = self.eyes_list["right"][self.selected_eyes]
        eyes_image.set_colorkey(self.bg_pink)
        torso_image = self.change_colour(self.torso_list["right"]["frame_4"][self.selected_torso], "right", "frame_4", self.selected_torso_colour, self.selected_torso_secondary_colour)
        torso_image.set_colorkey(self.bg_pink)
        legs_image = self.change_colour(self.legs_list["right"]["frame_4"][self.selected_legs], "right", "frame_4", self.selected_legs_colour, self.selected_legs_secondary_colour)
        legs_image.blit(torso_image, (0, 0))
        legs_image.blit(head_image, (1, 0))
        legs_image.blit(mouth_image, (1, 0))
        legs_image.blit(eyes_image, (1, 0))
        legs_image.blit(hair_image, (1, 0))
        final_image = self.change_skin_colour(legs_image, self.selected_head_colour, self.selected_head_secondary_colour)
        return final_image

    def assemble_left_1(self):
        right_image = self.assemble_right_1()
        flipped_image = pygame.transform.flip(right_image, True, False)
        flipped_image.set_colorkey(self.bg_pink)
        return flipped_image

    def assemble_left_2(self):
        right_image = self.assemble_right_2()
        flipped_image = pygame.transform.flip(right_image, True, False)
        flipped_image.set_colorkey(self.bg_pink)
        return flipped_image

    def assemble_left_4(self):
        right_image = self.assemble_right_4()
        flipped_image = pygame.transform.flip(right_image, True, False)
        flipped_image.set_colorkey(self.bg_pink)
        return flipped_image

    def change_skin_colour(self, image, new_primary_colour, new_secondary_colour):
        img_copy = image.copy()
        isolate_primary_skin = self.isolate_part(img_copy, self.skin_base)
        isolate_secondary_skin = self.isolate_part(img_copy, self.skin_base_2)

        with pygame.PixelArray(isolate_primary_skin) as pixel_array:
            pixel_array.replace(self.skin_base, new_primary_colour)

        img_copy.blit(isolate_primary_skin, (0, 0))

        with pygame.PixelArray(isolate_secondary_skin) as pixel_array2:
            pixel_array2.replace(self.skin_base_2, new_secondary_colour)

        img_copy.blit(isolate_secondary_skin, (0, 0))
        img_copy.set_colorkey(self.bg_pink)

        return img_copy

    def change_colour(self, part, view, frame, new_primary_colour, new_secondary_colour):
        img_copy = part.copy()

        primary_part = self.isolate_part(img_copy, self.primary_colour)
        secondary_part = self.isolate_part(img_copy, self.secondary_colour)

        with pygame.PixelArray(primary_part) as pixel_array:
            pixel_array.replace(self.primary_colour, new_primary_colour)

        img_copy.blit(primary_part, (0, 0))

        with pygame.PixelArray(secondary_part) as pixel_array2:
            pixel_array2.replace(self.secondary_colour, new_secondary_colour)

        img_copy.blit(secondary_part, (0, 0))
        img_copy.set_colorkey(self.bg_pink)

        return img_copy

    def isolate_part(self, image, colour):
        temp_surface = image.copy()
        mapped_colour = colour
        dummy_colour = (105, 105, 105)

        mapped_integer = temp_surface.map_rgb(mapped_colour)
        dummy_integer = temp_surface.map_rgb(dummy_colour)

        with pygame.PixelArray(temp_surface) as pixel_array:
            for x in range(temp_surface.get_width()):
                for y in range(temp_surface.get_height()):
                    if pixel_array[x, y] != mapped_integer:
                        pixel_array[x, y] = dummy_integer

        temp_surface.set_colorkey(dummy_colour)

        return temp_surface

    def cursor_left(self, details=None):
        relevant_number = getattr(self, "selected_" + self.current_part)
        current_list = getattr(self, self.current_part + "_list")

        if self.current_part == "torso" or self.current_part == "legs":
            list_length = len(current_list["front"]["frame_1"])
        else:
            list_length = len(current_list["front"])

        if relevant_number > 1:
            relevant_number -= 1
            setattr(self, "selected_" + self.current_part, relevant_number)
        elif relevant_number == 1:
            relevant_number = list_length
            setattr(self, "selected_" + self.current_part, relevant_number)

        self.perform_assemblies()

    def cursor_right(self, details=None):
        relevant_number = getattr(self, "selected_" + self.current_part)
        current_list = getattr(self, self.current_part + "_list")

        if self.current_part == "torso" or self.current_part == "legs":
            list_length = len(current_list["front"]["frame_1"])
        else:
            list_length = len(current_list["front"])

        if relevant_number >= list_length:
            relevant_number = 1
            setattr(self, "selected_" + self.current_part, relevant_number)
        elif relevant_number < list_length:
            relevant_number += 1
            setattr(self, "selected_" + self.current_part, relevant_number)

        self.perform_assemblies()

    def cursor_up(self, details=None):
        current_number = self.parts_list.index(self.current_part)
        if current_number > 0:
            self.current_part = self.parts_list[current_number-1]
        else:
            self.current_part = self.parts_list[len(self.parts_list) - 1]

    def cursor_down(self, details=None):
        current_number = self.parts_list.index(self.current_part)
        if current_number < len(self.parts_list) - 1:
            self.current_part = self.parts_list[current_number+1]
        else:
            self.current_part = self.parts_list[0]

    def make_main_item(self, list_type, number):
        setattr(self, list_type + "_number", number)
        list_keys = getattr(self, list_type + "_item_list").keys()
        sorted_keys = sorted(list_keys)
        setattr(self, "selected_" + list_type, sorted_keys[number])

        length = len(sorted_keys)
        if number == (length - 1):
            setattr(self, "is_last_" + list_type, True)
        else:
            setattr(self, "is_last_" + list_type, False)
        if number == 0:
            setattr(self, "is_first_" + list_type, True)
        else:
            setattr(self, "is_first_" + list_type, False)


class RoomSelectMenuGhost(MenuGhost):
    BASE = "room_select_menu"
    NAME = BASE + "_ghost"
    AVATAR = ListMenuAvatar

    def __init__(self, gc):
        super().__init__(gc)
        self.menu_header = None
        self.menu_item_list = ["Staging_Area", "Farmland", "Marsh", "Beach", "Forest", "Mountain"]
        self.menu_item_list.append("Exit")
        self.menu_images_list = []
        self.cursor = "-"
        self.prepare_menu_for_display(None)

    def do_option(self, choice=None):
        menu_selection = self.get_current_menu_item()

        if menu_selection == "Exit":
            self.gc.menu_controller.exit_all_menus()
        else:
            self.gc.view_room(menu_selection)


class BuilderFunctionsMenuGhost(MenuGhost):
    BASE = "builder_functions_menu"
    NAME = BASE + "_ghost"
    AVATAR = ClickListMenuAvatar

    def __init__(self, gc):
        super().__init__(gc)
        self.menu_header = None
        self.menu_item_list = ["Design Sprite", "View Sprites", "Change Map", "Toggle Display", "Toggle Names"]
        self.setup_buttons_list()
        self.menu_images_list = []
        self.cursor = "-"
        self.prepare_menu_for_display(None)

    def do_option(self, choice=None):
        menu_selection = self.get_current_menu_item()
        if choice is not None:
            menu_selection = choice
        self.gc.menu_controller.builder_function_menu_selection(menu_selection)

    def setup_buttons_list(self):
        for item in self.menu_item_list:
            button_name = str(item) + "_button"
            button_object = ButtonGhost(self.gc, button_name, self.BASE, "do_option", item)
            self.button_list[button_name] = button_object

    def generate_menu_information_package(self):
        source = self.get_menu_items_to_display().copy()
        cursor_at = self.cursor_at
        cursor_image = self.cursor
        text_display_list = []

        # setting up parts selection list
        text_list_passes = []
        for item in self.menu_item_list:
            passer = ComponentPass(item, item + "_button")
            text_list_passes.append(passer)

        menu_specific = {"text_list_passes": text_list_passes}

        menu_information = MenuInformation(self.menu_header, text_display_list, cursor_image, cursor_at, menu_specific)
        return menu_information


class CharacterSpritesheetViewMenuGhost(MenuGhost):
    BASE = "character_spritesheet_view_menu"
    NAME = BASE + "_ghost"
    AVATAR = CharacterSpritesheetViewMenu

    def __init__(self, gc):
        super().__init__(gc)
        self.menu_header = None
        self.menu_type = Types.BASE
        self.menu_item_list = []
        self.menu_images_list = []
        self.cursor = None
        self.shifts = 0
        self.max_displayed_items = 14
        self.currently_displayed_items = []
        self.spritesheet_images_dict = {}
        self.currently_selected_spritesheet = 0
        self.functions_list = ["Rename", "Delete"]
        self.setup_buttons_list()

    def prepare_menu_for_display(self, details):
        self.spritesheet_images_dict = self.gc.gs.gd.get_character_spritesheet_dict()

    def generate_menu_information_package(self):
        cursor_at = self.cursor_at
        cursor_image = self.cursor
        text_display_list = []

        # setting up parts selection list
        spritesheet_image_pass = []
        name_text_pass = []
        sheet_image_keys = self.spritesheet_images_dict.keys()

        for sheet_name in sheet_image_keys:
            sheet_object = self.spritesheet_images_dict[sheet_name]

            name_text = ComponentPass(sheet_object.sheet_name, None)
            name_text_pass.append(name_text)

            passer = ComponentPass(sheet_object.spritesheet_object.sheet, None)
            spritesheet_image_pass.append(passer)

        functions_text_pass = []
        for text in self.functions_list:
            function_text = ComponentPass(text, text)
            functions_text_pass.append(function_text)

        left_arrow = ComponentPass("<", "left_arrow_button")
        right_arrow = ComponentPass(">", "right_arrow_button")

        menu_specific = {"spritesheet_image_pass": [spritesheet_image_pass[self.currently_selected_spritesheet]],
                         "name_text_pass": [name_text_pass[self.currently_selected_spritesheet]],
                         "functions_text_pass": functions_text_pass,
                         "arrows_pass": [left_arrow, right_arrow]}

        menu_information = MenuInformation(self.menu_header, text_display_list, cursor_image, cursor_at, menu_specific)
        return menu_information

    def do_option(self):
        self.gc.menu_controller.exit_all_menus()

    def cursor_left(self, details=None):
        if 0 < self.currently_selected_spritesheet:
            self.currently_selected_spritesheet -= 1
        else:
            self.currently_selected_spritesheet = len(self.spritesheet_images_dict.keys()) - 1

    def cursor_right(self, details=None):
        if len(self.spritesheet_images_dict.keys()) - 1 > self.currently_selected_spritesheet:
            self.currently_selected_spritesheet += 1
        else:
            self.currently_selected_spritesheet = 0

    def setup_buttons_list(self):
        left_arrow_button = ButtonGhost(self.gc, "left_arrow_button", self.BASE, "cursor_left", {})
        self.button_list["left_arrow_button"] = left_arrow_button

        right_arrow_button = ButtonGhost(self.gc, "right_arrow_button", self.BASE, "cursor_right", {})
        self.button_list["right_arrow_button"] = right_arrow_button

        # rename_button = ButtonGhost(self.gc, "Rename", self.BASE, "rename_sheet", {})
        # self.button_list["Rename"] = rename_button

        delete_button = ButtonGhost(self.gc, "Delete", self.BASE, "delete_sheet", {})
        self.button_list["Delete"] = delete_button

    def delete_sheet(self, details):
        character_spritesheet_object = self.spritesheet_images_dict[list(self.spritesheet_images_dict.keys())[self.currently_selected_spritesheet]]
        file_name = character_spritesheet_object.sheet_image_name
        source_path = "assets/spritesheets/feature_spritesheets/character_spritesheets/" + file_name
        destination_path = "assets/spritesheets/feature_spritesheets/character_spritesheets_deleted"

        # Move the file
        shutil.move(source_path, destination_path)

        # Delete item from game data
        self.gc.gs.gd.delete_character_spritesheet_from_dict(character_spritesheet_object.sheet_name)

        # Redo this menu
        self.prepare_menu_for_display({})

        # ensure that we didn't mess up currently selected number
        if len(self.spritesheet_images_dict.keys()) - 1 < self.currently_selected_spritesheet:
            self.currently_selected_spritesheet = 0


class TextEntryBoxGhost(object):
    def __init__(self, gc, name):
        self.gc = gc
        self.name = name
        self.length_limit = 10
        self.current_text = ""
        self.selected = False
        self.box_surface = self.build_box_image(34, 4)
        self.final_surface = None
        self.redefine_final_surface()

    def add_letter(self, letter):
        self.current_text += letter
        self.redefine_final_surface()

    def erase_letter(self):
        self.current_text = self.current_text[:-1]
        self.redefine_final_surface()

    def clear_all_text(self):
        self.current_text = ""
        self.redefine_final_surface()

    def redefine_final_surface(self):
        box_image = copy.copy(self.box_surface)
        if self.selected:
            box_image = Mundane.change_single_colour_of_surface(box_image, (255, 255, 255), (255, 255, 130))
        text = copy.copy(self.current_text)
        text_surface = pygame.font.Font(GameSettings.FONT_FILE, GameSettings.FONT_SIZE).render(text, True, (0, 0, 0))
        box_image.blit(text_surface, (5, 5))
        self.final_surface = box_image

    def select_box(self):
        self.selected = True
        self.redefine_final_surface()

    def deselect_box(self):
        self.selected = False
        self.redefine_final_surface()

    def return_current_text(self):
        return copy.copy(self.current_text)

    def build_box_image(self, size_x, size_y):
        box = self.gc.gs.gv.build_overlay_image(self.name, size_x, size_y)
        return box


class ButtonGhost(object):
    def __init__(self, gc, name, menu_name, press_function, details):
        self.gc = gc
        self.name = name
        self.menu_name = menu_name
        self.press_function = press_function
        self.details = details

    def get_pressed(self):
        menu = self.gc.gs.ms.get_menu_ghost(self.menu_name)
        function = getattr(menu, self.press_function)
        function(self.details)


class ComponentPass(object):
    def __init__(self, text_or_image, related_button_name):
        if type(text_or_image) == str:
            self.text_or_image = text_or_image
            self.surface = pygame.font.Font(GameSettings.FONT_FILE, GameSettings.FONT_SIZE).render(text_or_image, True, (0, 0, 0))
        else:
            self.text_or_image = None
            self.surface = text_or_image
        self.related_button_name = related_button_name

    def lowlight_text(self):
        if type(self.text_or_image) == str:
            self.surface = pygame.font.Font(GameSettings.FONT_FILE, GameSettings.FONT_SIZE).render(self.text_or_image, True, (99, 99, 99))