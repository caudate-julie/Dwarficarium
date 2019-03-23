from dataclasses import dataclass


@dataclass
class Vec2:
    x: float  # int is also fine
    y: float

    def as_tuple(self):
        return (self.x, self.y)

    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vec2(self.x * other, self.y * other)
        raise NotImplementedError()

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Vec2(self.x / other, self.y / other)
        raise NotImplementedError()
