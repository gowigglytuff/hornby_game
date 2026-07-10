import textwrap

from animations_page_view_page import Action
from definitions import Direction, GameSettings
from menu_avatars_view_page import TextDisplay, ImageDisplay
from menu_ghosts_data_page import MenuInformation


class Scene(object):

    def __init__(self, gc, actions_list):
        self.gc = gc  # type: Game
        self.actions_list = actions_list
        self.number_of_actions = len(actions_list)
        self.current_action = 0
        self.complete = False
        self.total_player_x_movement = 0
        self.total_player_y_movement = 0

    def return_current_action(self):
        if self.current_action == self.number_of_actions:
            result = None
            self.complete = True
        else:
            result = self.actions_list[self.current_action]
            self.current_action += 1
        return result, self.complete

    def reset(self):
        self.current_action = 0
        self.total_player_x_movement = 0
        self.total_player_y_movement = 0


class ScenePictureTutorial(object):

    def __init__(self, gc, actions_list):
        self.gc = gc  # type: Game
        self.actions_list = [("walk_left", Action.move(Direction.LEFT)), ("walk_left", Action.move(Direction.LEFT)), ("walk_left", Action.move(Direction.LEFT))]
        self.number_of_actions = len(actions_list)
        self.current_action = 0
        self.complete = False
        self.total_player_x_movement = 0
        self.total_player_y_movement = 0

    def return_current_action(self):
        if self.current_action == self.number_of_actions:
            result = None
            self.complete = True
        else:
            result = self.actions_list[self.current_action]
            self.current_action += 1
        return result, self.complete

    def reset(self):
        self.current_action = 0
        self.total_player_x_movement = 0
        self.total_player_y_movement = 0


class DialogueInformation(object):
    def __init__(self, header, text_display_list, menu_specific_details_dict):
        self.header = header
        self.text_display_list = text_display_list
        self.menu_specific_details_dict = menu_specific_details_dict

class SceneDialogueGhost(object):
    NAME = "scene_ghost"

    def __init__(self, gc):
        self.gc = gc
        self.additional_information = []
        self.name = self.NAME

        self.menu_header = None
        self.menu_item_list = []
        self.menu_images_list = []
        self.talking_to = "Jane"
        self.speaker_unique_name = "Jane"
        self.friendship = 1
        self.face_image = None
        self.phrase = "Hi there! I hope that you're having an amazing day!"
        self.speaking_queue = []
        self.current_phrase = []

    def get_friendship(self, friendship):
        friendship_counter = " - - - - "
        if friendship == 0:
            friendship_counter = " - - - - "

        elif 5 >= friendship >= 1 :
            friendship_counter = " \u2665 - - - "
        elif 10 >= friendship >= 6:
            friendship_counter = " \u2665 \u2665 - - "
        elif 15 >= friendship >= 11:
            friendship_counter = " \u2665 \u2665 \u2665 - "
        elif friendship >= 16:
            friendship_counter = " \u2665 \u2665 \u2665 \u2665 "
        return friendship_counter

    def get_menu_items_to_display(self):
        return self.menu_item_list

    def prepare_menu_for_display(self, details):
        self.talking_to = details["speaker_name"]
        self.friendship = details["friendship_level"]
        self.face_image = details["face_image"]
        self.speaker_unique_name = details["speaker_unique_name"]
        self.menu_item_list = details["phrase"]


    def generate_menu_information_package(self):
        source = self.get_menu_items_to_display().copy()
        text_display_list = []

        for item in range(len(source)):
            text_display_list.append(source[item])

        menu_specific = {"friendship_level": self.friendship,
                         "face_image": self.face_image,
                         "speaker_name": self.talking_to}

        menu_information = DialogueInformation(self.menu_header, text_display_list, menu_specific)
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
            self.gc.menu_controller.chat_menu_selection(menu_selection)

    def reset_elements(self):
        speaker_ghost = self.gc.gs.get_feature_ghost(self.speaker_unique_name)
        speaker_ghost.currently_chatting = False


class SceneDialogueAvatar(object):
    NAME = "chat_menu_avatar"

    def __init__(self, gc, name):
        self.gc = gc

        self.overlay_body_x = 0
        self.overlay_body_Y = 0
        self.overlay_header_x = 0
        self.overlay_header_y = 0

        self.x = 0
        self.y = 0
        self.header_spacing = 0
        self.cursor_at = 0

        self.y_space_size = 15

        self.menu_spread_y = self.y_space_size + GameSettings.FONT_SIZE
        self.menu_spread_x = 0
        self.name = name

        self.menu_type = None

        self.spritesheet_width = 0
        self.spritesheet_height = 0

        self.overlay_image = None
        self.menu_display_details = {"default_width": 70, "default_height": 25, "align_x": "center", "align_y": "3/4", "coordinates": [0, 0]}
        self.set_menu_display_coordinates()
        self.offset_x = 130
        self.offset_y = 20
        self.image_offset_x = 10
        self.image_offset_y = 10

        self.set_menu_width = 70
        self.set_menu_height = 25

        menu_specific = {"friendship_level": None,
                         "face_image": None,
                         "speaker_name": None}

        text_display_list = []

        menu_info = DialogueInformation(None, text_display_list, menu_specific)

        self.fill_out_menu_info(menu_info)

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
        speaker_name = menu_info.menu_specific_details_dict["speaker_name"]
        friendship_level = menu_info.menu_specific_details_dict["friendship_level"]

        final_menu_text = []

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

        # loc_x = self.image_offset_x
        # loc_y = self.image_offset_y
        # image = ImageDisplay(face, loc_x, loc_y)
        # final_menu_images.append(image)

        return final_menu_images

    def set_menu_display_coordinates(self):
        menu_avatar = self
        x_instruction = menu_avatar.menu_display_details["align_x"]
        y_instruction = menu_avatar.menu_display_details["align_y"]
        x = 0
        y = 0

        if x_instruction == "center":
            x = GameSettings.RESOLUTION[0] / 2 - menu_avatar.spritesheet_width / 2
        elif x_instruction == "left":
            x = 0 + GameSettings.RESOLUTION[0] / GameSettings.MENUEDGE
        elif x_instruction == "right":
            x = GameSettings.RESOLUTION[0] - menu_avatar.spritesheet_width - GameSettings.RESOLUTION[0] / GameSettings.MENUEDGE
        else:
            x = x_instruction

        if y_instruction == "center":
            y = GameSettings.RESOLUTION[1] / 2 - menu_avatar.spritesheet_height / 2
        elif y_instruction == "1/4":
            y = GameSettings.RESOLUTION[1] / 4 - menu_avatar.spritesheet_height / 4
        elif y_instruction == "top":
            y = 0 + GameSettings.RESOLUTION[1] / GameSettings.MENUEDGE
        elif y_instruction == "3/4":
            y = GameSettings.RESOLUTION[1] / 4 * 3 - menu_avatar.spritesheet_height / 4 * 3
        elif y_instruction == "bottom":
            y = GameSettings.RESOLUTION[1] - menu_avatar.spritesheet_height - GameSettings.RESOLUTION[1] / GameSettings.MENUEDGE
        else:
            y = y_instruction

        menu_avatar.menu_display_details["coordinates"][0] = x
        menu_avatar.menu_display_details["coordinates"][1] = y