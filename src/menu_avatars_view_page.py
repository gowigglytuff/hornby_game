import copy
import textwrap

import pygame

from definitions import GameSettings, Types, Mundane
from game_view import GameView
from spritesheet import Spritesheet


class DisplayText(object):
    def __init__(self, text):
        self.text = text


class DisplayPicture(object):
    def __init__(self, img):
        self.img = img


class TextDisplay(object):
    def __init__(self, text, x, y):
        self.text = text
        self.x = x
        self.y = y


class ImageDisplay(object):
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y


class BaseMenuAvatar(object):
    NAME = "Base_Menu_Avatar"

    def __init__(self, gc, name):
        self.menu_display_details = {}
        self.gc = gc
        self.x = 0
        self.y = 0
        self.offset_x = 15
        self.offset_y = 15
        self.cursor_offset_x = 5
        self.cursor_offset_y = 0
        self.cursor_at = 0
        self.y_space_size = 15
        self.menu_spread_y = self.y_space_size + GameSettings.FONT_SIZE
        self.menu_spread_x = 0
        self.name = name
        self.overlay_body_x = 0
        self.overlay_body_Y = 0
        self.has_header = False
        self.overlay_header_x = 0
        self.overlay_header_y = 0
        self.header_spacing = 0
        self.base_segment_size = 0
        self.spritesheet_height = 0
        self.spritesheet_width = 0
        self.overlay_image = None
        self.shifts = 0
        self.menu_items_list = []
        self.currently_displayed_items = []
        self.final_menu_text = []
        self.final_menu_images = []

        self.max_display_items = 14
        self.menu_display_details = {"default_width": 100, "default_height": 100, "align_x": "center", "align_y": "center", "coordinates": [0, 0]}
        self.fill_out_menu_info()
        self.button_list = []
        self.main_font = pygame.font.Font("assets/fonts/PressStart.ttf", GameSettings.FONT_SIZE)

    def add_button_to_list(self, button_avatar):
        self.button_list.append(button_avatar)

    def fill_out_menu_info(self):
        self.overlay_body_x = self.menu_display_details["default_width"]
        self.overlay_body_Y = self.menu_display_details["default_height"]

        if self.has_header:
            header_calc = self.set_header_y()
            self.overlay_header_x = header_calc[0]
            self.overlay_header_y = header_calc[1]
            self.header_spacing = header_calc[2]

        self.base_segment_size = self.overlay_body_x * GameSettings.MENUSEGMENTSIZE
        self.spritesheet_height = (self.overlay_body_Y * GameSettings.MENUSEGMENTSIZE) + (self.overlay_header_y * GameSettings.MENUSEGMENTSIZE)
        self.spritesheet_width = self.overlay_body_x * GameSettings.MENUSEGMENTSIZE

        if self.has_header:
            self.overlay_image = self.gc.game_view.build_overlay_image("special_menu" + "_overlay", self.overlay_body_x, self.overlay_body_Y, header=self.has_header)
        else:
            self.overlay_image = self.gc.game_view.build_overlay_image("special_menu" + "_overlay", self.overlay_body_x, self.overlay_body_Y)

        self.set_display_coordinates()

    def set_header_y(self):
        font_size = GameSettings.FONT_SIZE
        segment_size = GameSettings.MENUSEGMENTSIZE
        segment_proportion = font_size/segment_size

        header_number_of_items = 1
        header_items_height = header_number_of_items * segment_proportion
        header_border_height = int(self.offset_y / segment_size) * 2
        header_height = header_items_height + header_border_height
        header_width = copy.copy(self.overlay_body_x)
        header_spacing = header_height * segment_size - 5

        return header_width, header_height, header_spacing

    def add_header_spaces(self, header):
        header_text_length = len(header) * 2
        max_width = self.overlay_body_x
        offset = (self.offset_x / GameSettings.MENUSEGMENTSIZE)
        width_less_offsets = max_width / 2 - offset
        header_spaces = int((width_less_offsets - header_text_length / 2) / 2)
        for space in range(header_spaces):
            header = " " + header
        return header

    def get_cursor_at(self, cursor_at):
        cursor_y = 0
        if cursor_at[1] + 1 < self.max_display_items:
            cursor_y = cursor_at[1]
        else:
            cursor_y = self.max_display_items-1

        cursor_loc_x = (cursor_at[0] * self.menu_spread_x) + self.cursor_offset_x
        cursor_loc_y = (cursor_y * self.menu_spread_y) + self.header_spacing + self.offset_y + self.cursor_offset_y

        return cursor_loc_x, cursor_loc_y

    def set_display_coordinates(self):
        x_instruction = self.menu_display_details["align_x"]
        y_instruction = self.menu_display_details["align_y"]
        x = 0
        y = 0

        if x_instruction == "center":
            x = GameSettings.RESOLUTION[0] / 2 - self.spritesheet_width / 2
        elif x_instruction == "left":
            x = 0 + GameSettings.RESOLUTION[0] / GameSettings.MENUEDGE
        elif x_instruction == "right":
            x = GameSettings.RESOLUTION[0] - self.spritesheet_width - GameSettings.RESOLUTION[0] / GameSettings.MENUEDGE
        else:
            x = x_instruction

        if y_instruction == "center":
            y = GameSettings.RESOLUTION[1] / 2 - self.spritesheet_height / 2
        elif y_instruction == "1/4":
            y = GameSettings.RESOLUTION[1] / 4 - self.spritesheet_height / 4
        elif y_instruction == "top":
            y = 0 + GameSettings.RESOLUTION[1] / GameSettings.MENUEDGE
        elif y_instruction == "3/4":
            y = GameSettings.RESOLUTION[1] / 4 * 3 - self.spritesheet_height / 4 * 3
        elif y_instruction == "bottom":
            y = GameSettings.RESOLUTION[1] - self.spritesheet_height - GameSettings.RESOLUTION[1] / GameSettings.MENUEDGE
        else:
            y = y_instruction

        self.menu_display_details["coordinates"][0] = x
        self.menu_display_details["coordinates"][1] = y

    def return_currently_displayed(self, full_items_list, cursor_at):
        currently_displayed_items = []
        size = len(full_items_list)
        shifts = cursor_at[1] + 1 - self.max_display_items
        if shifts < 0:
            shifts = 0

        if size <= self.max_display_items:
            for item in range(size):
                currently_displayed_items.append(full_items_list[item])
        else:
            for item in range(self.max_display_items):
                currently_displayed_items.append(full_items_list[item + shifts])
        return currently_displayed_items

    def get_menu_text_drawing_instructions(self, menu_info):
        menu_info = menu_info
        text_display_list = menu_info.text_display_list
        header = menu_info.header
        cursor_image = menu_info.cursor_image
        cursor_at = menu_info.cursor_at

        final_menu_text = []

        if header:
            self.add_header_spaces(header)
            final_menu_text.append(TextDisplay(header, self.offset_x, self.offset_y))

        if cursor_image:
            cursor_loc = self.get_cursor_at(cursor_at)
            final_menu_text.append(TextDisplay(cursor_image, cursor_loc[0], cursor_loc[1]))

        currently_visible_items = self.return_currently_displayed(text_display_list, cursor_at)

        for position_y in range(len(currently_visible_items)):
            loc_x = self.menu_spread_x + self.offset_x
            loc_y = (position_y * self.menu_spread_y) + self.offset_y + self.header_spacing
            final_menu_text.append(TextDisplay(text_display_list[position_y], loc_x, loc_y))

        self.final_menu_text = final_menu_text
        return final_menu_text

    def get_menu_image_drawing_instructions(self, menu_info):
        final_menu_images = []
        self.final_menu_images = final_menu_images
        return None


