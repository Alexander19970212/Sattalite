from OCC.Display.SimpleGui import init_display
#from OCC.Core.BRepPrimAPI import BrepPrimAPI_MakeBox
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakePolygon
import ifc_builder
import ifcopenshell.geom

display, start_display, add_menu, add_function_to_menu = init_display()
#my_box = BrepPrimAPI_MakeBox(10., 20., 30.).Shape()
my_poly = BRepBuilderAPI_MakePolygon((0., 0., 0.), (2., 2., 2.), (0., 0., 5.))

display.DisplayShape(my_poly, update=True)
start_display()
ifcopenshell.geom.utils.main_loop()
