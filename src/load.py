import csv
import os

import pygame

from feature_avatar_view_page import PlayerAvatar
from definitions import Direction, Types, GameSettings
from feature_ghost_data_page import PlayerGhost
from item_page import *
from input_manager_controller_page import InGameKeyboardManager, InMenuKeyboardManager, InSceneKeyboardManager
from menu_avatars_view_page import MenuAvatar
from position_manager_state_page import Door, Consolidated


def init_game(g):

    pygame.key.set_repeat()
    # g.game_events.initiate_timers()

    if g.gs.new_game:

        new_game_procedures(g.game_controller, g.gs)
    else:
        continue_game_procedures(g.game_controller, g.gs)

    install_all_data(g.game_controller, g.gs)


def new_game_procedures(gc, gs):
    pass

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
        gs.gd.add_room_data("Test_Room", (Consolidated("Test_Room", 20, 20, 1, 1)))
        gs.gd.add_room_data("Staging_Area", (Consolidated("Staging_Area", 7, 9, 1, 1)))
        gs.gd.add_room_data("Cave", (Consolidated("Cave", 20, 20, 1, 1)))
        gs.gd.add_room_data("My_House", (Consolidated("My_House", 6, 4, 1, 1)))
        gs.gd.add_room_data("Bird_Room", (Consolidated("Bird_Room", 20, 20, 1, 1)))
        gs.gd.add_room_data("Marsh", (Consolidated("Marsh", 50, 50, 1, 1)))
        gs.gd.add_room_data("Trophy_Room", (Consolidated("Trophy_Room", 9, 30, 1, 1)))
        gs.gd.add_room_data("Aviary_Room", (Consolidated("Aviary_Room", 9, 30, 1, 1)))
        gs.gd.add_room_data("Zoo_Room", (Consolidated("Zoo_Room", 9, 30, 1, 1)))
        gs.gd.add_room_data("Beach", (Consolidated("Beach", 50, 50, 1, 1)))

    def install_features(gc, gs):
        gs.add_player_ghost(PlayerGhost(gc.game.gs, 1, 3))
        for room_name in gs.gd.room_data_list.keys():
            feature_file_name = "assets/rooms/" + room_name + "/" + room_name + "_" + "feature_import_dict.csv"
            if os.path.isfile(feature_file_name):
                gc.import_features_from_csv(feature_file_name)
            map_objects_file_name = "assets/rooms/" + room_name + "/" + room_name + "_1_1_objects.csv"
            if os.path.isfile(map_objects_file_name):
                gc.import_map_objects_from_csv(map_objects_file_name)
            npc_file_name = "assets/rooms/" + room_name + "/" + room_name + "_" + "NPC_import_dict.csv"
            if os.path.isfile(npc_file_name):
                gc.import_npcs_from_csv(npc_file_name)
            deco_file_name = "assets/rooms/" + room_name + "/" + room_name + "_" + "deco_import_dict.csv"
            if os.path.isfile(deco_file_name):
                gc.import_features_from_csv(deco_file_name)

    def install_doors(gc, gs):
        gc.position_manager.add_door("Ladder", "Staging_Area", "Test_Room", 2, 6, 13, 16)
        gc.position_manager.add_door("Ladder", "Staging_Area", "Marsh", 3, 6, 21, 33)
        gc.position_manager.add_door("Ladder", "Staging_Area", "Cave", 4, 6, 8, 10)
        gc.position_manager.add_door("Ladder", "Staging_Area", "Beach", 5, 6, 35, 35)
        gc.position_manager.add_door("Passage", "Test_Room", "Cave", 8, 12, 8, 12)
        gc.position_manager.add_door("Double_back", "Staging_Area", "Marsh", 5, 2, 22, 17)
        gc.position_manager.add_door("Passage", "Test_Room", "Cave", 15, 10, 15, 10)
        gc.position_manager.add_door("Ladder", "Cave", "Cave", 15, 8, 5, 7)
        gc.position_manager.add_door("Feature_Passage", "Test_Room", "My_House", 5, 17, 2, 5)
        gc.position_manager.add_door("Ladder", "Test_Room", "Bird_Room", 8, 10, 4, 4)
        gc.position_manager.add_door("Ladder", "Staging_Area", "Bird_Room", 6, 6, 15, 15)
        gc.position_manager.add_door("Double_back", "Bird_Room", "Cave", 4, 8, 8, 5)
        gc.position_manager.add_door("Double_back", "Bird_Room", "Marsh", 16, 1, 2, 19)
        gc.position_manager.add_door("Double_back", "Beach", "Beach", 34, 19, 1, 16)
        gc.position_manager.add_door("Passage", "Staging_Area", "Trophy_Room", 2, 2, 5, 30)
        gc.position_manager.add_door("Passage", "Staging_Area", "Aviary_Room", 4, 2, 5, 30)
        gc.position_manager.add_door("Passage", "Staging_Area", "Zoo_Room", 6, 2, 5, 30)

    def install_spritesheets(gc, gs):
        # gc.game_data.add_spritesheet("player_base_spritesheet", Spritesheet("player_base_spritesheet", "assets/spritesheets/Player_CS.png", 32, 40))
        pass

    def install_player_avatar(gc, gs):
        gs.gv.add_player_avatar(PlayerAvatar(gc.game_view.base_locator_x, gc.game_view.base_locator_y))
        pass

    def install_avatar_all(gc, gs):
        npc_name_list = gs.get_all_feature_unique_names()
        for npc_item in npc_name_list:
            related_ghost = gc.gs.feature_ghost_list[npc_item]
            gc.gs.gv.install_element_avatar(related_ghost)

        deco_name_list = gs.get_all_deco_unique_names()
        for deco_item in deco_name_list:
            related_ghost = gc.gs.deco_ghost_list[deco_item]
            gc.gs.gv.install_element_avatar(related_ghost)

    def install_triggers(gc, gs):
        gc.trigger_manager.setup_trigger_list()

    def spawn_first_room(gc, gs):
        gc.position_manager.spawn_all_initial_room_elements(gs.get_room(gs.current_room))

    def install_keyboard_managers(gc, gs):
        gc.game_view.game_data.add_keyboard_manager_data(InGameKeyboardManager.ID, InGameKeyboardManager(gc))
        gc.game_view.game_data.add_keyboard_manager_data(InMenuKeyboardManager.ID, InMenuKeyboardManager(gc))
        gc.game_view.game_data.add_keyboard_manager_data(InSceneKeyboardManager.ID, InSceneKeyboardManager(gc))

    def set_initial_keyboard_manager(gc, gs):
        gc.set_active_keyboard_manager(InGameKeyboardManager.ID)

    def install_temp_items(gc, gs):
        items_to_install = [Cheese, Milk, Cream, Banana, Apple, Orange, Mike, Spoon, Mouse, Match, Game, Card, Pizza, Meat, Egg]
        q = 1
        for item in items_to_install:
            gs.gd.add_item_data(item.NAME, item(gc))
            gs.acquire_item(item.NAME, q)
            q *= 3

    def install_key_items(gc, gs):
        items_to_install = [Hammer, Permit, Pickaxe, Shovel, Wrench, MermaidCrown, GhostEye, Axe]
        for item in items_to_install:
            gs.gd.add_key_item_data(item.NAME, item(gc))
            gs.acquire_key_item(item.NAME)

    def install_bird_pages(gc, gs): #TODO: Keep working on this
        gc.import_pages_from_csv("assets/import_data/pages_import_dict.csv")
        pages_to_install = gc.import_pages_from_csv("assets/import_data/pages_import_dict.csv")
        for page in pages_to_install:
            if page["segment"] == "top":
                gs.gd.add_bird_page_data(page["bird"] + page["segment"], BirdPage(gc, page["bird"], page["segment"], page["colour"], page["size"], page["call"], None))
            elif page["segment"] == "bottom":
                gs.gd.add_bird_page_data(page["bird"] + page["segment"], BirdPage(gc, page["bird"], page["segment"], None, None, None, page["approach"]))

        for page in gs.gd.bird_page_data_list.keys():
            gc.inventory_manager.get_page(gs.gd.bird_page_data_list[page].page_name)


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
        gc.position_manager.fill_room_grid(gc.game.gs.current_room)
        gc.position_manager.add_player_to_grid(gc.game.gs.current_room)

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
    install_bird_pages(gc, gs)
    install_menus(gc, gs)
    install_goals(gc, gs)
    install_tileset(gc, gs)
    install_spritesheets(gc, gs)
    install_rooms(gc, gs)
    install_features(gc, gs)
    install_player_avatar(gc, gs)
    install_avatar_all(gc, gs)
    install_doors(gc, gs)
    install_triggers(gc, gs)
    spawn_first_room(gc, gs)
    set_camera_position(gc, gs)
    initiate_mixer()
    fill_initial_room(gc, gs)




