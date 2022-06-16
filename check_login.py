from PyQt5.QtWidgets import *
from PyQt5 import uic,QtWidgets, QtGui

class Check(QWidget):
    def __init__(self, predict_list, login_page):
        QWidget.__init__(self)
        self.ui = uic.loadUi("./UI/check.ui")
        self.login_page = login_page
        self.set_Text(predict_list)
        self.predict = predict_list
        self.ui.label.setText(predict_list[0][1] + "님이 맞으신가요?")
        self.ui.show()
        print(predict_list)
        self.ui.btn_yes.clicked.connect(self.answer_yes)
        self.ui.list1_ok.clicked.connect(self.answer_1)
        self.ui.list2_ok.clicked.connect(self.answer_2)
        self.ui.list3_ok.clicked.connect(self.answer_3)

    def answer_yes(self):
        self.login_success(self.predict[0])
    def answer_1(self):
        self.login_success(self.predict[1][0])
    def answer_2(self):
        self.login_success(self.predict[1][1])
    def answer_3(self):
        self.login_success(self.predict[1][2])

    def login_success(self, user):
        self.ui.hide()
        self.login_page.succ(user)

    def set_Text(self,p_list):
        self.ui.label.setText(p_list[0][1] + "님이 맞으신가요?")
        self.ui.list1_name.setText(p_list[1][0][1])
        self.ui.list1_num.setText(p_list[1][0][5])
        self.ui.list2_name.setText(p_list[1][1][1])
        self.ui.list2_num.setText(p_list[1][1][5])
        self.ui.list3_name.setText(p_list[1][2][1])
        self.ui.list3_num.setText(p_list[1][2][5])