class SubMenuAvatar(BaseMenuAvatar):
    NAME = "sub_menu_avatar"

    def __init__(self, gc, name):
        super().__init__(gc, name)

    def update_for_display(self, information_from_ghost, master_menu_display_details):
        menu_x, menu_y = self.determine_menu_size(information_from_ghost.text_display_list)
        self.menu_display_details["default_width"] = menu_x
        self.menu_display_details["default_height"] = menu_y
        spritesheet_width = menu_x * GameSettings.MENUSEGMENTSIZE
        self.menu_display_details["align_x"] = master_menu_display_details["coordinates"][0] - spritesheet_width - 5
        self.menu_display_details["align_y"] = master_menu_display_details["coordinates"][1]
        self.menu_display_details["coordinates"][0] = master_menu_display_details["coordinates"][0] - spritesheet_width - 5
        self.menu_display_details["coordinates"][1] = master_menu_display_details["coordinates"][1]

        self.fill_out_menu_info()

    def determine_menu_size(self, text_display_list):
        longest = max(text_display_list, key=len)
        count = len(text_display_list)
        x_size = (len(longest) * GameSettings.FONT_SIZE + (self.offset_x * 2))/GameSettings.MENUSEGMENTSIZE
        y_size = ((count * GameSettings.FONT_SIZE) + ((count-1) * self.menu_spread_y) + (self.offset_y))/GameSettings.MENUSEGMENTSIZE
        return x_size, y_size


class ListMenuAvatar(BaseMenuAvatar):
    NAME = "list_menu_avatar"

    def __init__(self, gc, name):
        super().__init__(gc, name)

        self.menu_display_details = {"default_width": 25, "default_height": 53, "align_x": "right", "align_y": "center", "coordinates": [0, 0]}
        self.fill_out_menu_info()

    def get_menu_text_drawing_instructions(self, menu_info):
        menu_info = menu_info
        text_display_list = menu_info.text_display_list
        header = menu_info.header
        cursor_image = menu_info.cursor_image
        cursor_at = menu_info.cursor_at

        final_menu_text = []

        if header:
            self.add_header_spaces(header)
            final_menu_text.append(TextDisplay(header, self.offset_x, self.offset_y))

        if cursor_image:
            cursor_loc = self.get_cursor_at(cursor_at)
            final_menu_text.append(TextDisplay(cursor_image, cursor_loc[0], cursor_loc[1]))

        currently_visible_items = self.return_currently_displayed(text_display_list, cursor_at)

        for position_y in range(len(currently_visible_items)):
            loc_x = self.menu_spread_x + self.offset_x
            loc_y = (position_y * self.menu_spread_y) + self.offset_y + self.header_spacing
            item = currently_visible_items[position_y]
            final_menu_text.append(TextDisplay(item, loc_x, loc_y))

        self.final_menu_text = final_menu_text

        return final_menu_text


class BasketMenuAvatar(BaseMenuAvatar):
    NAME = "basket_menu_avatar"

    def __init__(self, gc, name):
        super().__init__(gc, name)

        self.menu_display_details = {"default_width": 40, "default_height": 18, "align_x": "center", "align_y": "3/4", "coordinates": [0, 0]}
        self.fill_out_menu_info()


class ChattingMenuAvatar(BaseMenuAvatar):
    NAME = "chatting_menu_avatar"

    def __init__(self, gc, name):
        super().__init__(gc, name)
        self.offset_x = 130
        self.offset_y = 20
        self.title_offset_y = 20
        self.image_offset_x = 10
        self.image_offset_y = 10
        self.cursor_offset_x = self.offset_x - 10
        self.cursor_offset_y = self.offset_y + 7

        self.menu_display_details = {"default_width": 70, "default_height": 25, "align_x": "center", "align_y": "3/4", "coordinates": [0, 0]}
        self.fill_out_menu_info()

    def get_menu_text_drawing_instructions(self, menu_info):
        menu_info = menu_info
        header = menu_info.header
        text_display_list = menu_info.text_display_list
        cursor_image = menu_info.cursor_image
        cursor_at = menu_info.cursor_at
        speaker_name = menu_info.menu_specific_details_dict["speaker_name"]
        friendship_level = menu_info.menu_specific_details_dict["friendship_level"]
        actor_type = menu_info.menu_specific_details_dict["actor_type"]

        final_menu_text = []

        if header:
            self.add_header_spaces(header)
            final_menu_text.append(TextDisplay(header, self.offset_x, self.offset_y))

        if cursor_image:
            cursor_loc = self.get_cursor_at(cursor_at)
            final_menu_text.append(TextDisplay(cursor_image, cursor_loc[0], cursor_loc[1]))

        currently_visible_items = self.return_currently_displayed(text_display_list, cursor_at)

        for position_y in range(len(currently_visible_items)):
            loc_x = self.menu_spread_x + self.offset_x
            loc_y = ((position_y + 1) * self.menu_spread_y) + self.offset_y + self.header_spacing
            item = currently_visible_items[position_y]
            final_menu_text.append(TextDisplay(item, loc_x, loc_y))

        # name and Friendship
        text = speaker_name

        if actor_type == Types.FRIEND:
            text = speaker_name + " [" + str(friendship_level) + "]"

        loc_x = self.menu_spread_x + self.offset_x
        loc_y = self.offset_y
        text = TextDisplay(text, loc_x, loc_y)
        final_menu_text.append(text)

        self.final_menu_text = final_menu_text
        return final_menu_text

    def get_menu_image_drawing_instructions(self, menu_info):
        face = menu_info.menu_specific_details_dict["face_image"]

        final_menu_images = []

        loc_x = self.image_offset_x
        loc_y = self.image_offset_y
        image = ImageDisplay(face, loc_x, loc_y)
        final_menu_images.append(image)

        self.final_menu_images = final_menu_images
        return final_menu_images


class GalleryMenuAvatar(BaseMenuAvatar):
    NAME = "gallery_menu_avatar"

    def __init__(self, gc, name):
        super().__init__(gc, name)
        self.offset_x = 130
        self.offset_y = 20
        self.title_offset_y = 20
        self.image_offset_x = 10
        self.image_offset_y = 10
        self.cursor_offset_x = self.offset_x - 10
        self.cursor_offset_y = self.offset_y + 7

        self.menu_display_details = {"default_width": 30, "default_height": 20, "align_x": "center", "align_y": "center", "coordinates": [0, 0]}
        self.fill_out_menu_info()

    def get_menu_text_drawing_instructions(self, menu_info):
        menu_info = menu_info
        text_display_list = menu_info.text_display_list
        item_name = menu_info.menu_specific_details_dict["item_name"]

        final_menu_text = []

        # item_names
        name_text = Mundane.center_text_x(self.overlay_body_x, 0, item_name)
        final_menu_text.append(TextDisplay(name_text[0], name_text[1], 75))

        # Header
        header_text = Mundane.center_text_x(self.overlay_body_x, 0, menu_info.menu_specific_details_dict["menu_title"])
        final_menu_text.append(TextDisplay(header_text[0], header_text[1], 10))

        if not menu_info.menu_specific_details_dict["is_first_item"]:
            # left arrow
            text = TextDisplay("<", 10, 45)
            final_menu_text.append(text)

        if not menu_info.menu_specific_details_dict["is_last_item"]:
            # left arrow
            text = TextDisplay(">", 130, 45)
            final_menu_text.append(text)

        self.final_menu_text = final_menu_text

        return final_menu_text

    def get_menu_image_drawing_instructions(self, menu_info):
        item_image = menu_info.menu_specific_details_dict["item_image"]
        final_menu_images = []

        loc_y = 20
        image = ImageDisplay(item_image, Mundane.center_image_x(self.overlay_body_x, 0, item_image), loc_y)
        final_menu_images.append(image)

        self.final_menu_images = final_menu_images
        return final_menu_images


