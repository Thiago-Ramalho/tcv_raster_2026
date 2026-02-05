from .base import Shape

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
        # Assuming all vertices are declaired in counter-clockwise order, we can use the cross product
        # to determine if the point is to the same side of all edges of the triangle
        edge_vec1 = (self.v2[0] - self.v1[0], self.v2[1] - self.v1[1])
        edge_vec2 = (self.v3[0] - self.v2[0], self.v3[1] - self.v2[1])
        edge_vec3 = (self.v1[0] - self.v3[0], self.v1[1] - self.v3[1])

        point_vec1 = (point[0] - self.v1[0], point[1] - self.v1[1])
        point_vec2 = (point[0] - self.v2[0], point[1] - self.v2[1])
        point_vec3 = (point[0] - self.v3[0], point[1] - self.v3[1])

        cross1 = edge_vec1[0] * point_vec1[1] - edge_vec1[1] * point_vec1[0]
        cross2 = edge_vec2[0] * point_vec2[1] - edge_vec2[1] * point_vec2[0]
        cross3 = edge_vec3[0] * point_vec3[1] - edge_vec3[1] * point_vec3[0]

        # All points to the left of the edges (counter-clockwise order)
        if (cross1 >= 0 and cross2 >= 0 and cross3 >= 0):
            return True
        # All point to the right of the edges (clockwise order)
        if (cross1 <= 0 and cross2 <= 0 and cross3 <= 0):
            return True
        
        return False

class ImplicitFunction(Shape):
    def __init__(self, function):
        super().__init__("implicit_function")
        self.func = function

    def in_out(self, point):
        return self.func(point) <= 0