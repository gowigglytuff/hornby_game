import textwrap

from definitions import GameSettings, Types, Mundane
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

        self.set_menu_width = None
        self.set_menu_height = None

        self.spritesheet_width = 0
        self.spritesheet_height = 0

        self.overlay_image = None
        self.fill_out_menu_info(items)

    def set_menu_display_coordinates(self):
        dictionary = {"start_menu_avatar": {"default_width": 32, "default_height": None, "align_x": "right", "align_y": "center", "coordinates": [0, 0]},
                         "acquire_menu_avatar": {"default_width": 32, "default_height": 500, "align_x": "right", "align_y": "center", "coordinates": [0, 0]},
                         "special_menu_avatar": {"default_width": None, "default_height": None, "align_x": "left", "align_y": "top", "coordinates": [0, 0]},
                         "supplies_inventory_menu_avatar": {"default_width": 34, "default_height": None, "align_x": "right", "align_y": "center", "coordinates": [0, 0]},
                         "key_inventory_menu_avatar": {"default_width": 34, "default_height": None, "align_x": "right", "align_y": "center", "coordinates": [0, 0]},
                         "gift_giving_menu_avatar": {"default_width": 34, "default_height": None, "align_x": "right", "align_y": "center", "coordinates": [0, 0]},
                         "number_selection_menu_avatar": {"default_width": 34, "default_height": None, "align_x": "right", "align_y": "center", "coordinates": [0, 0]}}


        generic = {"default_width": 100, "default_height": 100, "align_x": "center", "align_y": "center", "coordinates": [0, 0]}

        skip_list = ["conversation_options_menu_avatar", "chat_menu_avatar", "outfit_menu_avatar", "map_menu_avatar", "picture_menu_avatar", "quiz_menu_avatar", "stat_menu_avatar", "game_action_dialogue_menu_avatar"]

        if self.name in dictionary.keys():
            self.menu_display_details = dictionary[self.name]
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
            # self.overlay_image = self.gc_input.build_special_overlay_image("special_menu" + "_overlay", menu_width, menu_height, self.offset_y)
            self.overlay_image = self.gc_input.game_view.build_overlay_image("special_menu" + "_overlay", menu_width, menu_height, header=header)
        else:
            self.overlay_image = self.gc_input.game_view.build_overlay_image("special_menu" + "_overlay", menu_width, menu_height)

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

        return final_menu_text

    def get_menu_image_drawing_instructions(self, menu_info):
        return None


class StatMenuAvatar(MenuAvatar):
    NAME = "stat_menu_avatar"

    def __init__(self, gc_input, name, items):
        super().__init__(gc_input, name,  items)
        self.menu_display_details = {"default_width": None, "default_height": None, "align_x": "center", "align_y": "top", "coordinates": [0, 0]}
        self.set_menu_width = 70
        self.set_menu_height = 8
        self.fill_out_menu_info(items)

    def get_menu_text_drawing_instructions(self, menu_info):
        menu_info = menu_info
        text_display_list = menu_info.text_display_list
        header = menu_info.header
        cursor_image = menu_info.cursor_image
        cursor_at = menu_info.cursor_at

        final_menu_text = []

        x_spacing = 0
        last_item_x = 0
        for item in text_display_list:
            length = len(item) * GameSettings.FONT_SIZE
            loc_x = last_item_x + 15
            loc_y = self.offset_y + self.header_spacing
            final_menu_text.append(TextDisplay(item, loc_x, loc_y))
            last_item_x = last_item_x + length + 15

        return final_menu_text

    def get_menu_image_drawing_instructions(self, menu_info):
        return None


class GameActionDialogueMenuAvatar(MenuAvatar):
    NAME = "game_action_dialogue_menu_avatar"

    def __init__(self, gc_input, name, items):
        super().__init__(gc_input, name,  items)
        self.menu_display_details = {"default_width": None, "default_height": None, "align_x": "center", "align_y": "bottom", "coordinates": [0, 0]}
        self.offset_y = 20
        self.set_menu_width = 70
        self.set_menu_height = 25
        self.fill_out_menu_info(items)

    def get_menu_image_drawing_instructions(self, menu_info):
        return None