class CoupledListMenuAvatar(BaseMenuAvatar):
    def __init__(self, gc, name):
        super().__init__(gc, name)

        self.menu_display_details = {"default_width": 28, "default_height": 85, "align_x": "right", "align_y": "center", "coordinates": [0, 0]}
        self.symbol = "x"
        self.fill_out_menu_info()

    def combine_item_with_detail(self, item, detail, spaces_available):
        final_item = item
        if detail == "0":
            final_item = item
        else:
            available_spaces = spaces_available
            item_word_length = len(item)
            quantity_word_length = len(detail)
            total_length = item_word_length + quantity_word_length

            number_of_spaces = available_spaces - total_length
            spaces_str = ""
            for x in range(number_of_spaces):
                spaces_str = spaces_str + " "
            final_item = item + spaces_str + self.symbol + detail
        return final_item

    def get_menu_text_drawing_instructions(self, menu_info):
        menu_info = menu_info
        text_display_list = menu_info.text_display_list
        header = menu_info.header
        cursor_image = menu_info.cursor_image
        cursor_at = menu_info.cursor_at

        final_menu_text = []

        if header:
            self.add_header_spaces(header)
            final_menu_text.append(TextDisplay(header, self.offset_x, self.offset_y))

        if cursor_image:
            cursor_loc = self.get_cursor_at(cursor_at)
            final_menu_text.append(TextDisplay(cursor_image, cursor_loc[0], cursor_loc[1]))

        fixed_text_list = []
        for item in text_display_list:
            item_adjusted = self.combine_item_with_detail(item[0], item[1], 13)
            fixed_text_list.append(item_adjusted)

        currently_visible_items = self.return_currently_displayed(fixed_text_list, cursor_at)

        for position_y in range(len(currently_visible_items)):
            loc_x = self.menu_spread_x + self.offset_x
            loc_y = (position_y * self.menu_spread_y) + self.offset_y + self.header_spacing
            item = currently_visible_items[position_y]
            final_menu_text.append(TextDisplay(item, loc_x, loc_y))

        self.final_menu_text = final_menu_text

        return final_menu_text


class SuppliesMenuAvatar(CoupledListMenuAvatar):
    def __init__(self, gc, name):
        super().__init__(gc, name)

        self.has_header = True
        self.menu_display_details = {"default_width": 33, "default_height": 73, "align_x": "right", "align_y": "center", "coordinates": [0, 0]}
        self.fill_out_menu_info()


class GiftGivingMenuAvatar(CoupledListMenuAvatar):
    def __init__(self, gc, name):
        super().__init__(gc, name)

        self.has_header = True
        self.menu_display_details = {"default_width": 33, "default_height": 73, "align_x": "right", "align_y": "center", "coordinates": [0, 0]}
        self.fill_out_menu_info()


class KeyInventoryMenuAvatar(ListMenuAvatar):
    def __init__(self, gc, name):
        super().__init__(gc, name)

        self.has_header = True
        self.menu_display_details = {"default_width": 33, "default_height": 73, "align_x": "right", "align_y": "center", "coordinates": [0, 0]}
        self.fill_out_menu_info()


class SellerMenuAvatar(CoupledListMenuAvatar):
    def __init__(self, gc, name):
        super().__init__(gc, name)

        self.has_header = True
        self.symbol = "$"
        self.menu_display_details = {"default_width": 33, "default_height": 73, "align_x": "right", "align_y": "center", "coordinates": [0, 0]}
        self.fill_out_menu_info()


class AcquireMenuAvatar(ListMenuAvatar):
    NAME = "acquire_menu_avatar"
    def __init__(self, gc, name):
        super().__init__(gc, name)

        self.has_header = True
        self.menu_display_details = {"default_width": 33, "default_height": 73, "align_x": "right", "align_y": "center", "coordinates": [0, 0]}
        self.fill_out_menu_info()


class TreasuresInventoryMenuAvatar(ListMenuAvatar):
    def __init__(self, gc, name):
        super().__init__(gc, name)

        self.has_header = True
        self.menu_display_details = {"default_width": 33, "default_height": 73, "align_x": "right", "align_y": "center", "coordinates": [0, 0]}
        self.fill_out_menu_info()


class StatMenuAvatar(ListMenuAvatar):
    NAME = "stat_menu_avatar"

    def __init__(self, gc, name):
        super().__init__(gc, name)
        self.menu_display_details = {"default_width": 80, "default_height": 8, "align_x": "center", "align_y": "top", "coordinates": [0, 0]}
        self.fill_out_menu_info()

    def get_menu_text_drawing_instructions(self, menu_info):
        menu_info = menu_info
        text_display_list = menu_info.text_display_list
        header = menu_info.header
        cursor_image = menu_info.cursor_image
        cursor_at = menu_info.cursor_at

        final_menu_text = []

        if header:
            self.add_header_spaces(header)
            final_menu_text.append(TextDisplay(header, self.offset_x, self.offset_y))

        if cursor_image:
            cursor_loc = self.get_cursor_at(cursor_at)
            final_menu_text.append(TextDisplay(cursor_image, cursor_loc[0], cursor_loc[1]))

        currently_visible_items = self.return_currently_displayed(text_display_list, cursor_at)

        last_item_x = 0
        for position_y in range(len(currently_visible_items)):
            length = len(currently_visible_items[position_y]) * GameSettings.FONT_SIZE
            loc_x = last_item_x + 15
            loc_y = self.offset_y + self.header_spacing
            final_menu_text.append(TextDisplay(text_display_list[position_y], loc_x, loc_y))
            last_item_x = loc_x + length

        self.final_menu_text = final_menu_text
        return final_menu_text


class GameModeStatMenuAvatar(ListMenuAvatar):
    NAME = "game_mode_stat_menu_avatar"

    def __init__(self, gc, name):
        super().__init__(gc, name)
        self.menu_display_details = {"default_width": 60, "default_height": 60, "align_x": "left", "align_y": "top", "coordinates": [0, 0]}
        self.fill_out_menu_info()

    def get_menu_text_drawing_instructions(self, menu_info):
        menu_info = menu_info
        text_display_list = menu_info.text_display_list
        header = menu_info.header
        cursor_image = menu_info.cursor_image
        cursor_at = menu_info.cursor_at

        final_menu_text = []

        if header:
            self.add_header_spaces(header)
            final_menu_text.append(TextDisplay(header, self.offset_x, self.offset_y))

        if cursor_image:
            cursor_loc = self.get_cursor_at(cursor_at)
            final_menu_text.append(TextDisplay(cursor_image, cursor_loc[0], cursor_loc[1]))

        currently_visible_items = self.return_currently_displayed(text_display_list, cursor_at)

        y_shift = 15
        initial = 15
        for position_y in range(len(currently_visible_items)):
            length = len(currently_visible_items[position_y]) * GameSettings.FONT_SIZE
            loc_x = 15
            loc_y = self.offset_y + self.header_spacing
            final_menu_text.append(TextDisplay(text_display_list[position_y], loc_x, loc_y + y_shift - copy.copy(initial)))
            y_shift += 20
            initial = 0

        self.final_menu_text = final_menu_text
        return final_menu_text


class GameActionDialogueMenuAvatar(ListMenuAvatar):
    NAME = "game_action_dialogue_menu_avatar"

    def __init__(self, gc, name):
        super().__init__(gc, name)
        self.menu_display_details = {"default_width": 70, "default_height": 23, "align_x": "center", "align_y": "bottom", "coordinates": [0, 0]}
        self.fill_out_menu_info()


