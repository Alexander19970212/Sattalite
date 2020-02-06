from OCC.Core.BRepFeat import BRepFeat_Gluer
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeEdge
from OCC.Display.SimpleGui import init_display
from OCC.Core.LocOpe import LocOpe_FindEdges
from OCC.Core.TopAbs import TopAbs_FACE
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Core.TopoDS import topods_Face, topods_Edge
from OCC.Core.TopAbs import TopAbs_EDGE, TopAbs_FACE, TopAbs_REVERSED
from OCC.Core.GProp import GProp_GProps
from OCC.Core.gp import gp_Pnt, gp_Trsf, gp_Vec, gp_Pln, gp_Dir
from OCC.Core.BRepGProp import brepgprop_VolumeProperties, brepgprop_SurfaceProperties, brepgprop_LinearProperties
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse, BRepAlgoAPI_Common, BRepAlgoAPI_Section, BRepAlgoAPI_Cut
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.TopoDS import topods, TopoDS_Edge, TopoDS_Compound
import os
from OCC.Core.BRepBndLib import brepbndlib_Add
from OCC.Extend.TopologyUtils import TopologyExplorer

from OCC.Extend.ShapeFactory import center_boundingbox

display, start_display, add_menu, add_function_to_menu = init_display()


def get_faces(_shape):
    """ return the faces from `_shape`
    :param _shape: TopoDS_Shape, or a subclass like TopoDS_Solid
    :return: a list of faces found in `_shape`
    """
    topExp = TopExp_Explorer()
    topExp.Init(_shape, TopAbs_FACE)
    _faces = []

    while topExp.More():
        fc = topods_Face(topExp.Current())
        # print(fc)
        _faces.append(fc)
        topExp.Next()

    return _faces


def glue_solids(event=None):
    display.EraseAll()
    display.Context.RemoveAll(True)
    # Without common edges
    S1 = BRepPrimAPI_MakeBox(gp_Pnt(500., 500., 0.), gp_Pnt(100., 250., 300.)).Shape()
    S2 = BRepPrimAPI_MakeBox(gp_Pnt(300., 300., 300.), gp_Pnt(600., 600., 600.)).Shape()
    bbox = Bnd_Box()
    brepbndlib_Add(S2, bbox)
    xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
    p0 = gp_Pnt(xmin+(xmax-xmin)/2, ymin + (ymax-ymin)/2, zmin)

    vnorm = gp_Dir(0, 0, 1)
    pln = gp_Pln(p0, vnorm)
    face = BRepBuilderAPI_MakeFace(pln, -(xmax-xmin)/2-1, (xmax-xmin)/2+1, -(ymax-ymin)/2-1, (ymax-ymin)/2+1).Face()
    #face = BRepBuilderAPI_MakeFace(pln, -10, 10, -10,10).Face()
    '''planeZ = BRepBuilderAPI_MakeFace(
        gp_Pln(gp_Pnt(xmin, ymin, zmin), gp_Pnt(xmax, ymax, zmin), gp_Pnt(xmin, ymax, zmin))).Face()'''
    facesS_2 = BRepAlgoAPI_Section(face, S2).Shape()
    print(facesS_2)

    #aMirroredWire = topods.Wire(facesS_2)

    props = GProp_GProps()
    brepgprop_LinearProperties(facesS_2, props)
    # Get inertia properties
    mass_1 = props.Mass()
    print(mass_1)

    '''MW1 = BRepBuilderAPI_MakeWire(facesS_2)
    print(MW1)'''

    # Ex = TopExp_Explorer(facesS_2, TopAbs_EDGE)
    # print(Ex)

    topExp = TopExp_Explorer()
    topExp.Init(facesS_2, TopAbs_EDGE)
    edges = []
    #https://www.freecadweb.org/wiki/Topological_data_scripting

    while topExp.More():
        fc = topods_Edge(topExp.Current())
        # print(fc)
        edges.append(fc)
        topExp.Next()

    print(edges)

    MW1 = BRepBuilderAPI_MakeWire()
    for edge in edges:
        MW1.Add(edge)
########################################################################################end

    #MW1 = BRepBuilderAPI_MakeWire(edges[0], edges[1], edges[2], edges[3])
    if not MW1.IsDone():
        raise AssertionError("MW1 is not done.")
    yellow_wire = MW1.Wire()
    brown_face = BRepBuilderAPI_MakeFace(yellow_wire)
    display.DisplayColoredShape(brown_face.Face(), 'BLUE')

    props = GProp_GProps()
    brepgprop_SurfaceProperties(facesS_2, props)
    # Get inertia properties
    mass_3 = props.Mass()
    print(mass_3)


    display.DisplayShape(p0, update=True)
    display.DisplayShape(facesS_2, update=True)

    facesS = BRepAlgoAPI_Section(S1, S2).Shape()
    print(facesS)

    props = GProp_GProps()
    brepgprop_LinearProperties(facesS, props)
    # Get inertia properties
    mass_2 = props.Mass()
    print(mass_2)

    print((mass_1 - mass_2)/mass_1)


    display.DisplayShape(facesS, update=True)

    '''#t = TopologyExplorer(facesS)
    props = GProp_GProps()
    #for face in t.faces():
    brepgprop_SurfaceProperties(facesS, props)
    face_surf = props.Mass()
    #shp_idx = 1
    print("Surface for face nbr %i : %f" % ('1', face_surf))'''

    '''t = TopologyExplorer(the_shape)
    props = GProp_GProps()
    shp_idx = 1
    for face in t.faces():
        brepgprop_SurfaceProperties(face, props)
        face_surf = props.Mass()
        print("Surface for face nbr %i : %f" % (shp_idx, face_surf))
        shp_idx += 1'''


if __name__ == "__main__":
    menu_name = 'glue topology'
    add_menu(menu_name)
    add_function_to_menu(menu_name, glue_solids)
    # add_function_to_menu(menu_name, exit)
    start_display()
