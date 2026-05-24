import textwrap

from definitions import GameSettings, Types
from spritesheet import Spritesheet


class DisplayText(object):
    def __init__(self, text):
        self.text = text


class DisplayPicture(object):
    def __init__(self, img):
        self.img = img


class TextPrint(object):
    def __init__(self, text, x, y):
        self.text = text
        self.x = x
        self.y = y


class ImagePrint(object):
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y


class MenuAvatar(object):
    NAME = "Menu_Base_Avatar"

    def __init__(self, gc_input, name, items):
        self.menu_display_details = {}
        self.gc_input = gc_input

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
        self.set_menu_display_coordinates()
        self.menu_type = None

        self.set_menu_width = self.menu_display_details["default_width"]
        self.set_menu_height = self.menu_display_details["default_height"]

        self.spritesheet_width = 0
        self.spritesheet_height = 0

        self.overlay_image = None
        self.fill_out_menu_info(items)

    def set_menu_display_coordinates(self):
        dictionary = {"start_menu_avatar": {"default_width": 32, "default_height": None, "align_x": "right", "align_y": "center", "coordinates": [0, 0]},
                         "acquire_menu_avatar": {"default_width": 32, "default_height": None, "align_x": "right", "align_y": "center", "coordinates": [0, 0]},
                         "stat_menu_avatar": {"default_width": None, "default_height": None, "align_x": "right", "align_y": "top", "coordinates": [0, 0]},
                         "special_menu_avatar": {"default_width": None, "default_height": None, "align_x": "left", "align_y": "top", "coordinates": [0, 0]},
                         "supplies_inventory_menu_avatar": {"default_width": 34, "default_height": None, "align_x": "right", "align_y": "center", "coordinates": [0, 0]},
                         "quiz_menu_avatar": {"default_width": 100, "default_height": 100, "align_x": "center", "align_y": "center", "coordinates": [0, 0]},
                         "key_inventory_menu_avatar": {"default_width": 34, "default_height": None, "align_x": "right", "align_y": "center", "coordinates": [0, 0]},
                         "conversation_options_menu_avatar": {"default_width": 200, "default_height": 100, "align_x": "center", "align_y": "bottom", "coordinates": [0, 0]},
                         "chat_menu_avatar": {"default_width": 200, "default_height": 100, "align_x": "center", "align_y": "bottom", "coordinates": [0, 0]},
                         "game_action_dialogue_menu_avatar": {"default_width": 70, "default_height": 23, "align_x": "right", "align_y": "bottom", "coordinates": [0, 0]},
                         "use_menu_avatar": {"default_width": 20, "default_height": None, "align_x": "right", "align_y": "bottom", "coordinates": [0, 0]},
                         "yes_no_menu_avatar": {"default_width": 20, "default_height": None, "align_x": "right", "align_y": "bottom", "coordinates": [0, 0]},
                         "sub_menu_avatar": {"default_width": 20, "default_height": None, "align_x": "right", "align_y": "bottom", "coordinates": [0, 0]},
                         "outfit_menu_avatar": {"default_width": 20, "default_height": 20, "align_x": "center", "align_y": "center", "coordinates": [0, 0]},
                         "map_menu_avatar": {"default_width": 20, "default_height": 20, "align_x": "center", "align_y": "center", "coordinates": [0, 0]}}

        generic = {"default_width": 100, "default_height": 100, "align_x": "center", "align_y": "center", "coordinates": [0, 0]}

        if self.name in dictionary.keys():
            self.menu_display_details = dictionary[self.name]
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
        menu_items_list = menu_information["text_print_list"]
        header = menu_information["header"]
        cursor_at = menu_information["cursor_at"]

        # menu_items_list = menu_information.text_print_list # TODO: Fix this so that all the ghosts use this version
        # header = menu_information.header
        # cursor_at = menu_information.cursor_at


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
            # self.overlay_image = self.gc_input.build_special_overlay_image("special_menu" + "_overlay", menu_width, menu_height, self.offset_y)
            self.overlay_image = self.gc_input.game_view.build_overlay_image("special_menu" + "_overlay", menu_width, menu_height, header=header)
        else:
            self.overlay_image = self.gc_input.game_view.build_overlay_image("special_menu" + "_overlay", menu_width, menu_height)

        self.name = self.NAME

    def get_menu_text_drawing_instructions(self, menu_info):
        menu_info = menu_info
        text_print_list = menu_info["text_print_list"]
        header = menu_info["header"]
        cursor_image = menu_info["cursor_image"]
        cursor_at = menu_info["cursor_at"]

        final_menu_text = []

        if header:
            header_text_length = len(header)*2
            max_width = self.overlay_body_x
            offset = (self.offset_x/GameSettings.MENUSEGMENTSIZE)
            width_less_offsets = max_width/2 - offset
            header_spaces = int((width_less_offsets - header_text_length/2)/2)
            for space in range(header_spaces):
                header = " " + header
            final_menu_text.append(TextPrint(header, self.offset_x, self.offset_y))

        if cursor_image:
            cursor_loc_x = (cursor_at[0] * self.menu_spread_x) + self.cursor_offset_x
            cursor_loc_y = (cursor_at[1] * self.menu_spread_y) + self.header_spacing + self.offset_y
            final_menu_text.append(TextPrint(cursor_image, cursor_loc_x, cursor_loc_y))

        for position_y in range(len(text_print_list)):
            loc_x = self.menu_spread_x + self.offset_x
            loc_y = (position_y * self.menu_spread_y) + self.offset_y + self.header_spacing
            final_menu_text.append(TextPrint(text_print_list[position_y], loc_x, loc_y))

        return final_menu_text

    def get_menu_image_drawing_instructions(self, menu_info):
        return None


