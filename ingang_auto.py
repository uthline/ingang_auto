import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

class WhiteWindow(QMainWindow):
    sig_region_updated = pyqtSignal(QRect)

    def __init__(self):
        super().__init__()
        self.pos_start = None
        self.pos_end = None

    def paintEvent(self, event=None):
        painter = QPainter(self)
        painter.setOpacity(0.7)
        painter.setBrush(Qt.white)
        painter.setPen(QPen(Qt.white))
        painter.drawRect(self.rect())

        if self.pos_start is not None:
            rect = QRect(self.pos_start.x(), self.pos_start.y(),
                         self.pos_end.x() - self.pos_start.x(),
                         self.pos_end.y() - self.pos_start.y());
            painter.setPen(QPen(Qt.red))
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

    def closeEvent(self, QEvent):
        rect = QRect(self.pos_start.x(), self.pos_start.y(),
                     self.pos_end.x() - self.pos_start.x(),
                     self.pos_end.y() - self.pos_start.y());
        self.sig_region_updated.emit(rect)
        QApplication.setOverrideCursor(Qt.ArrowCursor)

form_class = uic.loadUiType("dialog.ui")[0]

class MyWindow(QMainWindow, form_class):
    sig_show_white = pyqtSignal()

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
        path = QFileDialog.getExistingDirectory(self, 'Select png folder')
        self.folderPath.setText(path)

class MyApplication(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.main_wind = MyWindow()
        self.main_wind.sig_show_white.connect(self.show_white_board)

        # Create the main window
        self.white_wind = WhiteWindow()

        self.white_wind.setWindowFlags(Qt.FramelessWindowHint)
        self.white_wind.setAttribute(Qt.WA_NoSystemBackground, True)
        self.white_wind.setAttribute(Qt.WA_TranslucentBackground, True)

        self.white_wind.sig_region_updated.connect(self.main_wind.update_region)

    def start_application(self):
        self.main_wind.show()

    @pyqtSlot()
    def show_white_board(self):
        QApplication.setOverrideCursor(Qt.CrossCursor)
        self.white_wind.showFullScreen()

if __name__ == "__main__":
    app = MyApplication(sys.argv)
    app.start_application()
    sys.exit(app.exec_())