class ConversationOptionsMenuAvatar(MenuAvatar):
    NAME = "conversation_options_menu_avatar"

    def __init__(self, gc_input, name,  items):
        super().__init__(gc_input, name,  items)
        self.menu_display_details = {"default_width": 200, "default_height": 100, "align_x": "center", "align_y": "3/4", "coordinates": [0, 0]}
        self.offset_x = 130
        self.offset_y = 20
        self.image_offset_x = 10
        self.image_offset_y = 10
        self.cursor_offset_x = self.offset_x - 10
        self.set_menu_width = 70
        self.set_menu_height = 25
        self.fill_out_menu_info(items)

    def get_menu_text_drawing_instructions(self, menu_info):
        menu_info = menu_info
        text_display_list = menu_info.text_display_list
        cursor_image = menu_info.cursor_image
        cursor_at = menu_info.cursor_at
        speaker_name = menu_info.menu_specific_details_dict["speaker_name"]
        friendship_level = menu_info.menu_specific_details_dict["friendship_level"]

        final_menu_text = []

        if cursor_image:
            cursor_loc_x = (cursor_at[0] * self.menu_spread_x) + self.cursor_offset_x
            cursor_loc_y = (cursor_at[1] * self.menu_spread_y) + self.menu_spread_y + self.offset_y
            final_menu_text.append(TextDisplay(cursor_image, cursor_loc_x, cursor_loc_y))

        for position_y in range(len(text_display_list)):
            loc_x = self.menu_spread_x + self.offset_x
            loc_y = (position_y * self.menu_spread_y) + self.menu_spread_y + self.offset_y
            text = TextDisplay(text_display_list[position_y], loc_x, loc_y)
            final_menu_text.append(text)

        # name and Friendship
        loc_x = self.menu_spread_x + self.offset_x
        loc_y = self.offset_y
        text = TextDisplay(speaker_name + " [" + str(friendship_level) + "]", loc_x, loc_y)
        final_menu_text.append(text)

        return final_menu_text

    def get_menu_image_drawing_instructions(self, menu_info):
        face = menu_info.menu_specific_details_dict["face_image"]

        final_menu_images = []

        loc_x = self.image_offset_x
        loc_y = self.image_offset_y
        image = ImageDisplay(face, loc_x, loc_y)
        final_menu_images.append(image)

        return final_menu_images


class ChatMenuAvatar(MenuAvatar):
    NAME = "chat_menu_avatar"

    def __init__(self, gc_input, name,  items):
        super().__init__(gc_input, name,  items)

        self.menu_display_details = {"default_width": 200, "default_height": 100, "align_x": "center", "align_y": "3/4", "coordinates": [0, 0]}

        self.offset_x = 130
        self.offset_y = 20
        self.image_offset_x = 10
        self.image_offset_y = 10
        self.cursor_offset_x = self.offset_x - 10

        self.set_menu_width = 70
        self.set_menu_height = 25

        self.fill_out_menu_info(items)

    def get_menu_text_drawing_instructions(self, menu_info):
        menu_info = menu_info
        text_display_list = menu_info.text_display_list
        cursor_image = menu_info.cursor_image
        cursor_at = menu_info.cursor_at
        speaker_name = menu_info.menu_specific_details_dict["speaker_name"]
        friendship_level = menu_info.menu_specific_details_dict["friendship_level"]

        final_menu_text = []


        if cursor_image:
            cursor_loc_x = (cursor_at[0] * self.menu_spread_x) + self.cursor_offset_x
            cursor_loc_y = (cursor_at[1] * self.menu_spread_y) + self.menu_spread_y + self.offset_y
            final_menu_text.append(TextDisplay(cursor_image, cursor_loc_x, cursor_loc_y))

        for position_y in range(len(text_display_list)):
            loc_x = self.menu_spread_x + self.offset_x
            loc_y = (position_y * self.menu_spread_y) + self.menu_spread_y + self.offset_y
            text = TextDisplay(text_display_list[position_y], loc_x, loc_y)
            final_menu_text.append(text)

        # name and Friendship
        loc_x = self.menu_spread_x + self.offset_x
        loc_y = self.offset_y
        text = TextDisplay(speaker_name + " [" + str(friendship_level) + "]", loc_x, loc_y)
        final_menu_text.append(text)

        return final_menu_text

    def get_menu_image_drawing_instructions(self, menu_info):
        face = menu_info.menu_specific_details_dict["face_image"]

        final_menu_images = []

        loc_x = self.image_offset_x
        loc_y = self.image_offset_y
        image = ImageDisplay(face, loc_x, loc_y)
        final_menu_images.append(image)

        return final_menu_images


