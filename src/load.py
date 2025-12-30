import pygame

from avatar_page import NpcAvatar, PlayerAvatar
from definitions import Direction
from ghost_page import NpcGhost, PlayerGhost
from item_page import *
from keyboard_manager_page import InGameKeyboardManager, InMenuKeyboardManager
from menu_avatars import MenuAvatar
from menu_ghosts import SpecialMenuGhost, StatMenuGhost, StartMenuGhost, KeyInventoryMenuGhost, ConversationOptionsMenuGhost, SuppliesInventoryMenuGhost, GameActionDialogueGhost, SubMenuGhost, UseMenuGhost
# from menu_page import GameActionDialogue, CharacterDialogue, ConversationOptionsMenu, Overlay, KeyInventoryMenu, YesnoMenu, UseMenu
from room_page import BasicRoom

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
    gs.add_player_ghost(PlayerGhost(gc.game.game_state, 1, 1))
    gs.add_npc_ghost("Clown", NpcGhost("Clown", gc.game.game_state, "Basic_Room", 2, 1, Direction.DOWN))
    gs.add_npc_ghost("Cowboy", NpcGhost("Cowboy", gc.game.game_state, "Basic_Room", 1, 3, Direction.DOWN))


def continue_game_procedures(gc, gs):
    pass


def install_all_data(gc, gs):

    def install_rooms(gc, gs):
        gs.gd.add_room_data(BasicRoom.ID, (BasicRoom()))

    def install_spritesheets(gc, gs):
        # gc.game_data.add_spritesheet("player_base_spritesheet", Spritesheet("player_base_spritesheet", "assets/spritesheets/Player_CS.png", 32, 40))
        pass

    def install_player_avatar(gc, gs):
        gs.gd.add_player_avatar(PlayerAvatar(gc.game_view.base_locator_x, gc.game_view.base_locator_y))
        pass

    def install_npc_avatar(gc, gs):
        npc_name_list = ["Clown", "Cowboy"]
        for npc_item in npc_name_list:
            gs.gd.add_character_avatar(npc_item, NpcAvatar(npc_item, gc.game_state.npc_ghost_list[npc_item].x, gc.game_state.npc_ghost_list[npc_item].y))

    def install_keyboard_managers(gc, gs):
        gc.game_view.game_data.add_keyboard_manager_data(InGameKeyboardManager.ID, InGameKeyboardManager(gc))
        gc.game_view.game_data.add_keyboard_manager_data(InMenuKeyboardManager.ID, InMenuKeyboardManager(gc))

    def set_initial_keyboard_manager(gc, gs):
        gc.set_active_keyboard_manager(InGameKeyboardManager.ID)

    def install_temp_items(gc, gs):
        items_to_install = [Cheese, Milk, Cream, Banana, Apple, Orange, Mike, Spoon, Mouse, Match, Game, Card, Pizza, Meat, Egg]
        q = 1
        for item in items_to_install:
            gs.gd.install_item_data(item.NAME, item(gc))
            gs.acquire_item(item, q)
            q *= 3

    def install_key_items(gc, gs):
        items_to_install = [Hammer, Shovel, Wrench]
        for item in items_to_install:
            gs.gd.install_key_item_data(item.NAME, item(gc))
            gc.inventory_manager.get_key_item(item)

    def install_menus(gc, gs):
        for ghost in gc.game_data.menu_load_list:
            gs.ms.add_menu_ghost(ghost.NAME, ghost(gc))

        for menu in gs.ms.menu_ghost_data_list:
            menu_ghost = gs.ms.menu_ghost_data_list[menu]
            avatar_name = menu_ghost.BASE + "_avatar"
            display_details = gs.ms.menu_display_details[menu_ghost.BASE]
            items = menu_ghost.generate_text_print()
            gs.ms.add_menu_avatar(avatar_name, MenuAvatar(gc, avatar_name, items, display_details))
            gs.ms.set_menu_display_coordinates(menu_ghost.BASE)

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

    install_keyboard_managers(gc, gs)
    set_initial_keyboard_manager(gc, gs)

    install_temp_items(gc, gs)
    install_outfits(gc, gs)
    install_key_items(gc, gs)
    install_menus(gc, gs)
    install_goals(gc, gs)
    install_tileset(gc, gs)
    install_player_avatar(gc, gs)
    install_npc_avatar(gc, gs)
    install_spritesheets(gc, gs)
    install_rooms(gc, gs)
    set_camera_position(gc, gs)
    fill_initial_room(gc, gs)




