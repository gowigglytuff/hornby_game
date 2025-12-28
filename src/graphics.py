import textwrap

import pygame

from definitions import GameSettings, Types
from spritesheet import Spritesheet


class BuiltOverlay(object):
    def __init__(self, name, width, height, style="gray", tile_segment_size=GameSettings.MENUSEGMENTSIZE, menu_style=GameSettings.MENU_STYLE, header=False):
        self.x = None
        self.y = None
        self.square_size = (24, 24)
        self.width = int(width)
        self.height = int(height)
        self.name = name
        self.image = None
        self.style = style
        self.tile_segment_size = tile_segment_size
        self.menu_style = menu_style
        self.header = header
        self.offset_y = 0

    def build_overlay(self):
        sheet = Spritesheet("overlay_pieces", self.menu_style, self.tile_segment_size, self.tile_segment_size)
        base = 0
        head_y = 0
        if not self.header:
            x = self.width * self.tile_segment_size
            y = self.height * self.tile_segment_size
            base = pygame.Surface((x, y))
        if self.header:
            self.offset_y = self.tile_segment_size * 7  # TODO: fix this
            head_x = self.width * self.tile_segment_size
            offset_value = self.offset_y / self.tile_segment_size
            header_size = GameSettings.FONT_SIZE / self.tile_segment_size
            head_y_segments = int(offset_value * 2 + header_size)

            base_size_x = self.width * self.tile_segment_size
            base_size_y = self.height * self.tile_segment_size + self.offset_y
            base = pygame.Surface((base_size_x, base_size_y))

            head_y = head_y_segments * self.tile_segment_size
            head_base = pygame.Surface((head_x, head_y))
            for item_y in range(head_y_segments):
                for item_x in range(int(self.width)):
                    loc_x = 0
                    loc_y = 0
                    if item_y == 0:
                        loc_y = 0
                    elif item_y == head_y_segments - 1:
                        loc_y = 2
                    else:
                        loc_y = 1
                    if item_x == 0:
                        loc_x = 0
                    elif item_x == self.width - 1:
                        loc_x = 2
                    else:
                        loc_x = 1
                    head_base.blit(sheet.get_image(loc_x, loc_y, transparent=False), [item_x * self.tile_segment_size, item_y * self.tile_segment_size])
            base.blit(head_base, [0, 0])
            head_y = self.offset_y
        else:
            pass

        body_x = self.width * self.tile_segment_size
        body_y = self.height * self.tile_segment_size
        body_base = pygame.Surface((body_x, body_y))
        for item_y in range(int(self.height)):
            for item_x in range(int(self.width)):
                loc_x = 0
                loc_y = 0

                if item_y == 0:
                    loc_y = 0
                elif item_y == self.height - 1:
                    loc_y = 2
                else:
                    loc_y = 1

                if item_x == 0:
                    loc_x = 0
                elif item_x == self.width - 1:
                    loc_x = 2
                else:
                    loc_x = 1

                body_base.blit(sheet.get_image(loc_x, loc_y, transparent=False), [item_x * self.tile_segment_size, item_y * self.tile_segment_size])
        base.blit(body_base, [0, head_y])
        return base
