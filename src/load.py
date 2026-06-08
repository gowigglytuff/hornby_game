import csv
import os

import pygame

from feature_avatar_view_page import PlayerAvatar
from definitions import Direction, Types, GameSettings
from feature_ghost_data_page import PlayerGhost
from item_page import *
from input_manager_controller_page import InGameKeyboardManager, InMenuKeyboardManager
from menu_avatars_view_page import MenuAvatar
from position_manager_state_page import Ringside, Door, Consolidated


def init_game(g):

    pygame.key.set_repeat()
    # g.game_events.initiate_timers()

    if g.game_state.new_game:

        new_game_procedures(g.game_controller, g.game_state)
    else:
        continue_game_procedures(g.game_controller, g.game_state)

    install_all_data(g.game_controller, g.game_state)


def new_game_procedures(gc, gs):
    gc.import_features_from_csv("assets/import_data/feature_import_dict.csv")
    gc.import_npcs_from_csv("assets/import_data/NPC_import_dict.csv")
    gc.import_features_from_csv("assets/import_data/Deco_import.csv")
    gs.add_player_ghost(PlayerGhost(gc.game.game_state, 1, 1))
    tree_coords = [(24,10), (22,7), (20,5), (17,5), (15,4), (16,2), (20,2), (24,2), (28,10), (31,10), (33,8), (32,5), (36,3), (38,10), (35,13), (35,16), (40,14), (43,11), (45,8), (47,5), (49,3), (49,7), (49,11), (49,13), (49,14),(46,14),(39,18), (38,18)]
    # for tree_coord in tree_coords:
    #     feature_type = gs.type_translator["Prop"]
    #     feature_subtype = gs.sub_type_translator["Tree"]
    #     unique_name = "Pine" + "_" + str(GameSettings.get_unique_ID())
    #     feature_ghost_object = gs.ghost_classes["Tree"](feature_type, feature_subtype, "Pine", unique_name, "None", gs, "Marsh", tree_coord[0], tree_coord[1], Direction.DOWN, 1, 1, 1, 1, "yes", "Hi")
    #     gs.add_feature_ghost(unique_name, feature_ghost_object)

    room_name = "Marsh"
    plot_x = 1
    plot_y = 1
    csv = read_csv("assets/room_csv/feature_csv/" + room_name + "_" + str(plot_x) + "_" + str(plot_y) + "_" + "objects.csv")

    feature_reference_dict = {0: "Pine", 1: "Apple_Tree", 2: "Oak", 3: "Arbutus"}

    feature_list = []

    row_counter = 0
    for row in csv:
        row_counter += 1
        item_counter = 0
        for item in row:
            item_counter += 1
            if item in feature_reference_dict.keys():
                x = item_counter
                y = row_counter
                feature_list.append((x, y, feature_reference_dict[item]))
                print(feature_reference_dict[item], x, y)

    for item in feature_list:
        feature_type = gs.type_translator["Prop"]
        feature_subtype = gs.sub_type_translator["Tree"]
        unique_name = item[2] + "_" + str(GameSettings.get_unique_ID())
        feature_ghost_object = gs.ghost_classes["Tree"](feature_type, feature_subtype, item[2], unique_name, "None", gs, "Marsh", item[0], item[1], Direction.DOWN, 1, 1, 1, 1, "yes", "Hi")
        gs.add_feature_ghost(unique_name, feature_ghost_object)


def access_csv(x, y, csv):
    return csv[y][x]

def read_csv(filename):
    map = []
    int_map = []
    with open(os.path.join(filename), mode='r', encoding='utf-8-sig') as data:
        data = csv.reader(data, delimiter=',')
        for row in data:
            map.append(list(row))
    for row in map:
        int_list = [int(i) for i in row]
        int_map.append(int_list)
    return int_map


def continue_game_procedures(gc, gs):
    pass


