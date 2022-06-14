import sys
import os
import dlib,cv2,threading
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5 import uic,QtWidgets, QtGui
from keras.models import load_model

load_model = load_model('tl_20_cropped_e20_b200.h5')

class Main(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.ui = uic.loadUi("./UI/main.ui")
        self.ui.show()
        self.ui.btn_login.clicked.connect(self.toLogin)

    def toLogin(self):
        self.ui.hide()
        self.login = Login(self)

    def toMain(self):
        self.ui.show()

class Login(QWidget):
    def __init__(self, main):
        QWidget.__init__(self)
        self.main = main
        self.ui = uic.loadUi("./UI/login.ui")
        self.ui.to_main.clicked.connect(self.close)
        self.ui.cam_on.clicked.connect(self.start_cam)
        self.ui.cam_off.clicked.connect(self.close_cam)
        self.ui.show()
    def close(self):
        self.main.toMain()
        self.ui.hide()

    def setCam(self):
        detector = dlib.get_frontal_face_detector()
        cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        width = cam.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print(round(width), height)
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
                # print(a)
                if np.argmax(a) > 0.9:
                    print(np.argmax(a),"th user")
                    print(a)


            cvt_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, c = cvt_frame.shape
            qImg = QtGui.QImage(cvt_frame.data, w, h, w * c, QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(qImg)
            self.ui.cam.resize(round(width), round(height))
            self.ui.cam.setPixmap(pixmap)
            print("1")

    def start_cam(self):
        print("start")
        self.working = True
        th = threading.Thread(target=self.setCam)
        th.start()

    def close_cam(self):
        self.working = False


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Main()
    sys.exit(app.exec_())
