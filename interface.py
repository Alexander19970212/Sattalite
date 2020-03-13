'''
Class have function for creation list with pozition of the faces
- create the work windows
- export the frame
- export the models
- choose the faces
- revers of the normal
- choose the direct of the X-axis
- revers of this direct
'''
from __future__ import print_function

import os
import os.path
import sys
import wx

from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.IFSelect import IFSelect_RetDone, IFSelect_ItemsByEntity
from OCC.Core.GeomAbs import GeomAbs_Plane, GeomAbs_Cylinder
from OCC.Core.TopoDS import topods_Face
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Display.SimpleGui import init_display
from OCC.Extend.DataExchange import read_step_file
from OCC.Core.gp import gp_Pnt, gp_Trsf, gp_Vec, gp_Pln, gp_Dir, gp_Ax3, gp_Ax1
from OCC.Core.Bnd import Bnd_Box
from OCC.Extend.TopologyUtils import TopologyExplorer
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon
from OCC.Core.BRepBndLib import brepbndlib_Add
from collections import defaultdict
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Copy
from OCC.Core.BRepGProp import brepgprop_VolumeProperties, brepgprop_SurfaceProperties, brepgprop_LinearProperties
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Core.GProp import GProp_GProps
from OCC.Core.BOPAlgo import BOPAlgo_Builder
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse, BRepAlgoAPI_Common, BRepAlgoAPI_Section, BRepAlgoAPI_Cut
import math
#display, start_display, add_menu, add_function_to_menu = init_display('wx')
from OCC.Core.BRepClass3d import BRepClass3d_SolidClassifier
import Modules_walls


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 file dialogs - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        #self.openFileNameDialog()
        #self.openFileNamesDialog()
        #self.saveFileDialog()

        #self.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            #print(fileName)
            return fileName

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self, "QFileDialog.getOpenFileNames()", "",
                                                "All Files (*);;Python Files (*.py)", options=options)
        if files:
            print(files)

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)

class Balance_mass:
    def __init__(self, frame, modules, walls):

        #self.display, self.start_display, self.add_menu, self.add_function_to_menu = init_display()
        self.name_frame = frame
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
            #self.reserv_models[model[2]] = read_step_file(os.path.join(model[0], model[1], model[2]))
            self.reserv_models[model] = read_step_file(modules[model])
            self.names_models.append(model)

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
        if v_x.X != v_r.X and v_x.Y != v_r.Y and v_x.Z != v_r.Z:
            trsf = gp_Trsf()
            #print(v_r.Angle(v_x))
            trsf.SetRotation(gp_Ax1(P0, gp_Dir(0, 0, 1)), v_r.Angle(v_x))
            shape.Move(TopLoc_Location(trsf))

        # rotation in parallel to face
        v0 = gp_Vec(P0, P1)
        v1 = gp_Vec(P0, P2)
        # print(v1.Angle(v0))
        if v1.X != v0.X and v1.Y != v0.Y and v1.Z != v0.Z:
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
        #print(name_body, shape)

        self.modules[name_body] = shape

    # def rotate_by_centre(self, shape, number, angle, P0, P2):

    def optimithation_evolution(self):
        from scipy.optimize import differential_evolution
        print('Start optimithtion')

        bounds = []


        for name in self.reserv_models:
            for i in range(4):
                bounds.append((-1, 1))
        result = differential_evolution(self.goal_function2, bounds=bounds, maxiter=6, disp=True,
                                        popsize=10, workers=7)  # , x0)

        print(result.x, result.fun)

        with open("file7.txt", 'w') as f:
            for s in self.progress:
                f.write(str(s) + '\n')

        self.save_all_assamle()

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

        m = len(self.names_models)

        for i, name in enumerate(self.reserv_models):
            self.Locate_centre_face(int(m * (args[i * 4] + 1) / 2), name, math.radians(int(args[i * 4 + 1] + 1) * 2),
                                    int(args[i * 4 + 2]), int(args[i * 4 + 3]))

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
                res = 1
        else:
            res = 1
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
        #self.frame = read_step_file(os.path.join('part_of_sattelate', 'karkase', self.name_frame))
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
        # print('Start_inter_analyse')
        #print(self.names_models)
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
            #print(mass)
            if mass > 1e-6:
                # print(mass)
                all_result += 1

        return all_result

    def inter_objects(self):

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

    def centre_mass_vizuall(self):
        flag = 0
        shape = 0
        for name in self.modules:
            if flag == 0:
                cp = BRepBuilderAPI_Copy(self.modules[name])
                cp.Perform(self.modules[name])
                shape = cp.Shape()
                flag = 1
            shape = BRepAlgoAPI_Fuse(shape, self.modules[name]).Shape()

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
        list_1 = [mat.Value(1, 1), mat.Value(1, 2), mat.Value(1, 3)]
        list_2 = [mat.Value(2, 1), mat.Value(2, 2), mat.Value(2, 3)]
        list_3 = [mat.Value(3, 1), mat.Value(3, 2), mat.Value(3, 3)]


        print('\t'.join(str(i) for i in list_1))
        print('\t'.join(str(i) for i in list_2))
        print('\t'.join(str(i) for i in list_3))

        var1 = (cog_x ** 2 + cog_y ** 2 + cog_z ** 2) ** 0.5
        print(var1)

    def centre_mass2(self):

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

