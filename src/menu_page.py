# import textwrap
#
# import pygame
#
# from definitions import GameSettings, Types
# from spritesheet import Spritesheet
# from graphics import BuiltOverlay
# #
# # class BuiltOverlay(object):
# #     def __init__(self, name, width, height):
# #         self.x = None
# #         self.y = None
# #         self.square_size = (24, 24)
# #         self.width = int(width)
# #         self.height = int(height)
# #         self.name = name
# #         self.image = None
# #
# #     def build_overlay(self):
# #         tile_segment_size = GameSettings.MENUSEGMENTSIZE
# #         sheet = Spritesheet("overlay_pieces", "assets/spritesheets/menu_spritesheets/menu_structure_gray.png", tile_segment_size, tile_segment_size)
# #         x = self.width * tile_segment_size
# #         y = self.height * tile_segment_size
# #         base = pygame.Surface((x, y))
# #         for item_y in range(self.height):
# #             for item_x in range(self.width):
# #                 loc_x = 0
# #                 loc_y = 0
# #
# #                 if item_y == 0:
# #                     loc_y = 0
# #                 elif item_y == self.height-1:
# #                     loc_y = 2
# #                 else:
# #                     loc_y = 1
# #
# #                 if item_x == 0:
# #                     loc_x = 0
# #                 elif item_x == self.width-1:
# #                     loc_x = 2
# #                 else:
# #                     loc_x = 1
# #
# #                 base.blit(sheet.get_image(loc_x, loc_y, transparent=False), [item_x * tile_segment_size, item_y * tile_segment_size])
# #
# #         return base
# #
# #     def build_overlay_with_header(self, offset_y):
# #         segment_size = GameSettings.MENUSEGMENTSIZE
# #         sheet = Spritesheet("overlay_pieces", "assets/spritesheets/menu_spritesheets/menu_structure_gray.png", segment_size, segment_size)
# #
# #         head_x = self.width * segment_size
# #         offset_value = offset_y/segment_size
# #         header_size = GameSettings.FONT_SIZE/segment_size
# #         head_y_segments = int(offset_value * 2 + header_size)
# #
# #         base_size_x = self.width * segment_size
# #         base_size_y = self.height * segment_size + (head_y_segments * segment_size)
# #         base = pygame.Surface((base_size_x, base_size_y))
# #         print(self.height)
# #
# #         head_y = head_y_segments * segment_size
# #         head_base = pygame.Surface((head_x, head_y))
# #         for item_y in range(head_y_segments):
# #             for item_x in range(int(self.width)):
# #                 loc_x = 0
# #                 loc_y = 0
# #                 if item_y == 0:
# #                     loc_y = 0
# #                 elif item_y == head_y_segments - 1:
# #                     loc_y = 2
# #                 else:
# #                     loc_y = 1
# #                 if item_x == 0:
# #                     loc_x = 0
# #                 elif item_x == self.width - 1:
# #                     loc_x = 2
# #                 else:
# #                     loc_x = 1
# #                 head_base.blit(sheet.get_image(loc_x, loc_y, transparent=False), [item_x * segment_size, item_y * segment_size])
# #
# #         body_x = self.width * segment_size
# #         body_y = self.height * segment_size
# #         body_base = pygame.Surface((body_x, body_y))
# #         for item_y in range(int(self.height)):
# #             for item_x in range(int(self.width)):
# #                 loc_x = 0
# #                 loc_y = 0
# #
# #                 if item_y == 0:
# #                     loc_y = 0
# #                 elif item_y == self.height - 1:
# #                     loc_y = 2
# #                 else:
# #                     loc_y = 1
# #
# #                 if item_x == 0:
# #                     loc_x = 0
# #                 elif item_x == self.width - 1:
# #                     loc_x = 2
# #                 else:
# #                     loc_x = 1
# #
# #                 body_base.blit(sheet.get_image(loc_x, loc_y, transparent=False), [item_x * segment_size, item_y * segment_size])
# #
# #         base.blit(head_base, [0, 0])
# #         base.blit(body_base, [0, head_y])
# #
# #
# #         return base
#
# class Overlay(object):
#     def __init__(self, name, image):
#         self.name = name
#         self.image = image
#
#
# class TextPrint(object):
#     def __init__(self, text, x, y):
#         self.text = text
#         self.x = x
#         self.y = y
#
#
# class PhotoPrint(object):
#     def __init__(self, image, x, y):
#         self.image = image
#         self.x = x
#         self.y = y
#
#
# class Menu(object):
#     NAME = "Menu_Base"
#
#     def __init__(self, gc_input):
#         super().__init__()
#         self.gc_input = gc_input  #  type: GameController
#         self.overlay_size_x = 0
#         self.overlay_size_Y = 0
#         self.x = 0
#         self.y = 0
#
#         self.offset_x = 20
#         self.offset_y = 20
#         self.header_spacing = 10
#         self.menu_spread = 25
#
#         self.menu_item_list = []
#         self.menu_header = None
#
#         self.cursor = None
#         self.cursor_at = 0
#
#         self.name = self.NAME
#         self.menu_type = None
#
#         self.max_menu_width = 0
#         self.max_menu_length = 0
#
#     def fill_out_menu_info(self, screen_x, screen_y):
#             self.name = self.NAME
#
#             spritesheet_width = self.overlay_size_x * GameSettings.MENUSEGMENTSIZE
#             spritesheet_height = self.overlay_size_Y * GameSettings.MENUSEGMENTSIZE
#
#             edge = GameSettings.MENUEDGE
#
#             x = 0
#             y = 0
#
#             if screen_x == "center":
#                 x = GameSettings.RESOLUTION[0] / 2 - spritesheet_width / 2
#             elif screen_x == "left":
#                 x = 0 + GameSettings.RESOLUTION[0] / edge
#             elif screen_x == "right":
#                 x = GameSettings.RESOLUTION[0] - spritesheet_width - GameSettings.RESOLUTION[0] / edge
#             else:
#                 x = screen_x
#
#             if screen_y == "center":
#                 y = GameSettings.RESOLUTION[1] / 2 - spritesheet_height / 2
#             elif screen_y == "top":
#                 y = 0 + GameSettings.RESOLUTION[1] / edge
#             elif screen_y == "bottom":
#                 y = GameSettings.RESOLUTION[1] - spritesheet_height - GameSettings.RESOLUTION[1] / edge
#             else:
#                 y = screen_y
#
#             self.x = x
#             self.y = y
#
#             if self.menu_header:
#                 self.header_spacing = 20
#
#     def get_menu_items_to_print(self):
#         return self.menu_item_list
#
#     def generate_text_print(self):
#         source = self.get_menu_items_to_print().copy()
#         cursor_spot = self.cursor_at
#         text_print_list = []
#         if self.menu_header:
#             source.insert(0, self.menu_header)
#             cursor_spot = self.cursor_at + 1
#             # text_print_list.append(TextPrint(, self.offset_x, self.offset_y))
#         for item in range(len(source)):
#             text_print_list.append(TextPrint(source[item], self.offset_x, self.offset_y + (item * self.menu_spread)))
#         if self.cursor:
#             text_print_list.append(TextPrint(self.cursor, self.offset_x - GameSettings.FONT_SIZE * 1.5, self.offset_y + GameSettings.FONT_SIZE / 4 + (cursor_spot * self.menu_spread)))
#
#         return text_print_list
#
#     def generate_image_print(self):
#         image_print_list = []
#         return image_print_list
#
#     def calculate_overlay_dimensions(self):
#         pass
#
#     def update_menu_items_list(self):
#         pass
#
#
# class MenuStatic(Menu):
#     NAME = "Menu_Static"
#
#     def __init__(self, gc_input):
#         super().__init__(gc_input)
#         self.menu_type = "static"
#
#     @property
#     def size(self):
#         return len(self.menu_item_list)
#
#     def update_menu_items_list(self):
#         pass
#
#     def generate_image_print(self):
#         image_print_list = []
#         return image_print_list
#
#
# class StatsMenu(MenuStatic):
#     NAME = "stats_menu"
#
#     def __init__(self, gc_input):
#         super().__init__(gc_input)
#         self.gc_input = gc_input
#         self.offset_x = 10
#         self.offset_y = 10
#         self.name = self.NAME
#         self.menu_item_list = []
#         self.y_spacing = 0
#         self.menu_type = "static"
#         self.menu_header = None
#
#         self.overlay_size_x = 36
#         self.overlay_size_Y = 26
#         self.fill_out_menu_info("right", "top")
#         self.update_menu_items_list()
#
#     def update_menu_items_list(self):
#         stat_dict = self.gc_input.get_stat_items()
#         self.menu_item_list = [("Coins: ", stat_dict["Coins"]), ("Day: ", stat_dict["day"]), ("Time: ", stat_dict["time"]), ("Seeds:", stat_dict["seeds"]), ("Select: ", stat_dict["selected_tool"])]
#
#     def get_menu_items_to_print(self):
#         printable_item_list = []
#
#         for option in range(self.size):
#             item = self.menu_item_list[option][0]
#             available_spaces = 16
#             item_word_length = len(item)
#             quantity = self.menu_item_list[option][1]
#             quantity_word_length = len(quantity)
#             total_length = item_word_length + quantity_word_length
#             number_of_spaces = available_spaces - total_length
#             spaces_str = ""
#             for x in range(number_of_spaces):
#                 spaces_str = spaces_str + " "
#             final_item = item + spaces_str + quantity
#             printable_item_list.append(final_item)
#
#         return printable_item_list
#
#
# class GameActionDialogue(MenuStatic):
#     NAME = "game_action_dialogue_menu"
#
#     def __init__(self, gc_input):
#         super().__init__(gc_input)
#         self.gc_input = gc_input
#         self.offset_x = 10
#         self.offset_y = 10
#         self.name = self.NAME
#         self.menu_item_list = ["This is the game dialouge box!"]
#         self.cursor_at = 0
#         self.y_spacing = 0
#         self.menu_type = "static"
#         self.menu_header = None
#
#         self.overlay_size_x = 70
#         self.overlay_size_Y = 21
#         self.fill_out_menu_info("right", "bottom")
#
#     @property
#     def size(self):
#         return len(self.menu_item_list)
#
#     def show_dialogue(self, phrase):
#         if len(self.menu_item_list) >= 4:
#             del self.menu_item_list[0]
#         self.menu_item_list.append(phrase)
#
#     def generate_image_print(self):
#         image_print_list = []
#         return image_print_list
#
#
# class MenuTemporary(Menu):
#     NAME = "Menu_Temporary"
#
#     def __init__(self, gc_input):
#         super().__init__(gc_input)
#         self.menu_item_list = []
#         self.menu_photo_list = []
#         self.cursor = "-"
#         self.cursor_at = 0
#         self.menu_type = Types.BASE
#
#     @property
#     def size(self):
#         return len(self.menu_item_list)
#
#     # Same for most menus
#     def cursor_down(self):
#         if self.cursor_at == len(self.menu_item_list) -1:
#             self.cursor_at = 0
#         else:
#             self.cursor_at += 1
#
#     def cursor_up(self):
#         if self.cursor_at == 0:
#             self.cursor_at = len(self.menu_item_list) -1
#         else:
#             self.cursor_at -= 1
#
#     def cursor_left(self):
#         pass
#
#     def cursor_right(self):
#         pass
#
#     def reset_cursor(self):
#         self.cursor_at = 0
#
#     def choose_option(self):
#         self.do_option()
#
#     def do_option(self):
#         menu_selection = self.get_current_menu_item()
#
#         if menu_selection == "Bag":
#             pass
#
#         elif menu_selection == "Key Items":
#             pass
#         elif menu_selection == "Chore List":
#             pass
#
#         elif menu_selection == "Profile":
#             pass
#
#         elif menu_selection == "Map":
#             pass
#
#         elif menu_selection == "Options":
#             pass
#
#         elif menu_selection == "Vibes":
#             pass
#
#         elif menu_selection == "Outfits":
#             pass
#
#         elif menu_selection == "Save":
#             pass
#
#         elif menu_selection == "Exit":
#             self.gc_input.menu_manager.exit_all_menus()
#
#         else:
#             self.gc_input.menu_manager.exit_all_menus()
#
#     def get_current_menu_item(self):
#         menu_selection = self.menu_item_list[self.cursor_at]
#         return menu_selection
#
#     def update_menu_items_list(self):
#         pass
#
#     def get_menu_items_to_print(self):
#         return self.menu_item_list
#
#     def generate_image_print(self):
#         image_print_list = []
#         return image_print_list
#
#
# # class StartMenu(MenuTemporary):
# #     NAME = "start_menu"
# #
# #     def __init__(self, gc_input):
# #         super().__init__(gc_input)
# #         self.menu_item_list = ["Bag", "Outfits", "Map", "Chore List", "Profile", "Save", "Options", "Vibes"]
# #         self.menu_item_list.append("Exit")
# #         self.overlay_size_x = 35
# #         self.overlay_size_Y = 50
# #         self.fill_out_menu_info("right", "center")
# #
# #     # Same for most menus
# #     def cursor_down(self):
# #         if self.cursor_at == len(self.menu_item_list) -1:
# #             self.cursor_at = 0
# #         else:
# #             self.cursor_at += 1
# #
# #     def cursor_up(self):
# #         if self.cursor_at == 0:
# #             self.cursor_at = len(self.menu_item_list) -1
# #         else:
# #             self.cursor_at -= 1
# #
# #     def cursor_left(self):
# #         pass
# #
# #     def cursor_right(self):
# #         pass
# #
# #     def reset_cursor(self):
# #         self.cursor_at = 0
# #
# #     def choose_option(self):
# #         self.do_option()
# #
# #     def do_option(self):
# #         menu_selection = self.get_current_menu_item()
# #
# #         if menu_selection == "Bag":
# #             self.gc_input.menu_manager.set_menu(InventoryMenu.NAME)
# #
# #         elif menu_selection == "Key Items":
# #             pass
# #
# #         elif menu_selection == "Chore List":
# #             pass
# #
# #         elif menu_selection == "Profile":
# #             pass
# #
# #         elif menu_selection == "Map":
# #             pass
# #
# #         elif menu_selection == "Options":
# #             pass
# #
# #         elif menu_selection == "Vibes":
# #             pass
# #
# #         elif menu_selection == "Outfits":
# #             pass
# #
# #         elif menu_selection == "Save":
# #             pass
# #
# #         elif menu_selection == "Exit":
# #             self.gc_input.menu_manager.exit_all_menus()
# #
# #         else:
# #             self.gc_input.menu_manager.exit_all_menus()
# #
# #     def get_current_menu_item(self):
# #         menu_selection = self.menu_item_list[self.cursor_at]
# #         return menu_selection
# #
# #     def update_menu_items_list(self):
# #         pass
# #
# #
# # class InventoryMenu(MenuTemporary):
# #     NAME = "inventory_menu"
# #
# #     def __init__(self, gc_input):
# #         super().__init__(gc_input)
# #         self.menu_header = "<   ITEMS   >"
# #         self.max_length = 14
# #         self.currently_displayed_items = []
# #         self.list_shifts = 0
# #         self.overlay_size_x = 35
# #         self.overlay_size_Y = 80
# #         self.fill_out_menu_info("right", "center")
# #
# #     def get_menu_items_to_print(self):
# #         menu_length_calc = 0
# #         if self.size >= self.max_length:
# #             menu_length_calc = self.max_length
# #         elif self.size < self.max_length:
# #             menu_length_calc = self.size
# #
# #         printable_item_list = []
# #
# #         for option in range(menu_length_calc):
# #             item = self.currently_displayed_items[option]
# #             if item == "Exit":
# #                 printable_item_list.append(self.currently_displayed_items[option])
# #
# #             else:
# #                 available_spaces = 13
# #                 item_word_length = len(item)
# #                 quantity = str(self.gc_input.menu_manager.get_item_quantity(item))
# #                 quantity_word_length = len(quantity)
# #                 total_length = item_word_length + quantity_word_length
# #
# #                 number_of_spaces = available_spaces - total_length
# #                 spaces_str = ""
# #                 for x in range(number_of_spaces):
# #                     spaces_str = spaces_str + " "
# #                 final_item = item + spaces_str + "x" + quantity
# #                 printable_item_list.append(final_item)
# #
# #         return printable_item_list
# #
# #     def update_menu_items_list(self):
# #         keys_list = []
# #         for item in self.gc_input.game_state.current_inventory:
# #             keys_list.append(item)
# #         self.menu_item_list = keys_list
# #         self.menu_item_list.append("Exit")
# #         self.update_currently_displayed()
# #
# #     def update_currently_displayed(self):
# #         self.currently_displayed_items = []
# #         if self.size <= self.max_length:
# #             for item in range(self.size):
# #                 self.currently_displayed_items.append(self.menu_item_list[item + self.list_shifts])
# #         else:
# #             for item in range(self.max_length):
# #                 self.currently_displayed_items.append(self.menu_item_list[item + self.list_shifts])
# #
# #     def choose_option(self):
# #         chosen_item_name = self.get_current_menu_item()
# #         if chosen_item_name == "Exit":
# #             self.gc_input.menu_manager.exit_all_menus()
# #         else:
# #             self.gc_input.menu_manager.set_sub_menu(UseMenu.NAME, self)
# #
# #     def do_option(self, choice=None):
# #         menu_selection = choice
# #         print(menu_selection)
# #         chosen_item_name = self.get_current_menu_item()
# #
# #         if menu_selection == "Use":
# #             print("used the " + chosen_item_name)
# #             chosen_item = self.gc_input.inventory_manager.item_data_list[chosen_item_name]
# #             self.gc_input.inventory_manager.use_item(chosen_item, 1)
# #             self.update_menu_items_list()
# #
# #         elif menu_selection == "Toss":
# #             self.gc_input.menu_manager.exit_all_menus()
# #
# #         elif menu_selection == "Exit":
# #             self.gc_input.menu_manager.exit_all_menus()
# #
# #     def cursor_left(self):
# #         self.gc_input.menu_manager.set_menu(KeyInventoryMenu.NAME)
# #
# #     def cursor_right(self):
# #         self.gc_input.menu_manager.set_menu(KeyInventoryMenu.NAME)
# #
# #     def cursor_down(self):
# #         if self.size > 1:
# #             if (self.cursor_at + self.list_shifts) < self.size - 1:
# #                 if self.size > self.max_length:
# #                     if self.cursor_at == self.max_length - 1:
# #                         self.list_shifts += 1
# #                         self.update_currently_displayed()
# #                     elif self.cursor_at < self.max_length - 1:
# #                         self.cursor_at += 1
# #                     else:
# #                         pass
# #
# #                 elif self.max_length >= self.size > self.cursor_at:
# #                     self.cursor_at += 1
# #
# #     def cursor_up(self):
# #         if (self.cursor_at + self.list_shifts) > 0:
# #             if self.cursor_at == 0 and self.list_shifts > 0:
# #                 self.list_shifts -= 1
# #                 self.update_currently_displayed()
# #             elif self.cursor_at > 0:
# #                 self.cursor_at -= 1
# #             else:
# #                 pass
# #
# #     def get_current_menu_item(self):
# #         menu_selection = self.currently_displayed_items[self.cursor_at]
# #         return menu_selection
# #
# #     def reset_cursor(self):
# #         self.cursor_at = 0
# #         self.list_shifts = 0
# #
# #     def generate_image_print(self):
# #         image_print_list = []
# #         current_item = self.get_current_menu_item()
# #         if current_item != "Exit":
# #             item_info = self.gc_input.get_item_info(current_item)
# #             image = item_info[0]
# #             image_size_x = item_info[1]
# #             image_size_y = item_info[2]
# #             image_print_list = [PhotoPrint(image, self.x - image_size_x*1.5, self.y + 250)]
# #         return image_print_list
#
#
# class KeyInventoryMenu(MenuTemporary):
#     NAME = "key_inventory_menu"
#
#     def __init__(self, gc_input):
#         super().__init__(gc_input)
#         self.menu_header = "< KEY ITEMS >"
#         self.max_length = 14
#         self.currently_displayed_items = []
#         self.list_shifts = 0
#         self.overlay_size_x = 35
#         self.overlay_size_Y = 80
#         self.fill_out_menu_info("right", "center")
#
#     def get_menu_items_to_print(self):
#         menu_length_calc = 0
#         if self.size >= self.max_length:
#             menu_length_calc = self.max_length
#         elif self.size < self.max_length:
#             menu_length_calc = self.size
#
#         printable_item_list = []
#
#         for option in range(menu_length_calc):
#             printable_item_list.append(self.currently_displayed_items[option])
#
#         return printable_item_list
#
#     def update_menu_items_list(self):
#         keys_list = []
#         for item in self.gc_input.game_state.current_key_inventory:
#             keys_list.append(item)
#         self.menu_item_list = keys_list
#         self.menu_item_list.append("Exit")
#         self.update_currently_displayed()
#
#     def update_currently_displayed(self):
#         self.currently_displayed_items = []
#         if self.size <= self.max_length:
#             for item in range(self.size):
#                 self.currently_displayed_items.append(self.menu_item_list[item + self.list_shifts])
#         else:
#             for item in range(self.max_length):
#                 self.currently_displayed_items.append(self.menu_item_list[item + self.list_shifts])
#
#     def choose_option(self):
#         chosen_item_name = self.get_current_menu_item()
#         if chosen_item_name == "Exit":
#             self.gc_input.menu_manager.exit_all_menus()
#         else:
#             chosen_item = self.gc_input.inventory_manager.key_item_data_list[chosen_item_name]
#             self.gc_input.inventory_manager.use_key_item(chosen_item)
#             self.gc_input.menu_manager.exit_all_menus()
#
#     def do_option(self, choice=None):
#         menu_selection = choice
#
#         if menu_selection == "Use":
#             pass
#
#         elif menu_selection == "Toss":
#             pass
#
#         elif menu_selection == "Exit":
#             self.gc_input.menu_manager.exit_all_menus()
#
#     def cursor_left(self):
#         self.gc_input.menu_manager.set_menu(InventoryMenu.NAME)
#
#     def cursor_right(self):
#         self.gc_input.menu_manager.set_menu(InventoryMenu.NAME)
#
#     def cursor_down(self):
#         if self.size > 1:
#             if (self.cursor_at + self.list_shifts) < self.size - 1:
#                 if self.size > self.max_length:
#                     if self.cursor_at == self.max_length - 1:
#                         self.list_shifts += 1
#                         self.update_currently_displayed()
#                     elif self.cursor_at < self.max_length - 1:
#                         self.cursor_at += 1
#                     else:
#                         pass
#
#                 elif self.max_length >= self.size > self.cursor_at:
#                     self.cursor_at += 1
#
#     def cursor_up(self):
#         if (self.cursor_at + self.list_shifts) > 0:
#             if self.cursor_at == 0 and self.list_shifts > 0:
#                 self.list_shifts -= 1
#                 self.update_currently_displayed()
#             elif self.cursor_at > 0:
#                 self.cursor_at -= 1
#             else:
#                 pass
#
#     def get_current_menu_item(self):
#         menu_selection = self.currently_displayed_items[self.cursor_at]
#         return menu_selection
#
#     def reset_cursor(self):
#         self.cursor_at = 0
#         self.list_shifts = 0
#
#     def generate_image_print(self):
#         image_print_list = []
#         current_item = self.get_current_menu_item()
#         if current_item != "Exit":
#             item_info = self.gc_input.get_key_item_info(current_item)
#             image = item_info[0]
#             image_size_x = item_info[1]
#             image_size_y = item_info[2]
#             image_print_list = [PhotoPrint(image, self.x - image_size_x*1.5, self.y + 250)]
#         return image_print_list
#
#
# class ConversationOptionsMenu(MenuTemporary):
#     NAME = "conversation_options_menu"
#
#     def __init__(self, gc_input):
#         super().__init__(gc_input)
#         self.offset_x = 150
#         self.offset_y = 25
#         self.menu_header = "Default"
#         self.menu_item_list = ["Talk", "Give Gift"]
#         self.menu_item_list.append("Exit")
#
#         self.talking_to = None
#
#         self.overlay_size_x = 95
#         self.overlay_size_Y = 27
#         self.fill_out_menu_info("center", "bottom")
#         self.y_spacing = 35
#
#     def update_menu_items_list(self, speaker_name, friendship_level, face_image):
#         friendship_counter = "           "
#         if friendship_level == 0:
#             friendship_counter = "           "
#         elif 5 >= friendship_level >= 1:
#             friendship_counter = "<3         "
#         elif 10 >= friendship_level >= 6:
#             friendship_counter = "<3 <3      "
#         elif 15 >= friendship_level >= 11:
#             friendship_counter = "<3 <3 <3   "
#         elif friendship_level >= 16:
#             friendship_counter = "<3 <3 <3 <3"
#
#         self.menu_photo_list = [face_image]
#         self.menu_header = speaker_name + "   " + friendship_counter
#         self.talking_to = speaker_name
#
#     def do_option(self):
#         menu_selection = self.get_current_menu_item()
#         if menu_selection == "Talk":
#             npc_talking_to_ghost = self.gc_input.get_npc_ghost(self.talking_to)
#             npc_talking_to_avatar = self.gc_input.get_npc_avatar(self.talking_to)
#             self.gc_input.menu_manager.set_dialogue_menu("Something strange is going on around here, have you heard about the children disapearing? Their parents couldn't even remember their names...", npc_talking_to_ghost.name, 11, npc_talking_to_avatar.face_image)
#
#         elif menu_selection == "Give Gift":
#             pass
#
#         elif menu_selection == "Exit":
#             pass
#
#     def generate_image_print(self):
#         image_print_list = []
#         for item in self.menu_photo_list:
#             image_print_list = [PhotoPrint(item, 10, 5)]
#         return image_print_list
#
#
# class CharacterDialogue(MenuTemporary):
#     NAME = "character_dialogue"
#
#     def __init__(self, gc_input):
#         super().__init__(gc_input)
#         self.font_size = 10
#         self.offset_x = 150
#         self.offset_y = 25
#         self.menu_header = "Default"
#
#         self.cursor = None
#
#         self.currently_displayed_items = []
#         self.current_phrase = []
#         self.speaking_queue = []
#         self.set_current_phrase()
#
#         self.overlay_size_x = 95
#         self.overlay_size_Y = 27
#         self.fill_out_menu_info("center", "bottom")
#         self.y_spacing = 35
#
#     def update_menu_items_list(self, phrases, speaker_name, friendship_level, face_image):
#         friendship_counter = "           "
#         if friendship_level == 0:
#             friendship_counter = "           "
#         elif 5 >= friendship_level >= 1:
#             friendship_counter = "<3         "
#         elif 10 >= friendship_level >= 6:
#             friendship_counter = "<3 <3      "
#         elif 15 >= friendship_level >= 11:
#             friendship_counter = "<3 <3 <3   "
#         elif friendship_level >= 16:
#             friendship_counter = "<3 <3 <3 <3"
#
#         self.menu_photo_list = [face_image]
#         self.menu_header = speaker_name + "   " + friendship_counter
#         self.menu_item_list = [phrases]
#         self.set_current_phrase()
#         self.set_speaking_queue()
#
#     def set_current_phrase(self):
#         for item in range(len(self.menu_item_list)):
#             self.current_phrase = textwrap.wrap(self.menu_item_list[item], width=30)
#
#     def set_speaking_queue(self):
#         phrase_counter = 0
#         self.speaking_queue = []
#
#         if len(self.current_phrase) > 2:
#             for line in range(3):
#                 self.speaking_queue.append(self.current_phrase[0])
#                 self.current_phrase.pop(0)
#
#         elif (len(self.current_phrase) <= 2) and (len(self.current_phrase) > 0):
#             for line in range(len(self.current_phrase)):
#                 self.speaking_queue.append(self.current_phrase[0])
#                 self.current_phrase.pop(0)
#
#         elif len(self.current_phrase) == 0:
#             self.gc_input.menu_manager.exit_all_menus()
#
#     def get_menu_items_to_print(self):
#         return self.speaking_queue
#
#     def do_option(self):
#         self.set_speaking_queue()
#
#     def generate_image_print(self):
#         image_print_list = []
#         for item in self.menu_photo_list:
#             image_print_list = [PhotoPrint(item, 10, 5)]
#         return image_print_list
#
#
# class SubMenu(MenuTemporary):
#     NAME = "sub_menu"
#
#     def __init__(self, gc_input):
#         super().__init__(gc_input)
#         self.menu_item_list = ["Yes", "No"]
#         self.overlay_size_x = 15
#         self.overlay_size_Y = 15
#         self.fill_out_menu_info("right", "center")
#         self.master_menu = None
#
#     def update_menu_items_list(self, master_menu):
#         self.master_menu = master_menu
#         self.x = master_menu.x - self.overlay_size_x * 5 - 10
#         self.y = master_menu.y
#
#     def get_current_menu_item(self):
#         menu_selection = self.menu_item_list[self.cursor_at]
#         return menu_selection
#
#     def choose_option(self):
#         self.do_option()
#
#
# class YesnoMenu(SubMenu):
#     NAME = "yes_no_menu"
#
#     def __init__(self, gc_input):
#         super().__init__(gc_input)
#         self.menu_item_list = ["Yes", "No"]
#         self.cursor = "-"
#         self.overlay_size_x = 15
#         self.overlay_size_Y = 15
#         self.fill_out_menu_info("right", "center")
#         self.menu_type = "sub"
#
#     def do_option(self):
#         menu_selection = self.get_current_menu_item()
#         self.gc_input.menu_manager.exit_menu(self.name)
#         self.master_menu.do_option(option=menu_selection)
#
#
# class UseMenu(SubMenu):
#     NAME = "use_menu"
#
#     def __init__(self, gc_input):
#         super().__init__(gc_input)
#         self.menu_item_list = ["Use", "Toss"]
#         self.menu_item_list.append("Exit")
#         self.cursor = "-"
#         self.overlay_size_x = 16
#         self.overlay_size_Y = 20
#         self.fill_out_menu_info("right", "center")
#         self.menu_type = "sub"
#
#     def choose_option(self):
#         chosen_item_name = self.get_current_menu_item()
#         if chosen_item_name == "Exit":
#             self.gc_input.menu_manager.exit_all_menus()
#         else:
#             self.gc_input.menu_manager.set_sub_menu(YesnoMenu.NAME, self)
#
#     def do_option(self, option=None):
#         menu_selection = self.get_current_menu_item()
#         if option == "Yes":
#             self.gc_input.menu_manager.exit_menu(self.name)
#             self.master_menu.do_option(choice=menu_selection)
#         elif option == "No":
#             self.gc_input.menu_manager.exit_menu(self.name)
#
