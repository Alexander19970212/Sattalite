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
                             QGroupBox, QFormLayout, QComboBox, QListView,
                             QCheckBox, QHBoxLayout, QFileSystemModel, QVBoxLayout, QTreeWidgetItem, QTreeWidget,
                             QStackedWidget, QPushButton)
from PyQt5 import QtCore, Qt, uic
import os


class MyWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(300, 300, 500, 500)

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
        self.tree.setFixedHeight(500)
        self.tree.setFixedWidth(250)

        bt_op_conf = QPushButton('Open configuration', self)
        bt_op_conf.setToolTip('This is an example button')
        bt_op_conf.move(100, 70)
        bt_op_conf.setFixedSize(250, 30)

        bt_sv_conf = QPushButton('Save configuration', self)
        bt_sv_conf.setToolTip('This is an example button')
        bt_sv_conf.move(100, 70)
        bt_sv_conf.setFixedSize(250, 30)

        bt_app = QPushButton('Apply', self)
        bt_app.setToolTip('This is an example button')
        bt_app.move(100, 70)
        bt_app.setFixedSize(150, 30)

        bt_cls = QPushButton('Close', self)
        bt_cls.setToolTip('This is an example button')
        bt_cls.move(100, 70)
        bt_cls.setFixedSize(150, 30)

        h1_box = QHBoxLayout()
        h1_box.addWidget(bt_app, alignment=QtCore.Qt.AlignRight)
        h1_box.addWidget(bt_cls)#, alignment=QtCore.Qt.AlignRight)


        for category in self.tree_names:
            cg = QTreeWidgetItem(self.tree, [category])
            for constrain in self.tree_names[category]:
                c1 = QTreeWidgetItem(cg, [constrain])



        #cg = QTreeWidgetItem(self.tree, ['Name_category'])
        #c1 = QTreeWidgetItem(cg, ['Type_constrain_1'])
        #c2 = QTreeWidgetItem(cg, ['Type_constrain_2'])
        # self.tree.setModel(self.model)

        self.preparing_stack()

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.tree)
        self.vbox.addWidget(bt_op_conf)
        self.vbox.addWidget(bt_sv_conf)

        self.hbox = QHBoxLayout()
        self.hbox.addLayout(self.vbox)

        v1_box = QVBoxLayout()

        v1_box.addWidget(self.Stack)
        v1_box.addLayout(h1_box)

        self.hbox.addLayout(v1_box)

        self.setLayout(self.hbox)

        '''self.setWindowTitle('Direct tree')
        self.resize(600, 400)

        self.splitter = QSplitter()'''

        # self.textEdit = QTextEdit()

        '''self.splitter.addWidget(self.textEdit)
        self.splitter.setSizes([50, 200])'''
        # self.vbox.addWidget(self.splitter)
        # self.setLayout(self.vbox)

        self.tree.currentItemChanged.connect(self.display)

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
        self.Stack.setFixedWidth(600)


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
        #layout = QFormLayout()
        pass

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
        col_1 = QVBoxLayout()
        col_1.addWidget(QLabel('Minimal distance'))
        col_1.addWidget(QRadioButton('General'))
        col_1.addWidget(QRadioButton('For component'))
        col_1.addWidget(QLabel('Main component'))
        col_1.addWidget(QComboBox())
        col_1.addWidget(QLabel('D, distance'))

        row_val = QHBoxLayout()
        row_val.addWidget(QLineEdit())
        row_val.addWidget(QComboBox())

        col_1.addLayout(row_val)

        row_bots = QHBoxLayout()
        row_bots.addWidget(QPushButton('Add rule'))
        row_bots.addWidget(QPushButton('Save rule'))

        col_1.addLayout(row_bots)

        col_2 = QVBoxLayout()
        label = QLabel(self)
        pixmap = QtGui.QPixmap('Figure_1.png')
        label.setPixmap(pixmap)
        col_2.addWidget(label)
        col_2.addWidget(QLabel('Second component'))
        col_2.addWidget(QComboBox())
        col_2.addWidget(QListView())
        col_2.addWidget(QPushButton('Delete rule'))

        layout = QHBoxLayout()
        layout.addLayout(col_1)
        layout.addLayout(col_2)

        # groupbox.setEnabled(False)
        self.stack1.setLayout(layout)

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
    app.setStyle('Fusion')
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Base, QtGui.QColor(15, 15, 15))
    palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)

    palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(200, 200, 200).lighter())
    palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
    app.setPalette(palette)
    win = MyWidget()
    # win.show()
    sys.exit(app.exec_())
    #142, 45, 197
