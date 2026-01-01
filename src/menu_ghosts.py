from definitions import GameSettings, Types


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
        self.menu_type = "base"

        self.cursor = "-"
        self.cursor_at = [0, 0]
        self.name = self.NAME

    def get_menu_items_to_print(self):
        return self.menu_item_list

    def choose_option(self):
        self.do_option()

    def get_current_menu_item(self):
        menu_selection = self.menu_item_list[self.cursor_at[1]]
        return menu_selection

    def do_option(self):
        menu_selection = self.get_current_menu_item()

    def generate_text_print(self):
        source = self.get_menu_items_to_print().copy()
        cursor_at = self.cursor_at
        cursor_img = self.cursor
        text_print_list = []

        for item in range(len(source)):
            text_print_list.append(source[item])

        menu_information = {"header": self.menu_header,
                            "text_print_list": text_print_list,
                            "cursor_img": cursor_img,
                            "cursor_at": cursor_at}

        return menu_information

    def generate_image_print(self):
        image_print_list = {}
        for image in range(len(self.menu_images_list)):
            image_print_list["Item_" + str(image)] = self.menu_images_list[image]
        return image_print_list

    def update_menu_items_list(self):
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

    def reset_cursor(self):
        self.cursor_at[0] = 0
        self.cursor_at[1] = 0

    @property
    def size(self):
        return len(self.menu_item_list)


class SpecialMenuGhost(MenuGhost):
    BASE = "special_menu"
    NAME = BASE + "_ghost"

    def __init__(self, gc_input):
        super().__init__(gc_input)


class StatMenuGhost(MenuGhost):
    BASE = "stat_menu"
    NAME = BASE + "_ghost"

    def __init__(self, gc_input):
        super().__init__(gc_input)
        self.menu_header = "STATISTICS"

        self.menu_item_list = []
        self.menu_images_list = []
        self.cursor = None
        self.update_menu_items_list()
        self.menu_type = Types.OVERWORLD

    def update_menu_items_list(self):
        stat_dict = self.gc_input.get_stat_items()
        self.menu_item_list = [("Coins: ", stat_dict["Coins"]), ("Day: ", stat_dict["day"]), ("Time: ", stat_dict["time"]), ("Seeds:", stat_dict["seeds"]), ("Select: ", stat_dict["selected_tool"])]

    def get_menu_items_to_print(self):
        printable_item_list = []

        for option in range(self.size):
            item = self.menu_item_list[option][0]
            available_spaces = 16
            item_word_length = len(item)
            quantity = self.menu_item_list[option][1]
            quantity_word_length = len(quantity)
            total_length = item_word_length + quantity_word_length
            number_of_spaces = available_spaces - total_length
            spaces_str = ""
            for x in range(number_of_spaces):
                spaces_str = spaces_str + " "
            final_item = item + spaces_str + quantity
            printable_item_list.append(final_item)

        return printable_item_list

    def get_current_menu_item(self):
        menu_selection = self.menu_item_list[self.cursor_at[1]]
        return menu_selection


class StartMenuGhost(MenuGhost):
    BASE = "start_menu"
    NAME = BASE + "_ghost"

    def __init__(self, gc_input):
        super().__init__(gc_input)
        self.menu_header = None
        self.menu_item_list = ["Bag", "Outfits", "Map", "Chore List", "Profile", "Save", "Options", "Vibes"]
        self.menu_item_list.append("Exit")
        self.menu_images_list = []
        self.cursor = "-"
        self.update_menu_items_list()

    def do_option(self):
        menu_selection = self.get_current_menu_item()
        self.gc_input.game_state.ms.start_menu_selection(menu_selection)


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
        self.update_menu_items_list()
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
        self.gc_input.game_state.ms.previous_menu(self.BASE)

    def cursor_right(self):
        self.gc_input.game_state.ms.next_menu(self.BASE)

    def update_menu_items_list(self):
        keys_list = []
        current_inventory = self.gc_input.game_state.get_menu_items(self.BASE)
        for item in current_inventory:
            keys_list.append(item)
        self.menu_item_list = keys_list
        self.menu_item_list.append("Exit")
        self.update_currently_displayed()

    def get_menu_items_to_print(self): #TODO: move most of this to menu avatar/display
        menu_length_calc = 0
        if self.size >= self.max_displayed_items:
            menu_length_calc = self.max_displayed_items
        elif self.size < self.max_displayed_items:
            menu_length_calc = self.size

        printable_item_list = []

        for option in range(menu_length_calc):
            item = self.currently_displayed_items[option]
            if item == "Exit":
                printable_item_list.append(self.currently_displayed_items[option])

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
                printable_item_list.append(final_item)

        return printable_item_list

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
            self.gc_input.game_state.ms.exit_all_menus()
        else:
            self.gc_input.game_state.ms.set_menu("use_menu", {"master_menu": self.BASE})

    def do_option(self, choice=None):
        sub_menu_selection = choice
        chosen_item_name = self.get_current_menu_item()

        if sub_menu_selection == "Use":
            print("used the " + chosen_item_name)
            chosen_item = self.gc_input.inventory_manager.gc_input.game_state.gd.item_data_list[chosen_item_name]
            self.gc_input.inventory_manager.use_item(chosen_item, 1)
            self.update_menu_items_list()

        elif sub_menu_selection == "Toss":
            self.gc_input.game_state.ms.exit_all_menus()

        elif sub_menu_selection == "Cancel":
            self.gc_input.game_state.ms.exit_all_menus()


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
        self.update_menu_items_list()
        self.update_currently_displayed()


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
        self.update_menu_items_list()
        self.update_currently_displayed()

    def get_menu_items_to_print(self):
        menu_length_calc = 0
        if self.size >= self.max_displayed_items:
            menu_length_calc = self.max_displayed_items
        elif self.size < self.max_displayed_items:
            menu_length_calc = self.size

        printable_item_list = []

        for option in range(menu_length_calc):
            item = self.currently_displayed_items[option]
            printable_item_list.append(self.currently_displayed_items[option])

        return printable_item_list


