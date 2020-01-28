from OCC.Core.gp import gp_Lin2d, gp_Pnt2d, gp_Dir2d
from OCC.Display.SimpleGui import init_display

# from core_geometry_utils import make_edge2d
from OCC.Extend.ShapeFactory import make_edge2d

display, start_display, add_menu, add_function_to_menu = init_display()

# Creating 2d points
p1 = gp_Pnt2d(2., 3.)
p2 = gp_Pnt2d(2., 5.)
display.DisplayShape(p1)
display.DisplayShape(p2, update=True)

# Creating a 2d line requires: a point and a direction
d1 = gp_Dir2d(1., 1.)
l1 = gp_Lin2d(p1, d1)
display.DisplayShape(make_edge2d(l1), update=True)