import pygame


def init_game(g):
    pygame.init()
    pygame.display.set_caption('window title')
    pygame.key.set_repeat()
    g.game_view.initiate_timers()


def load_all_data(gs):
    load_keyboard_managers(gs)
    load_menus(gs)
    load_temp_items(gs)
    load_outfits(gs)
    load_key_items(gs)
    load_goals(gs)
    load_tileset(gs)
    load_player(gs)


def load_keyboard_managers(gs):
    pass


def load_menus(gs):
    pass


def load_temp_items(gs):
    pass


def load_key_items(gs):
    pass


def load_outfits(gs):
    pass


def load_player(gs):
    pass


def load_tileset(gs):
    pass


def load_goals(gs):
    pass