class DeveloperMenuAvatar(ListMenuAvatar):
    NAME = "developer_menu_avatar"

    def __init__(self, gc, name):
        super().__init__(gc, name)
        self.menu_display_details = {"default_width": 42, "default_height": 30, "align_x": "right", "align_y": "top", "coordinates": [0, 0]}
        self.fill_out_menu_info()


class GuideMenuAvatar(BaseMenuAvatar):
    NAME = "guide_menu_avatar"

    def __init__(self, gc, name):
        super().__init__(gc, name)

        self.menu_display_details = {"default_width": 70, "default_height": 53, "align_x": "center", "align_y": "center", "coordinates": [0, 0]}
        self.offset_x = 10
        self.bg_offset_x = 7
        self.bg_offset_y = 7
        self.offset_y = 1
        self.menu_spread_y = 25
        self.paper_width = 168
        self.image1_light = Spritesheet("Hornby_map_spritesheet", "assets/spritesheets/map_spritesheets/Guide_Top_Light" + ".png",  168, 252).get_image(0, 0)
        self.image2_light = Spritesheet("Hornby_map_spritesheet", "assets/spritesheets/map_spritesheets/Guide_Bottom_Light" + ".png",  168, 252).get_image(0, 0)
        self.image3_light = Spritesheet("Hornby_map_spritesheet", "assets/spritesheets/map_spritesheets/Guide_Top_Light" + ".png",  168, 252).get_image(0, 0)
        self.image4_light = Spritesheet("Hornby_map_spritesheet", "assets/spritesheets/map_spritesheets/Guide_Bottom_Light" + ".png",  168, 252).get_image(0, 0)

        self.image1_dark = Spritesheet("Hornby_map_spritesheet", "assets/spritesheets/map_spritesheets/Guide_Top_Dark" + ".png", 168, 252).get_image(0, 0)
        self.image2_dark = Spritesheet("Hornby_map_spritesheet", "assets/spritesheets/map_spritesheets/Guide_Bottom_Dark" + ".png", 168, 252).get_image(0, 0)
        self.image3_dark = Spritesheet("Hornby_map_spritesheet", "assets/spritesheets/map_spritesheets/Guide_Top_Dark" + ".png", 168, 252).get_image(0, 0)
        self.image4_dark = Spritesheet("Hornby_map_spritesheet", "assets/spritesheets/map_spritesheets/Guide_Bottom_Dark" + ".png", 168, 252).get_image(0, 0)

        self.fill_out_menu_info()

    def get_menu_text_drawing_instructions(self, menu_info):
        final_menu_text = []

        page_width = self.menu_display_details["default_width"]/2

        # left page top half
        header_name1 = menu_info.text_display_list[0]
        header_text1 = Mundane.center_text_x(page_width, 0, header_name1)
        final_menu_text.append(TextDisplay(header_text1[0], header_text1[1] + self.bg_offset_x, self.offset_y + 25))
        colour = menu_info.text_display_list[1]
        final_menu_text.append(TextDisplay(colour, self.offset_x + self.bg_offset_x, self.offset_y + 25 + self.menu_spread_y * 1))
        size = menu_info.text_display_list[2]
        final_menu_text.append(TextDisplay(size, self.offset_x + self.bg_offset_x, self.offset_y + 25 + self.menu_spread_y * 2))
        call = menu_info.text_display_list[3]
        final_menu_text.append(TextDisplay(call, self.offset_x + self.bg_offset_x, self.offset_y + 25 + self.menu_spread_y * 3))

        # left page bottom half
        text_spread = 4
        description = menu_info.text_display_list[4]
        for line in description:
            final_menu_text.append(TextDisplay(line, self.offset_x + self.bg_offset_x, self.offset_y + 60 + self.menu_spread_y * text_spread))
            text_spread += 1

        # right page top half
        header_name2 = menu_info.text_display_list[5]
        header_text2 = Mundane.center_text_x(page_width, 0, header_name2)
        final_menu_text.append(TextDisplay(header_text2[0], header_text2[1] + self.offset_x + self.paper_width, self.offset_y + 25))

        colour2 = menu_info.text_display_list[6]
        final_menu_text.append(TextDisplay(colour2, self.offset_x + self.bg_offset_x + self.paper_width, self.offset_y + 25 + self.menu_spread_y * 1))
        size2 = menu_info.text_display_list[7]
        final_menu_text.append(TextDisplay(size2, self.offset_x + self.bg_offset_x + self.paper_width, self.offset_y + 25 + self.menu_spread_y * 2))
        call2 = menu_info.text_display_list[8]
        final_menu_text.append(TextDisplay(call2, self.offset_x + self.bg_offset_x + self.paper_width, self.offset_y + 25 + self.menu_spread_y * 3))

        # right page bottom half
        description = menu_info.text_display_list[9]
        text_spread = 4
        for line in description:
            final_menu_text.append(TextDisplay(line, self.offset_x + self.bg_offset_x + self.paper_width, self.offset_y + 60 + self.menu_spread_y * text_spread))
            text_spread += 1

        # blinking arrows
        on_first_page = self.gc.make_flashing_text(menu_info.text_display_list[10])
        final_menu_text.append(TextDisplay(on_first_page, self.offset_x + self.bg_offset_x, self.offset_y + 240))

        on_last_page = self.gc.make_flashing_text(menu_info.text_display_list[11])
        final_menu_text.append(TextDisplay(on_last_page, self.offset_x - self.bg_offset_x + self.paper_width * 2 - 12, self.offset_y + 240))

        # page numbers
        left_page = menu_info.menu_specific_details_dict["page_left"]
        if left_page < 10:
            left_page = "0" + str(left_page)
        else:
            left_page = str(left_page)
        final_menu_text.append(TextDisplay(left_page, 80, self.offset_y + 240))
        right_page = menu_info.menu_specific_details_dict["page_right"]
        if right_page < 10:
            right_page = "0" + str(right_page)
        else:
            right_page = str(right_page)
        final_menu_text.append(TextDisplay(right_page, 260, self.offset_y + 240))

        self.final_menu_text = final_menu_text

        return final_menu_text

    def get_menu_image_drawing_instructions(self, menu_info):
        image_list = menu_info.menu_specific_details_dict["image"]
        final_menu_images = []

        image_1_top = self.image1_dark
        image_1_bottom = self.image2_dark
        image_2_top = self.image3_dark
        image_2_bottom = self.image4_dark

        if image_list[0]:
            image_1_top = self.image1_light
        if image_list[1]:
            image_1_bottom = self.image2_light
        if image_list[2]:
            image_2_top = self.image3_light
        if image_list[2]:
            image_2_bottom = self.image4_light

        image = ImageDisplay(image_1_top, self.bg_offset_x, self.bg_offset_y)
        final_menu_images.append(image)

        image = ImageDisplay(image_1_bottom,  self.bg_offset_x, self.bg_offset_y)
        final_menu_images.append(image)

        image = ImageDisplay(image_2_top, self.bg_offset_x + self.paper_width, self.bg_offset_y)
        final_menu_images.append(image)

        image = ImageDisplay(image_2_bottom, self.bg_offset_x + self.paper_width, self.bg_offset_y)
        final_menu_images.append(image)

        self.final_menu_images = final_menu_images

        return final_menu_images


