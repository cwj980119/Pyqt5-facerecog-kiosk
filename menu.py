from PyQt5.QtWidgets import *
from PyQt5 import uic

class Menu(QWidget):
    def __init__(self, main ,user):
        QWidget.__init__(self)
        self.main = main
        self.ui = uic.loadUi("./UI/menu.ui")
        self.ui.label.setText("어서오세요 " + user[1] + "님!")
        self.ui.btn_main.clicked.connect(self.toMain)
        self.ui.show()

    def toMain(self):
        self.ui.hide()
        self.main.toMain()