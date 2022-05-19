import cv2, dlib



def cam_test():
    detector = dlib.get_frontal_face_detector()
    cam =cv2.VideoCapture(0, cv2.CAP_DSHOW)

    while True:
        img, frame =cam.read()
        face =detector(frame)
        for f in face:
            cv2.rectangle(frame, (f.left(), f.top()), (f.right(), f.bottom()), (0,0,255), 1)

        cv2.imshow('A', frame)

        if cv2.waitKey(1) == 'q':
            cam.release()
            break

def test2():
    print("zzzzzzzz")
