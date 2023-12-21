from __future__ import annotations


class Vector(tuple):
    def __new__(cls, x: float, y: float, z: float) -> Vector:
        return tuple.__new__(cls, (x, y, z))

    def __add__(self, other: Vector) -> Vector:
        return Vector(
            self[0] + other[0], self[1] + other[1], self[2] + other[2]
        )

    def __sub__(self, other: Vector) -> Vector:
        return Vector(
            self[0] - other[0], self[1] - other[1], self[2] - other[2]
        )
