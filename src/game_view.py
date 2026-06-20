import copy

from animations_page_view_page import IndependentAnimation, BirdDisappearAnimation

from graphics import BuiltOverlay
from input_manager_controller_page import *
from feature_avatar_view_page import NPCAvatar, TreeAvatar, OldgodAvatar, HouseAvatar, PropAvatar, DecoAvatar, BirdAvatar
from definitions import GameSettings, Types
from menu_avatars_view_page import QuizMenuAvatar, ConversationOptionsMenuAvatar, ChatMenuAvatar, OutfitMenuAvatar, MapMenuAvatar, GalleryMenuAvatar, PictureMenuAvatar, StatMenuAvatar, GameActionDialogueMenuAvatar, NumberSelectionMenuAvatar, GuideMenuAvatar
from spritesheet import Spritesheet
if TYPE_CHECKING:
    from game_state import GameData, GameState

class OutfitManager(object): #TODO: work on this
    def __init__(self, gc):
        self.gc = gc
        self.character_frame_x = 32
        self.character_frame_y = 48
        self.red_shirt = Spritesheet("player_base_spritesheet", "assets/spritesheets/player_spritesheets/player_red_shirt_spritesheet.png", self.character_frame_x, self.character_frame_y)
        self.green_shirt = Spritesheet("player_base_spritesheet", "assets/spritesheets/player_spritesheets/player_green_shirt_spritesheet.png", self.character_frame_x, self.character_frame_y)
        self.lab_coat = Spritesheet("player_base_spritesheet", "assets/spritesheets/player_spritesheets/player_lab_coat_spritesheet.png", self.character_frame_x, self.character_frame_y)

    def put_on_outfit(self, outfit_name):
        outgoing_outfit = copy.copy(self.gc.gs.current_outfit)
        self.gc.gs.current_outfit = outfit_name
        self.gc.gs.revert_outfit = outfit_name
        player = self.gc.game_view.get_player_avatar()
        image = Spritesheet("Player_base_spritesheet", "assets/spritesheets/player_spritesheets/player_" + outfit_name + "_spritesheet.png",  32, 48)
        player.spritesheet = image

    def put_on_temporary_outfit(self, outfit_name):
        outgoing_outfit = copy.copy(self.gc.gs.current_outfit)
        self.gc.gs.revert_outfit = outgoing_outfit
        self.gc.gs.current_outfit = outfit_name
        player = self.gc.game_view.get_player_avatar()
        image = Spritesheet("Player_base_spritesheet", "assets/spritesheets/player_spritesheets/player_" + outfit_name + "_spritesheet.png",  32, 48)
        player.spritesheet = image


