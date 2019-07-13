from dataclasses import dataclass


@dataclass
class Vec2:
    x: float  # int is also fine
    y: float

    def as_tuple(self):
        return (self.x, self.y)

    def __add__(self, other):
        if isinstance(other, Vec2):
            return Vec2(self.x + other.x, self.y + other.y)
        raise NotImplementedError()

    def __sub__(self, other):
        if isinstance(other, Vec2):
            return Vec2(self.x - other.x, self.y - other.y)
        raise NotImplementedError()

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vec2(self.x * other, self.y * other)
        raise NotImplementedError()

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Vec2(self.x / other, self.y / other)
        raise NotImplementedError()

    def __floordiv__(self, other):
        if isinstance(other, int):
            return Vec2(int(self.x) // other, int(self.y) // other)
        raise NotImplementedError()


@dataclass
class Vec3:
    x: float  # int is also fine
    y: float
    z: int

    def as_tuple(self):
        return (self.x, self.y, self.z)

    def __add__(self, other):
        if isinstance(other, Vec3):
            return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
        raise NotImplementedError()

    def __sub__(self, other):
        if isinstance(other, Vec3):
            return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)
        raise NotImplementedError()

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vec3(self.x * other, self.y * other, self.z * other)
        raise NotImplementedError()

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Vec3(self.x / other, self.y / other, self.z / other)
        raise NotImplementedError()

    def __floordiv__(self, other):
        if isinstance(other, int):
            return Vec3(int(self.x) // other, int(self.y) // other, int(self.z) // other)
        raise NotImplementedError()

    def vec2(self):
        return Vec2(self.x, self.y)

