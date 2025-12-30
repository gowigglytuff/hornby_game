from position_manager import Room2
from game_core import Game
from load import init_game
import pygame

pygame.init()
g = Game()  # type: Game


def main():
    init_game(g)
    run_game_loop()


def run_game_loop():

    while g.game_running:
        for event in pygame.event.get():
            if event.type in [pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT]:
                g.game_events.parse_input_event(event)

            if event.type in g.game_events.timer_list:
                g.game_events.parse_input_event(event)

        pygame.display.update()
        g.game_view.tick()
        g.game_state.update_view()


if __name__ == "__main__":
    main()

