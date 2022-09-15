import pygame

from spritesheet import Spritesheet

from player import Player_Avatar, Player_Data


def init_game(g):
    pygame.init()
    pygame.display.set_caption('window title')
    pygame.key.set_repeat()
    g.game_controller.initiate_timers()
    install_all_data(g.game_controller)

    if g.game_state.new_game:
        new_game_procedures(g.game_controller)
    else:
        continue_game_procedures(g.game_controller)


def new_game_procedures(gc):
    gc.game.game_state.add_player_state(Player_Avatar(1, 1))


def continue_game_procedures(gc):
    pass


def install_all_data(gc):
    install_keyboard_managers(gc)
    install_menus(gc)
    install_temp_items(gc)
    install_outfits(gc)
    install_key_items(gc)
    install_goals(gc)
    install_tileset(gc)
    install_player_data(gc)
    install_spritesheets(gc)


def install_spritesheets(gc):
    # gc.game.game_data.add_spritesheet("player_base_spritesheet", Spritesheet("player_base_spritesheet", "assets/spritesheets/Player_CS.png", 32, 40))
    pass

def install_player_data(gc):
    gc.game.game_data.add_player_data(Player_Data())


def install_keyboard_managers(gc):
    pass


def install_menus(gc):
    pass


def install_temp_items(gc):
    pass


def install_key_items(gc):
    pass


def install_outfits(gc):
    pass


def install_tileset(gc):
    pass


def install_goals(gc):
    pass
