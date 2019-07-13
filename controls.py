from dataclasses import dataclass
import pygame
from pygame import locals
import time

from configs import *

modifiers = 0


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


prev_time = time.time() # temp!

def get_input(game):
    for event in pygame.event.get():
        # print(event)
        if event.type == pygame.locals.QUIT:
            return False

        # if event.type == pygame.locals.KEYUP:
            # if event.key == pygame.K_SHIFT:
            #     modifiers &= ~SHIFT
            # if event.key == pygame.K_CTRL:
            #     modifiers &= ~CTRL
            # if event.key == pygame.K_ALT:
            #     modifiers &= ~ALT


        if event.type == pygame.locals.KEYDOWN: # temp
            if event.key == pygame.K_ESCAPE:
                return False

            # if event.key == pygame.K_SHIFT:
            #     modifiers |= SHIFT
            # if event.key == pygame.K_CTRL:
            #     modifiers |= CTRL
            # if event.key == pygame.K_ALT:
            #     modifiers |= ALT

        if True:    # if map-manipulating context
            if event.type == pygame.locals.KEYDOWN: # temp
                if (event.key, modifiers) == MapKeyBindings.ZoomOut:
                    game.rescale(-1)
                if (event.key, modifiers) == MapKeyBindings.ZoomIn:
                    game.rescale(1)
        # assert False

    if True:    # if map-manipulating context
        # assert False
        global prev_time
        dt = time.time() - prev_time
        prev_time += dt
        if game.west_key_state.tick(dt, pygame.key.get_pressed()[MapKeyBindings.MoveWest.key]):
            game.move_cursor(-1, 0)
        if game.east_key_state.tick(dt, pygame.key.get_pressed()[MapKeyBindings.MoveEast.key]):
            game.move_cursor(1, 0)
        if game.north_key_state.tick(dt, pygame.key.get_pressed()[MapKeyBindings.MoveNorth.key]):
            game.move_cursor(0, -1)
        if game.south_key_state.tick(dt, pygame.key.get_pressed()[MapKeyBindings.MoveSouth.key]):
            game.move_cursor(0, 1)

    return True

