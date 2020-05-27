from PyQt5 import QtGui, QtCore
import sys

class BackgroundWidget(QtGui.QWidget):
    def __init__(self):
        super(BackgroundWidget, self).__init__()

        palette = QtGui.QPalette()
        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(QtGui.QPixmap("Figure_1.png")))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        self.show()

class BackgroundIssue(QtGui.QMainWindow):
    def __init__(self):
        super(BackgroundIssue, self).__init__()

        self._widget = BackgroundWidget()
        self.setCentralWidget(self._widget)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.resize(1002, 660)
        self.setWindowTitle("Partially Black Background Image")

        self.show()

    def resizeEvent(self, event):
        pixmap = QtGui.QPixmap("res/background.png")
        region = QtGui.QRegion(pixmap.mask())
        self.setMask(pixmap.mask())


def main():
    app     = QtGui.QApplication(sys.argv)
    window  = BackgroundIssue()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()