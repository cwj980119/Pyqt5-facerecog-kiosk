# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '8page.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from webcam import Ui_Webcam
import pymysql

def connectDB():
    host="database-1.cb5pctivsgrb.us-east-1.rds.amazonaws.com"
    username="root"
    port=3306
    database="log-in"
    password="ksc2021583"

    conn=pymysql.connect(host=host,user=username,password=password,db=database,port=port)
    return(conn)

def disconnnetDB(conn):
    conn.close()

class Ui_8page(object):
    def setupUi(self, sMainWindow):
        sMainWindow.setObjectName("Ui_8page")
        sMainWindow.resize(629, 652)
        self.window = sMainWindow
        self.centralwidget = QtWidgets.QWidget(sMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        #self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        #self.textEdit.setGeometry(QtCore.QRect(190, 0, 256, 71))
        #self.textEdit.setObjectName("textEdit")
        
        
        #회원가입창
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(180, 0, 256, 51))
        self.textBrowser.setObjectName("textBrowser")
        #사진촬영버튼
        self.pushbutton = QtWidgets.QToolButton(self.centralwidget)
        self.pushbutton.setGeometry(QtCore.QRect(240, 460, 151, 91))
        self.pushbutton.setObjectName("pushbutton")
        self.pushbutton.clicked.connect(self.take_pic)
        #
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(510, 540, 121, 71))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.close_window)
        
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(110, 90, 431, 61))
        self.lineEdit.setObjectName("lineEdit")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(120, 90, 381, 71))
        self.label_2.setObjectName("label_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(0, 540, 121, 71))
        self.pushButton_3.setObjectName("pushButton_3")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(110, 160, 431, 61))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(110, 230, 431, 61))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_4.setGeometry(QtCore.QRect(110, 300, 431, 61))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_5.setGeometry(QtCore.QRect(110, 380, 431, 61))
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(120, 160, 381, 71))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(110, 230, 381, 71))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(120, 300, 381, 71))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(120, 380, 381, 71))
        self.label_6.setObjectName("label_6")
        sMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(sMainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 629, 21))
        self.menubar.setObjectName("menubar")
        sMainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(sMainWindow)
        self.statusbar.setObjectName("statusbar")
        sMainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(sMainWindow)
        QtCore.QMetaObject.connectSlotsByName(sMainWindow)

    def take_pic(self):
        self.picture_window = QtWidgets.QMainWindow()
        self.picture= Ui_Webcam()
        self.picture.setupUi(self.picture_window)
        self.picture_window.show()
        
        #DB연결
        
        db_name=self.lineEdit.text()
        password1=self.lineEdit_2.text()
        #password2=self.lineEdit_3.text()
        db_birthday=self.lineEdit_4.text()
        db_malefemale=self.lineEdit_5.text()
        db_phonenumber=self.lineEdit_3.text()
        print("err")
        sql="INSERT INTO memberdata (memberID, name, password, birthdate, male/female, phonenumber) VALUES ('%s', '%s', '%s', '%s',%s,'%s')"
        
        
        #if password1==password2:
        if password1==db_phonenumber:    
            if db_malefemale=="여":
                db_malefemale=0
            else:
                db_malefemale=1
            db_password=password1
            conn = connectDB()
            curs = conn.cursor()
            curs.execute(sql,(db_name, db_password, db_birthday, db_malefemale, db_phonenumber))
        else:
             self.lineEdit.setText("")
             self.lineEdit_2.setText("")
             self.lineEdit_3.setText("")
             self.lineEdit_4.setText("")
             self.lineEdit_5.setText("")
             self.lineEdit_6.setText("")
        
        curs.close()
        disconnnet(conn)

    def close_window(self):
        self.window.close()

        

    def retranslateUi(self, sMainWindow):
        _translate = QtCore.QCoreApplication.translate
        sMainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        #self.textEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Gulim\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:26pt;\">회원가입</span></p></body></html>"))
        self.pushbutton.setText(_translate("MainWindow", "사진촬영"))
        self.pushButton_2.setText(_translate("MainWindow", "이전"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:16pt; color:#b5b5b5;\">이름을 입력해주세요</span></p></body></html>"))
        self.pushButton_3.setText(_translate("MainWindow", "처음으로"))
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:16pt; color:#b5b5b5;\">비밀번호를 입력해주세요</span></p></body></html>"))
        self.label_4.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:16pt; color:#b5b5b5;\">비밀번호를 다시 입력해주세요</span></p></body></html>"))
        self.label_5.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:16pt; color:#b5b5b5;\">생년월일을 입력해주세요</span><span style=\" font-size:12pt; color:#b5b5b5;\">(ex:19990909)</span></p></body></html>"))
        self.label_6.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:16pt; color:#b5b5b5;\">휴대폰번호를 입력해주세요</span></p></body></html>"))
        

 
       
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    sMainWindow = QtWidgets.QMainWindow()
    ui = Ui_8page()
    ui.setupUi(sMainWindow)
    sMainWindow.show()
    sys.exit(app.exec_())
