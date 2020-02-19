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
from OCC.Core.gp import gp_Pnt, gp_Trsf, gp_Vec, gp_Pln, gp_Dir
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
from OCC.Display.SimpleGui import init_display
from scipy.spatial.transform import Rotation as R
from OCC.Core.TopAbs import TopAbs_EDGE, TopAbs_FACE
from OCC.Core.TopoDS import topods_Face, topods_Edge
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Extend.DataExchange import read_step_file_with_names_colors
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from scipy.optimize import minimize
from collections import defaultdict


class Balance_mass:
    def __init__(self, frame, modules):

        self.name_frame = frame
        self.modules = {}
        self.names_models = []
        self.history_args = {}
        self.valume_inter_obj = defaultdict(dict)

        # for testing, remove later

        self.test_var = 20
        self.test_2_var = 0.0000
        self.current_body = ''

        self.d = 3.1
        self.px = 220 - self.d
        self.py = 220 - self.d
        self.pz = 246

        self.peep_factor = 0
        self.peep_list = {}

        self.dimensoins = {}
        self.profiles = {}
        self.valume_inter = {}
        self.inter_mass = 0
        self.display, self.start_display, self.add_menu, self.add_function_to_menu = init_display()
        for model in modules:
            self.modules[model[2]] = read_step_file(os.path.join(model[0], model[1], model[2]))
            self.names_models.append(model[2])

        self.reserv_models = self.modules.copy()

        for model in self.modules:
            bbox = Bnd_Box()
            brepbndlib_Add(self.modules[model], bbox)
            xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
            self.dimensoins[model] = [xmin, xmax, ymin, ymax, zmin, zmax]
            # print(model)
            self.profiles[model] = [self.glue_solids(self.modules[model])]

        # print(self.profiles)

    def max_counter(self, facesS_2):
        section_edges = list(Topo(facesS_2).edges())
        # print(len(section_edges))

        if len(section_edges) > 0:

            Wire_c = BRepBuilderAPI_MakeWire()
            prep_list = []
            Wire_c.Add(section_edges[0])
            prep_list.append(section_edges[0])
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
            flag = 0
            wires = []

            while len(section_edges) > 0:

                new_list = []

                for edges in section_edges:
                    # Wire_c.Add(edges)
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
                        flag = 0
                    elif End_1.X() == v1.X() and End_1.Y() == v1.Y() and End_1.Z() == v1.Z():
                        Wire_c.Add(edges)
                        v1 = End_2
                        flag = 0
                    elif End_2.X() == v0.X() and End_2.Y() == v0.Y() and End_2.Z() == v0.Z():
                        Wire_c.Add(edges)
                        v0 = End_1
                        flag = 0
                    elif End_2.X() == v1.X() and End_2.Y() == v1.Y() and End_2.Z() == v1.Z():
                        Wire_c.Add(edges)
                        v1 = End_1
                        flag = 0
                    else:
                        new_list.append(edges)

                flag += 1
                section_edges = new_list

                if flag >= 5:
                    # print('number_ostalos', len(section_edges))
                    wires.append(Wire_c.Wire())
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
                    flag = 0

            wires.append(Wire_c.Wire())

            areas = []
            props = GProp_GProps()

            for wire in wires:
                brown_face = BRepBuilderAPI_MakeFace(wire)
                brown_face = brown_face.Face()
                # props = GProp_GProps()
                brepgprop_SurfaceProperties(brown_face, props)
                areas.append(props.Mass())

            return max(areas)

        else:
            return 0

    def glue_solids(self, S2):

        bbox = Bnd_Box()
        brepbndlib_Add(S2, bbox)
        xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
        p0 = gp_Pnt(xmin + (xmax - xmin) / 2, ymin + (ymax - ymin) / 2, zmin + 0.1)

        vnorm = gp_Dir(0, 0, 1)
        pln = gp_Pln(p0, vnorm)
        face = BRepBuilderAPI_MakeFace(pln, -(xmax - xmin) / 2 - 1, (xmax - xmin) / 2 + 1, -(ymax - ymin) / 2 - 1,
                                       (ymax - ymin) / 2 + 1).Face()

        facesS_2 = BRepAlgoAPI_Section(face, S2).Shape()

        return self.max_counter(facesS_2)

    def move_frame(self):
        self.frame = read_step_file(os.path.join('part_of_sattelate', 'karkase', self.name_frame))
        # self.vizualization(self.frame, 'RED', 0.9)

    def change_position1(self, name, number_wall, pos_1, pos_2, pos_3):
        number_wall = int(number_wall % 7)

        alpha, beta, gamma, offset_x, offset_y, offset_z = 0, 0, 0, 0, 0, 0

        libra = int(pos_3 // 3) * 90
        pos_3 = 0
        if number_wall == 0:
            alpha = 90

            offset_y = self.py / 2 - self.d / 2 + self.dimensoins[name][4] + self.test_2_var
            beta = pos_3
            if pos_1 >= self.px / 2:
                offset_x = self.px / 2
            elif pos_1 <= -self.px / 2:
                offset_x = -self.px / 2
            else:
                offset_x = pos_1

            if pos_2 >= self.pz / 2:
                offset_z = self.pz / 2
            elif pos_2 <= -self.pz / 2:
                offset_z = -self.pz / 2
            else:
                offset_z = pos_2
            gamma = 0

        if number_wall == 1:
            alpha = -90
            offset_y = self.py / 2 + self.d / 2 - self.dimensoins[name][4] - self.test_2_var
            beta = pos_3
            flag = 'xyz'
            if pos_1 >= self.px / 2:
                offset_x = self.px / 2
            elif pos_1 <= -self.px / 2:
                offset_x = -self.px / 2
            else:
                offset_x = pos_1

            if pos_2 >= self.pz / 2:
                offset_z = self.pz / 2
            elif pos_2 <= -self.pz / 2:
                offset_z = -self.pz / 2
            else:
                offset_z = pos_2
            gamma = 0

        if number_wall == 2:
            beta = -90
            offset_x = self.px / 2 - self.d / 2 + self.dimensoins[name][4] + self.test_2_var
            alpha = pos_3
            flag = 'yxz'
            if pos_1 >= self.py / 2:
                offset_y = self.py / 2
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

        if number_wall == 3:
            beta = 90
            offset_x = self.px / 2 + self.d / 2 - self.dimensoins[name][4] - self.test_2_var
            alpha = pos_3
            flag = 'yxz'
            if pos_1 >= self.py / 2:
                offset_y = self.py / 2
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

        if number_wall == 4:
            alpha = -90
            offset_y = -(self.py / 2 - self.d / 2 + self.dimensoins[name][4] + self.test_2_var)
            beta = pos_3
            flag = 'xyz'
            if pos_1 >= self.px / 2:
                offset_x = self.px / 2
            elif pos_1 <= -self.px / 2:
                offset_x = -self.px / 2
            else:
                offset_x = pos_1

            if pos_2 >= self.pz / 2:
                offset_z = self.pz / 2
            elif pos_2 <= -self.pz / 2:
                offset_z = -self.pz / 2
            else:
                offset_z = pos_2
            gamma = 0

        if number_wall == 5:
            alpha = 90
            offset_y = -(self.py / 2 + self.d / 2 - self.dimensoins[name][4] - self.test_2_var)
            beta = pos_3
            flag = 'xyz'
            if pos_1 >= self.px / 2:
                offset_x = self.px / 2
            elif pos_1 <= -self.px / 2:
                offset_x = -self.px / 2
            else:
                offset_x = pos_1

            if pos_2 >= self.pz / 2:
                offset_z = self.pz / 2
            elif pos_2 <= -self.pz / 2:
                offset_z = -self.pz / 2
            else:
                offset_z = pos_2
            gamma = 0

        if number_wall == 6:
            beta = 90
            offset_x = -(self.px / 2 - self.d / 2 + self.dimensoins[name][4] + self.test_2_var)
            alpha = pos_3
            flag = 'yxz'
            if pos_1 >= self.py / 2:
                offset_y = self.py / 2
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

        if number_wall == 7:
            beta = -90
            offset_x = -(self.px / 2 + self.d / 2 - self.dimensoins[name][4] - self.test_2_var)
            alpha = pos_3
            flag = 'yxz'
            if pos_1 >= self.py / 2:
                offset_y = self.py / 2
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

        if number_wall in [0, 1, 4, 5]:
            alpha_2, beta_2, gamma_2 = 0, libra, 0

        elif number_wall in [2, 3, 6, 7]:
            alpha_2, beta_2, gamma_2 = libra, 0, 0

        # print(number_wall)
        # flag = 'xyz'

        self.history_args[name] = [number_wall, pos_1, pos_2, pos_3]

        self.filling(name, [alpha, beta, gamma, offset_x, offset_y, offset_z], [alpha_2, beta_2, gamma_2])

    def peeping_all_frame(self):
        self.peep_factor = 0
        for model in self.modules:
            peep = self.peeping_frame(model)
            if peep == 0:
                print(model, 'dont touch')
            else:
                proc_peep = peep / self.profiles[model][0]
                if proc_peep < 0.98:
                    self.peep_list[model] = proc_peep
                    self.peep_factor += 1 - proc_peep
                    print(model, 1 - proc_peep)
                # else: print(model, 1)

    def peeping_frame(self, model):

        facesS_2 = BRepAlgoAPI_Section(self.frame, self.modules[model]).Shape()

        return self.max_counter(facesS_2)

    def change_object(self):
        pass

    def filling(self, name_body, coord_centres, coord_centres_2):
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
        # print(name_body, coord_centres)
        # shape = self.modules[name_body]
        # print(body)

        cp = BRepBuilderAPI_Copy(self.reserv_models[name_body])
        cp.Perform(self.reserv_models[name_body])
        shape = cp.Shape()
        #print(shape)

        r = R.from_euler('xyz', [coord_centres[0], coord_centres[1], coord_centres[2]], degrees=True)
        Rot = r.as_dcm()

        trsf = gp_Trsf()
        Mat = gp_Mat(Rot[0][0], Rot[0][1], Rot[0][2],
                     Rot[1][0], Rot[1][1], Rot[1][2],
                     Rot[2][0], Rot[2][1], Rot[2][2])

        trsf.SetRotation(gp_Quaternion(Mat))
        shape.Move(TopLoc_Location(trsf))

        r = R.from_euler('xyz', [coord_centres_2[0], coord_centres_2[1], coord_centres_2[2]], degrees=True)
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
        self.modules[name_body] = shape
        #print(shape)

    def inter_with_frame(self):
        # print('Start_inter_analyse')
        props = GProp_GProps()
        print(self.modules)
        for model in self.modules:
            # print('#')
            body_inter = BRepAlgoAPI_Common(self.frame, self.modules[model]).Shape()
            self.display.DisplayShape(body_inter, color='YELLOW')
            brepgprop_VolumeProperties(body_inter, props)
            mass = props.Mass()
            if mass > 0:
                self.valume_inter[model] = props.Mass()

        # print(self.valume_inter)

    def inter_objects(self):

        # print('Start_inter_analyse')
        self.inter_mass = 0
        props = GProp_GProps()

        for i in range(len(self.names_models) - 2):
            for j in range(i + 1, len(self.names_models) - 1):
                body_inter = BRepAlgoAPI_Common(self.modules[self.names_models[i]],
                                                self.modules[self.names_models[j]]).Shape()
                self.display.DisplayShape(body_inter, color='WHITE')
                brepgprop_VolumeProperties(body_inter, props)
                mass = props.Mass()
                # print(mass)
                if mass > 0:
                    self.inter_mass += mass
                    self.valume_inter_obj[self.names_models[i]][self.names_models[j]] = mass

        # print(self.valume_inter_obj)
        # print(self.inter_mass)

    def inter_one_object_frame(self, name):
        props = GProp_GProps()
        body_inter = BRepAlgoAPI_Common(self.frame, self.modules[name]).Shape()
        brepgprop_VolumeProperties(body_inter, props)
        print(props.Mass())
        return props.Mass()

    def function_for_opt(self, args):

        self.change_position1(self.current_body, args[0], args[1], args[2], args[3])

        return self.inter_one_object_frame(self.current_body)

    def remove_inter_frame(self):
        print(self.valume_inter)
        for name in self.valume_inter:
            self.current_body = name
            x0 = self.history_args[self.current_body]
            res = minimize(self.function_for_opt, x0, method='powell',
                options={'xtol': 1e-8, 'disp': True})

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
            self.display.DisplayShape(self.modules[model], color='RED', transparency=0.9)

        self.start_display()

    def body_random(self):
        for name in self.modules:
            pos_1 = random.uniform(max(self.px, self.py) / 2 - self.test_var, self.test_var - max(self.px, self.py) / 2)
            pos_2 = random.uniform(self.pz / 2 - self.test_var, self.test_var - self.pz / 2)
            pos_3 = random.uniform(0, 4)
            Number_wall = random.uniform(0, 20)

            self.change_position1(name, Number_wall, pos_1, pos_2, pos_3)


if __name__ == '__main__':
    frame = ['part_of_sattelate', 'karkase', 'Assemb.STEP']
    modules = [['part_of_sattelate', 'pribore', 'Camara2_WS16.STEP'],
               ['part_of_sattelate', 'pribore', 'DAV_WS16.STEP'],
               # ['part_of_sattelate', 'pribore', 'All_SEP_WS16.STEP'],
               ['part_of_sattelate', 'pribore', 'Magnitometr.STEP'],
               # ['part_of_sattelate', 'pribore', 'Mahovik_WS16.STEP'],
               ['part_of_sattelate', 'pribore', 'Radio_WS16.STEP'],
               ['part_of_sattelate', 'pribore', 'Solar_battery_WS16.STEP'],
               ['part_of_sattelate', 'pribore', 'UKV.STEP'],
               ['part_of_sattelate', 'pribore', 'DAV_WS16.STEP'],
               ['part_of_sattelate', 'pribore', 'Vch_translator_WS16.STEP']]
    test = Balance_mass('Assemb.STEP', modules)
    test.body_random()
    test.move_frame()
    test.inter_with_frame()
    # test.peeping_all_frame()
    # test.inter_objects()
    test.remove_inter_frame()
    test.vizualization_all()
    test.move_frame()