def install_all_data(gc, gs):

    def install_rooms(gc, gs):
        gs.gd.add_room_data(Ringside.ID, (Ringside()))
        gs.gd.add_room_data("Test_Room", (Consolidated("Test_Room", 20, 20, 1, 1)))
        gs.gd.add_room_data("Staging_Area", (Consolidated("Staging_Area", 7, 7, 1, 1)))
        gs.gd.add_room_data("Cave", (Consolidated("Cave", 20, 20, 1, 1)))
        gs.gd.add_room_data("My_House", (Consolidated("My_House", 6, 4, 1, 1)))
        gs.gd.add_room_data("Bird_Room", (Consolidated("Bird_Room", 20, 20, 1, 1)))
        gs.gd.add_room_data("Marsh", (Consolidated("Marsh", 50, 50, 1, 1)))


    def install_doors(gc, gs):
        gs.gd.add_door_data("Ladder", "Staging_Area", "Test_Room", 2, 6, 13, 16)
        gs.gd.add_door_data("Ladder", "Staging_Area", "Marsh", 3, 6, 23, 15)
        gs.gd.add_door_data("Ladder", "Staging_Area", "Cave", 4, 6, 8, 10)
        gs.gd.add_door_data("Passage", "Test_Room", "Cave", 8, 12, 8, 12)
        gs.gd.add_door_data("Passage", "Test_Room", "Cave", 15, 10, 15, 10)
        gs.gd.add_door_data("Ladder", "Cave", "Cave", 15, 8, 5, 7)
        gs.gd.add_door_data("Passage", "Test_Room", "My_House", 5, 17, 2, 5)
        gs.gd.add_door_data("Ladder", "Test_Room", "Bird_Room", 8, 10, 4, 4)
        gs.gd.add_door_data("Ladder", "Staging_Area", "Bird_Room", 6, 6, 15, 15)
        gs.gd.add_door_data("Double_back", "Bird_Room", "Cave", 4, 8, 8, 5)
        gs.gd.add_door_data("Double_back", "Bird_Room", "Marsh", 16, 1, 2, 19)

    def install_spritesheets(gc, gs):
        # gc.game_data.add_spritesheet("player_base_spritesheet", Spritesheet("player_base_spritesheet", "assets/spritesheets/Player_CS.png", 32, 40))
        pass

    def install_player_avatar(gc, gs):
        gs.gv.add_player_avatar(PlayerAvatar(gc.game_view.base_locator_x, gc.game_view.base_locator_y))
        pass

    def install_avatar_all(gc, gs):
        npc_name_list = gs.get_all_feature_unique_names()
        for npc_item in npc_name_list:
            related_ghost = gc.game_state.feature_ghost_list[npc_item]
            if related_ghost.feature_subtype == Types.BIRD:
                gs.gv.add_npc_avatar(related_ghost.unique_name, gc.get_avatar_class(related_ghost.feature_subtype)(related_ghost.species, related_ghost.x, related_ghost.y, related_ghost.unique_name, related_ghost.figure_size_x, related_ghost.figure_size_y, related_ghost.spawn_facing))
            else:
                gs.gv.add_npc_avatar(related_ghost.unique_name, gc.get_avatar_class(related_ghost.feature_type)(related_ghost.species, related_ghost.x, related_ghost.y, related_ghost.unique_name, related_ghost.figure_size_x, related_ghost.figure_size_y, related_ghost.spawn_facing))

        deco_name_list = gs.get_all_deco_unique_names()
        for deco_item in deco_name_list:
            related_ghost = gc.game_state.deco_ghost_list[deco_item]
            gs.gv.add_deco_avatar(related_ghost.unique_name, gc.get_avatar_class(related_ghost.feature_type)(related_ghost.species, related_ghost.x, related_ghost.y, related_ghost.unique_name, related_ghost.figure_size_x, related_ghost.figure_size_y, related_ghost.spawn_facing))

    def install_triggers(gc, gs):
        gc.trigger_manager.setup_trigger_list()

    def spawn_first_room(gc, gs):
        gc.position_manager.spawn_all_initial_room_features(gs.get_room(gs.current_room))

    def install_keyboard_managers(gc, gs):
        gc.game_view.game_data.add_keyboard_manager_data(InGameKeyboardManager.ID, InGameKeyboardManager(gc))
        gc.game_view.game_data.add_keyboard_manager_data(InMenuKeyboardManager.ID, InMenuKeyboardManager(gc))

    def set_initial_keyboard_manager(gc, gs):
        gc.set_active_keyboard_manager(InGameKeyboardManager.ID)

    def install_temp_items(gc, gs):
        items_to_install = [Cheese, Milk, Cream, Banana, Apple, Orange, Mike, Spoon, Mouse, Match, Game, Card, Pizza, Meat, Egg]
        q = 1
        for item in items_to_install:
            gs.gd.add_item_data(item.NAME, item(gc))
            gs.acquire_item(item, q)
            q *= 3

    def install_key_items(gc, gs):
        items_to_install = [Hammer, Shovel, Wrench, Axe]
        for item in items_to_install:
            gs.gd.add_key_item_data(item.NAME, item(gc))
            gc.inventory_manager.get_key_item(item)

    def install_menus(gc, gs):
        for ghost in gc.menu_controller.menu_load_list:
            gs.ms.add_menu_ghost(ghost.NAME, ghost(gc))

        for menu in gs.ms.menu_ghost_data_list.values():
            if menu.BASE in gc.game_view.menu_avatar_names.keys():
                avatar_name = menu.BASE + "_avatar"
                items = menu.generate_menu_information_package()
                gs.gv.add_menu_avatar(avatar_name, gc.game_view.menu_avatar_names[menu.BASE](gc, avatar_name, items))
                gs.gv.set_menu_display_coordinates(menu.BASE)

            else:
                avatar_name = menu.BASE + "_avatar"
                items = menu.generate_menu_information_package()
                gs.gv.add_menu_avatar(avatar_name, MenuAvatar(gc, avatar_name, items))

                gs.gv.set_menu_display_coordinates(menu.BASE)

    def install_outfits(gc, gs):
        pass

    def install_tileset(gc, gs):
        pass

    def install_goals(gc, gs):
        pass

    def set_camera_position(gc, gs):
        gs.gv.set_camera(gs.player_ghost.x, gs.player_ghost.y)

    def fill_initial_room(gc, gs):
        gc.position_manager.fill_room_grid(gc.game.game_state.current_room)
        gc.position_manager.add_player_to_grid(gc.game.game_state.current_room)

    def initiate_mixer():
        pygame.mixer.init()
        pygame.mixer.music.load("assets/sound_effects/popping_sound.mp3")
        pygame.mixer.music.load("assets/music/flute_song.mp3")
        # pygame.mixer.music.play(-1)

    install_keyboard_managers(gc, gs)
    set_initial_keyboard_manager(gc, gs)

    install_temp_items(gc, gs)
    install_outfits(gc, gs)
    install_key_items(gc, gs)
    install_menus(gc, gs)
    install_goals(gc, gs)
    install_tileset(gc, gs)
    install_player_avatar(gc, gs)
    install_avatar_all(gc, gs)
    install_spritesheets(gc, gs)
    install_rooms(gc, gs)
    install_doors(gc, gs)
    install_triggers(gc, gs)
    spawn_first_room(gc, gs)
    set_camera_position(gc, gs)
    initiate_mixer()
    fill_initial_room(gc, gs)




