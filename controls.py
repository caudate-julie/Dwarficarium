from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
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
class KeysState:
    cooldown: float = 0.0
    action_to_pressed_ago: Dict[Any, float] = field(default_factory=dict)

    def tick(self, dt, action_to_pressed: Dict[Any, bool]) -> List[Any]:
        '''Returns the list of actions triggered at this tick.'''
        repetetion_trigger = False
        prev_pressed = bool(self.action_to_pressed_ago)
        if prev_pressed:
            self.cooldown -= dt
            if self.cooldown <= 0:
                self.cooldown += REPEAT_KEY_PRESS_DELAY
                repetetion_trigger = True

        result = []
        for a, pressed in action_to_pressed.items():
            if pressed:
                ago = self.action_to_pressed_ago.get(a)
                if ago is None:
                    result.append(a)
                    self.action_to_pressed_ago[a] = 0.0
                else:
                    if ago >= REPEAT_KEY_PRESS_DELAY and repetetion_trigger:
                        result.append(a)
            else:
                self.action_to_pressed_ago.pop(a, None)

        for a in self.action_to_pressed_ago:
            self.action_to_pressed_ago[a] += dt

        if any(action_to_pressed.values()):
            if not prev_pressed:
                self.cooldown = FIRST_KEY_PRESS_DELAY
        else:
            self.cooldown = 0.0

        return result


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
                if (event.key, modifiers) in MapKeyBindings.ZoomOut:
                    game.rescale(-1)
                if (event.key, modifiers) in MapKeyBindings.ZoomIn:
                    game.rescale(1)
        # assert False

    if True:    # if map-manipulating context
        global prev_time
        dt = time.time() - prev_time
        prev_time += dt

        action_to_key = {
            (-1,  0,  0): MapKeyBindings.MoveWest.key,
            ( 1,  0,  0): MapKeyBindings.MoveEast.key,
            ( 0, -1,  0): MapKeyBindings.MoveNorth.key,
            ( 0,  1,  0): MapKeyBindings.MoveSouth.key,
            ( 0,  0, -1): MapKeyBindings.MoveUp.key,
            ( 0,  0,  1): MapKeyBindings.MoveDown.key,
        }
        pressed = pygame.key.get_pressed()
        action_to_pressed = {a: bool(pressed[key]) for a, key in action_to_key.items()}
        for a in game.keys_state.tick(dt, action_to_pressed):
            game.move_cursor(*a)

    return True

