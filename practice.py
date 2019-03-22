import pygame
import pygame.locals
from random import choice

TILESIZE = 30


class WindowState:
    def __init__(self):
        # self.screen = pygame.display.set_mode((420, 300))
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption('Pre-embark')

        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.font = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()
        self.tiles = load_tile_table('data/tileset.png', TILESIZE, TILESIZE)
        self.map = load_map('map.map')
        self.pos = (0, 0)   # upper left corner


    def set_tile(self, i, j, pos):
        if self.map[i][j] == '.':
            tile = self.tiles[0][0] 
        else:
            tile = self.tiles[1][0]
        self.background.blit(tile, pos)

        
    def render(self):
        self.clock.tick()
        self.background.fill((200, 200, 200))

        tW, tH = len(self.map[0]), len(self.map)
        sW, sH = self.screen.get_size()
        cx, cy = self.pos

        for i in range(mH):
            y = i * TILESIZE - cy
            if y > sH: break
            if y + TILESIZE <= 0: continue
            for j in range(mW):
                x = j * TILESIZE - cx
                if x > sW: break
                if x + TILESIZE <= 0: continue

            self.set_tile(i, j, (x, y))

        # show fps
        text = self.font.render(str(self.clock.get_fps()), 1, (100, 10, 100))
        textpos = text.get_rect()
        textpos.centerx = self.background.get_rect().centerx
        self.background.blit(text, textpos)

        self.screen.blit(self.background, (0, 0))


    def move_screen(self, dx, dy):
        mW = len(self.map[0]) * TILESIZE
        mH = len(self.map) * TILESIZE
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


def load_tile_table(filename, width, height):
    tileset = pygame.image.load(filename).convert()
    W, H = tileset.get_size();
    tiles = []
    for x in range (W // width):
        tiles.append([])
        for y in range(H // height):
            rect = (x * width, y * height, width, height)
            tiles[-1].append(tileset.subsurface(rect))
    return tiles

def load_map(filename):
    f = open(filename, 'r')
    return f.read().splitlines()


def main():
    pygame.init()
    game = GameState()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                return
            if event.type == pygame.locals.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
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


def generate_map(width, height):
    f = open('map.map', 'w')
    for x in range(width):
        for y in range(height):
            f.write(choice('.#'))
        f.write('\n')
    f.close()


if __name__ == '__main__':
    generate_map(100, 100)
    main()