class OutfitMenuAvatar(MenuAvatar):
    NAME = "outfit_menu_avatar"

    def __init__(self, gc_input, name,  items):
        super().__init__(gc_input, name,  items)

        self.menu_display_details = {"default_width": 20, "default_height": 20, "align_x": "center", "align_y": "center", "coordinates": [0, 0]}

        self.set_menu_width = 30
        self.set_menu_height = 20

        self.fill_out_menu_info(items)

    def get_menu_text_drawing_instructions(self, menu_info):
        menu_info = menu_info
        text_display_list = menu_info.text_display_list
        outfit_name = menu_info.menu_specific_details_dict["outfit_name"]

        final_menu_text = []

        # outfit name
        name_text = Mundane.center_text_x(self.overlay_body_x, 0, outfit_name)
        final_menu_text.append(TextDisplay(name_text[0], name_text[1], 75))

        # Header
        header_name = "OUTFITS"
        header_text = Mundane.center_text_x(self.overlay_body_x, 0, header_name)
        final_menu_text.append(TextDisplay(header_text[0], header_text[1], 10))

        if not menu_info.menu_specific_details_dict["is_first_outfit"]:
            # left arrow
            text = TextDisplay("<", 10, 45)
            final_menu_text.append(text)

        if not menu_info.menu_specific_details_dict["is_last_outfit"]:
            # left arrow
            text = TextDisplay(">", 130, 45)
            final_menu_text.append(text)

        return final_menu_text

    def get_menu_image_drawing_instructions(self, menu_info):
        chosen_outfit = menu_info.menu_specific_details_dict["outfit_image"]
        final_menu_images = []
        #
        loc_y = 15
        image = ImageDisplay(chosen_outfit, Mundane.center_image_x(self.overlay_body_x, 0, chosen_outfit), loc_y)
        final_menu_images.append(image)

        return final_menu_images


class MapMenuAvatar(MenuAvatar):
    NAME = "map_menu_avatar"

    def __init__(self, gc_input, name,  items):
        super().__init__(gc_input, name,  items)

        self.menu_display_details = {"default_width": 20, "default_height": 20, "align_x": "center", "align_y": "center", "coordinates": [0, 0]}
        self.offset_x = 10
        self.offset_y = 10
        self.set_menu_width = 53
        self.set_menu_height = 34
        self.fill_out_menu_info(items)


    def get_menu_text_drawing_instructions(self, menu_info):
        final_menu_text = []
        return final_menu_text

    def get_menu_image_drawing_instructions(self, menu_info):
        image = menu_info.menu_specific_details_dict["image"]
        final_menu_images = []

        loc_x = 5
        loc_y = 5
        image = ImageDisplay(image, loc_x, loc_y)
        final_menu_images.append(image)

        return final_menu_images


class PictureMenuAvatar(MenuAvatar):
    NAME = "picture_menu_avatar"

    def __init__(self, gc_input, name,  items):
        super().__init__(gc_input, name,  items)

        self.menu_display_details = {"default_width": 20, "default_height": 20, "align_x": "center", "align_y": "center", "coordinates": [0, 0]}

        self.offset_x = 10
        self.offset_y = 10

        self.set_menu_width = 53
        self.set_menu_height = 34

        self.fill_out_menu_info(items)

    def get_menu_text_drawing_instructions(self, menu_info):
        final_menu_text = []
        return final_menu_text

    def get_menu_image_drawing_instructions(self, menu_info):
        image = menu_info.menu_specific_details_dict["image"]
        final_menu_images = []

        loc_x = 5
        loc_y = 5
        image = ImageDisplay(image, loc_x, loc_y)
        final_menu_images.append(image)

        return final_menu_images


