import copy
import math
import textwrap

from definitions import GameSettings, Types, Mundane
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

    def __init__(self, gc_input):
        super().__init__()
        self.gc_input = gc_input

        self.menu_header = "<Goodies>"
        self.menu_item_list = ["Poop", "Pee", "Dragon Eggs", "Weasel Toe"]
        self.menu_images_list = []
        self.additional_information = []
        self.menu_type = Types.BASE

        self.cursor = "-"
        self.cursor_at = [0, 0]
        self.name = self.NAME

    def get_menu_items_to_display(self):
        return self.menu_item_list

    def choose_option(self):
        self.do_option()

    def get_current_menu_item(self):
        menu_selection = self.menu_item_list[self.cursor_at[1]]
        return menu_selection

    def do_option(self):
        menu_selection = self.get_current_menu_item()

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

    @property
    def size(self):
        return len(self.menu_item_list)


class StatMenuGhost(MenuGhost):
    BASE = "stat_menu"
    NAME = BASE + "_ghost"

    def __init__(self, gc_input):
        super().__init__(gc_input)
        self.menu_header = None

        self.menu_item_list = []
        self.menu_images_list = []
        self.cursor = None
        self.prepare_menu_for_display()
        self.menu_type = Types.STATIC

    def prepare_menu_for_display(self):
        stat_dict = self.gc_input.get_stat_items()
        # self.menu_item_list = [("Birds: ", stat_dict["Birds"]),  ("Pigeons:", stat_dict["Pigeons"]), ("Day: ", stat_dict["day"]), ("Time: ", stat_dict["time"]), ("Select: ", stat_dict["selected_tool"])]
        # self.menu_item_list = [("Day: ", stat_dict["day"]), ("Time: ", stat_dict["time"]), ("Select: ", stat_dict["selected_tool"])]
        self.menu_item_list = ["Day:" + stat_dict["day"], "Time:" + stat_dict["time"], "Select: " + stat_dict["selected_tool"]]

    def get_current_menu_item(self):
        menu_selection = self.menu_item_list[self.cursor_at[1]]
        return menu_selection


class StartMenuGhost(MenuGhost):
    BASE = "start_menu"
    NAME = BASE + "_ghost"

    def __init__(self, gc_input):
        super().__init__(gc_input)
        self.menu_header = None
        self.menu_item_list = ["Bag", "Outfits", "Map", "Gallery", "Guide", "Profile", "Save", "Options", "Vibes"]
        self.menu_item_list.append("Exit")
        self.menu_images_list = []
        self.cursor = "-"
        self.prepare_menu_for_display(None)

    def do_option(self):
        menu_selection = self.get_current_menu_item()
        self.gc_input.menu_controller.start_menu_selection(menu_selection)


class AcquireMenuGhost(MenuGhost): #TODO: Work on this
    BASE = "acquire_menu"
    NAME = BASE + "_ghost"

    def __init__(self, gc_input):
        super().__init__(gc_input)
        self.menu_header = None
        self.menu_item_list = ["Cheese", "Spoon", "Match"]
        self.menu_item_list.append("Exit")
        self.menu_images_list = []
        self.cursor = "-"

    def prepare_menu_for_display(self, details):
        print("ping", self.menu_item_list)
        self.menu_item_list = details["item_list"]
        self.current_basket = details["basket_unique_name"]
        self.menu_item_list.append("Exit")
        information_from_ghost = self.generate_menu_information_package()
        self.gc_input.game_view.update_menu_display_details(self.BASE, information_from_ghost)

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


    def do_option(self):
        menu_selection = self.get_current_menu_item()
        if menu_selection == "Exit":
            self.gc_input.menu_controller.exit_all_menus()
        else:
            self.gc_input.take_from_basket(self.current_basket, menu_selection)
            self.gc_input.menu_controller.exit_all_menus()


