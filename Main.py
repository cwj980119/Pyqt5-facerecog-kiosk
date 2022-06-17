import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic,QtWidgets, QtGui

import learning
import login
import register
import menu
import register_pic2

class Main(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.ui = uic.loadUi("./UI/main.ui")
        self.ui.show()
        self.ui.btn_login.clicked.connect(self.toLogin)
        self.ui.btn_register.clicked.connect(self.toRegister)
        self.ui.btn_menu.clicked.connect(self.toMenu)
        self.ui.a.clicked.connect(self.tolearning)
        

    def toLogin(self):
        self.ui.hide()
        self.login = login.Login(self)
    
    def toRegister(self):
        self.ui.hide()
        self.register=register.Register(self)
        # self.signin_window = QtWidgets.QMainWindow()
        # self.register= register.Ui_register()
        # self.register.setupUi(self.signin_window)
        # self.signin_window.show()
        # self.regpic = register_pic.Take_pic(self)

    def toMain(self):
        self.ui.show()

    def tolearning(self):
        self.ui.hide()
        test_user = [0,"test","test","test"]
        self.learning = learning.Learnig(self, test_user)
        
    def toMenu(self, user):
        self.ui.hide()
        self.menu = menu.Menu(self, user)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Main()
    sys.exit(app.exec_())
