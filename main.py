from copy import deepcopy
import math
from random import choice

import pygame
import pygame.locals

from vec2 import Vec2

TILESIZE = [15, 21, 30, 42, 60]


class Tileset:
    def __init__(self, size):
        src_size = 30
        image = pygame.image.load('data/tileset.png').convert()
        imageW, imageH = image.get_size()
        tilesW, tilesH = imageW // src_size, imageH // src_size

        tileset = []
        img = pygame.Surface((tilesW * size, tilesH * size), flags=image.get_flags())
        for i in range(tilesW):
            tileset.append([])
            for j in range(tilesH):
                clip = image.subsurface((i*src_size, j*src_size, src_size, src_size))
                src = pygame.transform.scale(clip, (size, size))
                img.blit(src, (i*size, j*size))
                tileset[i].append(img.subsurface(i*size, j*size, size, size))

        self.stone = tileset[0][0]
        self.floor = tileset[1][0]
        self.size = size

        image = pygame.image.load('data/cursor.png').convert()
        assert image.get_size() == (src_size * 3, src_size * 3)
        image = pygame.transform.scale(image, (size * 3, size * 3))
        image.set_colorkey(image.get_at((0, 0)))
        self.cursor = image


class WindowState:
    def __init__(self):
        # self.screen = pygame.display.set_mode((420, 300))
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption('Pre-embark')

        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.font = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()

        self.tileset_by_size = {size: Tileset(size) for size in TILESIZE}
        self.scale = 2

        self.map = load_map('map.map')
        self.map_size = Vec2(len(self.map[0]), len(self.map))

        screen_size = Vec2(*self.screen.get_size()) / self.tileset.size
        self.screen_pos = (self.map_size - screen_size) * 0.5
        self.cursor_pos = Vec2(self.map_size.x // 2, self.map_size.y // 2)

    @property
    def tileset(self):
        return self.tileset_by_size[TILESIZE[self.scale]]

    def set_tile(self, i, j, pos):
        if self.map[i][j] == '.':
            tile = self.tileset.stone
        else:
            tile = self.tileset.floor
        self.background.blit(tile, pos)

    def render(self):
        self.clock.tick()
        self.background.fill((200, 200, 200))

        tile_size = self.tileset.size
        screenPW, screenPH = self.screen.get_size()

        screen_pos_pix = self.screen_pos * tile_size
        screen_pos_pix = Vec2(int(screen_pos_pix.x), int(screen_pos_pix.y))

        for i in range(self.map_size.y):
            y = i * tile_size - screen_pos_pix.y
            if y > screenPH: break
            if y + tile_size <= 0: continue
            for j in range(self.map_size.x):
                x = j * tile_size - screen_pos_pix.x
                if x > screenPW: break
                if x + tile_size <= 0: continue

                self.set_tile(i, j, (x, y))

        xy = (self.cursor_pos - Vec2(1, 1)) * tile_size - screen_pos_pix
        self.background.blit(self.tileset.cursor, xy.as_tuple())

        # show fps
        text = self.font.render(str(self.clock.get_fps()), 1, (100, 10, 100))
        textpos = text.get_rect()
        textpos.centerx = self.background.get_rect().centerx
        self.background.blit(text, textpos)

        self.screen.blit(self.background, (0, 0))


    def move_screen(self, dx, dy):
        screen_size = Vec2(*self.screen.get_size()) / self.tileset.size

        self.screen_pos += Vec2(dx, dy) / self.tileset.size
        self.screen_pos.x = max(0, min(self.screen_pos.x, self.map_size.x - screen_size.x))
        self.screen_pos.y = max(0, min(self.screen_pos.y, self.map_size.y - screen_size.y))

    def rescale(self, ds):
        if self.scale + ds < 0 or self.scale + ds >= len(TILESIZE):
            return
        self.scale += ds
        self.move_screen(0, 0)


def generate_map(width, height):
    f = open('map.map', 'w')
    for y in range(height):
        for x in range(width):
            f.write(choice('.#'))
        f.write('\n')
    f.close()


def load_map(filename):
    f = open(filename, 'r')
    return f.read().splitlines()


def main():
    pygame.init()
    game = WindowState()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                return
            if event.type == pygame.locals.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_PAGEUP:
                    game.rescale(-1)
                if event.key == pygame.K_PAGEDOWN:
                    game.rescale(1)
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            game.move_screen(-5, 0)
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            game.move_screen(5, 0)
        if pygame.key.get_pressed()[pygame.K_UP]:
            game.move_screen(0, -5)
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            game.move_screen(0, 5)

        game.render()            
        pygame.display.update()


if __name__ == '__main__':
    generate_map(100, 50)
    main()
