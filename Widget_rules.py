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
from PyQt5.QtWidgets import (QLabel, QRadioButton, QLineEdit, QApplication, QWidget, QSplitter, QTreeView, QTextEdit,
                             QGroupBox, QFormLayout,
                             QCheckBox, QHBoxLayout, QFileSystemModel, QVBoxLayout, QTreeWidgetItem, QTreeWidget,
                             QStackedWidget)
from PyQt5.QtCore import QDir
import os


class MyWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.tree_names = {'General requests': {'Min distances'},
                                 'General for satellite': {'Max angle of inertial axis', 'Distance of centre mass'},
                                 'Assembly': {'Assembly sequence', 'Dismantling', 'Transportation', 'Foolproof'},
                                 'Electrical': {'Length of cables', 'Bending radius', 'Space around connector',
                                                'Connector reach', 'Separate connectors location'},
                                 'Frequency compatibility': {'Natural frequency', 'Vibration isolation'},
                                 'EMC': {'GOST_1', 'GOST_2'},
                                 'Thermal compatibility': {'Component angle thermal change', 'Thermal bounds',
                                                           'Thermal tube', 'Material'},
                                 'System orientation': {'Non-overlapping', 'Pairing to axis',
                                                        'Min angle between component', 'Min distance', 'Max distance',
                                                        'Min angle distance', 'Total covering'},
                                 'System stabilization': {'Pairing to axis', 'Max distance', 'Min distance'},
                                 'System power': {'Location', 'Min distance', 'Number step', 'Connector location'},
                                 'System telemetry': {'Cable length', 'Non-overlapping', 'Location', 'Location rules',
                                                      'Pairing to axis'},
                                 'System navigation': {'Location', 'Location rules'}}

        self.category = {'Name_category': self.Name_category}

        self.type_constrain = {'Type_constrain_1': self.Type_constrain_1,
                               'Type_constrain_2': self.Type_constrain_2}

        self.tree = QTreeWidget()  # QTreeView()
        self.tree.setHeaderLabels(['Layout rules'])

        for category in self.tree_names:
            cg = QTreeWidgetItem(self.tree, [category])
            for constrain in self.tree_names[category]:
                c1 = QTreeWidgetItem(cg, [constrain])



        #cg = QTreeWidgetItem(self.tree, ['Name_category'])
        #c1 = QTreeWidgetItem(cg, ['Type_constrain_1'])
        #c2 = QTreeWidgetItem(cg, ['Type_constrain_2'])
        # self.tree.setModel(self.model)

        self.preparing_stack()

        '''self.setWindowTitle('Direct tree')
        self.resize(600, 400)

        self.splitter = QSplitter()'''

        # self.textEdit = QTextEdit()

        '''self.splitter.addWidget(self.textEdit)
        self.splitter.setSizes([50, 200])'''
        # self.vbox.addWidget(self.splitter)
        # self.setLayout(self.vbox)

        self.tree.currentItemChanged.connect(self.display)
        self.setGeometry(300, 50, 10, 10)
        self.setWindowTitle('StackedWidget demo')
        self.show()

        # self.tree.itemClicked.connect(self.display)

        # self.tree.setAnimated(False)
        # self.tree.setIndentation(20)
        # self.tree.setSortingEnabled(True)

    def preparing_stack(self):

        self.stack1 = QWidget()
        self.stack2 = QWidget()
        self.stack3 = QWidget()

        self.stack1UI()
        self.stack2UI()
        self.stack3UI()

        self.Stack = QStackedWidget(self)
        self.Stack.addWidget(self.stack1)
        self.Stack.addWidget(self.stack2)
        self.Stack.addWidget(self.stack3)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.tree)
        self.vbox.addWidget(self.Stack)

        self.setLayout(self.vbox)

    def _on_double_clicked(self, it, col):
        # print(it, col, it.text(col))
        if it.text(col) in self.category:
            self.category[it.text(col)]()
        elif it.text(col) in self.type_constrain:
            self.type_constrain[it.text(col)]()

    def Name_category(self):
        layout = QFormLayout()
        print('Name_caTEgory')
        layout.addRow("Name", QLineEdit())
        layout.addRow("Address", QLineEdit())

        self.stack1.setLayout(layout)

    def Type_constrain_1(self):
        layout = QFormLayout()
        print('Type_Constrain_1')
        sex = QHBoxLayout()
        sex.addWidget(QRadioButton("Male"))
        sex.addWidget(QRadioButton("Female"))
        layout.addRow(QLabel("Sex"), sex)

        # groupbox.setEnabled(False)
        self.stack1.setLayout(layout)

    def Type_constrain_2(self):
        layout = QFormLayout()
        print('Type_Constrain_2')
        layout.addWidget(QLabel("subjects"))
        layout.addWidget(QCheckBox("Physics"))
        layout.addWidget(QCheckBox("Maths"))

        self.stack1.setLayout(layout)

    def stack1UI(self):
        layout = QFormLayout()
        layout.addRow("Name", QLineEdit())
        layout.addRow("Address", QLineEdit())
        # self.setTabText(0,"Contact Details")
        self.stack1.setLayout(layout)

    def stack2UI(self):
        layout = QFormLayout()
        sex = QHBoxLayout()
        sex.addWidget(QRadioButton("Male"))
        sex.addWidget(QRadioButton("Female"))
        layout.addRow(QLabel("Sex"), sex)
        layout.addRow("Date of Birth", QLineEdit())

        self.stack2.setLayout(layout)

    def stack3UI(self):
        layout = QHBoxLayout()
        layout.addWidget(QLabel("subjects"))
        layout.addWidget(QCheckBox("Physics"))
        layout.addWidget(QCheckBox("Maths"))
        self.stack3.setLayout(layout)

    def display(self, i):
        print(type(i))
        self.Stack.setCurrentIndex(1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MyWidget()
    # win.show()
    sys.exit(app.exec_())
