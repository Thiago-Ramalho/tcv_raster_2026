from base import Shape

class Circle(Shape):
    def __init__(self, center, radius):
        super().__init__("circle")
        self.center = center
        self.radius = radius

    def in_out(self, point):
        dx = point[0] - self.center[0]
        dy = point[1] - self.center[1]
        return (dx * dx + dy * dy) <= (self.radius * self.radius)

class Triangle(Shape):
    def __init__(self, vertex1, vertex2, vertex3):
        super().__init__("triangle")
        self.v1 = vertex1
        self.v2 = vertex2
        self.v3 = vertex3

    def in_out(self, point):
        raise NotImplementedError("in_out method not implemented for Triangle")

class ImplicitFunction(Shape):
    def __init__(self, function):
        super().__init__("implicit_function")
        self.func = function

    def in_out(self, point):
        return self.func(point) <= 0