class InventoryMenuGhost(MenuGhost):
    BASE = "inventory_menu"
    NAME = BASE + "_ghost"

    def __init__(self, gc_input):
        super().__init__(gc_input)
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
                else:
                    pass
        else:
            pass

    def cursor_up(self):
        if (self.cursor_at[1] + self.shifts) > 0:
            if self.cursor_at[1] == 0 and self.shifts > 0:
                self.shifts -= 1
                self.update_currently_displayed()
            elif self.cursor_at[1] > 0:
                self.cursor_at[1] -= 1
            else:
                pass
        else:
            pass

    def cursor_left(self):
        self.gc_input.menu_controller.previous_menu(self.BASE)

    def cursor_right(self):
        self.gc_input.menu_controller.next_menu(self.BASE)

    def reset_elements(self):
        self.cursor_at[0] = 0
        self.cursor_at[1] = 0
        self.action_doing = None

    def prepare_menu_for_display(self, details):
        keys_list = []
        current_inventory = self.gc_input.game_state.get_inventory_items(self.BASE)
        for item in current_inventory:
            keys_list.append(item)
        self.menu_item_list = keys_list
        self.menu_item_list.append("Exit")
        self.update_currently_displayed()

    def get_menu_items_to_display(self): #TODO: move most of this to menu avatar/display
        menu_length_calc = 0
        if self.size >= self.max_displayed_items:
            menu_length_calc = self.max_displayed_items
        elif self.size < self.max_displayed_items:
            menu_length_calc = self.size

        displayable_item_list = []

        for option in range(menu_length_calc):
            item = self.currently_displayed_items[option]
            if item == "Exit":
                displayable_item_list.append(self.currently_displayed_items[option])

            else:
                available_spaces = 13
                item_word_length = len(item)
                quantity = str(self.gc_input.game_state.get_item_quantity(item))
                quantity_word_length = len(quantity)
                total_length = item_word_length + quantity_word_length

                number_of_spaces = available_spaces - total_length
                spaces_str = ""
                for x in range(number_of_spaces):
                    spaces_str = spaces_str + " "
                final_item = item + spaces_str + "x" + quantity
                displayable_item_list.append(final_item)

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
            self.gc_input.menu_controller.exit_all_menus()
        else:
            self.gc_input.menu_controller.set_menu(SubMenuGhost.BASE, {"master_menu": self.BASE, "menu_items_list": ["Use", "Toss", "Cancel"]})

    def do_option(self, choice=None):
        sub_menu_selection = choice
        chosen_item_name = self.get_current_menu_item()
        self.gc_input.menu_controller.inventory_menu_selection(self, sub_menu_selection, chosen_item_name)


class SuppliesInventoryMenuGhost(InventoryMenuGhost):
    BASE = "supplies_inventory_menu"
    NAME = BASE + "_ghost"

    def __init__(self, gc_input):
        super().__init__(gc_input)
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


class GiftGivingMenuGhost(InventoryMenuGhost):
    BASE = "gift_giving_menu"
    NAME = BASE + "_ghost"

    def __init__(self, gc_input):
        super().__init__(gc_input)
        self.menu_header = None
        self.menu_item_list = []
        self.menu_header = "<   ITEMS   >"
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
        keys_list = []
        current_inventory = self.gc_input.game_state.get_inventory_items(SuppliesInventoryMenuGhost.BASE)
        for item in current_inventory:
            keys_list.append(item)
        self.menu_item_list = keys_list
        self.menu_item_list.append("Exit")
        self.update_currently_displayed()

    def cursor_left(self):
        pass

    def cursor_right(self):
        pass

    def set_master_menu(self, master_menu):
        self.master_menu = master_menu

    def choose_option(self):
        chosen_item_name = self.get_current_menu_item()
        if chosen_item_name == "Exit":
            self.gc_input.menu_controller.exit_all_menus()
        else:
            self.gc_input.menu_controller.post_notice("Give this item?")
            self.gc_input.menu_controller.set_menu(SubMenuGhost.BASE, {"master_menu": self.BASE, "menu_items_list": ["Yes", "No"]})

    def do_option(self, choice=None):
        sub_menu_selection = choice
        chosen_item_name = self.get_current_menu_item()
        details = self.details
        self.gc_input.menu_controller.gift_menu_selection(sub_menu_selection, chosen_item_name, details)