class ConversationOptionsMenuAvatar(MenuAvatar):
    NAME = "conversation_options_menu_avatar"

    def __init__(self, gc_input, name,  items):
        super().__init__(gc_input, name,  items)
        self.gc_input = gc_input

        self.overlay_body_x = 0
        self.overlay_body_Y = 0
        self.overlay_header_x = 0
        self.overlay_header_y = 0

        self.x = 0
        self.y = 0
        self.offset_x = 175
        self.offset_y = 20
        self.cursor_offset_x = self.offset_x - 10
        self.header_spacing = 0
        self.cursor_at = 0

        self.y_space_size = 15

        self.menu_spread_y = self.y_space_size + GameSettings.FONT_SIZE
        self.menu_spread_x = 0
        self.name = name
        self.menu_type = None

        self.set_menu_width = None
        self.set_menu_height = None

        self.spritesheet_width = 0
        self.spritesheet_height = 0

        self.overlay_image = None
        self.fill_out_menu_info(items)

    def fill_out_menu_info(self, menu_information):
        menu_items_list = menu_information.text_print_list
        header = menu_information.header
        cursor_at = menu_information.cursor_at

        font_size = GameSettings.FONT_SIZE
        segment_size = GameSettings.MENUSEGMENTSIZE
        segment_proportion = font_size/segment_size


        menu_width = 90
        menu_height = 25
        header_height = 0

        # Update class info
        self.overlay_body_x = menu_width
        self.overlay_body_Y = menu_height

        total_width = menu_width
        self.spritesheet_width = menu_width * segment_size

        total_height = menu_height + header_height
        self.spritesheet_height = (menu_height * segment_size) + (self.overlay_header_y * segment_size)

        self.overlay_image = self.gc_input.game_view.build_overlay_image("special_menu" + "_overlay", menu_width, menu_height)

        self.name = self.NAME

    def get_menu_text_drawing_instructions(self, menu_info):
        menu_info = menu_info
        text_print_list = menu_info.text_print_list
        cursor_image = menu_info.cursor_image
        cursor_at = menu_info.cursor_at
        speaker_name = menu_info.menu_specific_details_dict["speaker_name"]
        friendship_level = menu_info.menu_specific_details_dict["friendship_level"]

        final_menu_text = []


        if cursor_image:
            cursor_loc_x = (cursor_at[0] * self.menu_spread_x) + self.cursor_offset_x
            cursor_loc_y = (cursor_at[1] * self.menu_spread_y) + self.menu_spread_y + self.offset_y
            final_menu_text.append(TextPrint(cursor_image, cursor_loc_x, cursor_loc_y))

        for position_y in range(len(text_print_list)):
            loc_x = self.menu_spread_x + self.offset_x
            loc_y = (position_y * self.menu_spread_y) + self.menu_spread_y + self.offset_y
            text = TextPrint(text_print_list[position_y], loc_x, loc_y)
            final_menu_text.append(text)

        # name and Friendship
        loc_x = self.menu_spread_x + self.offset_x
        loc_y = self.offset_y
        text = TextPrint(speaker_name + " [" + str(friendship_level) + "]", loc_x, loc_y)
        final_menu_text.append(text)

        return final_menu_text

    def get_menu_image_drawing_instructions(self, menu_info):
        face = menu_info.menu_specific_details_dict["face_image"]

        final_menu_images = []

        loc_x = 5
        loc_y = 0
        image = ImagePrint(face, loc_x, loc_y)
        final_menu_images.append(image)

        return final_menu_images


