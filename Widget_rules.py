'''import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

uifile_1 = "rules.ui"  # Enter file here.
form_1, base_1 = uic.loadUiType(uifile_1)

class Main(form_1, base_1):
    def __init__(self, parent=None):
        super(Main, self).__init__()
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())'''

import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import (QApplication, QWidget, QSplitter, QTreeView, QTextEdit, QGroupBox,
                             QFileSystemModel, QVBoxLayout, QTreeWidgetItem, QTreeWidget)
from PyQt5.QtCore import QDir
import os

class MyWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.category = {'Name_category': self.Name_category}

        self.type_constrain = {'Type_constrain_1': self.Type_constrain_1,
                          'Type_constrain_2': self.Type_constrain_2}

        self.setWindowTitle('Direct tree')
        self.resize(600, 400)
        self.vbox = QVBoxLayout()
        self.splitter = QSplitter()



        self.tree = QTreeWidget() # QTreeView()
        cg = QTreeWidgetItem(self.tree, ['Name_category'])
        c1 = QTreeWidgetItem(cg, ['Type_constrain_1'])
        c2 = QTreeWidgetItem(cg, ['Type_constrain_2'])
        #self.tree.setModel(self.model)

        self.textEdit = QTextEdit()
        self.splitter.addWidget(self.tree)
        '''self.splitter.addWidget(self.textEdit)
        self.splitter.setSizes([50, 200])'''
        self.vbox.addWidget(self.splitter)
        self.setLayout(self.vbox)

        self.tree.itemClicked.connect(self._on_double_clicked)

        #self.tree.setAnimated(False)
        #self.tree.setIndentation(20)
        #self.tree.setSortingEnabled(True)

    def _on_double_clicked(self, it, col):
        #print(it, col, it.text(col))
        if it.text(col) in self.category:
            self.category[it.text(col)]()
        elif it.text(col) in self.type_constrain:
            self.type_constrain[it.text(col)]()


    def Name_category(self):
        print('Name_caTEgory')
        groupbox = QGroupBox("Name_category")
        self.splitter.addWidget(groupbox)
        self.splitter.setSizes([50, 200])


    def Type_constrain_1(self):
        print('Type_Constrain_1')

        groupbox = QGroupBox("Type_Constrain_1")
        self.splitter.addWidget(groupbox)
        self.splitter.setSizes([50, 200])
        #groupbox.setEnabled(False)


    def Type_constrain_2(self):
        print('Type_Constrain_2')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MyWidget()
    win.show()
    sys.exit(app.exec_())