class KeyInventoryMenuGhost(InventoryMenuGhost):
    BASE = "key_inventory_menu"
    NAME = BASE + "_ghost"

    def __init__(self, gc_input):
        super().__init__(gc_input)
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

    def get_menu_items_to_display(self):
        menu_length_calc = 0
        if self.size >= self.max_displayed_items:
            menu_length_calc = self.max_displayed_items
        elif self.size < self.max_displayed_items:
            menu_length_calc = self.size

        displayable_item_list = []

        for option in range(menu_length_calc):
            item = self.currently_displayed_items[option]
            displayable_item_list.append(self.currently_displayed_items[option])

        return displayable_item_list

    def choose_option(self):
        chosen_item_name = self.get_current_menu_item()
        if chosen_item_name == "Exit":
            self.gc_input.menu_controller.exit_all_menus()
        else:
            self.gc_input.menu_controller.set_menu(SubMenuGhost.BASE, {"master_menu": self.BASE, "menu_items_list": ["Use", "Toss", "Select", "Cancel"]})

    def do_option(self, choice=None):
        sub_menu_selection = choice
        chosen_item_name = self.get_current_menu_item()

        if sub_menu_selection == "Use":
            chosen_item = self.gc_input.inventory_manager.gc_input.game_state.gd.key_item_data_list[chosen_item_name]
            self.gc_input.inventory_manager.use_key_item(chosen_item)
            self.prepare_menu_for_display(None)
            self.gc_input.menu_controller.exit_all_menus()

        elif sub_menu_selection == "Toss":
            self.gc_input.menu_controller.exit_all_menus()

        elif sub_menu_selection == "Select":
            self.gc_input.game_state.selected_tool = chosen_item_name
            self.gc_input.menu_controller.exit_all_menus()

        elif sub_menu_selection == "Cancel":
            self.gc_input.menu_controller.exit_all_menus()


class ConversationOptionsMenuGhost(MenuGhost):
    BASE = "conversation_options_menu"
    NAME = BASE + "_ghost"

    def __init__(self, gc_input):
        super().__init__(gc_input)
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

    def generate_menu_information_package(self):
        source = self.get_menu_items_to_display().copy()
        cursor_at = self.cursor_at
        cursor_image = self.cursor
        text_display_list = []

        for item in range(len(source)):
            text_display_list.append(source[item])

        menu_specific = {"friendship_level": self.friendship,
                         "face_image": self.face_image,
                         "speaker_name": self.talking_to}

        menu_information = MenuInformation(self.menu_header, text_display_list, cursor_image, cursor_at, menu_specific)
        return menu_information

    def do_option(self):
        menu_selection = self.get_current_menu_item()
        self.gc_input.menu_controller.conversation_options_menu_selection(menu_selection)

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


