import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic



class WhiteWindow(QtWidgets.QMainWindow):
    sig_region_updated = QtCore.pyqtSignal(QtCore.QRect)

    def __init__(self):
        super().__init__()
        self.pos_start = None
        self.pos_end = None

    def paintEvent(self, event=None):
        painter = QtGui.QPainter(self)
        painter.setOpacity(0.7)
        painter.setBrush(QtCore.Qt.white)
        painter.setPen(QtGui.QPen(QtCore.Qt.white))
        painter.drawRect(self.rect())

        if self.pos_start is not None:
            rect = QtCore.QRect(self.pos_start.x(), self.pos_start.y(),
                         self.pos_end.x() - self.pos_start.x(),
                         self.pos_end.y() - self.pos_start.y());
            painter.setPen(QtGui.QPen(QtCore.Qt.red))
            painter.drawRect(rect);

    def mousePressEvent(self, QMouseEvent):
        print(QMouseEvent.pos())
        self.pos_end = self.pos_start = QMouseEvent.pos()
        self.update()

    def mouseReleaseEvent(self, QMouseEvent):
        print(QMouseEvent.pos())
        self.pos_end = QMouseEvent.pos()
        self.close()

    def mouseMoveEvent(self, QMouseEvent):
        self.pos_end = QMouseEvent.pos()
        if self.pos_start is not None:
            self.update()

    def keyPressEvent(self, QEvent):
        self.close()

    def closeEvent(self, QEvent):
        if self.pos_start is not None and self.pos_end is not None:
            rect = QtCore.QRect(self.pos_start.x(), self.pos_start.y(),
                         self.pos_end.x() - self.pos_start.x(),
                         self.pos_end.y() - self.pos_start.y());
            self.sig_region_updated.emit(rect)
            QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.ArrowCursor)

form_class = uic.loadUiType("dialog.ui")[0]

class MyWindow(QtWidgets.QMainWindow, form_class):
    sig_show_white = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def setting(self):
        self.sig_show_white.emit()

    def accept(self):
        quit()

    def update_region(self, rect):
        self.pos_start_x.setText(str(rect.left()))
        self.pos_start_y.setText(str(rect.top()))
        self.pos_end_x.setText(str(rect.right()))
        self.pos_end_y.setText(str(rect.bottom()))

    def folderbuttonclicked(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select image folder')
        self.folderPath.setText(path)

class MyApplication(QtWidgets.QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.main_wind = MyWindow()
        self.main_wind.sig_show_white.connect(self.show_white_board)

        # Create the main window
        self.white_wind = WhiteWindow()

        self.white_wind.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.white_wind.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.white_wind.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)

        self.white_wind.sig_region_updated.connect(self.main_wind.update_region)

    def start_application(self):
        self.main_wind.show()

    @QtCore.pyqtSlot()
    def show_white_board(self):
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.CrossCursor)
        self.white_wind.showFullScreen()

if __name__ == "__main__":
    app = MyApplication(sys.argv)
    app.start_application()
    sys.exit(app.exec_())