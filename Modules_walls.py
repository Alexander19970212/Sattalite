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
#from scipy.spatial.transform import Rotation as R
from OCC.Core.TopAbs import TopAbs_EDGE, TopAbs_FACE
from OCC.Core.TopoDS import topods_Face, topods_Edge
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Extend.DataExchange import read_step_file_with_names_colors
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
#from scipy.optimize import minimize
from collections import defaultdict
from OCC.Core.GC import GC_MakePlane
from OCC.Core.BOPAlgo import BOPAlgo_COMMON
from OCC.Core.TopOpeBRep import TopOpeBRep_ShapeIntersector
from OCC.Core.BRepExtrema import BRepExtrema_DistShapeShape
from OCC.Core.BOPAlgo import BOPAlgo_Builder
import math


class Balance_mass:
    def __init__(self, frame, modules, walls, limits):

        # self.display, self.start_display, self.add_menu, self.add_function_to_menu = init_display()
        self.name_frame = frame
        self.limits = limits
        self.modules = {}
        self.names_models = []
        self.history_args = {}
        self.progress = []
        self.valume_inter_obj = defaultdict(dict)

        # for testing, remove later

        self.inter_mass = 0
        self.reserv_models = {}
        # self.display, self.start_display, self.add_menu, self.add_function_to_menu = init_display()
        for model in modules:
            # self.reserv_models[model[2]] = read_step_file(os.path.join(model[0], model[1], model[2]))
            self.reserv_models[model] = read_step_file(modules[model])
            self.names_models.append(model)

        self.walls = walls

        '''for number, wall in enumerate(walls):
            self.walls[number] = [[wall[0], wall[1], wall[2]], [wall[3], wall[4], wall[5]], [wall[3], wall[4], wall[5]],
                                  [wall[6], wall[7]]]'''

    def rot_point(self, x, y, angle):
        import math

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
        from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeEdge, \
            BRepBuilderAPI_Copy
        from OCC.Core.Bnd import Bnd_Box
        from OCC.Core.BRepBndLib import brepbndlib_Add
        from OCC.Core.gp import gp_Pnt, gp_Trsf, gp_Vec, gp_Pln, gp_Dir, gp_Ax3, gp_Ax1
        from OCC.Core.TopLoc import TopLoc_Location

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
        x, y = 1, 1
        try:
            x = -self.walls[number][1][1]
            y = self.walls[number][1][0]
        except:
            print("ERRORRR:")
            print(self.walls)
            print(number)
        z = 0
        P0 = gp_Pnt(0, 0, 0)
        P1 = gp_Pnt(0, 0, 1)
        P2 = gp_Pnt(self.walls[number][1][0], self.walls[number][1][1], self.walls[number][1][2])

        # rotation to Ax z
        v_x = gp_Vec(P0, gp_Pnt(0, 1, 0))
        v_r = gp_Vec(P0, gp_Pnt(x, y, z))
        trsf = gp_Trsf()
        #print(v_r.Angle(v_x))
        trsf.SetRotation(gp_Ax1(P0, gp_Dir(0, 0, 1)), v_r.Angle(v_x))
        shape.Move(TopLoc_Location(trsf))

        # rotation in parallel to face
        v0 = gp_Vec(P0, P1)
        v1 = gp_Vec(P0, P2)
        # print(v1.Angle(v0))
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

        move_x = int(limit_x * x_drive)
        move_y = int(limit_y * y_drive)

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
        # print(name_body, shape)

        self.modules[name_body] = shape

    def Locate_centre_face2(self, number, name_body, angle, x_drive, y_drive):
        from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeEdge, \
            BRepBuilderAPI_Copy
        from OCC.Core.Bnd import Bnd_Box
        from OCC.Core.BRepBndLib import brepbndlib_Add
        from OCC.Core.gp import gp_Pnt, gp_Trsf, gp_Vec, gp_Pln, gp_Dir, gp_Ax3, gp_Ax1
        from OCC.Core.TopLoc import TopLoc_Location

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
        x, y = 1, 1

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
        #print(v_r.Angle(v_x))
        trsf.SetRotation(gp_Ax1(P0, gp_Dir(0, 0, 1)), v_r.Angle(v_x))
        shape.Move(TopLoc_Location(trsf))

        # rotation in parallel to face
        v0 = gp_Vec(P0, P1)
        v1 = gp_Vec(P0, P2)
        # print(v1.Angle(v0))
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

        move_x = int(limit_x * x_drive)
        move_y = int(limit_y * y_drive)

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
        # print(name_body, shape)

        self.modules[name_body] = shape

    # def rotate_by_centre(self, shape, number, angle, P0, P2):

    '''def optimithation_evolution(self):
        from scipy.optimize import differential_evolution
        print('Start optimithtion')

        bounds = []

        for name in self.reserv_models:
            for i in range(4):
                bounds.append((-1, 1))
        result = differential_evolution(self.goal_function2, bounds=bounds, maxiter=2, disp=True,
                                        popsize=10, workers=7)  # , x0)

        print(result.x, result.fun)

        with open("file7.txt", 'w') as f:
            for s in self.progress:
                f.write(str(s) + '\n')

        self.save_all_assamle()'''

    def optimithation_evolution2(self):
        import matplotlib.pyplot as plt
        from stochsearch import EvolSearch
        from OCC.Core.Bnd import Bnd_Box
        bounds = []
        for name in self.reserv_models:
            bounds.append([0, len(self.limits[name][0])])
            bounds.append([0, len(self.limits[name][1])])
            bounds.append([-1, 1])
            bounds.append([-1, 1])

        evol_params = {
            'num_processes': 4,  # (optional) number of proccesses for multiprocessing.Pool
            'pop_size': 40,  # population size
            'bounds': bounds,
            'genotype_size': len(bounds),  # dimensionality of solution
            'fitness_function': self.goal_function2,  # custom function defined to evaluate fitness of a solution
            'elitist_fraction': 0.04,  # fraction of population retained as is between generations
            'mutation_variance': 0.1  # mutation noise added to offspring.
        }

        # create evolutionary search object
        es = EvolSearch(evol_params)

        '''OPTION 1
        # execute the search for 100 generations
        num_gens = 100
        es.execute_search(num_gens)
        '''

        '''OPTION 2'''
        # keep searching till a stopping condition is reached
        best_fit = []
        mean_fit = []
        num_gen = 0
        max_num_gens = 8
        desired_fitness = 0.01
        best_fitn = 1
        while best_fitn > desired_fitness and num_gen < max_num_gens:
        #while num_gen < max_num_gens:
            print('Gen #' + str(num_gen) + ' Best Fitness = ' + str(es.get_best_individual_fitness()))
            es.step_generation()
            best_fit.append(es.get_best_individual_fitness())
            mean_fit.append(es.get_mean_fitness())
            best_fitn = es.get_best_individual_fitness()
            num_gen += 1

        # print results
        print('Min fitness of population = ', es.get_best_individual_fitness())
        print('Best individual in population = ', es.get_best_individual())

        # plot results
        plt.figure()
        plt.plot(best_fit)
        plt.plot(mean_fit)
        plt.xlabel('Generations')
        plt.ylabel('Fitness')
        plt.legend(['best fitness', 'avg. fitness'])
        plt.show()

    def save_all_assamle(self):
        from OCC.Core.BOPAlgo import BOPAlgo_Builder
        print(self.modules.keys())
        builder = BOPAlgo_Builder()

        for name in self.modules:
            builder.AddArgument(self.modules[name])

        builder.SetRunParallel(True)
        builder.Perform()
        shape = builder.Shape()
        self.save_assembly(shape)

    def goal_function2(self, args):
        import math
        from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeEdge, \
            BRepBuilderAPI_Copy

        m = len(self.names_models)

        for i, name in enumerate(self.reserv_models):
            # self.Locate_centre_face(int(m * (args[i * 4] + 1) / 2)-1, name, math.radians(int(args[i * 4 + 1] + 1) * 2),
            #                         int(args[i * 4 + 2]), int(args[i * 4 + 3]))
            number = self.limits[name][0][int(args[i * 4])]
            rotation = math.radians(self.limits[name][1][int(args[i * 4 + 1])])


            self.Locate_centre_face(number, name, rotation, args[i * 4 + 2], args[i * 4 + 3])

        intr1 = self.inter_with_frame2()
        if intr1 == 0:
            intr2 = self.inter_objects()
            if intr2 == 0:
                var1, var2 = self.centre_mass_assamble()
                var1 = var1 / 100
                var2 = var2 / (10 ** 10)
                res = var1 + var2
                self.progress.append(res)

            else:
                res = 0.99
        else:
            res = 0.99
        if res >= 1: res = 0.99
        return res

    def save_assembly(self, shape):
        from OCC.Core.STEPControl import STEPControl_Writer, STEPControl_AsIs
        from OCC.Core.Interface import Interface_Static_SetCVal
        from OCC.Core.IFSelect import IFSelect_RetDone

        step_writer = STEPControl_Writer()
        Interface_Static_SetCVal("write.step.schema", "AP203")

        # transfer shapes and write file
        step_writer.Transfer(shape, STEPControl_AsIs)
        status = step_writer.Write("assembly5.stp")

        if status != IFSelect_RetDone:
            raise AssertionError("load failed")

    def vizualization_all(self):
        # print(self.modules)
        self.display, self.start_display, self.add_menu, self.add_function_to_menu = init_display()
        frame1 = read_step_file(self.name_frame)
        self.display.DisplayShape(frame1, color='GREEN', transparency=0.9)
        print(len(self.modules))
        for model in self.modules:
            self.display.DisplayShape(self.modules[model], color='RED', transparency=0.9)

        self.start_display()

    def move_frame(self):
        from OCC.Core.BOPAlgo import BOPAlgo_Builder
        from OCC.Extend.DataExchange import read_step_file_with_names_colors
        # self.frame = read_step_file(os.path.join('part_of_sattelate', 'karkase', self.name_frame))
        self.frame = read_step_file(self.name_frame)
        '''frame = read_step_file_with_names_colors('part_of_sattelate/karkase/Assemb.STEP')

        #shapes = list(Topo(frame).myShape())

        builder = BOPAlgo_Builder()

        for name in frame:
            builder.AddArgument(name)

        builder.SetRunParallel(True)
        builder.Perform()
        self.frame = builder.Shape()'''

    def inter_with_frame(self):
        from OCC.Core.GProp import GProp_GProps
        from OCC.Core.BOPAlgo import BOPAlgo_Builder
        from OCC.Core.BRepGProp import brepgprop_VolumeProperties, brepgprop_SurfaceProperties, \
            brepgprop_LinearProperties
        from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeEdge, \
            BRepBuilderAPI_Copy
        from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse, BRepAlgoAPI_Common, BRepAlgoAPI_Section, BRepAlgoAPI_Cut
        # print('Start_inter_analyse')
        # print(self.names_models)

        all_result = 0
        props = GProp_GProps()
        # self.display.DisplayShape(body_inter, color='YELLOW')
        brepgprop_VolumeProperties(self.frame, props)
        mass_frame = props.Mass()

        cp = BRepBuilderAPI_Copy(self.frame)
        cp.Perform(self.frame)
        shape = cp.Shape()

        builder = BOPAlgo_Builder()

        for name in self.modules:
            builder.AddArgument(self.modules[name])

        builder.SetRunParallel(True)
        builder.Perform()
        models = builder.Shape()

        props = GProp_GProps()
        # self.display.DisplayShape(body_inter, color='YELLOW')

        brepgprop_VolumeProperties(models, props)
        mass_models = props.Mass()

        mass_1 = mass_frame + mass_models

        '''builder = BOPAlgo_Builder()

        builder.AddArgument(shape)
        builder.AddArgument(models)

        builder.SetRunParallel(True)
        builder.Perform()
        m_w_frame = builder.Shape()'''

        self.m_w_frame = BRepAlgoAPI_Fuse(shape, models).Shape()
        # self.display.DisplayShape(m_w_frame, color='YELLOW', transparency=0.9)

        props = GProp_GProps()

        brepgprop_VolumeProperties(self.m_w_frame, props)
        mass_2 = props.Mass()

        mass = mass_1 - mass_2

        # print(self.modules)
        '''for model in self.modules:
            # print('#')
            props = GProp_GProps()
            new_shape = BRepAlgoAPI_Cut(shape, self.modules[model]).Shape()
            # self.display.DisplayShape(body_inter, color='YELLOW')
            brepgprop_VolumeProperties(new_shape, props)
            mass_frame_2 = props.Mass()
            self.display.DisplayShape(new_shape, color='YELLOW', transparency=0.9)

            mass = mass_frame - mass_frame_2

            props = GProp_GProps()
            inter = TopOpeBRep_ShapeIntersector()
            inter.InitIntersection(self.modules[model], self.frame)
            flag = inter.MoreIntersection()
            body_inter = inter.CurrentGeomShape(1)
            brepgprop_VolumeProperties(body_inter, props)
            mass = props.Mass()

            props = GProp_GProps()
            body_inter = inter.CurrentGeomShape(2)
            brepgprop_VolumeProperties(body_inter, props)
            mass = abs(mass) + abs(props.Mass())

            dss = BRepExtrema_DistShapeShape()
            dss.LoadS1(self.modules[model])
            dss.LoadS2(self.frame)
            dss.Perform()

            flag = dss.IsDone()
            mass = dss.Value()
            print(mass)
            print(flag)'''
        print(mass)

        if mass > 1e-6:
            # print(mass)
            all_result += 1

        return all_result

    def inter_with_frame2(self):
        from OCC.Core.GProp import GProp_GProps
        from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse, BRepAlgoAPI_Common, BRepAlgoAPI_Section, BRepAlgoAPI_Cut
        from OCC.Core.BRepGProp import brepgprop_VolumeProperties, brepgprop_SurfaceProperties, \
            brepgprop_LinearProperties
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
            # print(mass)
            if mass > 1e-6:
                # print(mass)
                all_result += 1

        return all_result

    def inter_objects(self):
        from OCC.Core.GProp import GProp_GProps
        from OCC.Core.BRepGProp import brepgprop_VolumeProperties, brepgprop_SurfaceProperties, \
            brepgprop_LinearProperties
        from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse, BRepAlgoAPI_Common, BRepAlgoAPI_Section, BRepAlgoAPI_Cut

        # print('Start_inter_analyse')
        inter_mass = 0
        props = GProp_GProps()
        # print(self.names_models)

        for i in range(len(self.names_models) - 1):
            for j in range(i + 1, len(self.names_models)):
                # print(self.names_models[i], self.names_models[j])
                if self.names_models[i] == self.names_models[j]: continue
                body_inter = BRepAlgoAPI_Section(self.modules[self.names_models[i]],
                                                 self.modules[self.names_models[j]]).Shape()
                brepgprop_LinearProperties(body_inter, props)
                mass = props.Mass()
                # print(mass)
                if mass > 0:
                    inter_mass += mass

        # self.start_display()
        return inter_mass

    def centre_mass(self, shape):
        from OCC.Core.GProp import GProp_GProps
        from OCC.Core.BRepGProp import brepgprop_VolumeProperties, brepgprop_SurfaceProperties, \
            brepgprop_LinearProperties

        props = GProp_GProps()
        brepgprop_VolumeProperties(shape, props)
        # Get inertia properties
        mass = props.Mass()
        cog = props.CentreOfMass()
        matrix_of_inertia = props.MatrixOfInertia()
        # Display inertia properties
        # print("Cube mass = %s" % mass)
        cog_x, cog_y, cog_z = cog.Coord()
        # print("Center of mass: x = %f;y = %f;z = %f;" % (cog_x, cog_y, cog_z))
        mat = props.MatrixOfInertia()
        #######################################################################################

        variation_inertial = abs(mat.Value(2, 3)) + abs(mat.Value(1, 2)) + abs(mat.Value(1, 3)) + abs(
            mat.Value(2, 1)) + abs(mat.Value(3, 1)) + abs(mat.Value(3, 2))

        var1, var2 = (cog_x ** 2 + cog_y ** 2 + cog_z ** 2) ** 0.5, variation_inertial
        if var1 < 0.0001 or var2 < 0.0001: var1, var2 = 10 ** 10, 10 ** 10
        return var1, var2

    def centre_mass_assamble(self):
        from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeEdge, \
            BRepBuilderAPI_Copy
        from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse, BRepAlgoAPI_Common, BRepAlgoAPI_Section, BRepAlgoAPI_Cut

        flag = 0
        shape = 0
        for name in self.modules:
            if flag == 0:
                cp = BRepBuilderAPI_Copy(self.modules[name])
                cp.Perform(self.modules[name])
                shape = cp.Shape()
                flag = 1
            shape = BRepAlgoAPI_Fuse(shape, self.modules[name]).Shape()

        variation, var_inert = self.centre_mass(shape)
        # self.save_assembly(shape)
        return variation, var_inert

    def centre_mass2(self):
        from OCC.Core.GProp import GProp_GProps
        from OCC.Core.BRepGProp import brepgprop_VolumeProperties, brepgprop_SurfaceProperties, \
            brepgprop_LinearProperties

        props = GProp_GProps()
        brepgprop_VolumeProperties(self.m_w_frame, props)
        # Get inertia properties
        mass = props.Mass()
        cog = props.CentreOfMass()
        matrix_of_inertia = props.MatrixOfInertia()
        # Display inertia properties
        # print("Cube mass = %s" % mass)
        cog_x, cog_y, cog_z = cog.Coord()
        # print("Center of mass: x = %f;y = %f;z = %f;" % (cog_x, cog_y, cog_z))
        mat = props.MatrixOfInertia()
        #######################################################################################

        variation_inertial = abs(mat.Value(2, 3)) + abs(mat.Value(1, 2)) + abs(mat.Value(1, 3)) + abs(
            mat.Value(2, 1)) + abs(mat.Value(3, 1)) + abs(mat.Value(3, 2))

        var1, var2 = (cog_x ** 2 + cog_y ** 2 + cog_z ** 2) ** 0.5, variation_inertial
        if var1 < 0.0001 or var2 < 0.0001: var1, var2 = 10 ** 10, 10 ** 10
        return var1, var2

    def random_location(self):
        from OCC.Core.BOPAlgo import BOPAlgo_Builder
        import random
        x = []
        for name in self.reserv_models:
            for i in range(4):
                x.append(random.uniform(-1, 1))
        print(self.goal_function2(x))

        '''print('Input')
        builder = BOPAlgo_Builder()
        builder.AddArgument(self.frame)

        for name in self.modules:
            builder.AddArgument(self.modules[name])

        builder.SetRunParallel(True)
        builder.Perform()
        shape = builder.Shape()
        return shape'''

    def var_test(self):

        # print(self.reserv_models)
        for i, name_body in enumerate(self.reserv_models):
            # print(name_body)
            self.Locate_centre_face(i, name_body, math.radians(30), 0, 0)


