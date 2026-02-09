from src.base import BaseScene, Color
from src.shapes import Mandelbrot

# class name should be Scene
class Scene(BaseScene):
    def __init__(self):
        super().__init__("Mandelbrot Fractal Scene")
        self.background = Color(0, 0, 0)  # Black background

        # Create Mandelbrot set with high iteration count for detail
        mandelbrot = Mandelbrot(max_iterations=200, escape_radius=2.0)
        
        # The set itself is white
        self.add(mandelbrot, Color(1.0, 1.0, 1.0))