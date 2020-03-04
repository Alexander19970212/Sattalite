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
from OCC.Core.gp import gp_Pnt, gp_Trsf, gp_Vec, gp_Pln, gp_Dir, gp_Ax3, gp_Ax1
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
from OCC.Core.BOPAlgo import BOPAlgo_COMMON
import math


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

        self.walls = walls

        '''for number, wall in enumerate(walls):
            self.walls[number] = [[wall[0], wall[1], wall[2]], [wall[3], wall[4], wall[5]], [wall[3], wall[4], wall[5]],
                                  [wall[6], wall[7]]]'''

    def rot_point(self, x, y, angle):

        x1, y1 = -x / 2, y / 2
        x2, y2 = x / 2, y / 2

        ox = 0
        oy = 0

        x1_n = ox + math.cos(angle) * (x1 - ox) - math.sin(angle) * (y1 - oy)
        y1_n = oy + math.sin(angle) * (x1 - ox) + math.cos(angle) * (y1 - oy)
        x2_n = ox + math.cos(angle) * (x2 - ox) - math.sin(angle) * (y2 - oy)
        y2_n = oy + math.sin(angle) * (x2 - ox) + math.cos(angle) * (y2 - oy)

        return max(abs(x1_n), abs(x2_n)), max(abs(y1_n), abs(y2_n))

    def Locate_centre_face(self, number, name_body, angle, x_drive, y_drive):
        cp = BRepBuilderAPI_Copy(self.reserv_models[name_body])
        cp.Perform(self.reserv_models[name_body])
        shape = cp.Shape()

        # move to zero
        bbox = Bnd_Box()
        brepbndlib_Add(shape, bbox)
        xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()

        trsf = gp_Trsf()
        trsf.SetTranslation(gp_Vec(-xmin - (xmax - xmin) / 2, -ymin - (ymax - ymin) / 2, -zmin))
        shape.Move(TopLoc_Location(trsf))

        # Process vector of rotation to face
        x = -self.walls[number][1][1]
        y = self.walls[number][1][0]
        z = 0
        P0 = gp_Pnt(0, 0, 0)
        P1 = gp_Pnt(0, 0, 1)
        P2 = gp_Pnt(self.walls[number][1][0], self.walls[number][1][1], self.walls[number][1][2])

        # rotation to Ax z
        v_x = gp_Vec(P0, gp_Pnt(0, 1, 0))
        v_r = gp_Vec(P0, gp_Pnt(x, y, z))
        trsf = gp_Trsf()
        trsf.SetRotation(gp_Ax1(P0, gp_Dir(0, 0, 1)), v_r.Angle(v_x))
        shape.Move(TopLoc_Location(trsf))

        # rotation in parallel to face
        v0 = gp_Vec(P0, P1)
        v1 = gp_Vec(P0, P2)
        #print(v1.Angle(v0))
        trsf = gp_Trsf()
        trsf.SetRotation(gp_Ax1(P0, gp_Dir(x, y, z)), v1.Angle(v0))
        # move to face
        shape.Move(TopLoc_Location(trsf))
        trsf = gp_Trsf()
        trsf.SetTranslation(gp_Vec(self.walls[number][0][0], self.walls[number][0][1], self.walls[number][0][2]))
        shape.Move(TopLoc_Location(trsf))

        # Rotation by given angle
        trsf = gp_Trsf()
        trsf.SetRotation(
            gp_Ax1(P0, gp_Dir(self.walls[number][1][0], self.walls[number][1][1], self.walls[number][1][2])), angle)
        shape.Move(TopLoc_Location(trsf))

        # initional x, y
        offset_y, offset_x = self.rot_point(xmax - xmin, ymax - ymin, angle)

        limit_x = self.walls[number][3][0] / 2 - offset_x
        limit_y = self.walls[number][3][1] / 2 - offset_y

        move_x = limit_x * x_drive
        move_y = limit_y * y_drive


        # Move to x and y
        x_axy = self.walls[number][1][1] * self.walls[number][2][2] - self.walls[number][1][2] * self.walls[number][2][
            1]
        y_axy = -(self.walls[number][1][0] * self.walls[number][2][2] - self.walls[number][1][2] *
                  self.walls[number][2][
                      0])
        z_axy = self.walls[number][1][0] * self.walls[number][2][1] - self.walls[number][1][1] * self.walls[number][2][
            0]


        x_axy *= move_y
        y_axy *= move_y
        z_axy *= move_y

        trsf = gp_Trsf()
        trsf.SetTranslation(gp_Vec(x_axy, y_axy, z_axy))
        shape.Move(TopLoc_Location(trsf))

        trsf = gp_Trsf()
        trsf.SetTranslation(gp_Vec(self.walls[number][2][0] * move_x, self.walls[number][2][1] * move_x,
                                   self.walls[number][2][2] * move_x))
        shape.Move(TopLoc_Location(trsf))

        self.modules[name_body] = shape

    # def rotate_by_centre(self, shape, number, angle, P0, P2):

    def vizualization_all(self):
        # print(self.modules)
        self.display, self.start_display, self.add_menu, self.add_function_to_menu = init_display()
        frame1 = read_step_file(os.path.join('part_of_sattelate', 'karkase', self.name_frame))
        self.display.DisplayShape(frame1, color='GREEN', transparency=0.9)
        for model in self.modules:
            self.display.DisplayShape(self.modules[model], color='RED', transparency=0.9)

        self.start_display()

    def move_frame(self):
        from OCC.Core.BOPAlgo import BOPAlgo_Builder
        from OCC.Extend.DataExchange import read_step_file_with_names_colors
        self.frame = read_step_file(os.path.join('part_of_sattelate', 'karkase', self.name_frame))
        '''frame = read_step_file_with_names_colors('part_of_sattelate/karkase/Assemb.STEP')

        #shapes = list(Topo(frame).myShape())

        builder = BOPAlgo_Builder()

        for name in frame:
            builder.AddArgument(name)

        builder.SetRunParallel(True)
        builder.Perform()
        self.frame = builder.Shape()'''

    def inter_with_frame(self):
        # print('Start_inter_analyse')
        all_result = 0
        props = GProp_GProps()
        # print(self.modules)
        for model in self.modules:
            # print('#')
            body_inter = BRepAlgoAPI_Common(self.frame, self.modules[model]).Shape()
            # self.display.DisplayShape(body_inter, color='YELLOW')
            brepgprop_VolumeProperties(body_inter, props)
            mass = props.Mass()
            if mass > 0:
                all_result += mass

        return all_result

    def var_test(self):

        # print(self.reserv_models)
        for i, name_body in enumerate(self.reserv_models):
            # print(name_body)
            self.Locate_centre_face(i, name_body, 0, 1, 1)


