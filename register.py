from PyQt5.QtWidgets import *
from PyQt5 import uic,QtWidgets, QtGui
import pymysql
import os
import register_pic2
import register_pic
'''
# 상황에 맞게 table변경필요    
def connectDB():
    host="database-1.cb5pctivsgrb.us-east-1.rds.amazonaws.com"
    username="root"
    port=3306
    database="log-in"
    password="ksc2021583"

    conn=pymysql.connect(host=host,user=username,password=password,db=database,port=port)
    return(conn)

def disconnectDB(conn):
    conn.close()
    
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)

def findnumber(db_name,db_phonenumber):
    sql2="SELECT memberID, name FROM memberdata where name ="+"'"+db_name+"'" "AND phonenumber ="+"'"+ db_phonenumber+"'"   
    conn2 = connectDB()
    curs2 = conn2.cursor()
    print(db_name)
    curs2.execute(sql2)  
    
    result=curs2.fetchone()
    print(result)
    print(int(result[0]))
    #print(str(result[1]))
        
    ## 이미지저장경로 설정, 컴퓨터에 맞게 변경필요
    #route='/Users/admin/Documents/GitHub/Pyqt5-facerecog-kiosk/image/'
    #routenumber=str(result[0])
    #createFolder(route+str(result[1])+str(result[0]))
        
    curs2.close()
    disconnectDB(conn2)
'''
class Register(QWidget):
    def __init__(self, main):
        QWidget.__init__(self)
        self.main = main
        self.ui = uic.loadUi("./UI/register.ui")
        self.ui.pushbutton.clicked.connect(self.take_pic)
        self.ui.pushButton_2.clicked.connect(self.close_window)
        self.ui.pushButton_3.clicked.connect(self.gotoMain)
        self.ui.lineEdit_1.textChanged.connect(self.lineEdit_1changed)
        self.ui.lineEdit_2.textChanged.connect(self.lineEdit_2changed)
        self.ui.lineEdit_3.textChanged.connect(self.lineEdit_3changed)
        self.ui.lineEdit_4.textChanged.connect(self.lineEdit_4changed)
        self.ui.lineEdit_5.textChanged.connect(self.lineEdit_5changed)
        self.ui.lineEdit_6.textChanged.connect(self.lineEdit_6changed)
        self.ui.show()
    
    def take_pic(self):
        
        #DB연결
        
        db_name=self.ui.lineEdit_1.text()
        password1=self.ui.lineEdit_2.text()
        password2=self.ui.lineEdit_3.text()
        db_birthdate=self.ui.lineEdit_4.text()
        gender=self.ui.lineEdit_5.text()
        db_phonenumber=self.ui.lineEdit_6.text()
        
        #사진연동
        
        if password1==password2:
            if gender=="여":
                db_gender=False
            elif gender=="남":
                db_gender=True

            db_password=password1
            #conn = connectDB()
            #curs = conn.cursor()
            
            #val=( db_name, db_password, db_birthdate, db_gender, db_phonenumber)
            self.ui.hide()
            self.regpic = register_pic.Take_pic(self.main, db_name, db_password, db_birthdate, db_gender, db_phonenumber)
        
            #sql="INSERT INTO memberdata ( name, password, birthdate, gender, phonenumber) VALUES ( %s, %s, %s, '%s', %s)"
            
            #curs.execute(sql,val)
            #conn.commit()
            
           
        else:
            self.ui.lineEdit_1.setText("")
            self.ui.lineEdit_2.setText("")
            self.ui.lineEdit_3.setText("")                
            self.ui.lineEdit_4.setText("")
            self.ui.lineEdit_5.setText("")
            self.ui.lineEdit_6.setText("")
        
   
        #sql2="SELECT memberID, name FROM memberdata where name ="+"'"+db_name+"'" "AND phonenumber ="+"'"+ db_phonenumber+"'"   
        
        #curs.execute(sql2)  
        #result=curs.fetchone()
        
        ## 이미지저장경로 설정, 컴퓨터에 맞게 변경필요
        #route='/Users/admin/Documents/GitHub/Pyqt5-facerecog-kiosk/image/'
        #db_photoaddress=route+str(result[1])+str(result[0])
        #createFolder(db_photoaddress)
        
        ##경로 photoaddress에 입력
        #sql2="UPDATE memberdata SET photoaddress = %s WHERE memberID = %s"
        #val2=(db_photoaddress,result[0])
        #curs.execute(sql2,val2)
        #conn.commit()
        #curs.close()
        #conn.close()
        
    def close_window(self):
        self.ui.close()
    
    def gotoMain(self):
        self.ui.hide()
        self.main.toMain()
        
        
    def lineEdit_1changed(self):
        if self.ui.lineEdit_1:
            self.ui.label_1.setVisible(False)
    
    def lineEdit_2changed(self):
        if self.ui.lineEdit_2:
            self.ui.label_2.setVisible(False)
            
    def lineEdit_3changed(self):
        if self.ui.lineEdit_3:
            self.ui.label_3.setVisible(False)
    
    def lineEdit_4changed(self):
        if self.ui.lineEdit_4:
            self.ui.label_4.setVisible(False)        
    
    def lineEdit_5changed(self):
        if self.ui.lineEdit_5:
            self.ui.label_5.setVisible(False)
    
    def lineEdit_6changed(self):
        if self.ui.lineEdit_6:
            self.ui.label_6.setVisible(False) 
    
