import pygame

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
    ZoomIn : Binding = Binding(pygame.K_KP_PLUS, SHIFT)
    ZoomOut : Binding = Binding(pygame.K_KP_MINUS, SHIFT)

if __name__ == '__main__':
    print(MapKeyBindings.ZoomIn == (pygame.K_KP_PLUS, SHIFT))
    