class OutfitMenuGhost(MenuGhost):
    BASE = "outfit_menu"
    NAME = BASE + "_ghost"

    def __init__(self, gc_input):
        super().__init__(gc_input)
        self.menu_header = None
        self.menu_type = Types.BASE
        self.menu_item_list = []
        self.menu_images_list = []
        self.cursor = "-"
        self.shifts = 0
        self.max_displayed_items = 14
        self.currently_displayed_items = []
        self.update_currently_displayed()
        self.outfit_list = {"green_shirt": ["green_shirt", "Green Shirt"],
                            "red_shirt": ["red_shirt", "Red Shirt"],
                            "mermaid": ["mermaid", "Mermaid"],
                            "lab_coat": ["lab", "Lab Coat"],
                            "ninja_shinobi": ["ninja_shinobi", "Ninja Shinobi"],
                            "au_naturel": ["au_naturel", "Au Naturel"]}
        self.selected_outfit = "green_shirt"
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
        self.make_main_outfit(0)

    def generate_menu_information_package(self):
        source = self.get_menu_items_to_display().copy()
        cursor_at = self.cursor_at
        cursor_image = self.cursor
        text_display_list = []

        for item in range(len(source)):
            text_display_list.append(source[item])

        outfit_sprite_code = self.selected_outfit

        is_first_outfit = self.is_first_outfit
        is_last_outfit = self.is_last_outfit
        image = Spritesheet("Player_base_spritesheet", "assets/spritesheets/player_spritesheets/player_" + outfit_sprite_code + "_spritesheet.png",  32, 48)
        image_choice = image.get_image(0, 0)

        menu_specific = {"outfit_name": self.outfit_list[self.selected_outfit][1],
                         "is_first_outfit": is_first_outfit,
                         "is_last_outfit": is_last_outfit,
                         "outfit_image": image_choice}

        menu_information = MenuInformation(self.menu_header, text_display_list, cursor_image, cursor_at, menu_specific)
        return menu_information

    def do_option(self):
        player = self.gc_input.game_view.get_player_avatar()
        image = Spritesheet("Player_base_spritesheet", "assets/spritesheets/player_spritesheets/player_" + self.selected_outfit + "_spritesheet.png",  32, 48)
        player.spritesheet = image
        self.gc_input.outfit_manager.put_on_outfit(self.selected_outfit)
        self.gc_input.menu_controller.exit_all_menus()


    def cursor_left(self):
        length = len(self.outfit_list)
        if 0 < self.outfit_number:
            new_number = self.outfit_number - 1
            self.make_main_outfit(new_number)
        else:
            pass

    def cursor_right(self):
        length = len(self.outfit_list)
        if (length - 1) > self.outfit_number:
            new_number = self.outfit_number + 1
            self.make_main_outfit(new_number)
        else:
            pass

    def make_main_outfit(self, number):
        self.outfit_number = number
        outfit_keys = self.outfit_list.keys()
        sorted_keys = sorted(outfit_keys)
        self.selected_outfit = sorted_keys[number]

        length = len(sorted_keys)
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

    def __init__(self, gc_input):
        super().__init__(gc_input)
        self.menu_header = None
        self.menu_type = Types.BASE
        self.menu_item_list = []
        self.menu_images_list = []
        self.cursor = "-"
        self.shifts = 0
        self.max_displayed_items = 14
        self.currently_displayed_items = []
        self.galleries = ["Tree", "Bird"]
        # self.update_currently_displayed()
        self.Tree_item_list = {"Arbutus": ["Arbutus", "Arbutus"]}
        self.Bird_item_list = {"Robin": ["Robin", "Robin"],
                          "Tanager": ["Tanager", "Tanager"],
                          "Blackbird": ["Blackbird", "Blackbird"],
                          "Mallard": ["Mallard", "Mallard"],
                          "Pigeon 1": ["Pigeon 1", "Pigeon 1"],
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
        if pigeon_name == "Pigeon 2":
            image_choice = image.get_image(1, 0)
        if pigeon_name == "Pigeon 3":
            image_choice = image.get_image(2, 0)
        if pigeon_name == "Pigeon 4":
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

        if getattr(self, "selected_" + self.current_gallery) in ["Pigeon 1", "Pigeon 2", "Pigeon 3", "Pigeon 4"]:
            image_choice = self.get_pigeon_image(getattr(self, "selected_" + self.current_gallery))
        else:
            image = Spritesheet("Player_base_spritesheet", "assets/spritesheets/npc_spritesheets/" + sprite_code + "_spritesheet.png", 32, 48)
            image_choice = image.get_image(0, 0)

        menu_specific = {"item_name": getattr(self, self.current_gallery + "_item_list")[getattr(self, "selected_" + self.current_gallery)][1],
                         "is_first_item": is_first_item,
                         "is_last_item": is_last_item,
                         "item_image": image_choice}

        menu_information = MenuInformation(self.menu_header, text_display_list, cursor_image, cursor_at, menu_specific)
        return menu_information

    def do_option(self):
        details = {"image": "Crow"}
        self.gc_input.menu_controller.set_menu(PictureMenuGhost.BASE, details)

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

    def __init__(self, gc_input):
        super().__init__(gc_input)
        self.menu_header = None
        self.menu_type = Types.BASE
        self.menu_item_list = []
        self.menu_images_list = []
        self.cursor = "-"
        self.shifts = 0
        self.max_displayed_items = 14
        self.currently_displayed_items = []

    def prepare_menu_for_display(self, details):
        pass

    def generate_menu_information_package(self):
        cursor_at = self.cursor_at
        cursor_image = self.cursor
        text_display_list = []

        image = Spritesheet("Hornby_map_spritesheet", "assets/spritesheets/map_spritesheets/Hornby_map" + "_spritesheet.png",  256, 160)
        image_choice = image.get_image(0, 0)

        menu_specific = {"image": image_choice}

        menu_information = MenuInformation(self.menu_header, text_display_list, cursor_image, cursor_at, menu_specific)
        return menu_information

    def do_option(self):
        self.gc_input.menu_controller.exit_all_menus()


class PictureMenuGhost(MenuGhost):
    BASE = "picture_menu"
    NAME = BASE + "_ghost"

    def __init__(self, gc_input):
        super().__init__(gc_input)
        self.menu_header = None
        self.menu_type = Types.BASE
        self.menu_item_list = []
        self.image_name = "Tanager"
        self.menu_images_list = []
        self.cursor = "-"
        self.shifts = 0
        self.max_displayed_items = 14
        self.currently_displayed_items = []

    def prepare_menu_for_display(self, details):
        self.image_name = details["image"]

    def generate_menu_information_package(self):
        cursor_at = self.cursor_at
        cursor_image = self.cursor
        text_display_list = []

        image = Spritesheet("picture_spritesheet", "assets/spritesheets/irl_images/" + self.image_name + "_image.png",  256, 160)
        image_choice = image.get_image(0, 0)

        menu_specific = {"image": image_choice}

        menu_information = MenuInformation(self.menu_header, text_display_list, cursor_image, cursor_at, menu_specific)
        return menu_information

    def do_option(self):
        self.gc_input.menu_controller.exit_all_menus()


class ChatMenuGhost(MenuGhost):
    BASE = "chat_menu"
    NAME = BASE + "_ghost"

    def __init__(self, gc_input):
        super().__init__(gc_input)
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
                         "speaker_name": self.talking_to}

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
            self.gc_input.menu_controller.chat_menu_selection(menu_selection)


