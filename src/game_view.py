from keyboard_manager_page import *
from avatar_page import PlayerAvatar
from definitions import Direction, GameSettings, Types
from position_manager import Room2, PositionManager

class GameView(object):
    def __init__(self, game_data, game_state, menu_drawer):
        self.game_data = game_data  # type: GameData
        self.gs = game_state  # type: GameState
        self.menu_drawer = menu_drawer  # type: MenuDrawer
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

        self.player_avatar = PlayerAvatar(self.base_locator_x, self.base_locator_y)

    def tick(self):
        self.clock.tick(self.FPS)

    def draw_npc(self, npc_name):
        camera_x = -self.camera[0]
        camera_y = -self.camera[1]
        chosen_npc_avatar = self.game_data.npc_avatar_list[npc_name]
        npc_loc_x = camera_x + (self.game_data.npc_avatar_list[npc_name].image_x - 1) * self.square_size[0]
        npc_loc_y = camera_y + (self.game_data.npc_avatar_list[npc_name].image_y - 1) * self.square_size[1] - chosen_npc_avatar.image_offset_y
        self.screen.blit(chosen_npc_avatar.spritesheet.get_image(chosen_npc_avatar.current_image_x, chosen_npc_avatar.current_image_y), (npc_loc_x, npc_loc_y))

    def draw_player(self):
        player = self.game_data.player_avatar
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
        menu_avatar = self.gs.ms.menu_avatar_data_list[menu_name + "_avatar"]
        final_menu_text = menu_avatar.get_menu_text_drawing_instructions(menu_info)
        full_menu = self.compile_special_menu(final_menu_text, None, menu_avatar.overlay_image)
        self.screen.blit(full_menu, (x, y))

    def draw_sub_menu(self, menu_name, menu_info, x, y):
        menu_avatar = self.gs.ms.menu_avatar_data_list[menu_name + "_avatar"]
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
        self.camera[0] = -(self.game_data.player_avatar.image_x - player_ghost_x) * 24
        self.camera[1] = -(self.game_data.player_avatar.image_y - player_ghost_y) * 24


class MenuDrawer(object):
    def __init__(self, gv_input):
        self.font_size = GameSettings.FONT_SIZE
        print("using this")
