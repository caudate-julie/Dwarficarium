import pygame
import pygame.locals

from copy import deepcopy
import math
from random import choice

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
        self.mapTH = len(self.map)   # height in tiles
        self.mapTW = len(self.map[0])      # width in tiles

        self.pos = (self.mapTW / 2 * TILESIZE[self.scale],
                    self.mapTH / 2 * TILESIZE[self.scale])
        self.cursor_pos = (self.mapTW // 2, self.mapTH // 2)

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

        screenPW, screenPH = self.screen.get_size()
        cx, cy = self.pos   # in pixels

        tile_size = self.tileset.size
        for i in range(self.mapTH):
            y = i * tile_size - cy
            if y > screenPH: break
            if y + tile_size <= 0: continue
            for j in range(self.mapTW):
                x = j * tile_size - cx
                if x > screenPW: break
                if x + tile_size <= 0: continue

                self.set_tile(i, j, (x, y))

        x = (self.cursor_pos[0] - 1) * tile_size - cx
        y = (self.cursor_pos[1] - 1) * tile_size - cy
        self.background.blit(self.tileset.cursor, (x, y))

        # show fps
        text = self.font.render(str(self.clock.get_fps()), 1, (100, 10, 100))
        textpos = text.get_rect()
        textpos.centerx = self.background.get_rect().centerx
        self.background.blit(text, textpos)

        self.screen.blit(self.background, (0, 0))


    def move_screen(self, dx, dy):
        mW = len(self.map[0]) * self.tileset.size
        mH = len(self.map) * self.tileset.size
        sW, sH = self.screen.get_size()
        x, y = self.pos
        x += dx
        y += dy

        if x <= 0:
            x = 0
        elif x >= mW - sW:
            x = mW - sW

        if y <= 0:
            y = 0
        elif y >= mH - sH:
            y = mH - sH

        self.pos = (x, y)

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
            game.move_screen(-1, 0)
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            game.move_screen(1, 0)
        if pygame.key.get_pressed()[pygame.K_UP]:
            game.move_screen(0, -1)
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            game.move_screen(0, 1)

        game.render()            
        pygame.display.update()


if __name__ == '__main__':
    generate_map(100, 100)
    main()