class GameActionDialogueMenuGhost(MenuGhost):
    BASE = "game_action_dialogue_menu"
    NAME = BASE + "_ghost"

    def __init__(self, gc_input):
        super().__init__(gc_input)

        self.gc_input = gc_input

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

    def __init__(self, gc_input):
        super().__init__(gc_input)
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
        self.gc_input.menu_controller.exit_menu(self.BASE)
        self.gc_input.game_state.ms.get_menu_ghost(self.master_menu).do_option(chosen_item_name)


class NumberSelectionMenuGhost(MenuGhost):
    BASE = "number_selection_menu"
    NAME = BASE + "_ghost"

    def __init__(self, gc_input):
        super().__init__(gc_input)
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
        self.gc_input.menu_controller.exit_menu(self.BASE)
        self.gc_input.game_state.ms.get_menu_ghost(self.master_menu).do_option(chosen_number)

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


class QuizMenuGhost(MenuGhost):
    BASE = "quiz_menu"
    NAME = BASE + "_ghost"

    def __init__(self, gc_input):
        super().__init__(gc_input)
        self.menu_header = None
        self.menu_type = Types.BASE
        self.menu_item_list = ["Talk", "Give Gift", "Exit"]
        self.menu_images_list = []
        self.currently_displayed_items = []
        self.prepare_menu_for_display()
        self.update_currently_displayed()
        spritesheet = Spritesheet("dog", "assets/quiz_material/dog.png", 224, 224)
        face = spritesheet.get_image(0, 0)
        face = face.subsurface(0, 0, 224, 224)
        self.image = face

    def prepare_menu_for_display(self):
        spritesheet = Spritesheet("dog", "assets/quiz_material/dog.png", 224, 224)
        face = spritesheet.get_image(0, 0)
        face = face.subsurface(0, 0, 224, 224)
        self.image = face
        self.menu_item_list = ["What type of dog is this?"]

    def update_currently_displayed(self):
        self.currently_displayed_items = []
        self.currently_displayed_items.append(self.menu_item_list)

    def generate_menu_information_package(self):
        source = self.get_menu_items_to_display().copy()
        text_display_list = []

        for item in range(len(source)):
            text_display_list.append(source[item])

        menu_specific = {"image": self.image}

        menu_information = MenuInformation(self.menu_header, text_display_list, " ", [0, 0], menu_specific)

        return menu_information

    def do_option(self):
        info = get_input()