class ConversationOptionsMenuGhost(MenuGhost):
    BASE = "conversation_options_menu"
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
        self.update_menu_items_list()
        self.update_currently_displayed()

    def cursor_down(self):
        # print(self.size)
        # print(self.cursor_at[1])
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
        # print(self.cursor_at[1])

    def cursor_up(self):
        if (self.cursor_at[1] + self.shifts) > 0:
            if self.cursor_at[1] == 0 and self.shifts > 0:
                self.shifts -= 1
                self.update_currently_displayed()
            elif self.cursor_at[1] > 0:
                self.cursor_at[1] -= 1
            else:
                pass

    def update_menu_items_list(self):
        # keys_list = []
        # current_inventory = self.gc_input.game_state.current_inventory
        # for item in current_inventory:
        #     keys_list.append(item)
        # self.menu_item_list = keys_list
        # self.menu_item_list.append("Exit")
        # self.update_currently_displayed()
        pass

    def get_menu_items_to_print(self):
        menu_length_calc = 0
        if self.size >= self.max_displayed_items:
            menu_length_calc = self.max_displayed_items
        elif self.size < self.max_displayed_items:
            menu_length_calc = self.size

        printable_item_list = []

        for option in range(menu_length_calc):
            item = self.currently_displayed_items[option]
            if item == "Exit":
                printable_item_list.append(self.currently_displayed_items[option])

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
                printable_item_list.append(final_item)

        return printable_item_list

    def update_currently_displayed(self):
        self.currently_displayed_items = []
        if self.size <= self.max_displayed_items:
            for item in range(self.size):
                self.currently_displayed_items.append(self.menu_item_list[item + self.shifts])
        else:
            for item in range(self.max_displayed_items):
                self.currently_displayed_items.append(self.menu_item_list[item + self.shifts])


class GameActionDialogueGhost(MenuGhost):
    BASE = "game_action_dialogue_menu"
    NAME = BASE + "_ghost"

    def __init__(self, gc_input):
        super().__init__(gc_input)

        self.gc_input = gc_input

        self.menu_header = None
        self.menu_item_list = ["This is the game dialouge box!"]
        self.menu_images_list = []
        self.additional_information = []
        self.menu_type = "static"

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

    def generate_image_print(self):
        image_print_list = []
        return image_print_list


class SubMenuGhost(MenuGhost):
    BASE = "sub_menu"
    NAME = BASE + "_ghost"

    def __init__(self, gc_input):
        super().__init__(gc_input)
        self.menu_item_list = ["Yes", "No"]
        self.master_menu = None
        self.menu_type = "sub"
        self.menu_header = None

    def choose_option(self):
        self.do_option()
        print("we did it!")

    def set_master_menu(self, master_menu):
        self.master_menu = master_menu

class UseMenuGhost(MenuGhost):
    BASE = "use_menu"
    NAME = BASE + "_ghost"

    def __init__(self, gc_input):
        super().__init__(gc_input)
        self.menu_item_list = ["Use", "Toss", "Cancel"]
        self.master_menu = None
        self.menu_type = "sub"
        self.menu_header = None

    def choose_option(self):
        chosen_item_name = self.get_current_menu_item()
        if chosen_item_name == "Exit":
            self.gc_input.game_state.ms.exit_all_menus()
        else:
            print(self.NAME)
            self.gc_input.game_state.ms.deactivate_menu(self.BASE)
            self.gc_input.game_state.ms.menu_ghost_data_list[self.master_menu + "_ghost"].do_option(chosen_item_name)
            # self.do_option(chosen_item_name)
            # self.gc_input.menu_manager.set_sub_menu("yes_no_menu", self.BASE)

    def set_master_menu(self, master_menu):
        self.master_menu = master_menu

    def do_option(self, choice=None):
        menu_selection = choice
        chosen_item_name = self.get_current_menu_item()

        if menu_selection == "Use":
            print("used the " + chosen_item_name)
            chosen_item = self.gc_input.inventory_manager.gc_input.game_state.gd.item_data_list[chosen_item_name]
            self.gc_input.inventory_manager.use_item(chosen_item, 1)
            self.update_menu_items_list()

        elif menu_selection == "Toss":
            self.gc_input.game_state.ms.exit_all_menus()

        elif menu_selection == "Exit":
            self.gc_input.game_state.ms.exit_all_menus()


class YesNoMenuGhost(MenuGhost):
    BASE = "yes_no_menu"
    NAME = BASE + "_ghost"

    def __init__(self, gc_input):
        super().__init__(gc_input)
        self.menu_item_list = ["Yes", "No"]
        self.master_menu = None
        self.menu_type = "sub"
        self.menu_header = None

    def choose_option(self):
        self.do_option()
        print("we did it!")

    def set_master_menu(self, master_menu):
        self.master_menu = master_menu