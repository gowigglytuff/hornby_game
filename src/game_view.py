from keyboard_manager_page import *
from avatar_page import PlayerAvatar
from definitions import Direction, GameSettings, Types
from position_manager import Room2, PositionManager

class GameView(object):
    def __init__(self, game_data, game_state, menu_drawer):
        self.game_data = game_data  # type: GameData
        self.gs = game_state  # type: GameState
        self.menu_drawer = menu_drawer  # type: MenuDrawer
        self.animation_manager = AnimationManager(self)
        self.clock = pygame.time.Clock()
        self.resolution = GameSettings.RESOLUTION
        self.FPS = 72
        self.square_size = [GameSettings.TILESIZE, GameSettings.TILESIZE]
        self.base_locator_x = ((self.resolution[0] - self.square_size[0]) / self.square_size[0]) / 2 + 1
        self.base_locator_y = ((self.resolution[1] - self.square_size[1]) / self.square_size[1]) / 2 + 1

        self.camera = [0, 0]
        self.screen = pygame.display.set_mode(self.resolution)
        self.font_file = "assets/fonts/PressStart.ttf"

        self.font_medium = pygame.font.Font(self.font_file, GameSettings.FONT_SIZE)

        self.night_filter = pygame.Surface(pygame.Rect((0, 0, self.resolution[0], self.resolution[1])).size)
        self.sky_change_increments = 6
        self.fully_dark_hours = 4
        self.sky_change_degree = 15

        self.player_avatar = None
        self.menu_avatar_data_list = {}
        self.npc_avatar_list = {}
        self.prop_avatar_list = {}
        self.decoration_avatar_list = {}
        self.menu_display_details = {"start_menu": {"default_width": 32, "default_height": None, "align_x": "right", "align_y": "center", "coordinates": [0, 0]},
                                     "stat_menu": {"default_width": None, "default_height": None, "align_x": "right", "align_y": "top", "coordinates": [0, 0]},
                                     "special_menu": {"default_width": None, "default_height": None, "align_x": "left", "align_y": "top", "coordinates": [0, 0]},
                                     "supplies_inventory_menu": {"default_width": 34, "default_height": None, "align_x": "right", "align_y": "center", "coordinates": [0, 0]},
                                     "key_inventory_menu": {"default_width": 34, "default_height": None, "align_x": "right", "align_y": "center", "coordinates": [0, 0]},
                                     "conversation_options_menu": {"default_width": 34, "default_height": None, "align_x": "right", "align_y": "center", "coordinates": [0, 0]},
                                     "game_action_dialogue_menu": {"default_width": 70, "default_height": 23, "align_x": "right", "align_y": "bottom", "coordinates": [0, 0]},
                                     "use_menu": {"default_width": 20, "default_height": None, "align_x": "right", "align_y": "bottom", "coordinates": [0, 0]},
                                     "yes_no_menu": {"default_width": 20, "default_height": None, "align_x": "right", "align_y": "bottom", "coordinates": [0, 0]},
                                     "sub_menu": {"default_width": 20, "default_height": None, "align_x": "right", "align_y": "bottom", "coordinates": [0, 0]}}

    def add_player_avatar(self, player_object):
        self.player_avatar = player_object

    def add_character_avatar(self, character_name, character_object):
        self.npc_avatar_list[character_name] = character_object

    def add_prop_avatar(self, prop_name, prop_object):
        self.prop_avatar_list[prop_name] = prop_object

    def add_decoration_avatar(self, decoration_name, decoration_object):
        self.decoration_avatar_list[decoration_name] = decoration_object

    def tick(self):
        self.clock.tick(self.FPS)

    def add_menu_avatar(self, menu_avatar_name, menu_avatar_object):
        self.menu_avatar_data_list[menu_avatar_name] = menu_avatar_object

    def draw_npc(self, npc_name):
        camera_x = -self.camera[0]
        camera_y = -self.camera[1]
        chosen_npc_avatar = self.npc_avatar_list[npc_name]
        npc_loc_x = camera_x + (self.npc_avatar_list[npc_name].image_x - 1) * self.square_size[0]
        npc_loc_y = camera_y + (self.npc_avatar_list[npc_name].image_y - 1) * self.square_size[1] - chosen_npc_avatar.image_offset_y
        self.screen.blit(chosen_npc_avatar.spritesheet.get_image(chosen_npc_avatar.current_image_x, chosen_npc_avatar.current_image_y), (npc_loc_x, npc_loc_y))

    def draw_player(self):
        player = self.player_avatar
        play_loc_x = (player.image_x * self.square_size[0]) - self.square_size[0]
        play_loc_y = player.image_y * self.square_size[1] - (self.square_size[1] + player.image_offset_y)
        self.screen.blit(player.spritesheet.get_image(player.current_image_x, player.current_image_y), [play_loc_x, play_loc_y])

    def draw_bg(self, current_room):
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(0, 0, self.resolution[0], self.resolution[1]))
        camera_x = -self.camera[0]
        camera_y = -self.camera[1]
        room = self.game_data.room_data_list[current_room]
        for plot in room.plot_list.keys():
            selected_plot = room.plot_list[plot]
            plot_location_x = room.plot_size_x * (selected_plot.plot_x - 1) * self.square_size[0]
            plot_location_y = room.plot_size_y * (selected_plot.plot_y - 1) * self.square_size[1]
            self.screen.blit(selected_plot.background_map, (camera_x + plot_location_x, camera_y + plot_location_y))

    def draw_all(self, drawables_list, current_room):
        self.draw_bg(current_room)
        for drawable in drawables_list:

            if drawable[0].type == "Player":
                self.draw_player()
            elif drawable[0].type == "Npc":
                self.draw_npc(drawable[0].name)

    def draw_special_menu(self, menu_name, menu_info, x, y):
        menu_avatar = self.menu_avatar_data_list[menu_name + "_avatar"]
        final_menu_text = menu_avatar.get_menu_text_drawing_instructions(menu_info)
        full_menu = self.compile_special_menu(final_menu_text, None, menu_avatar.overlay_image)
        self.screen.blit(full_menu, (x, y))

    def draw_sub_menu(self, menu_name, menu_info, x, y):
        menu_avatar = self.menu_avatar_data_list[menu_name + "_avatar"]
        final_menu_text = menu_avatar.get_menu_text_drawing_instructions(menu_info)
        full_menu = self.compile_special_menu(final_menu_text, None, menu_avatar.overlay_image)
        self.screen.blit(full_menu, (x, y))

    def compile_special_menu(self, text_print_list, image_print_list, overlay):
        final_image = pygame.Surface((overlay.get_width(), overlay.get_height()))
        final_image.blit(overlay, [0, 0])
        # print("using compile")

        for item in text_print_list:
            my_font = pygame.font.Font(self.font_file, GameSettings.FONT_SIZE)
            item_text = my_font.render(item.text, True, (0, 0, 0))
            final_image.blit(item_text, [item.x, item.y])

        if image_print_list:
            for item in image_print_list:
                image = item.image
                final_image.blit(image, [item.x, item.y])

        return final_image

    def compile_menu(self, text_print_list, image_print_list, overlay):
        final_image = pygame.Surface((overlay.image.get_width(), overlay.image.get_height()))
        final_image.blit(overlay.image, [0, 0])
        for item in text_print_list:
            my_font = pygame.font.Font(self.font_file, GameSettings.FONT_SIZE)
            item_text = my_font.render(item.text, True, (0, 0, 0))
            final_image.blit(item_text, [item.x, item.y])

        if image_print_list:
            for item in image_print_list:
                image = item.image
                final_image.blit(image, [item.x, item.y])

        return final_image

    def set_camera(self, player_ghost_x, player_ghost_y):
        self.camera[0] = -(self.player_avatar.image_x - player_ghost_x) * 24
        self.camera[1] = -(self.player_avatar.image_y - player_ghost_y) * 24

    def set_menu_display_coordinates(self, name):
        for item in self.menu_display_details:
            menu_avatar = self.menu_avatar_data_list[name + "_avatar"]
            x_instruction = self.menu_display_details[name]["align_x"]
            y_instruction = self.menu_display_details[name]["align_y"]
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
            elif y_instruction == "top":
                y = 0 + GameSettings.RESOLUTION[1] / GameSettings.MENUEDGE
            elif y_instruction == "bottom":
                y = GameSettings.RESOLUTION[1] - menu_avatar.spritesheet_height - GameSettings.RESOLUTION[1] / GameSettings.MENUEDGE
            else:
                y = y_instruction

            self.menu_display_details[name]["coordinates"][0] = x
            self.menu_display_details[name]["coordinates"][1] = y

    def update_sub_menu_display_details(self, menu_name, master_menu):
        selected_menu_avatar = self.menu_avatar_data_list[menu_name + "_avatar"]
        self.menu_display_details[menu_name]["coordinates"][0] = self.menu_display_details[master_menu]["coordinates"][0] - selected_menu_avatar.spritesheet_width - 5
        self.menu_display_details[menu_name]["coordinates"][1] = self.menu_display_details[master_menu]["coordinates"][1]

    def get_player_avatar(self):
        return self.player_avatar

    def get_npc_avatar(self, name):
        return self.npc_avatar_list[name]

    def get_drawables_list(self, player_location, feature_locations):
        drawables_list = []

        for npc in feature_locations:
            npc_avatar = self.get_npc_avatar(npc[0])
            drawables_list.append([npc_avatar, npc[1], npc_avatar.drawing_priority])

        player_avatar = self.get_player_avatar()
        drawables_list.append([player_avatar, player_location[0], player_avatar.drawing_priority])

        drawing_order = sorted(drawables_list, key=lambda x: (x[1], x[2]))

        return drawing_order

class AnimationManager(object):
    def __init__(self, gv_input):
        self.gv = gv_input

    def perform_animation(self, animator):
        animation_result = (animator.animation_list[animator.current_animation].animate())
        animator.current_image_x = animation_result[2]
        animator.current_image_y = animation_result[3]
        self.gv.camera[0] += animation_result[0]
        self.gv.camera[1] += animation_result[1]
        complete = animation_result[4]
        if complete:
            animator.currently_animating = False
            animator.current_animation = None


class MenuDrawer(object):
    def __init__(self, gv_input):
        self.font_size = GameSettings.FONT_SIZE
        print("using this")
