from OCC.Core.gp import gp_Pnt, gp_Pln
from OCC.Core.ChFi2d import ChFi2d_AnaFilletAlgo
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeFace, BRepBuilderAPI_MakeWire
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.GProp import GProp_GProps
from OCC.Extend.DataExchange import read_step_file
from OCC.Core.BRepGProp import brepgprop_VolumeProperties, brepgprop_SurfaceProperties, brepgprop_LinearProperties
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakeOffsetShape
import os
from OCC.Core.BRepBndLib import brepbndlib_Add
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.gp import gp_Pnt, gp_Trsf, gp_Vec, gp_Quaternion, gp_Mat, gp_Dir
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse, BRepAlgoAPI_Common, BRepAlgoAPI_Section, BRepAlgoAPI_Cut
from OCC.Core.BRepFeat import BRepFeat_Gluer
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeEdge, \
    BRepBuilderAPI_Copy
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
from OCC.Core.gp import gp_Pnt, gp_Trsf, gp_Vec, gp_Pln, gp_Dir, gp_Ax3
from OCC.Core.BRepGProp import brepgprop_VolumeProperties, brepgprop_SurfaceProperties, brepgprop_LinearProperties
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse, BRepAlgoAPI_Common, BRepAlgoAPI_Section, BRepAlgoAPI_Cut
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.TopoDS import topods, TopoDS_Edge, TopoDS_Compound
import os
from OCC.Core.BRepBndLib import brepbndlib_Add
from OCC.Extend.DataExchange import read_step_file
from OCC.Core.BRep import BRep_Tool_Pnt
from OCC.Extend.ShapeFactory import make_wire
import random
# import matplotlib.pyplot as plt
from OCC.Display.SimpleGui import init_display
from scipy.spatial.transform import Rotation as R
from OCC.Core.TopAbs import TopAbs_EDGE, TopAbs_FACE
from OCC.Core.TopoDS import topods_Face, topods_Edge
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Extend.DataExchange import read_step_file_with_names_colors
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from scipy.optimize import minimize
from collections import defaultdict
from OCC.Core.GC import GC_MakePlane


