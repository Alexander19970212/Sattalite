from OCC.Core.BRepFeat import BRepFeat_Gluer
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeEdge
from OCC.Display.SimpleGui import init_display
from OCC.Core.LocOpe import LocOpe_FindEdges
from OCC.Core.TopAbs import TopAbs_FACE, TopAbs_VERTEX
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Core.TopoDS import topods_Face, topods_Edge, topods_Compound, topods_Wire, topods_Shell, topods, \
    topods_CompSolid, TopoDS_Iterator, topods_Vertex
from OCC.Core.TopAbs import TopAbs_EDGE, TopAbs_FACE, TopAbs_REVERSED, TopAbs_SHAPE, TopAbs_COMPOUND, TopAbs_REVERSED, \
    TopAbs_IN
from OCCUtils.Topology import Topo
from OCC.Core.GProp import GProp_GProps
from OCC.Core.gp import gp_Pnt, gp_Trsf, gp_Vec, gp_Pln, gp_Dir
from OCC.Core.BRepGProp import brepgprop_VolumeProperties, brepgprop_SurfaceProperties, brepgprop_LinearProperties
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse, BRepAlgoAPI_Common, BRepAlgoAPI_Section, BRepAlgoAPI_Cut
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.TopoDS import topods, TopoDS_Edge, TopoDS_Compound
import os
from OCC.Core.BRepBndLib import brepbndlib_Add
from OCC.Extend.DataExchange import read_step_file
from OCC.Core.BRep import BRep_Tool_Pnt
from OCC.Core.ShapeAnalysis import ShapeAnalysis_FreeBounds, ShapeAnalysis_FreeBounds_ConnectEdgesToWires
from OCC.Core.TopTools import TopTools_HSequenceOfShape, TopTools_SequenceOfShape, \
    Handle_TopTools_HSequenceOfShape_Create, Handle_TopTools_HSequenceOfShape_DownCast, Handle_TopTools_HSequenceOfShape_IsNull
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
    # S2 = BRepPrimAPI_MakeBox(gp_Pnt(300., 300., 300.), gp_Pnt(600., 600., 600.)).Shape()
    S2 = read_step_file(os.path.join('..', 'part_of_sattelate', 'pribore', 'DAV3_WS16.STEP'))
    bbox = Bnd_Box()
    brepbndlib_Add(S2, bbox)
    xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
    p0 = gp_Pnt(xmin + (xmax - xmin) / 2, ymin + (ymax - ymin) / 2, zmin)

    vnorm = gp_Dir(0, 0, 1)
    pln = gp_Pln(p0, vnorm)
    face = BRepBuilderAPI_MakeFace(pln, -(xmax - xmin) / 2 - 1, (xmax - xmin) / 2 + 1, -(ymax - ymin) / 2 - 1,
                                   (ymax - ymin) / 2 + 1).Face()
    # face = BRepBuilderAPI_MakeFace(pln, -10, 10, -10,10).Face()
    '''planeZ = BRepBuilderAPI_MakeFace(
        gp_Pln(gp_Pnt(xmin, ymin, zmin), gp_Pnt(xmax, ymax, zmin), gp_Pnt(xmin, ymax, zmin))).Face()'''
    facesS_2 = BRepAlgoAPI_Section(face, S2).Shape()
    # print(facesS_2)
    #display.DisplayShape(facesS_2, update=True)

    section_edges = list(Topo(facesS_2).edges())
    print(len(section_edges))

    '''toptool_seq_shape = TopTools_SequenceOfShape()
    for edge in section_edges:
        toptool_seq_shape.Append(edge)'''

    Wire_c = BRepBuilderAPI_MakeWire()

    Wire_c.Add(section_edges[0])
    ex = TopExp_Explorer(section_edges[0], TopAbs_VERTEX)

    # no need for a loop since we know for a fact that
    # the edge has only one start and one end
    c = ex.Current()
    cv = topods_Vertex(c)
    v0 = BRep_Tool_Pnt(cv)
    ex.Next()
    c = ex.Current()
    cv = topods_Vertex(c)
    v1 = BRep_Tool_Pnt(cv)
    section_edges.pop(0)

    while len(section_edges) > 0:

        new_list = []

        for edges in section_edges:
            Wire_c.Add(edges)
            ex = TopExp_Explorer(edges, TopAbs_VERTEX)
            c = ex.Current()
            cv = topods_Vertex(c)
            End_1 = BRep_Tool_Pnt(cv)
            ex.Next()
            c = ex.Current()
            cv = topods_Vertex(c)
            End_2 = BRep_Tool_Pnt(cv)

            if End_1.X() == v0.X() and End_1.Y() == v0.Y() and End_1.Z() == v0.Z():
                Wire_c.Add(edges)
                v0 = End_2
            elif End_1.X() == v1.X() and End_1.Y() == v1.Y() and End_1.Z() == v1.Z():
                Wire_c.Add(edges)
                v1 = End_2
            elif End_2.X() == v0.X() and End_2.Y() == v0.Y() and End_2.Z() == v0.Z():
                Wire_c.Add(edges)
                v0 = End_1
            elif End_2.X() == v1.X() and End_2.Y() == v1.Y() and End_2.Z() == v1.Z():
                Wire_c.Add(edges)
                v1 = End_1
            else:
                new_list.append(edges)

        section_edges = new_list
        print('+')






    yellow_wire = Wire_c.Wire()
    brown_face = BRepBuilderAPI_MakeFace(yellow_wire)
    display.DisplayColoredShape(brown_face.Face(), 'BLUE')

    #myWireProfile = Wire.Wire()
    #myFaceProfile = BRepBuilderAPI_MakeFace(myWireProfile)
    #display.DisplayShape(myFaceProfile, color='BLUE', transparency=0.9)




if __name__ == "__main__":
    menu_name = 'glue topology'
    add_menu(menu_name)
    add_function_to_menu(menu_name, glue_solids)
    # add_function_to_menu(menu_name, exit)
    start_display()