class GameView(object):
    def __init__(self, game_data, game_state):
        self.game_data = game_data  # type: GameData
        self.gs = game_state  # type: GameState
        self.animation_manager = AnimationManager(self)
        self.clock = pygame.time.Clock()
        self.resolution = GameSettings.RESOLUTION
        self.FPS = 64
        self.square_size = [GameSettings.TILESIZE, GameSettings.TILESIZE]
        self.base_locator_x = ((self.resolution[0] - self.square_size[0]) / self.square_size[0]) / 2 + 1
        self.base_locator_y = (((self.resolution[1] - self.square_size[1]) / self.square_size[1]) / 2 + 1) - GameSettings.SCREEN_OFFSET_Y
        self.avatar_classes = {Types.BIRD: BirdAvatar, Types.NPC: NPCAvatar, Types.PROP: PropAvatar, Types.HOUSE: HouseAvatar, "Tree": TreeAvatar, "Oldgod": OldgodAvatar, "House": HouseAvatar, Types.DECO: DecoAvatar}

        self.camera = [0, 0]
        self.screen = pygame.display.set_mode(self.resolution)
        self.font_file = "assets/fonts/PressStart.ttf"

        self.font_medium = pygame.font.Font(self.font_file, GameSettings.FONT_SIZE)

        self.tile_frame = 0
        self.night_filter = pygame.Surface(pygame.Rect((0, 0, self.resolution[0], self.resolution[1])).size)
        self.sky_change_increments = 6
        self.fully_dark_hours = 4
        self.sky_change_degree = 15

        self.player_avatar = None
        self.menu_avatar_data_list = {}
        self.feature_avatar_list = {}
        self.deco_avatar_list = {}
        self.menu_avatar_names = {"quiz_menu": QuizMenuAvatar,
                                 "conversation_options_menu": ConversationOptionsMenuAvatar,
                                 "chat_menu": ChatMenuAvatar,
                                  "outfit_menu": OutfitMenuAvatar,
                                  "map_menu": MapMenuAvatar,
                                  "guide_menu": GuideMenuAvatar,
                                  "picture_menu": PictureMenuAvatar,
                                  "gallery_menu": GalleryMenuAvatar,
                                  "stat_menu": StatMenuAvatar,
                                  "number_selection_menu": NumberSelectionMenuAvatar,
                                  "game_action_dialogue_menu": GameActionDialogueMenuAvatar}

    def tick(self):
        self.clock.tick(self.FPS)

    def translate_feature_type(self, type):
        list = None
        if type == Types.NPC:
            list = self.feature_avatar_list
        elif type == Types.DECO:
            list = self.deco_avatar_list
        elif type == Types.PROP:
            list = self.feature_avatar_list
        elif type == Types.HOUSE:
            list = self.feature_avatar_list
        return list

    # region DRAWING FEATURES
    def draw_feature(self, feature_name, feature_type):

        feature_list = self.translate_feature_type(feature_type)
        camera_x = -self.camera[0]
        camera_y = -self.camera[1]
        chosen_avatar = feature_list[feature_name]
        feature_loc_x = camera_x + (feature_list[feature_name].image_x - 1) * self.square_size[0] + feature_list[feature_name].image_offset_x
        feature = camera_y + (feature_list[feature_name].image_y - 1) * self.square_size[1] - chosen_avatar.image_offset_y
        self.screen.blit(chosen_avatar.spritesheet.get_image(chosen_avatar.current_image_x, chosen_avatar.current_image_y), (feature_loc_x, feature))

    def draw_player(self):
        player = self.player_avatar
        play_loc_x = (player.image_x * self.square_size[0]) - (self.square_size[0] - player.image_offset_x)
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
            self.screen.blit(selected_plot.background_map[self.tile_frame], (camera_x + plot_location_x, camera_y + plot_location_y))

    def draw_independent_animation(self, animation_ob):
        camera_x = -self.camera[0]
        camera_y = -self.camera[1]
        anim_loc_x = camera_x + (animation_ob.image_x - 1) * self.square_size[0] + animation_ob.image_offset_x
        anim_loc_y = camera_y + (animation_ob.image_y - 1) * self.square_size[1] - animation_ob.image_offset_y
        self.screen.blit(animation_ob.spritesheet.get_image(animation_ob.current_image_x, animation_ob.current_image_y), (anim_loc_x, anim_loc_y))


    def draw_all(self, drawables_list, current_room):
        self.draw_bg(current_room)
        for drawable in drawables_list:
            if not drawable[0].feature_type == "Player":
                pass
        for drawable in drawables_list:

            if drawable[0].feature_type == "Player":
                self.draw_player()
            elif drawable[0].feature_type == Types.INDANIM:
                self.draw_independent_animation(drawable[0])
            else:
                self.draw_feature(drawable[0].unique_name, drawable[0].feature_type)

    def get_drawables_list(self, player_location, feature_locations, deco_locations, anim_locations):
        drawables_list = []
        print(deco_locations)
        for deco in deco_locations:
            print("what's going on here??")

        for deco in deco_locations: #TODO: Fix this
            deco_avatar = self.get_deco_avatar(deco[0])
            # print("avatar", deco_avatar)
            drawables_list.append([deco_avatar, deco[1], deco_avatar.drawing_priority])

        for npc in feature_locations:
            npc_avatar = self.get_npc_avatar(npc[0])
            drawables_list.append([npc_avatar, npc[1], npc_avatar.drawing_priority])

        for ind_anim in anim_locations:
            drawables_list.append([ind_anim[0], ind_anim[1], ind_anim[2]])

        player_avatar = self.get_player_avatar()
        drawables_list.append([player_avatar, player_location[0], player_avatar.drawing_priority])

        drawing_order = sorted(drawables_list, key=lambda x: (x[1], x[2]))

        return drawing_order
    # endregion

    # region MENU AVATARS and DRAWING
    def add_menu_avatar(self, menu_avatar_name, menu_avatar_object):
        self.menu_avatar_data_list[menu_avatar_name] = menu_avatar_object

    def build_overlay_image(self, name, x_size, y_size, header=None):
        image = BuiltOverlay(name, x_size, y_size, header=header).build_overlay()
        return image

    def draw_special_menu(self, menu_name, menu_info, x, y):
        menu_avatar = self.menu_avatar_data_list[menu_name + "_avatar"]
        final_menu_text = menu_avatar.get_menu_text_drawing_instructions(menu_info)
        final_menu_images = menu_avatar.get_menu_image_drawing_instructions(menu_info)

        # compile menu
        final_image = pygame.Surface((menu_avatar.overlay_image.get_width(), menu_avatar.overlay_image.get_height()))
        final_image.blit(menu_avatar.overlay_image, [0, 0])

        if final_menu_images:
            for item in final_menu_images:
                image = item.image
                final_image.blit(image, [item.x, item.y])

        for item in final_menu_text:
            my_font = pygame.font.Font(self.font_file, GameSettings.FONT_SIZE)
            item_text = my_font.render(item.text, True, (0, 0, 0))
            final_image.blit(item_text, [item.x, item.y])



        full_menu = final_image

        self.screen.blit(full_menu, (x, y))

    def compile_special_menu(self, text_display_list, image_display_list, overlay):
        final_image = pygame.Surface((overlay.get_width(), overlay.get_height()))
        final_image.blit(overlay, [0, 0])
        for item in text_display_list:
            my_font = pygame.font.Font(self.font_file, GameSettings.FONT_SIZE)
            item_text = my_font.render(item.text, True, (0, 0, 0))
            final_image.blit(item_text, [item.x, item.y])

        if image_display_list:
            for item in image_display_list:
                image = item.image
                final_image.blit(image, [item.x, item.y])

        return final_image

    def set_menu_display_coordinates(self, name):
        name = name + "_avatar"
        menu_avatar = self.menu_avatar_data_list[name]
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

    def update_sub_menu_display_details(self, menu_name, master_menu, information_from_ghost):
        selected_menu_avatar = self.menu_avatar_data_list[menu_name + "_avatar"]
        selected_menu_avatar.fill_out_menu_info(information_from_ghost)
        selected_menu_display_details = selected_menu_avatar.menu_display_details

        master_menu_avatar = self.menu_avatar_data_list[master_menu + "_avatar"]
        master_menu_display_details = master_menu_avatar.menu_display_details

        selected_menu_display_details["coordinates"][0] = master_menu_display_details["coordinates"][0] - selected_menu_avatar.spritesheet_width - 5
        selected_menu_display_details["coordinates"][1] = master_menu_display_details["coordinates"][1]

    def update_menu_display_details(self, menu_name, information_from_ghost):
        selected_menu_avatar = self.menu_avatar_data_list[menu_name + "_avatar"]
        selected_menu_avatar.fill_out_menu_info(information_from_ghost)


    # endregion

    # region CAMERA
    def set_camera(self, player_ghost_x, player_ghost_y):
        self.camera[0] = -(self.player_avatar.image_x - player_ghost_x) * GameSettings.TILESIZE
        self.camera[1] = -(self.player_avatar.image_y - player_ghost_y) * GameSettings.TILESIZE

    def manually_update_camera(self, x_change, y_change):
        self.camera[0] += (x_change * GameSettings.TILESIZE)
        self.camera[1] += (y_change * GameSettings.TILESIZE)

    def slide_camera(self, x_change, y_change):
        self.camera[0] += x_change
        self.camera[1] += y_change
    # endregion

    # region PLAYER AVATAR
    def add_player_avatar(self, player_object):
        self.player_avatar = player_object

    def get_player_avatar(self):
        return self.player_avatar

    def update_player_avatar_location(self, player_ghost_x, player_ghost_y):
        self.get_player_avatar().x_image = self.base_locator_x * player_ghost_x
        self.get_player_avatar().y_image = self.base_locator_y * player_ghost_y

    def walk_player_avatar(self, direction):
        if direction == Direction.DOWN:
            self.player_avatar.initiate_animation("walk_front")
        elif direction == Direction.UP:
            self.player_avatar.initiate_animation("walk_up")
        elif direction == Direction.LEFT:
            self.player_avatar.initiate_animation("walk_left")
        elif direction == Direction.RIGHT:
            self.player_avatar.initiate_animation("walk_right")
    # endregion

    #region FEATURE AVATARS
    def get_npc_avatar(self, name):
        return self.feature_avatar_list[name]

    def get_deco_avatar(self, name):
        return self.deco_avatar_list[name]

    def add_npc_avatar(self, character_name, character_object):
        self.feature_avatar_list[character_name] = character_object

    def add_deco_avatar(self, deco_name, deco_object):
        self.deco_avatar_list[deco_name] = deco_object

    def change_feature_avatar_facing(self, name, direction):
        self.get_npc_avatar(name).face_feature(direction)

    def walk_feature_avatar(self, name, direction):
        feature_avatar = self.feature_avatar_list[name]
        if direction == Direction.DOWN:
            feature_avatar.initiate_animation("walk_front")
        elif direction == Direction.UP:
            feature_avatar.initiate_animation("walk_up")
        elif direction == Direction.LEFT:
            feature_avatar.initiate_animation("walk_left")
        elif direction == Direction.RIGHT:
            feature_avatar.initiate_animation("walk_right")
    #endregion

    # region INDEPENDENT ANIMATION
    def get_independent_anim_locations(self):
        anim_location_list = []
        for anim in self.animation_manager.active_independent_animations.values():
            anim_location_list.append([anim, anim.image_y, anim.image_x])
        return anim_location_list

    def trigger_independent_animation(self, animation_type, animation_name, bird_unique_name, room, drawing_priority, image_x, image_y, image_offset_x, image_offset_y):
        self.animation_manager.active_independent_animations[animation_name] = (self.animation_manager.independent_animation_name_translator[animation_type](animation_name, bird_unique_name, room, drawing_priority, image_x, image_y, image_offset_x, image_offset_y))

    def complete_independent_animation(self, animation_name):
        self.animation_manager.active_independent_animations.pop(animation_name)

    # endregion

    def perform_animation(self, animator):
        animation_result = (animator.animation_list[animator.current_animation].animate())
        animator.current_image_x = animation_result[2]
        animator.current_image_y = animation_result[3]
        self.camera[0] += animation_result[0]
        self.camera[1] += animation_result[1]
        complete = animation_result[4]
        if complete:
            animator.currently_animating = False
            animator.current_animation = None


