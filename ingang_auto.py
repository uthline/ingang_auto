import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

class WhiteWindow(QMainWindow):
    def paintEvent(self, event=None):
        painter = QPainter(self)

        painter.setOpacity(0.7)
        painter.setBrush(Qt.white)
        painter.setPen(QPen(Qt.white))
        painter.drawRect(self.rect())

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

class MyApplication(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.wind = MyWindow()
        self.wind.sig_show_white.connect(self.show_white_board)

        # Create the main window
        self.window = WhiteWindow()

        self.window.setWindowFlags(Qt.FramelessWindowHint)
        self.window.setAttribute(Qt.WA_NoSystemBackground, True)
        self.window.setAttribute(Qt.WA_TranslucentBackground, True)

    def start_application(self):
        self.wind.show()

    @pyqtSlot()
    def show_white_board(self):
        self.window.showFullScreen()

if __name__ == "__main__":
    app = MyApplication(sys.argv)
    app.start_application()
    sys.exit(app.exec_())