class ChatMenuAvatar(MenuAvatar):
    NAME = "chat_menu_avatar"

    def __init__(self, gc_input, name,  items):
        super().__init__(gc_input, name,  items)
        self.gc_input = gc_input

        self.overlay_body_x = 0
        self.overlay_body_Y = 0
        self.overlay_header_x = 0
        self.overlay_header_y = 0

        self.x = 0
        self.y = 0
        self.offset_x = 175
        self.offset_y = 20
        self.cursor_offset_x = self.offset_x - 10
        self.header_spacing = 0
        self.cursor_at = 0

        self.y_space_size = 15

        self.menu_spread_y = self.y_space_size + GameSettings.FONT_SIZE
        self.menu_spread_x = 0
        self.name = name
        self.menu_type = None

        self.set_menu_width = None
        self.set_menu_height = None

        self.spritesheet_width = 0
        self.spritesheet_height = 0

        self.overlay_image = None
        self.fill_out_menu_info(items)


    def fill_out_menu_info(self, menu_information):
        menu_items_list = menu_information.text_print_list
        header = menu_information.header
        cursor_at = menu_information.cursor_at

        font_size = GameSettings.FONT_SIZE
        segment_size = GameSettings.MENUSEGMENTSIZE
        segment_proportion = font_size/segment_size


        menu_width = 90
        menu_height = 25
        header_height = 0

        # Update class info
        self.overlay_body_x = menu_width
        self.overlay_body_Y = menu_height

        total_width = menu_width
        self.spritesheet_width = menu_width * segment_size

        total_height = menu_height + header_height
        self.spritesheet_height = (menu_height * segment_size) + (self.overlay_header_y * segment_size)

        self.overlay_image = self.gc_input.game_view.build_overlay_image("special_menu" + "_overlay", menu_width, menu_height)

        self.name = self.NAME

    def get_menu_text_drawing_instructions(self, menu_info):
        menu_info = menu_info
        text_print_list = menu_info.text_print_list
        cursor_image = menu_info.cursor_image
        cursor_at = menu_info.cursor_at
        speaker_name = menu_info.menu_specific_details_dict["speaker_name"]
        friendship_level = menu_info.menu_specific_details_dict["friendship_level"]

        final_menu_text = []


        if cursor_image:
            cursor_loc_x = (cursor_at[0] * self.menu_spread_x) + self.cursor_offset_x
            cursor_loc_y = (cursor_at[1] * self.menu_spread_y) + self.menu_spread_y + self.offset_y
            final_menu_text.append(TextPrint(cursor_image, cursor_loc_x, cursor_loc_y))

        for position_y in range(len(text_print_list)):
            loc_x = self.menu_spread_x + self.offset_x
            loc_y = (position_y * self.menu_spread_y) + self.menu_spread_y + self.offset_y
            text = TextPrint(text_print_list[position_y], loc_x, loc_y)
            final_menu_text.append(text)

        # name and Friendship
        loc_x = self.menu_spread_x + self.offset_x
        loc_y = self.offset_y
        text = TextPrint(speaker_name + " [" + str(friendship_level) + "]", loc_x, loc_y)
        final_menu_text.append(text)

        return final_menu_text

    def get_menu_image_drawing_instructions(self, menu_info):
        face = menu_info.menu_specific_details_dict["face_image"]

        final_menu_images = []

        loc_x = 5
        loc_y = 0
        image = ImagePrint(face, loc_x, loc_y)
        final_menu_images.append(image)

        return final_menu_images


