class GameData(object):
    def __init__(self):
        self.character_data_list = {}
        self.room_data_list = {}
        self.door_data_list = {}
        self.keyboard_manager_list = {}

    def add_character_data(self, key, body):
        self.character_data_list[key] = body


class GameSetting(object):
    def __init__(self):
        self.resolution = (1000, 1000)
        self.FPS = 30
        self.square_size = [32, 32]
        self.base_locator_x = self.resolution[0] / 2 - self.square_size[0] / 2
        self.base_locator_y = self.resolution[1] / 2 - self.square_size[1] / 2


class GameState(object):
    def __init__(self):
        self.player_state = []
        self.character_state_list = {}
        self.prop_state_list = {}
        self.decoration_state_list = {}

    def add_character_avatar(self, key, body):
        self.character_state_list[key] = body


class PositionManager(object):
    def __init__(self, ):
        pass


class UpdateManager(object):
    def __init__(self, ):
        pass


class EventsManager(object):
    def __init__(self):
        pass


class GraphicsManager(object):
    def __init__(self, ):
        pass
