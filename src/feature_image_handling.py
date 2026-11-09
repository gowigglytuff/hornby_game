from spritesheet import Spritesheet


class FeatureSpritesheet(object):
    def __init__(self, gv_input, sheet_name, sheet_image_name):
        self.gv_input = gv_input
        self.sheet_name = sheet_name
        self.sheet_image_name = sheet_image_name
        self.character_frame_x = 32
        self.character_frame_y = 48
        self.size_x = 4
        self.size_y = 4
        self.spritesheet_object = self.prepare_spritesheet_object(sheet_image_name)

    def prepare_spritesheet_object(self, sheet_image_name):
        spritesheet_object = Spritesheet(sheet_image_name, "assets/spritesheets/feature_spritesheets/character_spritesheets/" + sheet_image_name, self.character_frame_x, self.character_frame_y)
        return spritesheet_object