class NumberSelectionMenuAvatar(SubMenuAvatar):
    NAME = "number_selection_menu_avatar"

    def __init__(self, gc, name):
        super().__init__(gc, name)

        self.menu_display_details = {"default_width": 20, "default_height": 10, "align_x": "right", "align_y": "center", "coordinates": [0, 0]}
        self.offset_x = 0
        self.fill_out_menu_info()

    def get_menu_text_drawing_instructions(self, menu_info):
        menu_info = menu_info
        text_display_list = menu_info.text_display_list
        number_to_show = text_display_list[0]

        final_menu_text = []

        centered_text = Mundane.center_text_x(self.overlay_body_x, 0, number_to_show)
        final_menu_text.append(TextDisplay(number_to_show, 10, 20))

        self.final_menu_text = final_menu_text

        return final_menu_text

    def update_for_display(self, information_from_ghost, master_menu_display_details):
        spritesheet_width = self.menu_display_details["default_width"] * GameSettings.MENUSEGMENTSIZE
        self.menu_display_details["align_x"] = master_menu_display_details["coordinates"][0] - spritesheet_width - 5
        self.menu_display_details["align_y"] = master_menu_display_details["coordinates"][1]
        self.menu_display_details["coordinates"][0] = master_menu_display_details["coordinates"][0] - spritesheet_width - 5
        self.menu_display_details["coordinates"][1] = master_menu_display_details["coordinates"][1]

        self.fill_out_menu_info()


class TextInputMenuAvatar(SubMenuAvatar):
    NAME = "text_input_menu_avatar"

    def __init__(self, gc, name):
        super().__init__(gc, name)

        self.menu_display_details = {"default_width": 50, "default_height": 7, "align_x": "right", "align_y": "center", "coordinates": [0, 0]}
        self.offset_x = 0
        self.fill_out_menu_info()

    def get_menu_text_drawing_instructions(self, menu_info):
        menu_info = menu_info
        text_display_list = menu_info.text_display_list
        current_text_to_show = text_display_list[0]

        max_word_length = menu_info.menu_specific_details_dict["max_word_length"]

        final_menu_text = []

        underscore_text = ""

        if len(current_text_to_show) < max_word_length:
            for space in range(len(current_text_to_show)):
                underscore_text = underscore_text + " "
            underscore_text = underscore_text + "_"
            flashing_underscore = self.gc.make_flashing_text(underscore_text)
            final_menu_text.append(TextDisplay(flashing_underscore, 10, 20))

        final_menu_text.append(TextDisplay(current_text_to_show, 10, 20))

        self.final_menu_text = final_menu_text

        return final_menu_text

    def update_for_display(self, information_from_ghost, master_menu_display_details):
        spritesheet_width = self.menu_display_details["default_width"] * GameSettings.MENUSEGMENTSIZE
        self.menu_display_details["align_x"] = master_menu_display_details["coordinates"][0] - spritesheet_width - 5
        self.menu_display_details["align_y"] = master_menu_display_details["coordinates"][1]
        self.menu_display_details["coordinates"][0] = master_menu_display_details["coordinates"][0] - spritesheet_width - 5
        self.menu_display_details["coordinates"][1] = master_menu_display_details["coordinates"][1]

        self.fill_out_menu_info()


class MenuAvatar(object):
    NAME = "Menu_Base_Avatar"

    def __init__(self, gc, name, items):
        self.menu_display_details = {}
        self.gc = gc

        self.overlay_body_x = 0
        self.overlay_body_Y = 0
        self.overlay_header_x = 0
        self.overlay_header_y = 0

        self.x = 0
        self.y = 0
        self.offset_x = 15
        self.offset_y = 15
        self.cursor_offset_x = 5
        self.header_spacing = 0
        self.cursor_at = 0

        self.y_space_size = 15

        self.menu_spread_y = self.y_space_size + GameSettings.FONT_SIZE
        self.menu_spread_x = 0
        self.name = name

        self.set_menu_width = None
        self.set_menu_height = None
        self.set_menu_display_coordinates()
        self.menu_type = None

        self.spritesheet_width = 0
        self.spritesheet_height = 0

        self.overlay_image = None
        self.fill_out_menu_info(items)
        self.final_menu_text = []
        self.final_menu_images = []

    def set_menu_display_coordinates(self):
        dictionary = {"start_menu_avatar": {"default_width": None, "default_height": None, "align_x": "right", "align_y": "center", "coordinates": [0, 0]},
                      "words_menu_avatar": {"default_width": None, "default_height": None, "align_x": "right", "align_y": "center", "coordinates": [0, 0]},
                      "seller_menu_avatar": {"default_width": None, "default_height": None, "align_x": "right", "align_y": "center", "coordinates": [0, 0]},
                         "acquire_menu_avatar": {"default_width": None, "default_height": None, "align_x": "right", "align_y": "center", "coordinates": [0, 0]},
                         "special_menu_avatar": {"default_width": None, "default_height": None, "align_x": "left", "align_y": "top", "coordinates": [0, 0]},
                         "supplies_inventory_menu_avatar": {"default_width": 34, "default_height": 73, "align_x": "right", "align_y": "center", "coordinates": [0, 0]},
                         "key_inventory_menu_avatar": {"default_width": 34, "default_height": 73, "align_x": "right", "align_y": "center", "coordinates": [0, 0]},
                         "treasure_inventory_menu_avatar": {"default_width": 34, "default_height": 73, "align_x": "right", "align_y": "center", "coordinates": [0, 0]},
                         "gift_giving_menu_avatar": {"default_width": 34, "default_height": None, "align_x": "right", "align_y": "center", "coordinates": [0, 0]},
                         "number_selection_menu_avatar": {"default_width": 34, "default_height": None, "align_x": "right", "align_y": "center", "coordinates": [0, 0]},
                         "text_input_menu_avatar": {"default_width": 34, "default_height": None, "align_x": "right", "align_y": "center", "coordinates": [0, 0]}}

        generic = {"default_width": 100, "default_height": 100, "align_x": "center", "align_y": "center", "coordinates": [0, 0]}

        skip_list = ["conversation_options_menu_avatar", "guide_menu_avatar", "chat_menu_avatar", "outfit_menu_avatar", "map_menu_avatar", "picture_menu_avatar", "quiz_menu_avatar", "stat_menu_avatar", "game_action_dialogue_menu_avatar", "scene_dialogue_menu_avatar"]

        if self.name in dictionary.keys():
            self.menu_display_details = dictionary[self.name]
            self.set_menu_height = dictionary[self.name]["default_height"]
            self.set_menu_width = dictionary[self.name]["default_width"]
        elif self.name in skip_list:
            pass
        else:
            self.menu_display_details = generic

    def get_longest_item(self, menu_items_list, menu_header=None):
        longest_item = 3
        for item in menu_items_list:
            length = len(item)
            if length > longest_item:
                longest_item = length

        if menu_header:
            if len(menu_header) > longest_item:
                longest_item = len(menu_header)

        return longest_item

    def fill_out_menu_info(self, menu_information):
        menu_items_list = menu_information.text_display_list
        header = menu_information.header
        cursor_at = menu_information.cursor_at

        font_size = GameSettings.FONT_SIZE
        segment_size = GameSettings.MENUSEGMENTSIZE
        segment_proportion = font_size/segment_size

        # Calculate the menu body width
        edge_size = self.offset_x/segment_size
        longest_item = self.get_longest_item(menu_items_list, header)
        menu_width = 0
        if self.set_menu_width:
            menu_width = self.set_menu_width
        else:
            menu_width = (longest_item * segment_proportion) + (2 * int(edge_size))

        # Calculate menu body height
        if self.set_menu_height:
            menu_height = self.set_menu_height
        else:
            number_of_items = len(menu_items_list)
            number_of_spaces = number_of_items - 1
            items_height = number_of_items * segment_proportion
            space_size = int(self.y_space_size / segment_size)
            space_height = space_size * number_of_spaces
            border_height = int(self.offset_y/segment_size) * 2
            menu_height = items_height + space_height + border_height

        header_height = 0
        if header:
            # Calculate Header Height
            header_number_of_items = 1
            header_items_height = header_number_of_items * segment_proportion
            header_border_height = int(self.offset_y / segment_size) * 2
            header_height = header_items_height + header_border_height
            self.overlay_header_x = menu_width
            self.overlay_header_y = header_height
            self.header_spacing = header_height * segment_size - 5

        # Update class info
        self.overlay_body_x = menu_width
        self.overlay_body_Y = menu_height

        total_width = menu_width
        self.spritesheet_width = menu_width * segment_size

        total_height = menu_height + header_height
        self.spritesheet_height = (menu_height * segment_size) + (self.overlay_header_y * segment_size)

        if header:
            # self.overlay_image = self.gc.build_special_overlay_image("special_menu" + "_overlay", menu_width, menu_height, self.offset_y)
            self.overlay_image = self.gc.game_view.build_overlay_image("special_menu" + "_overlay", menu_width, menu_height, header=header)
        else:
            self.overlay_image = self.gc.game_view.build_overlay_image("special_menu" + "_overlay", menu_width, menu_height)

        self.name = self.NAME

    def get_menu_text_drawing_instructions(self, menu_info):
        menu_info = menu_info
        text_display_list = menu_info.text_display_list
        header = menu_info.header
        cursor_image = menu_info.cursor_image
        cursor_at = menu_info.cursor_at


        final_menu_text = []

        if header:
            header_text_length = len(header)*2
            max_width = self.overlay_body_x
            offset = (self.offset_x/GameSettings.MENUSEGMENTSIZE)
            width_less_offsets = max_width/2 - offset
            header_spaces = int((width_less_offsets - header_text_length/2)/2)
            for space in range(header_spaces):
                header = " " + header
            final_menu_text.append(TextDisplay(header, self.offset_x, self.offset_y))

        if cursor_image:
            cursor_loc_x = (cursor_at[0] * self.menu_spread_x) + self.cursor_offset_x
            cursor_loc_y = (cursor_at[1] * self.menu_spread_y) + self.header_spacing + self.offset_y
            final_menu_text.append(TextDisplay(cursor_image, cursor_loc_x, cursor_loc_y))

        for position_y in range(len(text_display_list)):
            loc_x = self.menu_spread_x + self.offset_x
            loc_y = (position_y * self.menu_spread_y) + self.offset_y + self.header_spacing
            final_menu_text.append(TextDisplay(text_display_list[position_y], loc_x, loc_y))

        self.final_menu_text = final_menu_text
        return final_menu_text

    def get_menu_image_drawing_instructions(self, menu_info):
        final_menu_images = []
        self.final_menu_images = final_menu_images
        return None


