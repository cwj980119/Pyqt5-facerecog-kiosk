import sys
import os
import dlib,cv2,threading
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5 import uic,QtWidgets, QtGui
from keras.models import load_model
import pymysql

def connectDB():
    host="database-1.cb5pctivsgrb.us-east-1.rds.amazonaws.com"
    username="root"
    port=3306
    database="log-in"
    password="ksc2021583"

    conn=pymysql.connect(host=host,user=username,password=password,db=database,port=port)
    return(conn)

load_model = load_model('tl_20_cropped_e20_b200.h5')

class Main(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.ui = uic.loadUi("./UI/main.ui")
        self.ui.show()
        self.ui.btn_login.clicked.connect(self.toLogin)
        self.ui.btn_register.clicked.connect(self.a)


    def toLogin(self):
        self.ui.hide()
        self.login = Login(self)

    def toMain(self):
        self.ui.show()
    def a(self):
        self.b = Check()

class Login(QWidget):
    def __init__(self, main):
        QWidget.__init__(self)
        self.main = main
        try:
            conn = connectDB()
            self.curs = conn.cursor()
            self.curs.execute("select count(*) from userdata")
            result = self.curs.fetchone()
            self.user_num = result[0]
            print(self.user_num)
            self.ui = uic.loadUi("./UI/login.ui")
            self.ui.to_main.clicked.connect(self.close)
            self.ui.cam_on.clicked.connect(self.start_cam)
            self.ui.cam_off.clicked.connect(self.close_cam)
            self.ui.show()
        except:
            conn.close()
            self.close()
    def close(self):
        self.close_cam()
        self.main.toMain()
        self.ui.hide()

    def setCam(self):
        detector = dlib.get_frontal_face_detector()
        cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        width = cam.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print(round(width), height)
        count = 0
        user_list = [0 for i in range(self.user_num)]
        while self.working:
            img, frame = cam.read()
            face = detector(frame)
            for f in face:
                # dlib으로 얼굴 검출
                cv2.rectangle(frame, (f.left(), f.top()), (f.right(), f.bottom()), (0, 0, 255), 1)
            if len(face) == 1:
                crop = frame[f.top():f.bottom(), f.left():f.right()]
                crop = cv2.resize(crop, (224, 224))
                image = np.array(crop)
                image = image.astype('float32') / 255
                #
                # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  ####gray
                # image = np.expand_dims(image,-1)                 ####gray

                image = np.expand_dims(image, 0)
                # print(image.shape)
                a = load_model.predict(image)
                #print(a[0][np.argmax(a)])
                if a[0][np.argmax(a)] > 0.9:
                    count+=1
                    user_list[np.argmax(a)] += 1
                    #print(np.argmax(a),"th user")
                    # if count>20:
                    #     print(user_list)
                    #     a = user_list.copy()
                    #     a.sort(reverse=True)
                    #     #self.check = Check()
                    #     self.close_cam()
                    #     print(a[0])
                    #     print(user_list)
                    #     print(user_list.index(a[0]))
                    # #print(a)

            print("done")
            cvt_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, c = cvt_frame.shape
            qImg = QtGui.QImage(cvt_frame.data, w, h, w * c, QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(qImg)
            self.ui.cam.resize(round(width), round(height))
            self.ui.cam.setPixmap(pixmap)
            if count > 20:
                print(user_list)
                a = user_list.copy()
                a.sort(reverse=True)
                print(a[0])
                print(user_list)
                print(user_list.index(a[0]))
                self.close()
        self.success_login()

    def start_cam(self):
        print("start")
        self.working = True
        th = threading.Thread(target=self.setCam)
        th.start()

    def close_cam(self):
        self.working = False

    def success_login(self):
        self.close_cam()
        th = threading.Thread(target=self.start_check)
        th.start()

    def start_check(self):
        self.check =Check()

class Check(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.ui = uic.loadUi("./UI/check.ui")
        self.ui.show()
        self.ui.btn_yes.clicked.connect(self.answer_yes)
        print("check init")

    def answer_yes(self):
        print("yes")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Main()
    sys.exit(app.exec_())
