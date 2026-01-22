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

class ImplicitFunction(Shape):
    def __init__(self, function):
        super().__init__("implicit_function")
        self.func = function

    def in_out(self, point):
        return self.func(point) <= 0