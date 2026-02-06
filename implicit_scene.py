from src.shapes import ImplicitFunction
from src.base import BaseScene, Color

# class name should be Scene
class Scene(BaseScene):
    def __init__(self):
        super().__init__("Implicit Scene")
        self.background = Color(1, 1, 1)

        def implicit_func(point):
            x, y = point
            return (0.004 + 0.110*x - 0.177*y - 0.174*x**2 + 0.224*x*y - 
                    0.303*y**2 - 0.168*x**3 + 0.327*x**2*y - 0.087*x*y**2 - 
                    0.013*y**3 + 0.235*x**4 - 0.667*x**3*y + 0.745*x**2*y**2 - 
                    0.029*x*y**3 + 0.072*y**4)

        self.add(ImplicitFunction(implicit_func), Color(1, 0, 0))  # Implicit function in red