class OutfitMenuAvatar(MenuAvatar):
    NAME = "outfit_menu_avatar"

    def __init__(self, gc_input, name,  items):
        super().__init__(gc_input, name,  items)
        self.gc_input = gc_input

        self.overlay_body_x = 0
        self.overlay_body_Y = 0
        self.overlay_header_x = 0
        self.overlay_header_y = 0

        self.x = 0
        self.y = 0
        self.offset_x = 175
        self.offset_y = 20
        self.name = name
        self.menu_type = Types.BASE

        self.set_menu_width = None
        self.set_menu_height = None

        self.spritesheet_width = 0
        self.spritesheet_height = 0

        self.overlay_image = None
        self.fill_out_menu_info(items)


    def fill_out_menu_info(self, menu_information):
        menu_items_list = menu_information.text_print_list
        header = menu_information.header
        cursor_at = menu_information.cursor_at

        font_size = GameSettings.FONT_SIZE
        segment_size = GameSettings.MENUSEGMENTSIZE
        segment_proportion = font_size/segment_size


        menu_width = 30
        menu_height = 20
        header_height = 0

        # Update class info
        self.overlay_body_x = menu_width
        self.overlay_body_Y = menu_height

        total_width = menu_width
        self.spritesheet_width = menu_width * segment_size

        total_height = menu_height + header_height
        self.spritesheet_height = (menu_height * segment_size) + (self.overlay_header_y * segment_size)

        self.overlay_image = self.gc_input.game_view.build_overlay_image("special_menu" + "_overlay", menu_width, menu_height)

        self.name = self.NAME

    def get_menu_text_drawing_instructions(self, menu_info):
        menu_info = menu_info
        text_print_list = menu_info.text_print_list
        outfit_name = menu_info.menu_specific_details_dict["outfit_name"]

        final_menu_text = []



        # outfit name
        loc_x = self.menu_spread_x + self.offset_x
        loc_y = self.offset_y
        text = TextPrint(menu_info.menu_specific_details_dict["outfit_name"], 20, 75)
        final_menu_text.append(text)

        is_first_outfit = True
        is_last_outfit = False

        # # Header
        # text = TextPrint("Outfits", 40, 10)
        # final_menu_text.append(text)

        if not menu_info.menu_specific_details_dict["is_first_outfit"]:
            # left arrow
            text = TextPrint("<", 10, 45)
            final_menu_text.append(text)

        if not menu_info.menu_specific_details_dict["is_last_outfit"]:
            # left arrow
            text = TextPrint(">", 130, 45)
            final_menu_text.append(text)

        return final_menu_text

    def get_menu_image_drawing_instructions(self, menu_info):
        chosen_outfit = menu_info.menu_specific_details_dict["outfit_image"]
        final_menu_images = []
        #
        loc_x = 60
        loc_y = 15
        image = ImagePrint(chosen_outfit, loc_x, loc_y)
        final_menu_images.append(image)

        return final_menu_images


class MapMenuAvatar(MenuAvatar):
    NAME = "map_menu_avatar"

    def __init__(self, gc_input, name,  items):
        super().__init__(gc_input, name,  items)
        self.gc_input = gc_input

        self.overlay_body_x = 0
        self.overlay_body_Y = 0
        self.overlay_header_x = 0
        self.overlay_header_y = 0

        self.x = 0
        self.y = 0
        self.offset_x = 10
        self.offset_y = 10
        self.name = name
        self.menu_type = Types.BASE

        self.set_menu_width = None
        self.set_menu_height = None

        self.spritesheet_width = 0
        self.spritesheet_height = 0

        self.overlay_image = None
        self.fill_out_menu_info(items)

    def fill_out_menu_info(self, menu_information):
        menu_items_list = menu_information.text_print_list
        header = menu_information.header
        cursor_at = menu_information.cursor_at

        font_size = GameSettings.FONT_SIZE
        segment_size = GameSettings.MENUSEGMENTSIZE
        segment_proportion = font_size/segment_size


        menu_width = 53
        menu_height = 34
        header_height = 0

        # Update class info
        self.overlay_body_x = menu_width
        self.overlay_body_Y = menu_height

        total_width = menu_width
        self.spritesheet_width = menu_width * segment_size

        total_height = menu_height + header_height
        self.spritesheet_height = (menu_height * segment_size) + (self.overlay_header_y * segment_size)

        self.overlay_image = self.gc_input.game_view.build_overlay_image("special_menu" + "_overlay", menu_width, menu_height)

        self.name = self.NAME

    def get_menu_text_drawing_instructions(self, menu_info):
        final_menu_text = []
        return final_menu_text

    def get_menu_image_drawing_instructions(self, menu_info):
        image = menu_info.menu_specific_details_dict["image"]
        final_menu_images = []

        loc_x = 5
        loc_y = 5
        image = ImagePrint(image, loc_x, loc_y)
        final_menu_images.append(image)

        return final_menu_images