if __name__ == '__main__':
    frame = ['part_of_sattelate', 'karkase', 'Assemb.STEP']
    modules = [  # ['part_of_sattelate', 'pribore', 'Camara2_WS16.STEP'],
        ['part_of_sattelate', 'pribore', 'DAV_WS16.STEP'],
        # ['part_of_sattelate', 'pribore', 'All_SEP_WS16.STEP'],
        # ['part_of_sattelate', 'pribore', 'Magnitometr.STEP'],
        # ['p3art_of_sattelate', 'pribore', 'Mahovik_WS16.STEP'],
        ['part_of_sattelate', 'pribore', 'Radio_WS16.STEP'],
        # ['part_of_sattelate', 'pribore', 'Solar_battery_WS16.STEP'],
        ['part_of_sattelate', 'pribore', 'UKV.STEP'],
        # ['part_of_sattelate', 'pribore', 'DAV2_WS16.STEP'],
        ['part_of_sattelate', 'pribore', 'Vch_translator_WS16.STEP']]
    '''walls = [[110, 0, 10, 0, -10, 0, 0, 186, 248],
             [110, 0, 10, 0, 0, 0, 10, 186, 248],
             [110, 0, 10, 0, 10, 0, 0, 186, 248],
             [110, 0, 10, 0, 0, 0, -10, 186, 248], ]'''

    walls = [[[0, 110, 0], [0, 1, 0], [1, 0, 0], [186, 248]],
             [[110, 0, 0], [1, 0, 0], [0, -1, 0], [186, 248]],
             [[0, -110, 0], [0, -1, 0], [-1, 0, 0], [186, 248]],
             [[-110, 0, 0], [-1, 0, 0], [0, 1, 0], [186, 248]]]

    # point of centre, normal, Axis-x, bound of x and y
    # distant between xero point and face plt, normal of wall
    # distant between zero point anf face plt, vector that will drop axis z, vector сонаправленный X

    test = Balance_mass('Assemb.STEP', modules, walls)
    test.var_test()
    test.move_frame()
    print(test.inter_with_frame())
    test.vizualization_all()
