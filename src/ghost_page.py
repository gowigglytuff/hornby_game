
class PlayerGhost:
    def __init__(self, gs_input, x, y):
        self.gs_input = gs_input
        self.x = x
        self.y = y
        self.name = "default"
        self.cur_img = (0, 0)
        self.state = "idle"
        self.facing = None
        self.current_outfit = "Normal Outfit"