class ImageMenuAvatar(BaseMenuAvatar):
    NAME = "image_menu_avatar"

    def __init__(self, gc, name):
        super().__init__(gc, name)
        self.offset_x = 130
        self.offset_y = 20
        self.title_offset_y = 20
        self.image_offset_x = 7
        self.image_offset_y = 8
        self.offset_x = 10
        self.offset_y = 10

        self.menu_display_details = {"default_width": 54, "default_height": 35, "align_x": "center", "align_y": "center", "coordinates": [0, 0]}
        self.fill_out_menu_info()


    def get_menu_image_drawing_instructions(self, menu_info):
        image = menu_info.menu_specific_details_dict["image"]
        final_menu_images = []
        image = ImageDisplay(image, self.image_offset_x, self.image_offset_y)
        final_menu_images.append(image)

        self.final_menu_images = final_menu_images
        return final_menu_images


class QuizMenuAvatar(BaseMenuAvatar):
    NAME = "quiz_menu_avatar"

    def __init__(self, gc, name):
        super().__init__(gc, name)
        self.offset_x = 130
        self.offset_y = 20
        self.title_offset_y = 20
        self.image_offset_x = 10
        self.image_offset_y = 10
        self.cursor_offset_x = self.offset_x - 10
        self.cursor_offset_y = self.offset_y + 7

        self.menu_display_details = {"default_width": 100, "default_height": 100, "align_x": "center", "align_y": "center", "coordinates": [0, 0]}
        self.fill_out_menu_info()

    def get_menu_text_drawing_instructions(self, menu_info):
        menu_info = menu_info
        text_display_list = menu_info.text_display_list
        final_menu_text = []

        for position_y in range(len(text_display_list)):
            loc_x = self.menu_spread_x + self.offset_x
            loc_y = (position_y * self.menu_spread_y) + self.menu_spread_y + self.offset_y
            text = TextDisplay(text_display_list[position_y], 10, 10)
            final_menu_text.append(text)

        self.final_menu_text = final_menu_text

        return final_menu_text

    def get_menu_image_drawing_instructions(self, menu_info):
        picture = menu_info.menu_specific_details_dict["image"]
        final_menu_images = []

        loc_x = 20
        loc_y = 50
        image = ImageDisplay(picture, loc_x, loc_y)
        final_menu_images.append(image)

        self.final_menu_images = final_menu_images
        return final_menu_images


