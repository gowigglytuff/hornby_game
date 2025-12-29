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
    g.game_controller.initiate_timers()

    if g.game_state.new_game:

        new_game_procedures(g.game_controller)
    else:
        continue_game_procedures(g.game_controller)

    install_all_data(g.game_controller)


def new_game_procedures(gc):
    gc.game.game_state.add_player_ghost(PlayerGhost(gc.game.game_state, 1, 1))

    gc.game.game_state.add_npc_ghost("Clown", NpcGhost("Clown", gc.game.game_state, "Basic_Room", 2, 1, Direction.DOWN))
    gc.game.game_state.add_npc_ghost("Cowboy", NpcGhost("Cowboy", gc.game.game_state, "Basic_Room", 1, 3, Direction.DOWN))


def continue_game_procedures(gc):
    pass


def install_all_data(gc):

    def install_rooms(gc):
        gc.game_view.game_data.add_room_data(BasicRoom.ID, (BasicRoom()))

    def install_spritesheets(gc):
        # gc.game_data.add_spritesheet("player_base_spritesheet", Spritesheet("player_base_spritesheet", "assets/spritesheets/Player_CS.png", 32, 40))
        pass

    def install_player_avatar(gc):
        gc.game_view.game_data.add_player_avatar(PlayerAvatar(gc.game_view.base_locator_x, gc.game_view.base_locator_y))
        pass

    def install_npc_avatar(gc):
        npc_name_list = ["Clown", "Cowboy"]
        for npc_item in npc_name_list:
            gc.game_view.game_data.add_character_avatar(npc_item, NpcAvatar(npc_item, gc.game_state.npc_ghost_list[npc_item].x, gc.game_state.npc_ghost_list[npc_item].y))

    def install_keyboard_managers(gc):
        gc.game_view.game_data.add_keyboard_manager_data(InGameKeyboardManager.ID, InGameKeyboardManager(gc))
        gc.game_view.game_data.add_keyboard_manager_data(InMenuKeyboardManager.ID, InMenuKeyboardManager(gc))

    def set_initial_keyboard_manager(gc):
        gc.set_active_keyboard_manager(InGameKeyboardManager.ID)

    def install_temp_items(gc):
        items_to_install = [Cheese, Milk, Cream, Banana, Apple, Orange, Mike, Spoon, Mouse, Match, Game, Card, Pizza, Meat, Egg]
        q = 1
        for item in items_to_install:
            gc.inventory_manager.install_item_data(item.NAME, item(gc))
            gc.inventory_manager.get_item(item, q)
            q *= 3

    def install_key_items(gc):
        items_to_install = [Hammer, Shovel, Wrench]
        for item in items_to_install:
            gc.inventory_manager.install_key_item_data(item.NAME, item(gc))
            gc.inventory_manager.get_key_item(item)

    def install_menus(gc):
        for ghost in gc.game_data.menu_load_list:
            gc.menu_manager.add_menu_ghost(ghost.NAME, ghost(gc))

        for menu in gc.menu_manager.menu_ghost_data_list:
            menu_ghost = gc.menu_manager.menu_ghost_data_list[menu]
            avatar_name = menu_ghost.BASE + "_avatar"
            display_details = gc.menu_manager.menu_display_details[menu_ghost.BASE]
            items = menu_ghost.generate_text_print()
            gc.game_view.game_data.add_menu_avatar(avatar_name, MenuAvatar(gc, avatar_name, items, display_details))
            gc.menu_manager.set_menu_display_coordinates(menu_ghost.BASE)

    def install_outfits(gc):
        pass

    def install_tileset(gc):
        pass

    def install_goals(gc):
        pass

    def set_camera_position(gc):
        gc.set_camera()

    def fill_initial_room(gc):
        gc.position_manager.fill_room_grid(gc.game.game_state.current_room)

    install_keyboard_managers(gc)
    set_initial_keyboard_manager(gc)

    install_temp_items(gc)
    install_outfits(gc)
    install_key_items(gc)
    install_menus(gc)
    install_goals(gc)
    install_tileset(gc)
    install_player_avatar(gc)
    install_npc_avatar(gc)
    install_spritesheets(gc)
    install_rooms(gc)
    set_camera_position(gc)
    fill_initial_room(gc)