class GuideMenuGhost(MenuGhost):
    BASE = "guide_menu"
    NAME = BASE + "_ghost"

    def __init__(self, gc_input):
        super().__init__(gc_input)
        self.menu_header = None
        self.menu_type = Types.BASE
        self.menu_item_list = []
        self.menu_images_list = []
        self.cursor = "-"
        self.shifts = 0
        self.max_displayed_items = 14
        self.currently_displayed_items = []
        bird_list = copy.copy(self.gc_input.game_state.gd.bird_master_list)
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
        if name in self.gc_input.game_state.held_pages:
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
                bird1_page_top = self.gc_input.inventory_manager.fetch_page(bird1 + "top")
            if panel2:
                bird1_page_bottom = self.gc_input.inventory_manager.fetch_page(bird1 + "bottom")

        if not bird2:
            panel3 = False
            panel4 = False
        else:
            panel3 = self.check_if_have_panel(bird2 + "top")
            panel4 = self.check_if_have_panel(bird2 + "bottom")
            if panel3:
                bird2_page_top = self.gc_input.inventory_manager.fetch_page(bird2 + "top")
                print(bird2_page_top.colour)
            if panel4:
                bird2_page_bottom = self.gc_input.inventory_manager.fetch_page(bird2 + "bottom")

        if panel1:
            image1 = Spritesheet("Hornby_map_spritesheet", "assets/spritesheets/map_spritesheets/Guide_Top_Light" + ".png",  168, 252)
            # bird_ghost = self.gc_input.game_state.gd.get_feature_ghost(self.master_birds_list[self.current_page])
            text_display_list.append(self.master_birds_list[self.current_page])
            text_display_list.append("Colour: " + bird1_page_top.colour)
            text_display_list.append("Size: " + bird1_page_top.size)
            text_display_list.append("Call: " + bird1_page_top.call)
        else:
            image1 = Spritesheet("Hornby_map_spritesheet", "assets/spritesheets/map_spritesheets/Guide_Top_Dark" + ".png", 168, 252)
            text_display_list.append(" ")
            text_display_list.append(" ")
            text_display_list.append(" ")
            text_display_list.append(" ")
        image_choice1 = image1.get_image(0, 0)

        if panel2:
            image2 = Spritesheet("Hornby_map_spritesheet", "assets/spritesheets/map_spritesheets/Guide_Bottom_Light" + ".png",  168, 252)
            description = textwrap.wrap(bird1_page_bottom.approach, width=15)
            text_display_list.append(description)
        else:
            image2 = Spritesheet("Hornby_map_spritesheet", "assets/spritesheets/map_spritesheets/Guide_Bottom_Dark" + ".png", 168, 252)
            text_display_list.append([" "])
        image_choice2 = image2.get_image(0, 0)

        if panel3:
            image3 = Spritesheet("Hornby_map_spritesheet", "assets/spritesheets/map_spritesheets/Guide_Top_Light" + ".png",  168, 252)
            text_display_list.append(self.master_birds_list[self.current_page + 1])
            text_display_list.append("Colour: " + bird2_page_top.colour)
            text_display_list.append("Size: " + bird2_page_top.size)
            text_display_list.append("Call: " + bird2_page_top.call)
        else:
            image3 = Spritesheet("Hornby_map_spritesheet", "assets/spritesheets/map_spritesheets/Guide_Top_Dark" + ".png", 168, 252)
            text_display_list.append(" ")
            text_display_list.append(" ")
            text_display_list.append(" ")
            text_display_list.append(" ")
        image_choice3 = image3.get_image(0, 0)

        if panel4:
            image4 = Spritesheet("Hornby_map_spritesheet", "assets/spritesheets/map_spritesheets/Guide_Bottom_Light" + ".png",  168, 252)
            description = textwrap.wrap(bird1_page_bottom.approach, width=15)
            text_display_list.append(description)
        else:
            image4 = Spritesheet("Hornby_map_spritesheet", "assets/spritesheets/map_spritesheets/Guide_Bottom_Dark" + ".png", 168, 252)
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

        image_choice4 = image4.get_image(0, 0)

        menu_specific = {"image": [image_choice1, image_choice2, image_choice3, image_choice4]}

        menu_information = MenuInformation(self.menu_header, text_display_list, cursor_image, cursor_at, menu_specific)
        return menu_information

    def do_option(self):
        self.gc_input.menu_controller.exit_all_menus()

    def reset_elements(self):
        self.current_page = 0