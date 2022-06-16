import dlib,cv2,threading
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5 import uic,QtGui
from PyQt5.QtCore import QThread,QTimer
import time

class Cam(QThread):
    def __init__(self, p=None):
        QThread.__init__(self,parent=p)
        self.parent = p

    def run(self):
        self.working = False
        cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        width = cam.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
        detector = dlib.get_frontal_face_detector()
        while self.parent.working:
            img, frame = cam.read()
            face = detector(frame)
            for f in face:
                # dlib으로 얼굴 검출
                cv2.rectangle(frame, (f.left() - 21, f.top() - 21), (f.right() + 21, f.bottom() + 21), (0, 0, 255), 1)
            if len(face) == 1:
                # 박스 크기만큼 크롭
                crop = frame[f.top() - 20:f.bottom() + 20, f.left() - 20:f.right() + 20]
                # 사이즈 조정
                crop = cv2.resize(crop, (224, 224))
                # train, validation data 구분
                # if count % 10 < 7:
                #     file_name_path = path_train + '/' + str(train_count) + '.jpg'
                #     file_name_path_gray = path_train_gray + '/' + str(train_count) + '.jpg'
                #     train_count += 1
                # else:
                #     file_name_path = path_test + '/' + str(test_count) + '.jpg'
                #     file_name_path_gray = path_test_gray + '/' + str(test_count) + '.jpg'
                #     test_count += 1
                # #gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)  # 흑백으로도 저장
                # cv2.imwrite(file_name_path, crop)
                # #cv2.imwrite(file_name_path_gray, gray)
                # count += 1
            cvt_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, c = cvt_frame.shape
            qImg = QtGui.QImage(cvt_frame.data, w, h, w * c, QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(qImg)
            self.parent.ui.label.move(130,100)
            self.parent.ui.label.resize(round(width), round(height))
            self.parent.ui.label.setPixmap(pixmap)

class Take_pic(QWidget):
    def __init__(self, main):
        QWidget.__init__(self)
        self.ui = uic.loadUi("./UI/register_pic.ui")
        self.ui.show()
        self.flow=0
        self.cnt = 0
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.sequence)
        self.start_cam()
        self.start_count()

    def start_cam(self):
        self.working = True
        self.worker = Cam(self)
        #self.worker.finished.connect(self.start_check)
        self.worker.start()

    def close_cam(self):
        self.working = False

    def start_count(self):
        self.timer.start()
        self.ask =True

    def sequence(self):
        if(self.ask):
            if(self.flow==0):
                self.ui.name.setText("정면을 봐 주세요.")
                self.ask = False
            elif(self.flow==1):
                self.ui.name.setText("이제 왼쪽을 봐 주세요")
                self.ask = False
            elif(self.flow==2):
                self.ui.name.setText("이제 오른쪽을 봐 주세요")
                self.ask = False
            elif (self.flow == 3):
                self.ui.name.setText("위쪽을 봐 주세요")
                self.ask = False
            elif (self.flow == 4):
                self.ui.name.setText("아래쪽을 봐 주세요")
                self.ask = False
            elif (self.flow == 5):
                self.ui.name.setText("웃어주세요")
                self.ask = False
            elif (self.flow == 6):
                self.ui.name.setText("아~")
                self.ask = False
            elif (self.flow == 7):
                self.ui.name.setText("에~")
                self.ask = False
            elif (self.flow == 8):
                self.ui.name.setText("이~")
                self.ask = False
            elif (self.flow == 9):
                self.ui.name.setText("오~")
                self.ask = False
            elif (self.flow == 10):
                self.ui.name.setText("우~")
                self.ask = False
            else:
                self.ui.name.setText("촬영이 종료되었습니다.")
                self.ask = False
                self.timer.stop()
                self.close_cam()
        else:
            if(self.cnt == 0):
                self.ui.name.setText("3")
                self.cnt +=1
            elif(self.cnt == 1):
                self.ui.name.setText("2")
                self.cnt += 1
            elif(self.cnt == 2):
                self.ui.name.setText("1")
                self.cnt += 1
            elif(self.cnt == 3):
                self.cnt+=1
            elif(self.cnt == 4):
                self.cnt = 0
                self.flow += 1
                self.ask = True