class GalleryMenuAvatar(MenuAvatar):
    NAME = "gallery_menu_avatar"

    def __init__(self, gc_input, name,  items):
        super().__init__(gc_input, name,  items)

        self.set_menu_width = 30
        self.set_menu_height = 20

        self.fill_out_menu_info(items)

    def get_menu_text_drawing_instructions(self, menu_info):
        menu_info = menu_info
        text_display_list = menu_info.text_display_list
        bird_name = menu_info.menu_specific_details_dict["item_name"]

        final_menu_text = []

        # bird names
        name_text = Mundane.center_text_x(self.overlay_body_x, 0, bird_name)
        final_menu_text.append(TextDisplay(name_text[0], name_text[1], 75))

        # Header
        header_text = Mundane.center_text_x(self.overlay_body_x, 0, "GALLERY")
        final_menu_text.append(TextDisplay(header_text[0], header_text[1], 10))

        if not menu_info.menu_specific_details_dict["is_first_item"]:
            # left arrow
            text = TextDisplay("<", 10, 45)
            final_menu_text.append(text)

        if not menu_info.menu_specific_details_dict["is_last_item"]:
            # left arrow
            text = TextDisplay(">", 130, 45)
            final_menu_text.append(text)

        return final_menu_text

    def get_menu_image_drawing_instructions(self, menu_info):
        bird_image = menu_info.menu_specific_details_dict["item_image"]
        final_menu_images = []

        loc_y = 20
        image = ImageDisplay(bird_image, Mundane.center_image_x(self.overlay_body_x, 0, bird_image), loc_y)
        final_menu_images.append(image)

        return final_menu_images


class NumberSelectionMenuAvatar(MenuAvatar):
    NAME = "number_selection_menu_avatar"

    def __init__(self, gc_input, name,  items):
        super().__init__(gc_input, name,  items)

        self.set_menu_width = 20
        self.set_menu_height = 10
        self.offset_x = 0

        self.fill_out_menu_info(items)

    def get_menu_text_drawing_instructions(self, menu_info):
        menu_info = menu_info
        text_display_list = menu_info.text_display_list
        number_to_show = text_display_list[0]

        final_menu_text = []

        centered_text = Mundane.center_text_x(self.overlay_body_x, 0, number_to_show)
        final_menu_text.append(TextDisplay(number_to_show, 10, 20))

        return final_menu_text

    def get_menu_image_drawing_instructions(self, menu_info):
        final_menu_images = []
        return final_menu_images


class QuizMenuAvatar(MenuAvatar):
    NAME = "quiz_menu_avatar"

    def __init__(self, gc_input, name,  items):
        super().__init__(gc_input, name,  items)
        self.gc_input = gc_input

        self.overlay_body_x = 0
        self.overlay_body_Y = 0
        self.overlay_header_x = 0
        self.overlay_header_y = 0

        self.menu_display_details = {"default_width": 100, "default_height": 100, "align_x": "center", "align_y": "center", "coordinates": [0, 0]}

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

        self.set_menu_width = 100
        self.set_menu_height = 100

        self.spritesheet_width = 0
        self.spritesheet_height = 0

        self.overlay_image = None
        self.fill_out_menu_info(items)

    def get_menu_text_drawing_instructions(self, menu_info):
        menu_info = menu_info
        text_display_list = menu_info.text_display_list
        final_menu_text = []

        for position_y in range(len(text_display_list)):
            loc_x = self.menu_spread_x + self.offset_x
            loc_y = (position_y * self.menu_spread_y) + self.menu_spread_y + self.offset_y
            text = TextDisplay(text_display_list[position_y], 10, 10)
            final_menu_text.append(text)
        return final_menu_text

    def get_menu_image_drawing_instructions(self, menu_info):
        picture = menu_info.menu_specific_details_dict["image"]
        final_menu_images = []

        loc_x = 20
        loc_y = 50
        image = ImageDisplay(picture, loc_x, loc_y)
        final_menu_images.append(image)

        return final_menu_images