class Interfac:

    def __init__(self):
        '''
        init display
        init function
        init list of characteristics of the faces

        '''
        self.name_frame = ''
        self.modules = {}
        self.faces = []
        self.display, self.start_display, self.add_menu, self.add_function_to_menu = init_display('wx')
        self.in_disp()



    def in_disp(self):
        #self.display, self.start_display, self.add_menu, self.add_function_to_menu = init_display()
        # self.display.SetSelectionModeFace()  # switch to Face selection mode
        # self.display.register_select_callback(self.recognize_clicked)
        self.add_menu('Import')
        self.add_menu('Choose')
        self.add_menu('Faces')
        self.add_menu('Optimization')
        self.add_menu('Export')
        self.add_menu('Modules')
        self.add_function_to_menu('Import', self.open_frame)
        self.add_function_to_menu('Import', self.open_models)
        self.add_function_to_menu('Modules', self.Print_all)
        self.add_function_to_menu('Modules', self.Clear)
        self.add_function_to_menu('Faces', self.select_faces)
        self.add_function_to_menu('Faces', self.print_all_faces)
        self.add_function_to_menu('Faces', self.clear_faces)
        self.add_function_to_menu('Optimization', self.random_location)
        self.add_function_to_menu('Optimization', self.Optimaze_evolution)
        self.start_display()
        

    def open_frame(self, event=None):
        '''
        open step model of the frame
        :return: None
        '''

        app = QApplication(sys.argv)
        ex = App()
        filename = ex.openFileNameDialog()
        #sys.exit(app.exec_())
        print(os.path.split(filename)[-1])
        self.name_frame = filename

        self.frame = read_step_file(filename)

        #self.frame = read_step_file(filename)
        self.display.EraseAll()
        self.display.Context.RemoveAll(True)
        self.display.DisplayShape(self.frame, color='GREEN', transparency=0.9)
        self.display.FitAll()



    def print_all_faces(self, event=None):
        print(self.faces)

    def clear_faces(self, event=None):
        self.faces = []


    def open_models(self, event=None):
        '''
        open steps model of the modules
        :return:
        '''

        app = QApplication(sys.argv)
        ex = App()
        filename = ex.openFileNameDialog()
        # sys.exit(app.exec_())
        name = os.path.split(filename)[-1]
        #print(name)
        self.modules[name] = filename

        #self.in_disp()


    def Clear(self, event=None):
        self.modules = {}

    def Print_all(self, event=None):
        print(self.modules)

    def recognize_clicked(self, shp, *kwargs):
        """ This is the function called every time
        a face is clicked in the 3d view
        """

        '''t = TopologyExplorer(self.frame)
        for shape in t.faces():  # this should be a TopoDS_Face TODO check it is
            print("Face selected: ", shape)
            self.recognize_face(topods_Face(shape))'''


        for shape in shp:  # this should be a TopoDS_Face TODO check it is
            print("Face selected: ", shape)
            bbox = Bnd_Box()
            brepbndlib_Add( shape, bbox)
            xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
            bounds = [sorted([xmax-xmin, ymax-ymin, zmax-zmin])[1], sorted([xmax-xmin, ymax-ymin, zmax-zmin])[2]]
            print('--> Bounds', xmax-xmin, ymax-ymin, zmax-zmin)
            centre, normal, X_axis = self.recognize_face(topods_Face(shape))
            self.faces.append([centre, normal, X_axis, bounds])


    def recognize_face(self, a_face):
        """ Takes a TopoDS shape and tries to identify its nature
        whether it is a plane a cylinder a torus etc.
        if a plane, returns the normal
        if a cylinder, returns the radius
        """
        surf = BRepAdaptor_Surface(a_face, True)
        surf_type = surf.GetType()
        if surf_type == GeomAbs_Plane:
            print("--> plane")
            # look for the properties of the plane
            # first get the related gp_Pln
            gp_pln = surf.Plane()
            location = gp_pln.Location()  # a point of the plane
            normal = gp_pln.Axis().Direction()  # the plane normal
            x_axis = gp_pln.XAxis().Direction()
            # then export location and normal to the console output
            print("--> Location (global coordinates)", location.X(), location.Y(), location.Z())
            print("--> Normal (global coordinates)", normal.X(), normal.Y(), normal.Z())
            print("--> X_axis", x_axis.X(), x_axis.Y(), x_axis.Z())
            centre = [location.X(), location.Y(), location.Z()]
            normal = [normal.X(), normal.Y(), normal.Z()]
            point_coords = [centre[0] + normal[0], centre[1] + normal[1], centre[2] + normal[2]]
            pnt = gp_Pnt(point_coords[0], point_coords[1], point_coords[2])
            _in_solid = BRepClass3d_SolidClassifier(self.frame, pnt, 1e-5)
            if _in_solid.State()==0:
                normal = [-normal[0], -normal[1], -normal[2]]
            print(point_coords)


            X_axis = [x_axis.X(), x_axis.Y(), x_axis.Z()]
            return (centre, normal, X_axis)

        elif surf_type == GeomAbs_Cylinder:
            print("--> cylinder")
            # look for the properties of the cylinder
            # first get the related gp_Cyl
            gp_cyl = surf.Cylinder()
            location = gp_cyl.Location()  # a point of the axis
            axis = gp_cyl.Axis().Direction()  # the cylinder axis
            # then export location and normal to the console output
            print("--> Location (global coordinates)", location.X(), location.Y(), location.Z())
            print("--> Axis (global coordinates)", axis.X(), axis.Y(), axis.Z())
        else:
            # TODO there are plenty other type that can be checked
            # see documentation for the BRepAdaptor class
            # https://www.opencascade.com/doc/occt-6.9.1/refman/html/class_b_rep_adaptor___surface.html
            print("not implemented")

    def random_location(self, event=None):
        test = Balance_mass(self.name_frame, self.modules, self.faces)
        # test.var_test()
        test.move_frame()
        #test.optimithation_evolution()
        shape = test.random_location()
        #display.EraseAll()
        #display.Context.RemoveAll(True)
        #display.DisplayShape(shape, transparency=0.9)
        #display.FitAll()

        #print(test.inter_with_frame())
        test.vizualization_all()

    def Optimaze_evolution(self, event=None):
        test = Balance_mass(self.name_frame, self.modules, self.faces)
        # test.var_test()
        test.move_frame()
        test.optimithation_evolution()
        test.centre_mass_vizuall()
        #shape = test.random_location()
        # display.EraseAll()
        # display.Context.RemoveAll(True)
        # display.DisplayShape(shape, transparency=0.9)
        # display.FitAll()

        #print(test.inter_with_frame())
        test.vizualization_all()

    def select_faces(self, event=None):
        self.display.SetSelectionModeFace()  # switch to Face selection mode
        self.display.register_select_callback(self.recognize_clicked)




if __name__ == '__main__':
    test = Interfac()