if __name__ == '__main__':
    # frame = ['part_of_sattelate', 'karkase', 'Assemb.STEP']
    '''modules = [  # ['part_of_sattelate', 'pribore', 'Camara2_WS16.STEP'],
        ['part_of_sattelate', 'pribore', 'DAV_WS16.STEP'],
        # ['part_of_sattelate', 'pribore', 'All_SEP_WS16.STEP'],
        # ['part_of_sattelate', 'pribore', 'Magnitometr.STEP'],
        # ['p3art_of_sattelate', 'pribore', 'Mahovik_WS16.STEP'],
        ['part_of_sattelate', 'pribore', 'Radio_WS16.STEP'],
        # ['part_of_sattelate', 'pribore', 'Solar_battery_WS16.STEP'],
        ['part_of_sattelate', 'pribore', 'UKV.STEP'],
        # ['part_of_sattelate', 'pribore', 'DAV2_WS16.STEP'],
        ['part_of_sattelate', 'pribore', 'Vch_translator_WS16.STEP']]'''
    '''walls = [[110, 0, 10, 0, -10, 0, 0, 186, 248],
             [110, 0, 10, 0, 0, 0, 10, 186, 248],
             [110, 0, 10, 0, 10, 0, 0, 186, 248],
             [110, 0, 10, 0, 0, 0, -10, 186, 248], ]'''
    modules = {'DAV_WS16.STEP': 'C:/Users/Alexander/PycharmProjects/Sattalite/part_of_sattelate/pribore/DAV_WS16.STEP',
               'DAV2_WS16.STEP': 'C:/Users/Alexander/PycharmProjects/Sattalite/part_of_sattelate/pribore/DAV2_WS16.STEP',
               'DAV3_WS16.STEP': 'C:/Users/Alexander/PycharmProjects/Sattalite/part_of_sattelate/pribore/DAV3_WS16.STEP',
               'Magnitometr.STEP': 'C:/Users/Alexander/PycharmProjects/Sattalite/part_of_sattelate/pribore/Magnitometr.STEP'}

    # frame = 'C:\Users\Alexander\PycharmProjects\Sattalite\part_of_sattelate\karkase\Assemb.STEP'

    limits = {'DAV_WS16.STEP': [[1, 2], [0, 45, 60, 90]],
               'DAV2_WS16.STEP': [[1, 2, 3, 0], [30, 90, 180]],
               'DAV3_WS16.STEP': [[0, 3], [0, 180]],
               'Magnitometr.STEP': [[2], [30, 45, 90, 135]]}
    #[Faces, rotation]

    walls = [[[0, 110, 0], [0, 1, 0], [1, 0, 0], [186, 248]],
             [[110, 0, 0], [1, 0, 0], [0, -1, 0], [186, 248]],
             [[0, -110, 0], [0, -1, 0], [-1, 0, 0], [186, 248]],
             [[-110, 0, 0], [-1, 0, 0], [0, 1, 0], [186, 248]]]

    # point of centre, normal, Axis-x, bound of x and y
    # distant between xero point and face plt, normal of wall
    # distant between zero point anf face plt, vector that will drop axis z, vector сонаправленный X

    test = Balance_mass(r'C:\Users\Alexander\PycharmProjects\Sattalite\part_of_sattelate\karkase\Assemb.STEP', modules, walls, limits)
    # test.var_test()
    test.move_frame()
    test.optimithation_evolution2()

    print(test.inter_with_frame())
    test.vizualization_all()
