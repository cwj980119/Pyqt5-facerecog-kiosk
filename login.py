import dlib,cv2
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5 import uic,QtWidgets, QtGui
from PyQt5.QtCore import QThread
from keras.models import load_model
import pymysql
import check_login

def connectDB():
    host="database-1.cb5pctivsgrb.us-east-1.rds.amazonaws.com"
    username="root"
    port=3306
    database="log-in"
    password="ksc2021583"

    conn=pymysql.connect(host=host,user=username,password=password,db=database,port=port)
    return(conn)

load_model = load_model('tl_20_cropped_e20_b200.h5')


class Thread(QThread):
    def __init__(self, p=None):
        QThread.__init__(self,parent=p)
        self.parent = p

    def run(self):
        self.working = False
        detector = dlib.get_frontal_face_detector()
        cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        width = cam.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print(round(width), height)
        count = 0
        user_list = np.empty(shape=self.parent.user_num)
        self.l = [0 for i in range(4)]
        print(self.parent.working)
        while self.parent.working:
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
                print(type(a[0]))
                # print(a[0][np.argmax(a)])
                if a[0][np.argmax(a)] > 0.9:
                    count += 1
                    user_list += a[0]
                    print(user_list)
                    # print(np.argmax(a),"th user")
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
            self.parent.ui.cam.resize(round(width), round(height))
            self.parent.ui.cam.setPixmap(pixmap)
            if count > 20:
                a = np.sort(user_list)[::-1]
                for i in range(4):
                    self.l[i] = np.where(user_list==a[i])[0][0]
                self.parent.close_cam()
                self.quit()
                self.working = True
                return
        self.working =False


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

    def start_cam(self):
        self.working = True
        self.worker = Thread(self)
        self.worker.finished.connect(self.start_check)
        self.worker.start()

    def close_cam(self):
        self.working = False

    def start_check(self):
        if(self.worker.working):
            self.predict_list = []
            sql = "select * from userdata where memberID =" + str(self.worker.l[0]+1)
            self.curs.execute(sql)
            self.predict_list.append(self.curs.fetchone())
            sql = "select * from userdata where memberID in ("+str(self.worker.l[1]+1)+"," + str(self.worker.l[2]+1)+"," + str(self.worker.l[3]+1)+")"
            self.curs.execute(sql)
            self.predict_list.append(self.curs.fetchall())
            print(self.predict_list)
            self.check =check_login.Check(self.predict_list, self)

    def succ(self, user):
        self.close()
        self.main.toMenu(user)
