

class Scene(object):

    def __init__(self, gc, actions_list):
        self.gc = gc  # type: Game
        self.actions_list = actions_list
        self.number_of_actions = len(actions_list)
        self.current_action = 0
        self.complete = False
        self.total_player_x_movement = 0
        self.total_player_y_movement = 0

    def return_current_action(self):
        if self.current_action == self.number_of_actions:
            result = None
            self.complete = True
        else:
            result = self.actions_list[self.current_action]
            self.current_action += 1
        return result, self.complete

    def reset(self):
        self.current_action = 0
        self.total_player_x_movement = 0
        self.total_player_y_movement = 0