class GalleryMenuAvatar(MenuAvatar):
    NAME = "gallery_menu_avatar"

    def __init__(self, gc_input, name,  items):
        super().__init__(gc_input, name,  items)
        self.gc_input = gc_input

        self.overlay_body_x = 0
        self.overlay_body_Y = 0
        self.overlay_header_x = 0
        self.overlay_header_y = 0

        self.x = 0
        self.y = 0
        self.offset_x = 175
        self.offset_y = 20
        self.name = name
        self.menu_type = Types.BASE

        self.set_menu_width = None
        self.set_menu_height = None

        self.spritesheet_width = 0
        self.spritesheet_height = 0

        self.overlay_image = None
        self.fill_out_menu_info(items)


    def fill_out_menu_info(self, menu_information):
        menu_items_list = menu_information.text_print_list
        header = menu_information.header
        cursor_at = menu_information.cursor_at

        font_size = GameSettings.FONT_SIZE
        segment_size = GameSettings.MENUSEGMENTSIZE
        segment_proportion = font_size/segment_size


        menu_width = 30
        menu_height = 20
        header_height = 0

        # Update class info
        self.overlay_body_x = menu_width
        self.overlay_body_Y = menu_height

        total_width = menu_width
        self.spritesheet_width = menu_width * segment_size

        total_height = menu_height + header_height
        self.spritesheet_height = (menu_height * segment_size) + (self.overlay_header_y * segment_size)

        self.overlay_image = self.gc_input.game_view.build_overlay_image("special_menu" + "_overlay", menu_width, menu_height)

        self.name = self.NAME

    def get_menu_text_drawing_instructions(self, menu_info):
        menu_info = menu_info
        text_print_list = menu_info.text_print_list
        outfit_name = menu_info.menu_specific_details_dict["bird_name"]

        final_menu_text = []

        # bird name
        loc_x = self.menu_spread_x + self.offset_x
        loc_y = self.offset_y
        text = TextPrint(menu_info.menu_specific_details_dict["bird_name"], 20, 75)
        final_menu_text.append(text)

        if not menu_info.menu_specific_details_dict["is_first_bird"]:
            # left arrow
            text = TextPrint("<", 10, 45)
            final_menu_text.append(text)

        if not menu_info.menu_specific_details_dict["is_last_bird"]:
            # left arrow
            text = TextPrint(">", 130, 45)
            final_menu_text.append(text)

        return final_menu_text

    def get_menu_image_drawing_instructions(self, menu_info):
        chosen_outfit = menu_info.menu_specific_details_dict["bird_image"]
        final_menu_images = []
        #
        loc_x = 60
        loc_y = 15
        image = ImagePrint(chosen_outfit, loc_x, loc_y)
        final_menu_images.append(image)

        return final_menu_images


