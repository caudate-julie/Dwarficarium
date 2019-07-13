import time
import random
from dataclasses import dataclass

import pygame
import pygame.locals

from vecs import Vec2, Vec3
from controls import get_input, KeyState
import terrain

TILESIZE = [15, 21, 30, 42, 60]


class Tileset:
    def __init__(self, size):
        src_size = 30
        image = pygame.image.load('data/tileset.png').convert()
        image_pix_W, image_pix_H = image.get_size()
        tilesW, tilesH = image_pix_W // src_size, image_pix_H // src_size

        tileset = []
        resized_image = pygame.Surface((tilesW * size, tilesH * size), flags=image.get_flags())
        for j in range(tilesH):
            tileset.append([])
            for i in range(tilesW):
                clip = image.subsurface((i*src_size, j*src_size, src_size, src_size))
                src = pygame.transform.scale(clip, (size, size))
                resized_image.blit(src, (i*size, j*size))
                tileset[j].append(resized_image.subsurface(i*size, j*size, size, size))

        self.stone = tileset[0][0]
        self.floor = tileset[0][1]
        self.size = size

        image = pygame.image.load('data/cursor.png').convert()
        assert image.get_size() == (src_size * 3, src_size * 3)
        image = pygame.transform.scale(image, (size * 3, size * 3))
        image.set_colorkey(image.get_at((0, 0)))
        self.cursor = image


class WindowState:
    def __init__(self):
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption('Pre-embark')

        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.font = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()

        self.tileset_by_size = {size: Tileset(size) for size in TILESIZE}
        self.scale = 2

        seed = random.randrange(10**6)
        print('seed:', seed)
        self.map = terrain.generate_map(100, 50, 30, seed)
        self.map_size = Vec3(len(self.map[0][0]), len(self.map[0]), len(self.map))

        screen_size = Vec2(*self.screen.get_size()) / self.tileset.size
        self.cursor_pos = self.map_size // 2
        self.screen_pos = self.cursor_pos.vec2() - screen_size // 2

        self.north_key_state = KeyState()
        self.south_key_state = KeyState()
        self.west_key_state = KeyState()
        self.east_key_state = KeyState()
        self.up_key_state = KeyState()
        self.down_key_state = KeyState()

    @property
    def tileset(self):
        return self.tileset_by_size[TILESIZE[self.scale]]

    def set_tile(self, i, j, k, pos):
        if self.map[i][j][k] == '#':
            tile = self.tileset.stone
        elif self.map[i][j][k] == '.':
            tile = self.tileset.floor
        else:
            assert False, self.map[i][j][k]
        self.background.blit(tile, pos)


    def render(self):
        self.clock.tick()
        self.background.fill((200, 200, 200))

        tile_size = self.tileset.size
        screen_pix_W, screen_pix_H = self.screen.get_size()

        screen_pos_pix = self.screen_pos * tile_size

        for i in range(self.map_size.y):
            y = i * tile_size - screen_pos_pix.y
            if y > screen_pix_H: break
            if y + tile_size <= 0: continue
            for j in range(self.map_size.x):
                x = j * tile_size - screen_pos_pix.x
                if x > screen_pix_W: break
                if x + tile_size <= 0: continue

                self.set_tile(self.cursor_pos.z, i, j, (x, y))

        xy = (self.cursor_pos.vec2() - Vec2(1, 1)) * tile_size - screen_pos_pix
        self.background.blit(self.tileset.cursor, xy.as_tuple())

        # show fps
        text = self.font.render(str(self.clock.get_fps()), 1, (100, 10, 100))
        textpos = text.get_rect()
        textpos.centerx = self.background.get_rect().centerx
        self.background.blit(text, textpos)

        self.screen.blit(self.background, (0, 0))

    def clip_screen_to_map(self):
        screen_size = Vec2(*self.screen.get_size()) / self.tileset.size
        if screen_size.x < self.map_size.x:
            self.screen_pos.x = max(0, min(self.screen_pos.x, self.map_size.x - screen_size.x))
        else:
            self.screen_pos.x = (self.map_size.x - screen_size.x) / 2
        if screen_size.y < self.map_size.y:
            self.screen_pos.y = max(0, min(self.screen_pos.y, self.map_size.y - screen_size.y))
        else:
            self.screen_pos.y = (self.map_size.y - screen_size.y) / 2
        

    def rescale(self, ds):
        if self.scale + ds < 0 or self.scale + ds >= len(TILESIZE):
            return

        factor = TILESIZE[self.scale + ds] / TILESIZE[self.scale]
        self.scale += ds

        # preserve relative location of the cursor on the screen
        cursor_pos = self.cursor_pos.vec2() + Vec2(0.5, 0.5)
        self.screen_pos = cursor_pos - (cursor_pos - self.screen_pos) / factor

        self.clip_screen_to_map()

    def move_cursor(self, dx, dy, dz):
        self.cursor_pos += Vec3(dx, dy, dz)
        self.cursor_pos.x = max(0, min(self.cursor_pos.x, self.map_size.x - 1))
        self.cursor_pos.y = max(0, min(self.cursor_pos.y, self.map_size.y - 1))
        self.cursor_pos.z = max(0, min(self.cursor_pos.z, self.map_size.z - 1))

        screen_size = Vec2(*self.screen.get_size()) / self.tileset.size

        ALLOWED_GAP = 2
        JUMP = 10

        if self.cursor_pos.x + 0.5 < self.screen_pos.x + ALLOWED_GAP:
            self.screen_pos.x -= JUMP
        if self.cursor_pos.x - 0.5 > self.screen_pos.x + screen_size.x - ALLOWED_GAP:
            self.screen_pos.x += JUMP
        if self.cursor_pos.y + 0.5 < self.screen_pos.y + ALLOWED_GAP:
            self.screen_pos.y -= JUMP
        if self.cursor_pos.y - 0.5 > self.screen_pos.y + screen_size.y - ALLOWED_GAP:
            self.screen_pos.y += JUMP


        self.clip_screen_to_map()


def main():
    pygame.init()
    game = WindowState()
    
    while get_input(game):
        game.render()
        pygame.display.update()
        


if __name__ == '__main__':
    main()
