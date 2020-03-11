import pygame

from typing import Tuple
from dataclasses import dataclass
from collections import namedtuple

__all__ = ('Binding', 'MapKeyBindings', 'SHIFT', 'CTRL', 'ALT')

SHIFT = 1
CTRL = 2
ALT = 4

Binding = namedtuple('Binding', ('key', 'modifiers'))

@dataclass 
class MapKeyBindings:
    MoveNorth : Binding = Binding(pygame.K_UP, 0)
    MoveSouth : Binding = Binding(pygame.K_DOWN, 0)
    MoveWest : Binding = Binding(pygame.K_LEFT, 0)
    MoveEast : Binding = Binding(pygame.K_RIGHT, 0)
    MoveUp : Binding = Binding(pygame.K_PAGEUP, 0)
    MoveDown : Binding = Binding(pygame.K_PAGEDOWN, 0)
    ZoomIn : Tuple[Binding] = (Binding(pygame.K_KP_PLUS, 0), Binding(pygame.K_EQUALS, 0))
    ZoomOut : Tuple[Binding] = (Binding(pygame.K_KP_MINUS, 0), Binding(pygame.K_MINUS, 0))

if __name__ == '__main__':
    print(MapKeyBindings.ZoomIn == (pygame.K_KP_PLUS, SHIFT))
