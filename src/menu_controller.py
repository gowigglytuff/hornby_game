import copy
from typing import TYPE_CHECKING

from definitions import Types, Mundane
from input_manager_controller_page import InMenuKeyboardManager
from menu_ghosts_data_page import StartMenuGhost, GameActionDialogueMenuGhost, SceneDialogueMenuGhost, ChatMenuGhost, SellItemMenuGhost, SellerMenuGhost, SellerOptionsMenuGhost, GiftGivingMenuGhost, ConversationOptionsMenuGhost, OutfitMenuGhost, GalleryMenuGhost, MapMenuGhost, WordsMenuGhost, GuideMenuGhost, SuppliesInventoryMenuGhost, NumberSelectionMenuGhost, StatMenuGhost, GameModeStatMenuGhost, AcquireMenuGhost, DeveloperMenuGhost, TreasureInventoryMenuGhost, DepositMenuGhost, \
    KeyInventoryMenuGhost, BasketMenuGhost, PictureMenuGhost, CharacterAssemblyMenuGhost, QuizMenuGhost, SubMenuGhost, TextInputMenuGhost, RoomSelectMenuGhost, CharacterSpritesheetViewMenuGhost

if TYPE_CHECKING:
    from game_controller import Controller, BuilderController


class MenuController(object):
    def __init__(self, controller):
        self.controller = controller  # type: Controller
        self.text_box_controller = TextBoxController(self.controller, self)

    def get_current_text_box(self):
        active_menu = self.controller.gs.ms.get_active_menu()
        current_text_box = active_menu.get_current_text_box()
        return current_text_box

    def update_current_menu_text_and_images(self):
        self.update_menu_text_and_images(self.controller.gs.ms.get_active_menu())

    def update_menu_text_and_images(self, menu_ghost):
        menu_avatar = self.controller.game_view.menu_avatar_data_list[menu_ghost.BASE + "_avatar"]
        info_package = menu_ghost.generate_menu_information_package()
        menu_avatar.get_menu_text_drawing_instructions(info_package)
        menu_avatar.get_menu_image_drawing_instructions(info_package)

    def menu_cursor_down(self):
        active_menu = self.controller.gs.ms.menu_ghost_data_list[self.controller.gs.ms.menu_stack[0] + "_ghost"]
        active_menu.cursor_down()
        self.update_menu_text_and_images(active_menu)

    def menu_cursor_up(self):
        active_menu = self.controller.gs.ms.menu_ghost_data_list[self.controller.gs.ms.menu_stack[0] + "_ghost"]
        active_menu.cursor_up()
        self.update_menu_text_and_images(active_menu)

    def menu_cursor_left(self):
        active_menu = self.controller.gs.ms.menu_ghost_data_list[self.controller.gs.ms.menu_stack[0] + "_ghost"]
        active_menu.cursor_left()
        self.update_menu_text_and_images(active_menu)

    def push_menu_button(self, button_name, menu_ghost):
        menu_ghost.push_menu_button(button_name)
        self.update_menu_text_and_images(menu_ghost)

    def menu_cursor_right(self):
        active_menu = self.controller.gs.ms.menu_ghost_data_list[self.controller.gs.ms.menu_stack[0] + "_ghost"]
        active_menu.cursor_right()
        self.update_menu_text_and_images(active_menu)

    def menu_choose_option(self):
        active_menu = self.controller.gs.ms.menu_ghost_data_list[self.controller.gs.ms.menu_stack[0] + "_ghost"]
        active_menu.choose_option()
        self.update_menu_text_and_images(active_menu)

    def key_letter_pressed(self, letter):
        active_menu = self.controller.gs.ms.menu_ghost_data_list[self.controller.gs.ms.menu_stack[0] + "_ghost"]
        active_menu.key_letter(letter)
        self.update_menu_text_and_images(active_menu)

    def erase_letter_pressed(self):
        active_menu = self.controller.gs.ms.menu_ghost_data_list[self.controller.gs.ms.menu_stack[0] + "_ghost"]
        active_menu.erase_letter()
        self.update_menu_text_and_images(active_menu)

    def activate_menu(self):
        pass

    def get_stat_mode_items(self):
        mode = copy.copy(self.controller.game.mode)

        stat_dict = {"mode": mode}

        return stat_dict

    def get_developer_items(self):
        player_ghost = self.controller.gs.get_player_ghost()
        player_avatar = self.controller.gs.gv.get_player_avatar()
        camera = self.controller.gs.gv.camera
        room_name = self.controller.gs.get_current_room().room_name

        stat_dict = {"Room": str(room_name),
                     "Player": str(player_ghost.x) + ", " + str(player_ghost.y),
                     "Image": str(player_avatar.image_x) + ", " + str(player_avatar.image_y),
                     "Camera": str(camera[0]) + ", " + str(camera[1])}

        return stat_dict

    def set_menu(self, menu_name, details):
        selected_menu = self.controller.gs.ms.get_menu_ghost(menu_name)
        selected_menu_avatar = self.controller.gs.gv.get_menu_avatar(menu_name + "_avatar")
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
            self.controller.game_view.update_sub_menu_display_details(menu_name, details["master_menu"], information_from_ghost)

        if menu_name == ChatMenuGhost.BASE:
            selected_menu.set_current_phrase(details["phrase"])

        self.update_menu_text_and_images(selected_menu)

        self.controller.game.set_active_keyboard_manager(InMenuKeyboardManager.ID)
        selected_menu.gc.gs.ms.add_menu_to_stack(menu_name)

    def next_menu(self, current_menu):
        total_number_menus = len(self.controller.gs.ms.start_menu_stack)
        current_menu_index = self.controller.gs.ms.start_menu_stack.index(current_menu)
        self.exit_menu(self.controller.gs.ms.start_menu_stack[current_menu_index])
        next_menu = self.controller.gs.ms.start_menu_stack[0]
        if current_menu_index != (total_number_menus - 1):
            next_menu = self.controller.gs.ms.start_menu_stack[current_menu_index + 1]
        else:
            pass
        self.set_menu(next_menu, None)

    def previous_menu(self, current_menu):
        total_number_menus = len(self.controller.gs.ms.start_menu_stack)
        current_menu_index = self.controller.gs.ms.start_menu_stack.index(current_menu)
        self.exit_menu(self.controller.gs.ms.start_menu_stack[current_menu_index])
        previous_menu = self.controller.gs.ms.start_menu_stack[current_menu_index-1]
        if current_menu_index == 0:
            previous_menu = self.controller.gs.ms.start_menu_stack[total_number_menus - 1]
        else:
            pass
        self.set_menu(previous_menu, None)

    def exit_menu(self, menu_name):
        selected_menu = self.controller.gs.ms.get_menu_ghost(menu_name)
        selected_menu.reset_elements()
        self.controller.gs.ms.deactivate_menu(menu_name)

    def exit_scene_menu(self, menu_name):
        selected_menu = self.controller.gs.ms.get_menu_ghost(menu_name)
        selected_menu.reset_elements()
        self.controller.gs.ms.deactivate_menu(menu_name)
        self.controller.scene_manager.waiting_for_response = False
        self.controller.scene_manager.process_scene_queue()

    def exit_all_menus(self):
        list = []
        for x in self.controller.gs.ms.menu_stack:
            list.append(x)
        for item in list:
            self.exit_menu(item)

    def resize_sub_menu(self):
        pass