class CharacterAssemblyMenuAvatar(BaseMenuAvatar):
    NAME = "character_assembly_menu_avatar"

    def __init__(self, gc, name):
        super().__init__(gc, name)
        self.offset_x = 130
        self.offset_y = 20
        self.title_offset_y = 20
        self.image_offset_x = 10
        self.image_offset_y = 10
        self.cursor_offset_x = self.offset_x - 10
        self.cursor_offset_y = self.offset_y + 7

        self.menu_display_details = {"default_width": 48, "default_height": 70, "align_x": "center", "align_y": "center", "coordinates": [0, 0]}
        self.fill_out_menu_info()
        self.x_counter = 0
        self.y_counter = 0
        self.text_entry_boxes = {"assembly_box_1": TextEntryBoxAvatar(self.gc.gs.gv, "assembly_box_1", 35, 220)}
        self.button_list = []
        self.cage_group_dict = {"part_group": ComponentCageGroup(self.gc, self, "part_group", 3, 50, 10, 2, 10, 10, "center", 300, []),
                                "spritesheet_group": ComponentCageGroup(self.gc, self, "spritesheet_group", 4, 32, 0, 4, 48, 0, "center", 20, []),
                                "arrow_group": ComponentCageGroup(self.gc, self, "arrow_group", 2, 15, 200, 1, 15, 0, "center", 310, [])}

    def add_button_to_list(self, button_avatar):
        self.button_list.append(button_avatar)

    def add_image_to_cage_group_cage(self, group_name, image, image_x, image_y):
        self.cage_group_dict[group_name].assign_image_to_cage(image, image_x, image_y)

    def assign_list_of_images_to_group_cage(self, group_name, image_list):
        group = self.cage_group_dict[group_name]
        group.assign_list_of_images_to_cage(image_list)

    def get_menu_text_drawing_instructions(self, menu_info):
        menu_info = menu_info
        text_display_list = menu_info.text_display_list
        selected_part = menu_info.menu_specific_details_dict["selected_part"]
        text_box_dict = menu_info.menu_specific_details_dict["text_box_dict"]
        parts_list = menu_info.menu_specific_details_dict["parts_list"]

        self.assign_list_of_images_to_group_cage("spritesheet_group", menu_info.menu_specific_details_dict["frame_list"])
        # self.add_image_to_cage_group_cage("spritesheet_group", menu_info.menu_specific_details_dict["right_frame_3"], image_loc[0], image_loc[1])

        text_surface_list = []

        for item in menu_info.menu_specific_details_dict["parts_list"]:
            if item == selected_part:
                surface_text = self.main_font.render(item, True, (99, 99, 99))
            else:
                surface_text = self.main_font.render(item, True, (0, 0, 0))
            text_surface_list.append(surface_text)

        self.assign_list_of_images_to_group_cage("part_group", text_surface_list)

        left_arrow = self.main_font.render("<", True, (0, 0, 0))
        right_arrow = self.main_font.render(">", True, (0, 0, 0))
        self.assign_list_of_images_to_group_cage("arrow_group", [left_arrow, right_arrow])

        final_menu_text = []

        # text box
        box_1_text = self.text_entry_boxes["assembly_box_1"].make_text(text_box_dict["assembly_box_1"].return_current_text())
        final_menu_text.append(box_1_text)

        # cage group
        part_group = self.return_cage_group_images("part_group")
        spritesheet_group = self.return_cage_group_images("spritesheet_group")
        arrow_group = self.return_cage_group_images("arrow_group")

        final_menu_text = final_menu_text + part_group + spritesheet_group + arrow_group

        for index, item in enumerate(part_group):
            part_change_button_avatar = ButtonAvatar(self.gc, parts_list[index] + "_change_button", item.x, item.y, item.text.get_width(), item.text.get_height())
            self.add_button_to_list(part_change_button_avatar)

        left_arrow_button = ButtonAvatar(self.gc, "left_arrow_button", arrow_group[0].x, arrow_group[0].y, arrow_group[0].text.get_width(), arrow_group[0].text.get_height())
        self.add_button_to_list(left_arrow_button)

        right_arrow_button = ButtonAvatar(self.gc, "right_arrow_button", arrow_group[1].x, arrow_group[1].y, arrow_group[1].text.get_width(), arrow_group[1].text.get_height())
        self.add_button_to_list(right_arrow_button)

        # Header
        header_text = Mundane.center_text_x(self.overlay_body_x, 0, "ASSEMBLE")
        final_menu_text.append(TextDisplay(header_text[0], header_text[1], 10))

        self.final_menu_text = final_menu_text

        return final_menu_text

    def return_cage_group_images(self, group_name):
        return self.cage_group_dict[group_name].return_image_list()

    def get_offset_to_center_x(self, component_width):
        print("body", self.spritesheet_width, component_width)
        offset_x = (self.spritesheet_width - component_width)/2
        return offset_x

    def layout_text_in_a_grid(self, column_count, column_size, row_count, row_size, starting_x, starting_y, text_list):
        final_list = []

        column_locations = []
        row_locations = []

        column_spacing = 5
        row_spacing = 5

        for index in range(column_count):
            column_loc = starting_x + (index * column_spacing) + (index * column_size)
            column_locations.append(column_loc)

        for index in range(row_count):
            row_loc = starting_y + (index * row_spacing) + (index * row_size)
            row_locations.append(row_loc)

        counter_c = 0
        counter_r = 0
        for index, item in enumerate(text_list):
            text_surface = self.main_font.render(item, True, (0, 0, 0))
            text_item = TextDisplay(text_surface, column_locations[counter_c], row_locations[counter_r])
            final_list.append(text_item)
            counter_c += 1
            if counter_c == column_count:
                counter_r += 1
                counter_c = 0

        return final_list


    def get_menu_image_drawing_instructions(self, menu_info):
        final_menu_images = []

        front_fram_1_image = menu_info.menu_specific_details_dict["front_frame_1"]
        segment_1_x = Mundane.center_image_x(self.overlay_body_x, 0, front_fram_1_image)/2

        self.x_counter = 0
        self.y_counter = 0

        def get_x_addition():
            if self.x_counter == 4:
                self.x_counter = 0
                self.y_counter += 1
            result = 0 + copy.copy(self.x_counter)
            self.x_counter += 1


            return result*32


        loc_y = 20

        # front_frame_1 = ImageDisplay(menu_info.menu_specific_details_dict["front_frame_1"], segment_1_x + get_x_addition(), loc_y + self.y_counter*48)
        # front_frame_2 = ImageDisplay(menu_info.menu_specific_details_dict["front_frame_2"], segment_1_x + get_x_addition(), loc_y + self.y_counter*48)
        # front_frame_3 = ImageDisplay(menu_info.menu_specific_details_dict["front_frame_3"], segment_1_x + get_x_addition(), loc_y + self.y_counter*48)
        # front_frame_4 = ImageDisplay(menu_info.menu_specific_details_dict["front_frame_4"], segment_1_x + get_x_addition(), loc_y + self.y_counter*48)
        # back_frame_1 = ImageDisplay(menu_info.menu_specific_details_dict["back_frame_1"], segment_1_x + get_x_addition(), loc_y + self.y_counter *48)
        # back_frame_2 = ImageDisplay(menu_info.menu_specific_details_dict["back_frame_2"], segment_1_x + get_x_addition(), loc_y + self.y_counter *48)
        # back_frame_3 = ImageDisplay(menu_info.menu_specific_details_dict["back_frame_3"], segment_1_x + get_x_addition(), loc_y + self.y_counter *48)
        # back_frame_4 = ImageDisplay(menu_info.menu_specific_details_dict["back_frame_4"], segment_1_x + get_x_addition(), loc_y + self.y_counter *48)
        # right_frame_1 = ImageDisplay(menu_info.menu_specific_details_dict["right_frame_1"], segment_1_x + get_x_addition(), loc_y + self.y_counter * 48)
        # right_frame_2 = ImageDisplay(menu_info.menu_specific_details_dict["right_frame_2"], segment_1_x + get_x_addition(), loc_y + self.y_counter * 48)
        # right_frame_3 = ImageDisplay(menu_info.menu_specific_details_dict["right_frame_3"], segment_1_x + get_x_addition(), loc_y + self.y_counter * 48)
        # right_frame_4 = ImageDisplay(menu_info.menu_specific_details_dict["right_frame_4"], segment_1_x + get_x_addition(), loc_y + self.y_counter * 48)
        # left_frame_1 = ImageDisplay(menu_info.menu_specific_details_dict["left_frame_1"], segment_1_x + get_x_addition(), loc_y + self.y_counter * 48)
        # left_frame_2 = ImageDisplay(menu_info.menu_specific_details_dict["left_frame_2"], segment_1_x + get_x_addition(), loc_y + self.y_counter * 48)
        # left_frame_3 = ImageDisplay(menu_info.menu_specific_details_dict["left_frame_3"], segment_1_x + get_x_addition(), loc_y + self.y_counter * 48)
        # left_frame_4 = ImageDisplay(menu_info.menu_specific_details_dict["left_frame_4"], segment_1_x + get_x_addition(), loc_y + self.y_counter * 48)

        square_number = 0
        square_xy = 12
        spacing = 2
        square_offset = 15
        base_border_colour = (0, 0, 0)
        border_thickness = 2
        highlight_colour = (212, 212, 83)
        current_primary_colour_index = menu_info.menu_specific_details_dict["current_primary_colour_index"]

        primary_colour_squares = menu_info.menu_specific_details_dict["primary_colour_square_list"]

        for square_colour in primary_colour_squares:
            if square_number == current_primary_colour_index:
                border_colour = highlight_colour
            else:
                border_colour = base_border_colour
            boarder_square = pygame.Surface((square_xy, square_xy), pygame.SRCALPHA)
            boarder_square.fill(border_colour)

            colour_square_xy = (square_xy - border_thickness, square_xy - border_thickness)
            square_surface = pygame.Surface(colour_square_xy, pygame.SRCALPHA)
            square_surface.fill(square_colour.details["colour"])
            boarder_square.blit(square_surface, (border_thickness - 1, border_thickness - 1))

            square_x_loc = square_offset + square_number * (square_xy + spacing)
            square_y_loc = 250

            final_image = ImageDisplay(boarder_square, square_x_loc, square_y_loc)
            final_menu_images.append(final_image)
            square_number += 1
            button_avatar = ButtonAvatar(self.gc, square_colour.name, square_x_loc, square_y_loc, colour_square_xy[0], colour_square_xy[1])
            self.add_button_to_list(button_avatar)

        current_secondary_colour_index = menu_info.menu_specific_details_dict["current_secondary_colour_index"]
        secondary_colour_squares = menu_info.menu_specific_details_dict["secondary_colour_square_list"]
        square_number = 0

        for square_colour in secondary_colour_squares:
            if square_number == current_secondary_colour_index:
                border_colour = highlight_colour
            else:
                border_colour = base_border_colour
            boarder_square = pygame.Surface((square_xy, square_xy), pygame.SRCALPHA)
            boarder_square.fill(border_colour)

            colour_square_xy = (square_xy - border_thickness, square_xy - border_thickness)
            square_surface = pygame.Surface(colour_square_xy, pygame.SRCALPHA)
            square_surface.fill(square_colour.details["colour"])
            boarder_square.blit(square_surface, (border_thickness - 1, border_thickness - 1))

            square_x_loc = square_offset + square_number * (square_xy + spacing)
            square_y_loc = 275

            final_image = ImageDisplay(boarder_square, square_x_loc, square_y_loc)
            final_menu_images.append(final_image)
            square_number += 1
            button_avatar = ButtonAvatar(self.gc, square_colour.name, square_x_loc, square_y_loc, colour_square_xy[0], colour_square_xy[1])
            self.add_button_to_list(button_avatar)

        box_1_image = self.text_entry_boxes["assembly_box_1"].make_image()
        final_menu_images.append(box_1_image)

        # final_images = [front_frame_1, front_frame_2, front_frame_3, front_frame_4,
        #                 back_frame_1, back_frame_2, back_frame_3, back_frame_4,
        #                 right_frame_1, right_frame_2, right_frame_3, right_frame_4,
        #                 left_frame_1, left_frame_2, left_frame_3, left_frame_4
        #                 ]
        #
        # for image in final_images:
        #     final_menu_images.append(image)

        self.final_menu_images = final_menu_images
        return final_menu_images


