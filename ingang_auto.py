import sys
from PyQt5 import QtWidgets
from PyQt5 import uic

form_class = uic.loadUiType("dialog.ui")[0]

class MyWindow(QtWidgets.QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def accept(self):
        quit()

    def reject(self):
        pass

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    wind = MyWindow()
    wind.show()
    app.exec_()