class Balance_mass:
    def __init__(self, frame, modules, walls):

        self.name_frame = frame
        self.modules = {}
        self.names_models = []
        self.history_args = {}
        self.valume_inter_obj = defaultdict(dict)

        # for testing, remove later

        self.inter_mass = 0
        self.reserv_models = {}
        # self.display, self.start_display, self.add_menu, self.add_function_to_menu = init_display()
        for model in modules:
            self.reserv_models[model[2]] = read_step_file(os.path.join(model[0], model[1], model[2]))

        self.walls = {}

        for number, wall in enumerate(walls):
            self.walls[number] = [[wall[0], wall[1], wall[2]], [wall[3], wall[4], wall[5]], [wall[6], wall[7], wall[8]], [wall[9],
                                                                                                         wall[10]]]

    def Body_change_location(self, number, name_body):
        cp = BRepBuilderAPI_Copy(self.reserv_models[name_body])
        cp.Perform(self.reserv_models[name_body])
        shape = cp.Shape()

        bbox = Bnd_Box()
        brepbndlib_Add(shape, bbox)
        xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()

        trsf = gp_Trsf()
        trsf.SetTranslation(gp_Vec(0, 0, -zmin))
        shape.Move(TopLoc_Location(trsf))

        Ax0 = gp_Ax3(gp_Pnt(0, 0, 0), gp_Dir(self.walls[number][1][2], self.walls[number][1][1], self.walls[number][1][0]))  # ,gp_Dir(gp_Vec(gp_Pnt(0, 0, 0), gp_Pnt(10, 0, 0))))


        '''Ax1 = gp_Ax3(gp_Pnt(self.walls[number][0][0], self.walls[number][0][1], self.walls[number][0][2]),
                     gp_Dir(gp_Vec(gp_Pnt(self.walls[number][0][0], self.walls[number][0][1], self.walls[number][0][2]),
                                   gp_Pnt(self.walls[number][1][0], self.walls[number][1][1],
                                          self.walls[number][1][2]))),
                     gp_Dir(gp_Vec(
                         gp_Pnt(self.walls[number][0][0], self.walls[number][0][1], self.walls[number][0][2]),
                         gp_Pnt(self.walls[number][2][0], self.walls[number][2][1], self.walls[number][2][2]))))'''

        Ax1 = gp_Ax3(gp_Pnt(-self.walls[number][0][0], -self.walls[number][0][1], -self.walls[number][0][2]),
                     gp_Dir(self.walls[number][1][0], self.walls[number][1][1], self.walls[number][1][2]))  # ,gp_Dir(gp_Vec(gp_Pnt(-110, 0, 0), gp_Pnt(110, 20, 0))))

        trsf = gp_Trsf()
        trsf.SetTransformation(Ax0, Ax1)
        shape.Move(TopLoc_Location(trsf))

        self.modules[name_body] = shape

    '''def Paralel_two_axis(self, shape, point1_1, point2_1, point1_2, point2_2):


        ax_eld = gp_Vec(gp_Pnt(point1_1[0], point1_1[1], point1_1[2]), gp_Pnt(point1_2[0], point1_2[1], point1_2[2]))
        ax_eld = gp_Vec(gp_Pnt(point1_1[0], point1_1[1], point1_1[2]), gp_Pnt(point1_2[0], point1_2[1], point1_2[2]))
        pln_1 = GC_MakePlane(gp_Pnt(point1_1[0], point1_1[1], point1_1[2]), gp_Pnt(point1_2[0], point1_2[1], point1_2[2]), )


        trsf = gp_Trsf()
        trsf.SetRotation(gp_Quaternion(Mat))
        shape.Move(TopLoc_Location(trsf))'''

    def vizualization_all(self):
        self.display, self.start_display, self.add_menu, self.add_function_to_menu = init_display()
        frame1 = read_step_file(os.path.join('part_of_sattelate', 'karkase', self.name_frame))
        self.display.DisplayShape(frame1, color='GREEN', transparency=0.9)
        for model in self.modules:
            self.display.DisplayShape(self.modules[model], color='RED', transparency=0.9)

        self.start_display()

    def var_test(self):

        print(self.reserv_models)
        for i, name_body in enumerate(self.reserv_models):
            self.Body_change_location(i, name_body)

if __name__ == '__main__':
    frame = ['part_of_sattelate', 'karkase', 'Assemb.STEP']
    modules = [ ['part_of_sattelate', 'pribore', 'Camara2_WS16.STEP'],
        # ['part_of_sattelate', 'pribore', 'DAV_WS16.STEP'],
        # ['part_of_sattelate', 'pribore', 'All_SEP_WS16.STEP'],
        # ['part_of_sattelate', 'pribore', 'Magnitometr.STEP'],
        # ['p3art_of_sattelate', 'pribore', 'Mahovik_WS16.STEP'],
        ['part_of_sattelate', 'pribore', 'Radio_WS16.STEP'],
        # ['part_of_sattelate', 'pribore', 'Solar_battery_WS16.STEP'],
        ['part_of_sattelate', 'pribore', 'UKV.STEP'],
        # ['part_of_sattelate', 'pribore', 'DAV_WS16.STEP'],
        ['part_of_sattelate', 'pribore', 'Vch_translator_WS16.STEP']]
    walls = [[0, 0, 110, 10, 0, 0, 0, 10, 0, 186, 248],
        [250, 0, 0, 0, 10, 0, 0, 10, 0, 186, 248],
        [0, 0, 110, -10, 0, 0, 0, 10, 0, 186, 248],
        [0, 110, 0,
         10, 0, 0,
         0, 10, 0, 186, 248]]

    # distant between xero point and face plt, normal of wall

    test = Balance_mass('Assemb.STEP', modules, walls)
    test.var_test()
    test.vizualization_all()
