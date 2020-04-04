# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 17:41:05 2020

@author: Alexander
"""

# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QPushButton, QWidget, \
    QLineEdit, QFileDialog
from PyQt5 import uic
import OCC.Display.backend
from OCC.Display.OCCViewer import OffscreenRenderer
import os
import os
import os.path
import sys
# import wx

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
# display, start_display, add_menu, add_function_to_menu = init_display('wx')
from OCC.Core.BRepClass3d import BRepClass3d_SolidClassifier

back = OCC.Display.backend.load_backend()
from OCC.Display.backend import load_backend, get_qt_modules
from OCC.Display.qtDisplay import qtViewer3d
from OCC.Display.SimpleGui import init_display
from OCC.Extend.DataExchange import read_step_file
from PyQt5 import QtWidgets, QtCore, QtPrintSupport, QtGui
import construction
from PyQt5.QtWidgets import *

uifile_1 = "Main_widget/untitled.ui"  # Enter file here.

form_1, base_1 = uic.loadUiType(uifile_1)


class App_folder(QWidget):

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

        # self.openFileNameDialog()
        # self.openFileNamesDialog()
        # self.saveFileDialog()

        # self.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        fileName = QFileDialog.getExistingDirectory(self, "Open a folder")#, "/home/my_user_name/",
                                                       #QtGui.QFileDialog.ShowDirsOnl)
        if fileName:
            # print(fileName)
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

        # self.openFileNameDialog()
        # self.openFileNamesDialog()
        # self.saveFileDialog()

        # self.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            # print(fileName)
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


class Main(base_1, form_1):
    def __init__(self, parent=None):
        super(Main, self).__init__()
        self.setupUi(self)

        # self.display, self.start_display, self.add_menu, self.add_function_to_menu = init_display()
        # self.canvas = FigureCanvas(self.figure)
        QtCore, QtGui, QtWidgets, QtOpenGL = get_qt_modules()
        self.canvas = qtViewer3d(self)
        # self.canvas.sig_topods_selected.connect(self.handle_selection)
        self.display = self.canvas._display
        self.scrollArea.setWidget(self.canvas)
        # self.mess.setText('Выберите файл')
        # self.Bar_1.setValue(0)

        self.Open_frame.clicked.connect(self.open_frame)
        self.Random_composition.clicked.connect(self.random_composition)
        self.Save_result.clicked.connect(self.save_result)
        self.Show_frame.clicked.connect(self.show_frame)
        self.Add_file.clicked.connect(self.add_file)
        self.Start_optimization.clicked.connect(self.start_optimization)
        self.Remove_all.clicked.connect(self.remove_all)
        self.Remove_selected.clicked.connect(self.remove_selected)
        self.tableWidget.itemClicked.connect(self.tablewidgetclicked)
        self.Select_faces.clicked.connect(self.select_faces)
        self.Remove_all_faces.clicked.connect(self.remove_all_faces)
        self.Add_folder.clicked.connect(self.add_folder)
        # self.Random_composition.clicked.connect(self.random_composition)

        # self.canvas.mpl_connect('button_press_event',self.onClick)
        self.frame = None
        self.modules = {}
        self.path_modules = {}
        self.limits = []
        self.faces_name = []
        self.faces = []
        self.faces_shape = []
        self.constructor = construction.Balance_mass()

        #############################################################
        self.limits = {'DAV_WS16.STEP': [[1, 2], [0, 45, 60, 90]],
                       'DAV2_WS16.STEP': [[1, 2, 3, 0], [30, 90, 180]],
                       'DAV3_WS16.STEP': [[0, 3], [0, 180]],
                       'Magnitometr.STEP': [[2], [30, 45, 90, 135]]}
        #############################################################

    def add_folder(self):
        ex = App_folder()
        filename = ex.openFileNameDialog()
        # sys.exit(app.exec_())
        print(filename)
        from os import listdir
        from os.path import isfile, join
        onlyfiles = [f for f in listdir(filename) if isfile(join(filename, f))]
        print(onlyfiles)
        for name in onlyfiles:
            #self.path_modules[name] = filename
            self.modules[name] = read_step_file(filename+'/'+name)

        self.reload_modules()


    def random_composition(self):

        self.constructor.initial(self.frame, self.modules, self.faces, self.limits)
        self.constructor.random_location2()
        result = self.constructor.modules
        self.show_frame()

        for module in result:
            self.display.DisplayShape(result[module], color='RED')

    def select_faces(self):
        self.show_frame()
        self.display.SetSelectionModeFace()  # switch to Face selection mode
        self.display.register_select_callback(self.recognize_clicked)

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
            brepbndlib_Add(shape, bbox)
            xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
            bounds = [sorted([xmax - xmin, ymax - ymin, zmax - zmin])[1],
                      sorted([xmax - xmin, ymax - ymin, zmax - zmin])[2]]
            print('--> Bounds', xmax - xmin, ymax - ymin, zmax - zmin)
            centre, normal, X_axis = self.recognize_face(topods_Face(shape))
            if shape in self.faces_shape:
                # self.display.DisplayShape(shape, color='GREEN', transparency=0.9)
                # self.display.Context.Remove(shape)#######
                # self.display.Context.
                ind = self.faces_shape.index(shape)

                self.faces_shape.pop(ind)
                self.faces.pop(ind)
                self.faces_name.pop(ind)

            else:
                # self.display.DisplayShape(shape, color='RED', transparency=0.8)
                # self.display.FitAll()
                self.faces.append([centre, normal, X_axis, bounds])
                self.faces_shape.append(shape)
                self.faces_name.append(bounds[0] * bounds[1])

            # self.display.SetCloseAllContexts()
            self.reload_faces()
            self.display.SetSelectionModeFace()  # switch to Face selection mode
            # self.display.register_select_callback(self.recognize_clicked)

    def remove_all_faces(self):
        self.faces_shape = []
        self.faces = []
        self.faces_name = []
        self.reload_faces()
        self.display.SetSelectionModeFace()

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
            if _in_solid.State() == 0:
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

    def draw_coordinates(self, event=None):

        # The radius of a sphere at the origin
        centerpoint_sphere_radius = 30.0
        # The length of every axis starting at -length/2 and ending at length/2
        arrowlength = 1000.0
        # Radius of the arrow shaft of every axis
        radius_of_arrow_shaft = 10.0
        # Length of every axis
        lenght_of_arrow_head = 50.0
        # Radius of the arrow heads cone
        radius_of_arrow_head = 20.0
        # Create the Coordinate and Draw it
        self.CoordinateCrossShape(centerpoint_sphere_radius,
                                  arrowlength,
                                  radius_of_arrow_shaft,
                                  lenght_of_arrow_head,
                                  radius_of_arrow_head)

    def CoordinateCrossShape(self, centerpoint_sphere_radius,
                             arrowlength,
                             radius_of_arrow_shaft,
                             lenght_of_arrow_head,
                             radius_of_arrow_head):
        '''
        Function arrowshape creates the shape of an arrow starting at vector
        pointing into diretcion. We create a cylinder and a cone and combine the
        utilising OCC.BRepAlgoAPI.BRepAlgoAPI_Fuse.
        @param vector: starting point of the arrow
        @type vector: scipy array(3,1)
        @param directionvector: direction of the arrow
        @type directionvector: scipy array(3,1)
        @param arrowlength: length of the arrow
        @type arrowlength: scalar
        @param radius_of_arrow_shaft: radius of the arrow shaft
        @type radius_of_arrow_shaft: scalar
        @param lenght_of_arrow_head: length of the arrow head
        @type lenght_of_arrow_head: scalar
        @param radius_of_arrow_head: radius of the arrow head
        @type radius_of_arrow_head: scalar
        @return: Arrow as Shape object
        '''

    pass
    # The origin of the coordinate system
    '''Origin = scipy.zeros((3, 1), dtype=float)
    # The direction unit vectors of the axis
    xDir = scipy.zeros((3, 1), dtype=float)
    25
    xDir[0, 0] = 1.0
    yDir = scipy.zeros((3, 1), dtype=float)
    yDir[1, 0] = 1.0
    zDir = scipy.zeros((3, 1), dtype=float)
    zDir[2, 0] = 1.0
    # Create the center point sphere shape at the origin
    OriginSphere = sphere_from_vector_and_radius(Origin,
                                                 centerpoint_sphere_radius)
    OriginSphereShape = OriginSphere.Shape()
    # Create the XAxis shape
    XAxisShape = arrowShape(Origin - 0.5 * arrowlength * xDir,
                            xDir,
                            arrowlength,
                            radius_of_arrow_shaft,
                            lenght_of_arrow_head,
                            radius_of_arrow_head)
    # Create the YAxis shape
    YAxisShape = arrowShape(Origin - 0.5 * arrowlength * yDir,
                            yDir,
                            arrowlength,
                            radius_of_arrow_shaft,
                            lenght_of_arrow_head,
                            radius_of_arrow_head)
    # Create the ZAxis shape
    ZAxisShape = arrowShape(Origin - 0.5 * arrowlength * zDir,
                            zDir,
                            arrowlength,
                            radius_of_arrow_shaft,
                            lenght_of_arrow_head,
                            radius_of_arrow_head)
    # Display these shapes
    display.DisplayColoredShape(OriginSphereShape, 'WHITE')
    display.DisplayColoredShape(XAxisShape, 'BLUE')
    display.DisplayColoredShape(YAxisShape, 'ORANGE')
    display.DisplayColoredShape(ZAxisShape, 'GREEN')'''

    def tablewidgetclicked(self):
        if self.display_selected.isChecked() == True:
            # print(self.tableWidget.currentItem().text())
            self.display.EraseAll()
            self.display.Context.RemoveAll(True)
            self.display.DisplayShape(self.modules[self.tableWidget.currentItem().text()], color='RED',
                                      transparency=0.9)
            self.display.FitAll()

    def remove_selected(self):
        self.modules.pop(self.tableWidget.currentItem().text())
        self.path_modules.pop(self.tableWidget.currentItem().text())
        self.display.EraseAll()
        self.display.Context.RemoveAll(True)
        self.tableWidget.clearContents()
        self.reload_modules()

    def remove_all(self):
        '''for row, item in enumerate(self.modules):
            newitem = QTableWidgetItem(' ')
            newitem.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(row-1, 1, newitem)'''
        self.tableWidget.clearContents()
        self.modules = {}
        self.path_modules = {}
        self.display.EraseAll()
        self.display.Context.RemoveAll(True)
        # self.reload_modules()

    def add_file(self):
        # app = QApplication(sys.argv)
        ex = App()
        filename = ex.openFileNameDialog()
        # sys.exit(app.exec_())
        name = os.path.split(filename)[-1]
        # print(name)
        self.path_modules[name] = filename
        self.modules[name] = read_step_file(filename)

        self.reload_modules()

    def open_frame(self):
        '''
        open step model of the frame
        :return: None
        '''

        # app = QApplication(sys.argv)
        ex = App()
        filename = ex.openFileNameDialog()
        # sys.exit(app.exec_())
        print(os.path.split(filename)[-1])
        self.name_frame = filename

        # self.frame = read_step_file(filename)

        self.frame = read_step_file(filename)
        self.display.EraseAll()
        self.display.Context.RemoveAll(True)
        self.display.DisplayShape(self.frame, color='GREEN', transparency=0.9)
        # self.display.Repaint()
        self.display.FitAll()

    def reload_modules(self):
        for row, item in enumerate(self.modules):
            newitem = QTableWidgetItem(item)
            newitem.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(row - 1, 1, newitem)

    def reload_faces(self):

        self.show_frame()
        self.tableWidget_faces.clearContents()
        for row, item in enumerate(self.faces_name):
            # print(row)
            self.display.DisplayShape(self.faces_shape[row], color='RED')

            newitem = QTableWidgetItem(str(item))
            newitem.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget_faces.setItem(row - 1, 1, newitem)

    def show_frame(self):
        if self.frame != None:
            self.display.SetCloseAllContexts()
            self.display.EraseAll()
            self.display.Context.RemoveAll(True)
            self.display.DisplayShape(self.frame, color='GREEN', transparency=0.9)
            # self.display.Repaint()
            self.display.FitAll()

    def save_result(self):
        pass

    def start_optimization(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