class AnimationManager(object):
    def __init__(self, gv_input):
        self.gv = gv_input # type:GameView
        self.independent_animation_name_translator = {"bird_disappear_animation": IndependentAnimation, "disappear_animation": BirdDisappearAnimation}
        self.independent_animation_trigger_queue = []
        self.active_independent_animations = {}

    def perform_player_animation(self, animator):
        animation_result = (animator.animation_list[animator.current_animation].animate())
        animator.current_image_x = animation_result[2]
        animator.current_image_y = animation_result[3]
        self.gv.camera[0] += animation_result[0]
        self.gv.camera[1] += animation_result[1]
        complete = animation_result[4]
        if complete:
            animator.currently_animating = False
            animator.current_animation = None

    def perform_feature_animation(self, animator):

        wrap_up = False
        animation_result = (animator.animation_list[animator.current_animation].animate())
        animator.current_image_x = animation_result[2]
        animator.current_image_y = animation_result[3]
        animator.move_avatar(animation_result[0], animation_result[1])
        complete = animation_result[4]
        if complete:
            animator.currently_animating = False
            animator.current_animation = None
            wrap_up = True
        return wrap_up

    def perform_scene_animation(self, scene_animation):
        wrap_up = False
        animation_result = scene_animation.animate()
        self.gv.slide_camera(animation_result[0], animation_result[1])
        complete = animation_result[2]
        if complete:
            wrap_up = True
        return wrap_up, animation_result[3]