class TextEntryBoxAvatar(object):
    def __init__(self, gv, name, x_image, y_image):
        self.gv = gv   # type: GameView
        self.name = name
        self.selected = False
        self.x_image = x_image
        self.y_image = y_image
        self.box_image = self.build_box_image(34, 4)

    def make_image(self):
        image = ImageDisplay(self.box_image, self.x_image, self.y_image)
        return image

    def make_text(self, current_text):
        text = TextDisplay(current_text, self.x_image + 5, self.y_image + 5)
        return text

    def build_box_image(self, size_x, size_y):
        box = self.gv.build_overlay_image(self.name, size_x, size_y)
        return box


class ButtonAvatar(object):
    def __init__(self, gc, name, x, y, x_size, y_size):
        self.x = x
        self.y = y
        self.x_size = x_size
        self.y_size = y_size
        self.gc = gc
        self.name = name


class ComponentCage(object):
    def __init__(self, menu, name, x_size, y_size):
        self.menu = menu
        self.name = name
        self.selected = False
        self.x_size = x_size
        self.y_size = y_size
        self.cage_image = self.make_image()

    def assign_image_to_cage(self, image):
        self.cage_image = image

    def make_image(self):
        square_surface = pygame.Surface((self.x_size, self.y_size), pygame.SRCALPHA)
        square_surface.fill((99, 99, 99))
        return square_surface


class ComponentCageGroup(object):
    def __init__(self, gc, menu, group_name, column_count, column_size, column_spacing, row_count, row_size, row_spacing, starting_x, starting_y, text_list):
        self.gc = gc
        self.total_height = None
        self.total_width = None
        self.column_spacing = column_spacing
        self.row_spacing = row_spacing
        self.menu = menu
        self.group_name = group_name
        self.text_list = text_list
        self.row_size = row_size
        self.row_count = row_count
        self.column_size = column_size
        self.column_count = column_count
        self.cage_list = self.create_cage_grid()
        self.set_total_group_height_width()
        self.starting_y = starting_y
        self.starting_x = self.set_starting_x(starting_x)

    def set_starting_x(self, starting_x):
        if starting_x == "center":
            starting_x_loc = self.menu.get_offset_to_center_x(self.total_width)
        elif starting_x == "left":
            starting_x_loc = 0
        elif starting_x == "right":
            starting_x_loc = self.menu.overaly_x - self.total_width
        else:
            starting_x_loc = starting_x
        return starting_x_loc

    def set_total_group_height_width(self):
        self.total_width = (self.column_count * self.column_size) + ((self.column_count - 1) * self.column_spacing)
        self.total_height = (self.row_count * self.row_size) + ((self.row_count - 1) * self.row_spacing)

    def return_image_list(self):
        final_image_list = []
        for cage in self.cage_list.keys():
            x_loc = self.starting_x + self.cage_list[cage]["assigned_x"]
            y_loc = self.starting_y + self.cage_list[cage]["assigned_y"]
            item = TextDisplay(self.cage_list[cage]["cage_object"].cage_image, x_loc, y_loc)
            final_image_list.append(item)

        return final_image_list

    def assign_image_to_cage(self, image, image_x, image_y):
        cage_object = self.cage_list[(image_x - 1, image_y - 1)]["cage_object"]
        cage_object.assign_image_to_cage(image)
        rel_x = self.cage_list[(image_x - 1, image_y - 1)]["relative_x"]
        new_assigned_x = rel_x + self.get_assigned_x_offset(cage_object.cage_image.get_width())
        self.cage_list[(image_x - 1, image_y - 1)]["assigned_x"] = new_assigned_x

    def get_assigned_x_offset(self, surface_size_x):
        if surface_size_x < self.column_size:
            offset_x = (self.column_size - surface_size_x)/2
        else:
            offset_x = 0

        return offset_x

    def assign_list_of_images_to_cage(self, image_list):
        counter_c = 0
        counter_r = 0
        for index, item in enumerate(image_list):
            self.assign_image_to_cage(image_list[index], counter_c + 1, counter_r + 1)
            # self.cage_list[(counter_c, counter_r)]["cage_object"].cage_image = image_list[index]

            counter_c += 1
            if counter_c == self.column_count:
                counter_r += 1
                counter_c = 0

    def create_cage_grid(self):
        final_list = {}

        column_locations = []
        row_locations = []

        for index in range(self.column_count):
            column_loc = (index * self.column_spacing) + (index * self.column_size)
            column_locations.append(column_loc)

        for index in range(self.row_count):
            row_loc = (index * self.row_spacing) + (index * self.row_size)
            row_locations.append(row_loc)

        counter_c = 0
        counter_r = 0
        for item in range(self.row_count * self.column_count):
            cage_name = "cage_" + str(counter_c) + "_" + str(counter_r)
            text_item = {"cage_object": ComponentCage(self.gc, cage_name, self.column_size, self.row_size),
                         "relative_x": column_locations[counter_c],
                         "relative_y": row_locations[counter_r],
                         "assigned_x": column_locations[counter_c],
                         "assigned_y": row_locations[counter_r]}
            final_list[(counter_c, counter_r)] = text_item
            counter_c += 1
            if counter_c == self.column_count:
                counter_r += 1
                counter_c = 0

        return final_list