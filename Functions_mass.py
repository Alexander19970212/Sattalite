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

from OCC.Extend.ShapeFactory import make_wire
import random
from OCC.Display.SimpleGui import init_display
from scipy.spatial.transform import Rotation as R
from OCC.Core.TopAbs import TopAbs_EDGE, TopAbs_FACE
from OCC.Core.TopoDS import topods_Face, topods_Edge
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Extend.DataExchange import read_step_file_with_names_colors
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB


class Balance_mass:
    def __init__(self, frame, modules):

        self.name_frame = frame
        self.modules = {}

        #for testing, remove later
        self.d = 3.1
        self.px = 220 - self.d/2
        self.py = 220 - self.d/2
        self.pz = 246


        self.dimensoins = {}
        self.profiles = {}
        self.display, self.start_display, self.add_menu, self.add_function_to_menu = init_display()
        for model in modules:
            self.modules[model[2]] = read_step_file(os.path.join(model[0], model[1], model[2]))

        for model in self.modules:
            bbox = Bnd_Box()
            brepbndlib_Add(self.modules[model], bbox)
            xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
            self.dimensoins[model] = [xmin, xmax, ymin, ymax, zmin, zmax]
            p0 = gp_Pnt(xmin + (xmax - xmin) / 2, ymin + (ymax - ymin) / 2, zmin)

            vnorm = gp_Dir(0, 0, 1)
            pln = gp_Pln(p0, vnorm)
            face = BRepBuilderAPI_MakeFace(pln, -(xmax - xmin) / 2 - 1, (xmax - xmin) / 2 + 1, -(ymax - ymin) / 2 - 1,
                                           (ymax - ymin) / 2 + 1).Face()
            facesS_2 = BRepAlgoAPI_Section(face, self.modules[model]).Shape()
            props = GProp_GProps()
            brepgprop_LinearProperties(facesS_2, props)
            mass_1 = props.Mass()
            topExp = TopExp_Explorer()
            topExp.Init(facesS_2, TopAbs_EDGE)
            edges = []
            while topExp.More():
                fc = topods_Edge(topExp.Current())
                # print(fc)
                edges.append(fc)
                topExp.Next()
            MW1 = BRepBuilderAPI_MakeWire()
            for edge in edges:
                MW1.Add(edge)
            '''if not MW1.IsDone():
                raise AssertionError("MW1 is not done.")'''
            yellow_wire = MW1.Wire()
            brown_face = BRepBuilderAPI_MakeFace(yellow_wire)
            #display.DisplayColoredShape(brown_face.Face(), 'BLUE')
            props = GProp_GProps()
            brepgprop_SurfaceProperties(brown_face, props)
            # Get inertia properties
            mass_3 = props.Mass()
            self.profiles[model] = [mass_1, mass_3]

        print(self.profiles)

    def move_frame(self):
        self.frame = read_step_file(os.path.join('part_of_sattelate', 'karkase', self.name_frame))
        self.vizualization(self.frame, 'RED', 0.9)


    def change_position1(self, name, number_wall, pos_1, pos_2, pos_3):
        number_wall = int(number_wall % 7)

        alpha, beta, gamma, offset_x, offset_y, offset_z = 0, 0, 0, 0, 0, 0

        pos_3 = int(pos_3 // 3) * 90
        if number_wall == 0:
            alpha = 90
            offset_y = self.py / 2 - self.d / 2 + self.dimensoins[name][4]
            beta = pos_3
            if pos_1 >= self.px / 2: offset_x = self.px / 2
            elif pos_1 <= -self.px / 2:
                offset_x = -self.px / 2
            else:
                offset_x = pos_1

            if pos_2 >= self.pz / 2: offset_z = self.pz / 2
            elif pos_2 <= -self.pz / 2:
                offset_z = -self.pz / 2
            else:
                offset_z = pos_2
            gamma = 0

        if number_wall == 1:
            alpha = -90
            offset_y = self.py / 2 + self.d / 2 - self.dimensoins[name][4]
            beta = pos_3
            if pos_1 >= self.px / 2: offset_x = self.px / 2
            elif pos_1 <= -self.px / 2:
                offset_x = -self.px / 2
            else:
                offset_x = pos_1

            if pos_2 >= self.pz / 2: offset_z = self.pz / 2
            elif pos_2 <= -self.pz / 2:
                offset_z = -self.pz / 2
            else:
                offset_z = pos_2
            gamma = 0

        if number_wall == 2:
            beta = -90
            offset_x = self.px / 2 - self.d / 2 + self.dimensoins[name][4]
            alpha = pos_3
            if pos_1 >= self.py / 2: offset_y = self.py / 2
            elif pos_1 <= -self.py / 2:
                offset_y = -self.py / 2
            else:
                offset_y = pos_1

            if pos_2 >= self.pz / 2: offset_z = self.pz / 2
            elif pos_2 <= -self.pz / 2:
                offset_z = -self.pz / 2
            else:
                offset_z = pos_2
            gamma = 0

        if number_wall == 3:
            beta = 90
            offset_x = self.px / 2 + self.d / 2 - self.dimensoins[name][4]
            alpha = pos_3
            if pos_1 >= self.py / 2: offset_y = self.py / 2
            elif pos_1 <= -self.py / 2:
                offset_y = -self.py / 2
            else:
                offset_y = pos_1

            if pos_2 >= self.pz / 2: offset_z = self.pz / 2
            elif pos_2 <= -self.pz / 2:
                offset_z = -self.pz / 2
            else:
                offset_z = pos_2
            gamma = 0

        if number_wall == 4:
            alpha = -90
            offset_y = -(self.py / 2 - self.d / 2 + self.dimensoins[name][4])
            beta = pos_3
            if pos_1 >= self.px / 2: offset_x = self.px / 2
            elif pos_1 <= -self.px / 2:
                offset_x = -self.px / 2
            else:
                offset_x = pos_1

            if pos_2 >= self.pz / 2: offset_z = self.pz / 2
            elif pos_2 <= -self.pz / 2:
                offset_z = -self.pz / 2
            else:
                offset_z = pos_2
            gamma = 0

        if number_wall == 5:
            alpha = 90
            offset_y = -(self.py / 2 + self.d / 2 - self.dimensoins[name][4])
            beta = pos_3
            if pos_1 >= self.px / 2: offset_x = self.px / 2
            elif pos_1 <= -self.px / 2:
                offset_x = -self.px / 2
            else:
                offset_x = pos_1

            if pos_2 >= self.pz / 2: offset_z = self.pz / 2
            elif pos_2 <= -self.pz / 2:
                offset_z = -self.pz / 2
            else:
                offset_z = pos_2
            gamma = 0

        if number_wall == 6:
            beta = 90
            offset_x = -(self.px / 2 - self.d / 2 + self.dimensoins[name][4])
            alpha = pos_3
            if pos_1 >= self.py / 2: offset_y = self.py / 2
            elif pos_1 <= -self.py / 2:
                offset_y = -self.py / 2
            else:
                offset_y = pos_1

            if pos_2 >= self.pz / 2: offset_z = self.pz / 2
            elif pos_2 <= -self.pz / 2:
                offset_z = -self.pz / 2
            else:
                offset_z = pos_2
            gamma = 0

        if number_wall == 7:
            beta = -90
            offset_x = -(self.px / 2 + self.d / 2 - self.dimensoins[name][4])
            alpha = pos_3
            if pos_1 >= self.py / 2: offset_y = self.py / 2
            elif pos_1 <= -self.py / 2:
                offset_y = -self.py / 2
            else:
                offset_y = pos_1

            if pos_2 >= self.pz / 2:
                offset_z = self.pz / 2
            elif pos_2 <= -self.pz / 2:
                offset_z = -self.pz / 2
            else:
                offset_z = pos_2
            gamma = 0

        self.filling(name, [alpha, beta, gamma, offset_x, offset_y, offset_z])

    def change_object(self):
        pass

    def filling(self, name_body, coord_centres):
        '''

        :param name_body:
        :param coord_centres: 0 - угол поворота x (градусы)
        1 - угол поворота y (градусы)
        2 - угол поворота z (градусы)
        3 - смещенмие по x
        4 - смещенмие по y
        5 - смещенмие по z
        :return:
        '''
        print(name_body)
        shape = self.modules[name_body]
        # print(body)

        r = R.from_euler('xyz', [coord_centres[0], coord_centres[1], coord_centres[2]], degrees=True)
        Rot = r.as_dcm()

        trsf = gp_Trsf()
        Mat = gp_Mat(Rot[0][0], Rot[0][1], Rot[0][2],
                     Rot[1][0], Rot[1][1], Rot[1][2],
                     Rot[2][0], Rot[2][1], Rot[2][2])

        trsf.SetRotation(gp_Quaternion(Mat))
        shape.Move(TopLoc_Location(trsf))

        trsf = gp_Trsf()

        trsf.SetTranslation(gp_Vec(coord_centres[3], coord_centres[4], coord_centres[5]))
        shape.Move(TopLoc_Location(trsf))

    def inter_objects(self):
        pass

    def centre_mass(self):
        pass

    def moment_inertial(self):
        pass

    def goal_function(self):
        pass

    def save_assembly(self):
        pass

    def termal_analysis(self):
        pass

    def move_in_inter(self):
        pass

    def vizualization(self, shape, color, transp):
        self.display.DisplayShape(shape, color=color, transparency=transp)
        self.start_display()

    def vizualization_all(self):
        frame1 = read_step_file(os.path.join('part_of_sattelate', 'karkase', self.name_frame))
        self.display.DisplayShape(frame1, color='GREEN', transparency=0.9)
        for model in self.modules:
            self.display.DisplayShape(self.modules[model], color='RED')


        self.start_display()

    def body_random(self):
        for name in self.modules:
            pos_1 = random.uniform(max(self.px, self.py) / 2, -max(self.px, self.py) / 2)
            pos_2 = random.uniform(self.pz / 2, -self.pz / 2)
            pos_3 = random.uniform(0, 4)
            Number_wall = random.uniform(0, 9)

            self.change_position1(name, Number_wall, pos_1, pos_2, pos_3)

if __name__ == '__main__':
    frame = ['part_of_sattelate', 'karkase','Assemb.STEP']
    modules = [['part_of_sattelate', 'pribore', 'Camara_WS16.STEP'],
               ['part_of_sattelate', 'pribore', 'DAV_WS16.STEP'],
               ['part_of_sattelate', 'pribore', 'All_SEP_WS16.STEP'],
               ['part_of_sattelate', 'pribore', 'Magnitometr.STEP'],
               #['part_of_sattelate', 'pribore', 'Mahovik_WS16.STEP'],
               ['part_of_sattelate', 'pribore', 'Radio_WS16.STEP'],
               ['part_of_sattelate', 'pribore', 'Solar_battery_WS16.STEP'],
               ['part_of_sattelate', 'pribore', 'UKV.STEP'],
               ['part_of_sattelate', 'pribore', 'DAV_WS16.STEP'],
               ['part_of_sattelate', 'pribore', 'Vch_translator_WS16.STEP']]
    test = Balance_mass('Assemb.STEP', modules)
    test.body_random()
    test.vizualization_all()
    #test.move_frame()

