class Vector2D:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
        
    def __add__(self, other: "Vector2D"):
        new_x = self.x + other.x
        new_y = self.y + other.y
        return Vector2D(new_x, new_y)

    def __sub__(self, other):
        new_x = self.x - other.x
        new_y = self.y - other.y
        return Vector2D(new_x, new_y)
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector2D(self.x * other, self.y * other)
        elif isinstance(other, Vector2D):
            return self.x * other.x + self.y * other.y
        else:
            raise TypeError("Unsupported type for multiplication")
    
    def __truediv__(self, n):
        new_x = self.x / n
        new_y = self.y / n
        return Vector2D(new_x, new_y)

    def norm(self):
        return ((self * self) ** 0.5)