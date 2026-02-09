from src.base import BaseScene, Color
from src.shapes import MandelbrotColored
import math

class MandelbrotColoredShape(MandelbrotColored):
# Extended Mandelbrot that provides color based on iteration count
    def __init__(self, max_iterations=100):
        super().__init__(max_iterations)
        self.colors = self._generate_color_palette()
    
    def _generate_color_palette(self):
        # Generate a smooth color palette for the fractal
        colors = []
        for i in range(self.max_iterations):
            t = i / self.max_iterations
            # Create a smooth color transition
            r = 0.5 + 0.5 * math.cos(3.0 + t * 6.28)
            g = 0.5 + 0.5 * math.cos(2.0 + t * 6.28)  
            b = 0.5 + 0.5 * math.cos(1.0 + t * 6.28)
            colors.append(Color(r, g, b))
        colors.append(Color(0, 0, 0))  # Black for points in the set
        return colors
    
    def get_color(self, point):
        # Get color based on iteration count
        iterations = self.iteration_count(point)
        if iterations >= self.max_iterations:
            return Color(0, 0, 0)  # Black for points in the set
        else:
            return self.colors[iterations]

# class name should be Scene
class Scene(BaseScene):
    def __init__(self):
        super().__init__("Mandelbrot Colored Fractal Scene") 
        self.background = Color(0.1, 0.1, 0.2)  # Dark blue background
        
        # We'll handle coloring in a custom way, so we use a single colored shape
        mandelbrot = MandelbrotColoredShape(max_iterations=80)
        
        # Add the mandelbrot with a default color (will be overridden in custom eval_point)
        self.add(mandelbrot, Color(1.0, 1.0, 1.0))
        self.mandelbrot_shape = mandelbrot  # Keep reference for custom coloring
    
    def get_point_color(self, point):
        # Custom method to get color at a point
        return self.mandelbrot_shape.get_color(point)