# class ConversationMenuAvatar(object):
#     NAME = "Conversation_Menu_Avatar"
#
#     def __init__(self, gc_input, items, name):
#         self.gc_input = gc_input
#
#         self.overlay_body_x = 0
#         self.overlay_body_Y = 0
#         self.overlay_header_x = 0
#         self.overlay_header_y = 0
#
#         self.x = 0
#         self.y = 0
#         self.offset_x = 50
#         self.offset_y = 15
#         self.cursor_offset_x = 5
#         self.header_spacing = 0
#         self.cursor_at = 0
#
#         self.y_space_size = 15
#
#         self.menu_spread_y = self.y_space_size + GameSettings.FONT_SIZE
#         self.menu_spread_x = 0
#         self.name = name
#         self.menu_type = None
#
#         self.set_menu_width = None
#         self.set_menu_height = None
#
#         self.spritesheet_width = 0
#         self.spritesheet_height = 0
#
#         self.overlay_image = None
#         self.fill_out_menu_info(items)
#
#     def fill_out_menu_info(self, menu_information):
#         menu_items_list = menu_information["text_print_list"]
#         header = menu_information["header"]
#         cursor_at = menu_information["cursor_at"]
#
#         font_size = GameSettings.FONT_SIZE
#         segment_size = GameSettings.MENUSEGMENTSIZE
#         segment_proportion = font_size/segment_size
#
#
#         menu_width = 10
#         menu_height = 5
#         header_height = 0
#
#         # Update class info
#         self.overlay_body_x = menu_width
#         self.overlay_body_Y = menu_height
#
#         total_width = menu_width
#         self.spritesheet_width = menu_width * segment_size
#
#         total_height = menu_height + header_height
#         self.spritesheet_height = (menu_height * segment_size) + (self.overlay_header_y * segment_size)
#
#         self.overlay_image = self.gc_input.game_view.build_overlay_image("special_menu" + "_overlay", menu_width, menu_height)
#
#         self.name = self.NAME
#
#     def get_friendship(self, friendship):
#         friendship_counter = "           "
#         if friendship == 0:
#             friendship_counter = "           "
#         elif 5 >= friendship >= 1 :
#             friendship_counter = "<3         "
#         elif 10 >= friendship >= 6:
#             friendship_counter = "<3 <3      "
#         elif 15 >= friendship >= 11:
#             friendship_counter = "<3 <3 <3   "
#         elif friendship >= 16:
#             friendship_counter = "<3 <3 <3 <3"
#         return friendship_counter
#
#     def get_menu_text_drawing_instructions(self, menu_info):
#         menu_info = menu_info
#         text_print_list = menu_info["text_print_list"]
#         cursor_image = menu_info["cursor_image"]
#         cursor_at = menu_info["cursor_at"]
#
#         final_menu_text = []
#
#
#         if cursor_image:
#             cursor_loc_x = (cursor_at[0] * self.menu_spread_x) + self.cursor_offset_x
#             cursor_loc_y = (cursor_at[1] * self.menu_spread_y) + self.header_spacing + self.offset_y
#             final_menu_text.append(TextPrint(cursor_image, cursor_loc_x, cursor_loc_y))
#
#         for position_y in range(len(text_print_list)):
#             print("grabbing")
#             loc_x = self.offset_x
#             loc_y = self.offset_y
#             final_menu_text.append(TextPrint(text_print_list[position_y], loc_x, loc_y))
#
#         return final_menu_text


class QuizMenuAvatar(MenuAvatar):
    NAME = "quiz_menu_avatar"

    def __init__(self, gc_input, name,  items):
        super().__init__(gc_input, name,  items)
        self.gc_input = gc_input

        self.overlay_body_x = 0
        self.overlay_body_Y = 0
        self.overlay_header_x = 0
        self.overlay_header_y = 0

        self.x = 0
        self.y = 0
        self.offset_x = 175
        self.offset_y = 20
        self.cursor_offset_x = self.offset_x - 10
        self.header_spacing = 0
        self.cursor_at = 0

        self.y_space_size = 15

        self.menu_spread_y = self.y_space_size + GameSettings.FONT_SIZE
        self.menu_spread_x = 0
        self.name = name
        self.menu_type = None

        self.set_menu_width = None
        self.set_menu_height = None

        self.spritesheet_width = 0
        self.spritesheet_height = 0

        self.overlay_image = None
        self.fill_out_menu_info(items)

    def fill_out_menu_info(self, menu_information):
        menu_items_list = menu_information.text_print_list
        header = menu_information.header
        cursor_at = menu_information.cursor_at

        font_size = GameSettings.FONT_SIZE
        segment_size = GameSettings.MENUSEGMENTSIZE
        segment_proportion = font_size/segment_size


        menu_width = 100
        menu_height = 100
        header_height = 0

        # Update class info
        self.overlay_body_x = menu_width
        self.overlay_body_Y = menu_height

        total_width = menu_width
        self.spritesheet_width = menu_width * segment_size

        total_height = menu_height + header_height
        self.spritesheet_height = (menu_height * segment_size) + (self.overlay_header_y * segment_size)

        self.overlay_image = self.gc_input.game_view.build_overlay_image("special_menu" + "_overlay", menu_width, menu_height)

        self.name = self.NAME

    def get_menu_text_drawing_instructions(self, menu_info):
        menu_info = menu_info
        text_print_list = menu_info.text_print_list
        final_menu_text = []

        for position_y in range(len(text_print_list)):
            loc_x = self.menu_spread_x + self.offset_x
            loc_y = (position_y * self.menu_spread_y) + self.menu_spread_y + self.offset_y
            text = TextPrint(text_print_list[position_y], 10, 10)
            final_menu_text.append(text)
        return final_menu_text

    def get_menu_image_drawing_instructions(self, menu_info):
        picture = menu_info.menu_specific_details_dict["image"]
        final_menu_images = []

        loc_x = 20
        loc_y = 50
        image = ImagePrint(picture, loc_x, loc_y)
        final_menu_images.append(image)

        return final_menu_images