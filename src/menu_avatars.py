from definitions import GameSettings


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


class MenuAvatar(object):
    NAME = "Menu_Base_Avatar"

    def __init__(self, gc_input, name, items, display_details):
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
        self.menu_type = None

        self.set_menu_width = display_details["default_width"]
        self.set_menu_height = display_details["default_height"]

        self.spritesheet_width = 0
        self.spritesheet_height = 0

        self.overlay_image = None
        self.fill_out_menu_info(items)

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
            print(space_size, items_height, border_height)

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
            self.overlay_image = self.gc_input.build_overlay_image("special_menu" + "_overlay", menu_width, menu_height, header=header)
        else:
            self.overlay_image = self.gc_input.build_overlay_image("special_menu" + "_overlay", menu_width, menu_height)

        self.name = self.NAME

    def get_menu_text_drawing_instructions(self, menu_info):
        menu_info = menu_info
        text_print_list = menu_info["text_print_list"]
        header = menu_info["header"]
        cursor_img = menu_info["cursor_img"]
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

        if cursor_img:
            cursor_loc_x = (cursor_at[0] * self.menu_spread_x) + self.cursor_offset_x
            cursor_loc_y = (cursor_at[1] * self.menu_spread_y) + self.header_spacing + self.offset_y
            final_menu_text.append(TextPrint(cursor_img, cursor_loc_x, cursor_loc_y))

        for position_y in range(len(text_print_list)):
            loc_x = self.menu_spread_x + self.offset_x
            loc_y = (position_y * self.menu_spread_y) + self.offset_y + self.header_spacing
            final_menu_text.append(TextPrint(text_print_list[position_y], loc_x, loc_y))

        return final_menu_text