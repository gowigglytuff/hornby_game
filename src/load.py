import pygame

from feature_avatar_view_page import NpcAvatar, PlayerAvatar, TreeAvatar, OldgodAvatar
from definitions import Direction
from feature_ghost_data_page import NpcGhost, PlayerGhost, TreeGhost, OldgodGhost
from item_page import *
from input_manager_controller_page import InGameKeyboardManager, InMenuKeyboardManager
from menu_avatars_view_page import MenuAvatar, ConversationMenuAvatar
from menu_ghosts_data_page import SpecialMenuGhost, StatMenuGhost, StartMenuGhost, KeyInventoryMenuGhost, ConversationOptionsMenuGhost, SuppliesInventoryMenuGhost, GameActionDialogueGhost, SubMenuGhost, UseMenuGhost
# from menu_page import GameActionDialogue, CharacterDialogue, ConversationOptionsMenu, Overlay, KeyInventoryMenu, YesnoMenu, UseMenu
from position_manager_state_page import NewBasicRoom, Ringside, Island, Door, Mountain

from spritesheet import Spritesheet


def init_game(g):

    pygame.key.set_repeat()
    g.game_events.initiate_timers()

    if g.game_state.new_game:

        new_game_procedures(g.game_controller, g.game_state)
    else:
        continue_game_procedures(g.game_controller, g.game_state)

    install_all_data(g.game_controller, g.game_state)


def new_game_procedures(gc, gs):
    gc.import_NPCs_from_csv("assets/import_data/NPC_import.csv")
    gs.add_player_ghost(PlayerGhost(gc.game.game_state, 1, 1))

def continue_game_procedures(gc, gs):
    pass


def install_all_data(gc, gs):

    def install_rooms(gc, gs):
        # gs.gd.add_room_data(NewBasicRoom.ID, (NewBasicRoom()))
        gs.gd.add_room_data(Ringside.ID, (Ringside()))
        gs.gd.add_room_data(Island.ID, (Island()))
        gs.gd.add_room_data(Mountain.ID, (Mountain()))

    def install_doors(gc, gs):
        gs.gd.add_door_data("Ringside_1_3", Door("Ringside", "Island", 1, 3, 6, 2))
        gs.gd.add_door_data("Island_8_2", Door("Island", "Ringside", 8, 2, 1, 3))
        gs.gd.add_door_data("Island_2_2", Door("Island", "Mountain", 2, 2, 11, 12))
        gs.gd.add_door_data("Mountain_5_12", Door("Mountain", "Island", 5, 12, 2, 5))


    def install_spritesheets(gc, gs):
        # gc.game_data.add_spritesheet("player_base_spritesheet", Spritesheet("player_base_spritesheet", "assets/spritesheets/Player_CS.png", 32, 40))
        pass

    def install_player_avatar(gc, gs):
        gs.gv.add_player_avatar(PlayerAvatar(gc.game_view.base_locator_x, gc.game_view.base_locator_y))
        pass

    def install_avatar_all(gc, gs):
        npc_name_list = ["Clown", "Cowboy"]
        for npc_item in npc_name_list:
            related_ghost = gc.game_state.feature_ghost_list[npc_item]
            gs.gv.add_feature_avatar(npc_item, NpcAvatar(npc_item, related_ghost.x, related_ghost.y, related_ghost.unique_id))

        tree_name_list = ["Tree"]
        for tree_item in tree_name_list:
            related_ghost = gc.game_state.feature_ghost_list[tree_item]
            gs.gv.add_feature_avatar(tree_item, TreeAvatar(tree_item, related_ghost.x, related_ghost.y, related_ghost.unique_id))
        god_name_list = ["Oldgod"]
        for god_item in god_name_list:
            related_ghost = gc.game_state.feature_ghost_list[god_item]
            gs.gv.add_feature_avatar(god_item, OldgodAvatar(god_item, related_ghost.x, related_ghost.y, related_ghost.unique_id))

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
        items_to_install = [Hammer, Shovel, Wrench]
        for item in items_to_install:
            gs.gd.add_key_item_data(item.NAME, item(gc))
            gc.inventory_manager.get_key_item(item)

    def install_menus(gc, gs):
        for ghost in gc.game_data.menu_load_list:
            gs.ms.add_menu_ghost(ghost.NAME, ghost(gc))

        for menu in gs.ms.menu_ghost_data_list:
            menu_ghost = gs.ms.menu_ghost_data_list[menu]
            if menu_ghost.menu_type == "base" or "static":
                avatar_name = menu_ghost.BASE + "_avatar"
                display_details = gs.gv.menu_display_details[menu_ghost.BASE]
                items = menu_ghost.generate_text_print()
                gs.gv.add_menu_avatar(avatar_name, MenuAvatar(gc, avatar_name, items, display_details))
                gs.gv.set_menu_display_coordinates(menu_ghost.BASE)
            elif menu_ghost.menu_type == "conversation":
                avatar_name = menu_ghost.BASE + "_avatar"
                display_details = gs.gv.menu_display_details[menu_ghost.BASE]
                items = menu_ghost.generate_text_print()
                gs.gv.add_menu_avatar(avatar_name, ConversationMenuAvatar(gc, avatar_name, items, display_details))
                gs.gv.set_menu_display_coordinates(menu_ghost.BASE)

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
        pygame.mixer.music.play(-1)

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
    set_camera_position(gc, gs)
    initiate_mixer()
    fill_initial_room(gc, gs)




