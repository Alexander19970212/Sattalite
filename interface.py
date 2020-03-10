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

from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.IFSelect import IFSelect_RetDone, IFSelect_ItemsByEntity
from OCC.Core.GeomAbs import GeomAbs_Plane, GeomAbs_Cylinder
from OCC.Core.TopoDS import topods_Face
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Display.SimpleGui import init_display
from OCC.Extend.DataExchange import read_step_file
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon
display, start_display, add_menu, add_function_to_menu = init_display()


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
        self.modules = {}
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
        start_display()



    def recognize_clicked(self, shp, *kwargs):
        """ This is the function called every time
        a face is clicked in the 3d view
        """
        for shape in shp:  # this should be a TopoDS_Face TODO check it is
            print("Face selected: ", shape)
            # recognize_face(topods_Face(shape))

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

        self.frame = read_step_file(filename)
        print('tttt')
        #self.frame = read_step_file(filename)
        display.EraseAll()
        display.Context.RemoveAll(True)
        display.DisplayShape(self.frame, color='GREEN', transparency=0.9)
        display.FitAll()

    def open_models(self):
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
        print("ttt")
        self.in_disp()


    def Clear(self):
        self.modules = {}

    def Print_all(self):
        print(self.modules)



if __name__ == '__main__':
    test = Interfac()
