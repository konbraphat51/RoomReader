from __future__ import annotations

class Vector(tuple):
    def __init__(self, x: float, y: float, z: float) -> None:
        super().__init__((x, y, z))
        
    def __add__(self, other: Vector) -> Vector:
        return Vector(self[0] + other[0], self[1] + other[1], self[2] + other[2])
    
    def __sub__(self, other: Vector) -> Vector:
        return Vector(self[0] - other[0], self[1] - other[1], self[2] - other[2])