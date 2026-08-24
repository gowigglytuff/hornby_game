import copy
import time

from position_manager_state_page import Room
from game_controller import Game
from load import init_game
import pygame

pygame.init()
g = Game()  # type: Game

def main():
    init_game(g)
    run_game_loop()


# def delta_time_check():
#     check = time.perf_counter()
#     difference = check - g.now
#     print(g.now, check, difference)
#     # g.now = copy.copy(check)
#     if difference >= 0.017:
#         print("ding")
#         g.delay = False
#         g.now = copy.copy(check)
#     else:
#         g.delay = True


def run_game_loop():

    while g.game_running:
        if g.delay:
            pass

        else:
            for event in pygame.event.get():
                if event.type in [pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT]:
                    g.game_events.parse_input_event(event)

                if event.type in g.game_events.timer_list:
                    g.game_events.parse_input_event(event)

            g.game_events.parse_delayed_triggers()
            pygame.display.flip()
            g.game_controller.update_view()
            g.game_view.tick()
        # delta_time_check()



if __name__ == "__main__":
    main()