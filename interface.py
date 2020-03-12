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
from OCC.Core.gp import gp_Pnt, gp_Trsf, gp_Vec, gp_Pln, gp_Dir
from OCC.Core.Bnd import Bnd_Box
from OCC.Extend.TopologyUtils import TopologyExplorer
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon
from OCC.Core.BRepBndLib import brepbndlib_Add
display, start_display, add_menu, add_function_to_menu = init_display('wx')
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
        self.in_disp()


    def in_disp(self):
        #self.display, self.start_display, self.add_menu, self.add_function_to_menu = init_display()
        # self.display.SetSelectionModeFace()  # switch to Face selection mode
        # self.display.register_select_callback(self.recognize_clicked)
        add_menu('Import')
        add_menu('Choose')
        add_menu('Faces')
        add_menu('Optimization')
        add_menu('Export')
        add_menu('Modules')
        add_function_to_menu('Import', self.open_frame)
        add_function_to_menu('Import', self.open_models)
        add_function_to_menu('Modules', self.Print_all)
        add_function_to_menu('Modules', self.Clear)
        add_function_to_menu('Faces', self.select_faces)
        add_function_to_menu('Faces', self.print_all_faces)
        add_function_to_menu('Faces', self.clear_faces)
        add_function_to_menu('Optimization', self.random_location)
        add_function_to_menu('Optimization', self.Optimaze_evolution)
        start_display()
        

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
        display.EraseAll()
        display.Context.RemoveAll(True)
        display.DisplayShape(self.frame, color='GREEN', transparency=0.9)
        display.FitAll()



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
        test = Modules_walls.Balance_mass(self.name_frame, self.modules, self.faces)
        # test.var_test()
        test.move_frame()
        #test.optimithation_evolution()
        shape = test.random_location()
        # display.EraseAll()
        # display.Context.RemoveAll(True)
        # display.DisplayShape(shape, transparency=0.9)
        # display.FitAll()

        #print(test.inter_with_frame())
        test.vizualization_all()

    def Optimaze_evolution(self, event=None):
        test = Modules_walls.Balance_mass(self.name_frame, self.modules, self.faces)
        # test.var_test()
        test.move_frame()
        test.optimithation_evolution()
        #shape = test.random_location()
        # display.EraseAll()
        # display.Context.RemoveAll(True)
        # display.DisplayShape(shape, transparency=0.9)
        # display.FitAll()

        #print(test.inter_with_frame())
        #test.vizualization_all()

    def select_faces(self, event=None):
        display.SetSelectionModeFace()  # switch to Face selection mode
        display.register_select_callback(self.recognize_clicked)




if __name__ == '__main__':
    test = Interfac()
