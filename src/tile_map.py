import csv
import os
import pygame

from definitions import GameSettings



class Tilling(object):
    def __init__(self, image, x, y):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def draw_tile(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))


class TileSet(object):
    def __init__(self, filename, tile_width, tile_height, image_columns, image_rows, max_tile_num=None):
        self.filename = filename
        self.sheet = pygame.image.load(filename).convert_alpha()
        self.width = tile_width
        self.height = tile_height
        self.image_columns = image_columns
        self.image_rows = image_rows

        if max_tile_num is not None:
            self.max_tile_num = max_tile_num
        else:
            self.max_tile_num = (self.sheet.get_width()/self.width) * (self.sheet.get_height()/self.height)

        assert self.sheet.get_width() % self.width == 0
        assert self.sheet.get_height() % self.height == 0

    def tile_at(self, rectangle):
        # "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        return image

    def get_tile_img(self, img_x, img_y):
        chosen_img = self.tile_at((img_x * self.width, img_y * self.height, self.width, self.height))

        return chosen_img  # type: pygame.Surface

    def load_tile_images(self):
        tiles_dict = {}
        tiles_count = 0
        for column in range(self.image_columns):
            for row in range(self.image_rows):
                tiles_dict[tiles_count] = self.get_tile_img(row, column)
                tiles_count += 1
        return tiles_dict


class TileMap:
    def __init__(self, filename):
        self.tile_set = TileSet(GameSettings.TILESET_IMAGE, GameSettings.TILESIZE, GameSettings.TILESIZE, GameSettings.TILESET_SIZE, GameSettings.TILESET_SIZE).load_tile_images()
        self.tile_size = GameSettings.TILESIZE
        self.start_x, self.start_y = 0, 0
        self.tiles = self.load_tiles(filename, self.tile_set)
        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        self.map_surface.set_colorkey((0, 0, 0))
        self.load_map()

    def return_map(self):
        return self.map_surface

    def load_map(self):
        for tile in self.tiles:
            tile.draw_tile(self.map_surface)

    def read_csv(self, filename):
        tile_map = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                tile_map.append(list(row))
        return tile_map

    def load_tiles(self, filename, tile_source):
        tiles = []
        tile_map = self.read_csv(filename)
        x, y = 0, 0
        for row in tile_map:
            x = 0
            for tile in row:
                tiles.append(Tilling(tile_source[int(tile)], x * self.tile_size, y * self.tile_size))
                x += 1
            y += 1
        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size
        return tiles

