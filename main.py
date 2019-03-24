import time
import random
from dataclasses import dataclass

import pygame
import pygame.locals

from vec2 import Vec2
import terrain

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


FIRST_KEY_PRESS_DELAY = 0.25
REPEAT_KEY_PRESS_DELAY = 0.1
# When a key is pressed and hold at moment 0,
# key press events happen at the following times:
#   0
#   FIRST_KEY_PRESS_DELAY
#   FIRST_KEY_PRESS_DELAY + REPEAT_KEY_PRESS_DELAY
#   FIRST_KEY_PRESS_DELAY + REPEAT_KEY_PRESS_DELAY * 2
#   ...

@dataclass
class KeyState:
    cooldown: float = 0.0
    num_presses: int = 0

    def tick(self, dt, pressed):
        '''Returns whether event should be fired this tick.'''
        if not pressed:
            self.cooldown = 0
            self.num_presses = 0
            return False

        self.cooldown -= dt
        if self.cooldown > 0:
            return False
        if self.num_presses == 0:
            self.cooldown = FIRST_KEY_PRESS_DELAY
        else:
            self.cooldown = REPEAT_KEY_PRESS_DELAY
        self.num_presses += 1
        return True


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

        seed = random.randrange(10**6)
        print('seed:', seed)
        self.map = terrain.generate_map(100, 50, seed)
        self.map_size = Vec2(len(self.map[0]), len(self.map))

        screen_size = Vec2(*self.screen.get_size()) / self.tileset.size
        self.screen_pos = (self.map_size - screen_size) * 0.5
        self.cursor_pos = Vec2(self.map_size.x // 2, self.map_size.y // 2)

        self.up_key_state = KeyState()
        self.down_key_state = KeyState()
        self.left_key_state = KeyState()
        self.right_key_state = KeyState()

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

    def clip_screen_to_map(self):
        screen_size = Vec2(*self.screen.get_size()) / self.tileset.size
        self.screen_pos.x = max(0, min(self.screen_pos.x, self.map_size.x - screen_size.x))
        self.screen_pos.y = max(0, min(self.screen_pos.y, self.map_size.y - screen_size.y))

    def rescale(self, ds):
        if self.scale + ds < 0 or self.scale + ds >= len(TILESIZE):
            return

        factor = TILESIZE[self.scale + ds] / TILESIZE[self.scale]
        self.scale += ds

        # preserve relative location of the cursor on the screen
        cursor_pos = self.cursor_pos + Vec2(0.5, 0.5)
        self.screen_pos = cursor_pos - (cursor_pos - self.screen_pos) / factor

        self.clip_screen_to_map()

    def move_cursor(self, dx, dy):
        self.cursor_pos += Vec2(dx, dy)
        self.cursor_pos.x = max(0, min(self.cursor_pos.x, self.map_size.x - 1))
        self.cursor_pos.y = max(0, min(self.cursor_pos.y, self.map_size.y - 1))

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
    prev_time = time.time()
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

        dt = time.time() - prev_time
        prev_time += dt
        if game.left_key_state.tick(dt, pygame.key.get_pressed()[pygame.K_LEFT]):
            game.move_cursor(-1, 0)
        if game.right_key_state.tick(dt, pygame.key.get_pressed()[pygame.K_RIGHT]):
            game.move_cursor(1, 0)
        if game.up_key_state.tick(dt, pygame.key.get_pressed()[pygame.K_UP]):
            game.move_cursor(0, -1)
        if game.down_key_state.tick(dt, pygame.key.get_pressed()[pygame.K_DOWN]):
            game.move_cursor(0, 1)

        game.render()
        pygame.display.update()


if __name__ == '__main__':
    main()
