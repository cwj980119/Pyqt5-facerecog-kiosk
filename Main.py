import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic,QtWidgets, QtGui

import login
import register2
import menu
import register_pic

class Main(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.ui = uic.loadUi("./UI/main.ui")
        self.ui.show()
        self.ui.btn_login.clicked.connect(self.toLogin)
        self.ui.btn_register.clicked.connect(self.toRegister)
        

    def toLogin(self):
        self.ui.hide()
        self.login = login.Login(self)
    
    def toRegister(self):
        self.ui.hide()
        self.register=register2.Register(self)
        # self.signin_window = QtWidgets.QMainWindow()
        # self.register= register.Ui_register()
        # self.register.setupUi(self.signin_window)
        # self.signin_window.show()
        #sself.regpic = register_pic.Take_pic(self)

    def toMain(self):
        self.ui.show()
        
    def toMenu(self, user):
        self.ui.hide()
        self.menu = menu.Menu(self, user)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Main()
    sys.exit(app.exec_())