class BuilderMenuController(MenuController):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller  # type: BuilderController

    def builder_function_menu_selection(self, item_selected):
        menu_selection = item_selected
        if menu_selection == "Design Sprite":
            self.controller.menu_controller.exit_all_menus()
            self.controller.menu_controller.set_menu(CharacterAssemblyMenuGhost.BASE, None)

        elif menu_selection == "Change Map":
            self.controller.menu_controller.exit_all_menus()
            self.controller.menu_controller.set_menu(RoomSelectMenuGhost.BASE, None)

        if menu_selection == "View Sprites":
            self.controller.menu_controller.exit_all_menus()
            self.controller.menu_controller.set_menu(CharacterSpritesheetViewMenuGhost.BASE, None)

        elif menu_selection == "Toggle Display":
            self.controller.toggle_on_view_window()

        elif menu_selection == "Toggle Names":
            self.controller.toggle_name_display_on()

        else:
            pass

class InGameMenuController(MenuController):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller  # type: Controller

    def get_game_time_string(self):
        hour = self.controller.gs.hour_of_day
        minute = self.controller.gs.minute_of_hour
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
        for menu in self.controller.gs.ms.static_menus:
            ghost = self.controller.gs.ms.get_menu_ghost(menu)
            self.update_menu_text_and_images(ghost)

    def get_stat_items(self):
        hour = self.controller.gs.hour_of_day
        minute = self.controller.gs.minute_of_hour

        stat_dict = {"Birds": str(self.controller.gs.bird_count),
                     "Pigeons": str(self.controller.gs.pigeon_count),
                     "time": self.get_game_time_string(),
                     "day": str(self.controller.gs.day_of_summer),
                     "selected_tool": str(self.controller.gs.selected_tool)}

        return stat_dict

    def gift_menu_selection(self, sub_menu_selection, chosen_item_name, details):
        if sub_menu_selection == "Yes":
            chosen_item = self.controller.gs.gd.item_data_list[chosen_item_name]
            speaker = self.controller.gs.get_feature_ghost(details["speaker_unique_name"])

            self.controller.inventory_manager.remove_item(chosen_item, 1)
            self.controller.menu_controller.post_notice("You gave " + speaker.display_name + " a " + chosen_item.name)

            phrase, follow_up = speaker.receive_gift(chosen_item_name)

            details["phrase"] = [phrase]
            details["friendship_level"] = Mundane.get_friendship_hearts(speaker.friendship_level)
            details["follow_up"] = follow_up
            self.controller.menu_controller.exit_all_menus()
            speaker.currently_chatting = True
            self.controller.menu_controller.set_menu(ChatMenuGhost.BASE, details)

        else:
            self.controller.menu_controller.exit_all_menus()

    def inventory_menu_selection(self, inventory_menu_object, sub_menu_selection, chosen_item_name):
        chosen_item = self.controller.inventory_manager.gc.gs.gd.item_data_list[chosen_item_name]

        if not inventory_menu_object.action_doing:
            if sub_menu_selection == "Use":
                inventory_menu_object.action_doing = "Use"
                self.post_notice("Use how many " + chosen_item.name + "(s)?")
                self.controller.menu_controller.set_menu(NumberSelectionMenuGhost.BASE, {"master_menu": inventory_menu_object.BASE, "max_number": self.controller.inventory_manager.get_quantity_of_item(chosen_item.name), "min_number": 1})

            elif sub_menu_selection == "Toss":
                inventory_menu_object.action_doing = "Toss"
                self.post_notice("Toss how many " + chosen_item.name + "(s)?")
                self.controller.menu_controller.set_menu(NumberSelectionMenuGhost.BASE, {"master_menu": inventory_menu_object.BASE, "max_number": self.controller.inventory_manager.get_quantity_of_item(chosen_item.name), "min_number": 1})

            elif sub_menu_selection == "Cancel":
                self.controller.menu_controller.exit_all_menus()
        else:
            if inventory_menu_object.action_doing == "Use":
                self.controller.inventory_manager.use_item(chosen_item, sub_menu_selection)

            elif inventory_menu_object.action_doing == "Toss":
                self.toss_item(chosen_item, sub_menu_selection)

            inventory_menu_object.action_doing = None
            self.controller.menu_controller.exit_all_menus()

    def toss_item(self, item, number_to_toss):
        self.controller.inventory_manager.remove_item(item, number_to_toss)
        self.post_notice("You tossed " + str(number_to_toss) + " " + item.name + "(s)")

    def start_menu_selection(self, item_selected):
        menu_selection = item_selected
        if menu_selection == "Bag":
            self.controller.menu_controller.exit_menu(StartMenuGhost.BASE)
            self.controller.menu_controller.set_menu(SuppliesInventoryMenuGhost.BASE, None)

        elif menu_selection == "Guide":
            self.controller.menu_controller.exit_menu(StartMenuGhost.BASE)
            self.controller.menu_controller.set_menu(GuideMenuGhost.BASE, None)

        elif menu_selection == "Speak":
            # self.controller.menu_controller.exit_menu(StartMenuGhost.BASE)
            self.controller.menu_controller.set_menu(WordsMenuGhost.BASE, None)
            # self.controller.menu_controller.set_menu(TextInputMenuGhost.BASE, {"master_menu": StartMenuGhost.BASE})

        elif menu_selection == "Map":
            self.controller.menu_controller.exit_menu(StartMenuGhost.BASE)
            self.controller.menu_controller.set_menu(MapMenuGhost.BASE, None)

        elif menu_selection == "Options":
            pass

        elif menu_selection == "Gallery":
            self.controller.menu_controller.exit_menu(StartMenuGhost.BASE)
            self.controller.menu_controller.set_menu(GalleryMenuGhost.BASE, None)

        elif menu_selection == "Records":
            pass

        elif menu_selection == "Outfits":
            self.controller.menu_controller.exit_menu(StartMenuGhost.BASE)
            self.controller.menu_controller.set_menu(OutfitMenuGhost.BASE, None)

        elif menu_selection == "Save":
            pass

        elif menu_selection == "Exit":
            self.controller.menu_controller.exit_all_menus()

        else:
            self.controller.menu_controller.exit_all_menus()

    def conversation_options_menu_selection(self, item_selected):
        menu_selection = item_selected
        current_menu = self.controller.gs.ms.get_menu_ghost(ConversationOptionsMenuGhost.BASE)
        phrase_list = ["base_phrase", "good_gift_phrase", "bad_gift_phrase", "neutral_gift_phrase", "bird_hint_phrase"]
        selected_phrase = copy.copy(getattr(self.controller.gs.get_feature_ghost(current_menu.speaker_unique_name), choice(phrase_list)))
        # selected_phrase = self.gs.get_feature_ghost(current_menu.speaker_unique_name).base_phrase
        details = {"speaker_name": copy.copy(current_menu.talking_to),
                   "friendship_level": copy.copy(current_menu.friendship),
                   "face_image": copy.copy(current_menu.face_image),
                   "actor_type": copy.copy(current_menu.actor_type),
                   "speaker_unique_name": copy.copy(current_menu.speaker_unique_name),
                   "phrase": [selected_phrase],
                   "follow_up": {"action": None}}

        if menu_selection == "Talk":
            self.controller.menu_controller.exit_menu(ConversationOptionsMenuGhost.BASE)
            self.controller.gs.get_feature_ghost(details["speaker_unique_name"]).currently_chatting = True
            self.controller.menu_controller.set_menu(ChatMenuGhost.BASE, details)

        elif menu_selection == "Give Gift":
            details["master_menu"] = current_menu.BASE
            # self.controller.menu_controller.exit_menu(ConversationOptionsMenuGhost.BASE)
            self.controller.menu_controller.set_menu(GiftGivingMenuGhost.BASE, details)

        elif menu_selection == "Exit":
            self.controller.menu_controller.exit_all_menus()

        else:
            self.controller.menu_controller.exit_all_menus()

    def seller_options_menu_selection(self, item_selected):
        menu_selection = item_selected
        current_menu = self.controller.gs.ms.get_menu_ghost(SellerOptionsMenuGhost.BASE)
        character_talking_to_ghost = self.controller.gs.get_feature_ghost(current_menu.speaker_unique_name)

        if menu_selection == "Buy":
            details = {"seller_items": character_talking_to_ghost.get_items_list()[0],
                       "seller_item_prices": character_talking_to_ghost.get_items_list()[1]}
            self.controller.menu_controller.set_menu(SellerMenuGhost.BASE, details)

        elif menu_selection == "Sell":
            details = {}
            self.controller.menu_controller.exit_all_menus()
            self.controller.menu_controller.set_menu(SellItemMenuGhost.BASE, details)

        elif menu_selection == "Exit":
            self.controller.menu_controller.exit_all_menus()

        else:
            self.controller.menu_controller.exit_all_menus()


    def chat_menu_selection(self, item_selected, follow_up):
        if follow_up:
            if follow_up["action"] == "Gift":
                item_type = self.controller.inventory_manager.get_any_type_item(follow_up["item"], follow_up["quantity"])

                phrase_1 = None
                phrase_2 = None
                if item_type in ["Key Item", "Treasure Item"]:
                    phrase_1 = "You received the " + follow_up["item"] + "."
                    phrase_2 = "Put the " + follow_up["item"] + " in bag."
                elif item_type in ["Item"]:
                    phrase_1 = "You received " + str(follow_up["quantity"]) + " " + follow_up["item"] + "(s)."
                    phrase_2 = "Put " + follow_up["item"] + "(s) in bag"
                elif item_type in ["Bird Page"]:
                    phrase_1 = "You received the " + follow_up["item"] + "."
                    phrase_2 = "Put the " + follow_up["item"] + " in guide."
                else:
                    pass
                self.post_notice(phrase_1)
                self.post_notice(phrase_2)
                self.exit_all_menus()
            elif follow_up["action"] == "set_menu":
                self.exit_all_menus()
                self.set_menu(follow_up["menu_name"], follow_up["details_dict"])

            else:
                self.exit_all_menus()
        else:
            self.exit_all_menus()

    def scene_menu_selection(self, item_selected):
        self.controller.menu_controller.exit_scene_menu(SceneDialogueMenuGhost.BASE)

    def post_notice(self, phrase):
        self.controller.gs.ms.get_menu_ghost(GameActionDialogueMenuGhost.BASE).show_dialogue(phrase)

    def set_start_menu(self):
        self.set_menu(StartMenuGhost.BASE, None)


class TextBoxController(object):
    def __init__(self, gc, menu_controller):
        self.menu_controller = menu_controller
        self.controller = gc

    def key_letter_pressed(self, letter):
        current_text_box = self.menu_controller.get_current_text_box()
        current_text_box.add_letter(letter)
        self.menu_controller.update_current_menu_text_and_images()

    def key_return_pressed(self):
        self.controller.gs.ms.get_active_menu().unset_current_text_entry_box()
        self.menu_controller.update_current_menu_text_and_images()

    def key_backspace_pressed(self):
        current_text_box = self.menu_controller.get_current_text_box()
        current_text_box.erase_letter()
        self.menu_controller.update_current_menu_text_and_images()

    def mouse_clicked(self, click):
        current_text_box = self.menu_controller.get_current_text_box()
        current_menu_ghost = self.controller.gs.ms.get_active_menu()
        current_menu_avatar = self.controller.gs.gv.get_active_menu_avatar()
        # current_text_box_button = current_menu_avatar.button_list[current_text_box.name + "_button"]

        self.controller.gs.ms.get_active_menu().unset_current_text_entry_box()
        self.menu_controller.update_menu_text_and_images(current_menu_ghost)