from OCC.Display.SimpleGui import init_display

from OCC.Core.gp import gp_Pnt
from OCC.Core.GeomAbs import GeomAbs_Arc
#from OCC.Core.BRepPrimAPI import BrepPrimAPI_MakeBox
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakePolygon
#import ifc_builder
#import ifcopenshell.geom
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakeEvolved
from OCC.Display.SimpleGui import init_display
display, start_display, add_menu, add_function_to_menu = init_display()

#display, start_display, add_menu, add_function_to_menu = init_display()
#my_box = BrepPrimAPI_MakeBox(10., 20., 30.).Shape()
#my_poly = BRepBuilderAPI_MakePolygon((0., 0., 0.), (2., 2., 2.), (0., 0., 5.))
# P = BRepBuilderAPI_MakePolygon()
# P.Add(gp_Pnt(0., 0., 0.))
# P.Add(gp_Pnt(200., 0., 0.))
# P.Add(gp_Pnt(200., 200., 0.))
# P.Add(gp_Pnt(0., 200., 0.))
# P.Add(gp_Pnt(0., 0., 0.))
# wprof = BRepBuilderAPI_MakePolygon(gp_Pnt(0., 0., 0.), gp_Pnt(-60., -60., -200.))
# S = BRepOffsetAPI_MakeEvolved(P.Wire(), wprof.Wire(), GeomAbs_Arc, True, False, True, 0.0001)
# S.Build()
# display.DisplayShape(S.Shape(), update=True)


def evolved_shape():
    P = BRepBuilderAPI_MakePolygon()
    P.Add(gp_Pnt(0., 0., 0.))
    P.Add(gp_Pnt(200., 0., 0.))
    P.Add(gp_Pnt(200., 200., 0.))
    P.Add(gp_Pnt(0., 200., 0.))
    P.Add(gp_Pnt(0., 0., 0.))
    wprof = BRepBuilderAPI_MakePolygon(gp_Pnt(0., 0., 0.), gp_Pnt(-60., -60., -200.))
    S = BRepOffsetAPI_MakeEvolved(P.Wire(),
                                  wprof.Wire(),
                                  GeomAbs_Arc,
                                  True,
                                  False,
                                  True,
                                  0.0001)
    S.Build()
    display.DisplayShape(S.Shape(), update=True)


if __name__ == '__main__':
    evolved_shape()
    start_display()

#display.DisplayShape(my_poly, update=True)
#start_display()
#ifcopenshell.geom.utils.main_loop()
