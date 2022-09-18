from game_core import Game
from load import init_game
import pygame

g = Game()


def main():
    init_game(g)
    run_game_loop()


def run_game_loop():

    while g.game_running:
        for event in pygame.event.get():
            if event.type in [pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT]:
                g.game_controller.parse_input_event(event)

            if event.type in g.game_controller.timer_list:
                g.game_controller.parse_input_event(event)

        pygame.display.update()
        g.game_view.tick()
        g.game_view.draw_all()


if __name__ == "__main__":
    main()

