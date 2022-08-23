import cv2
import time

def motorAngle(x,y,w,h):
    cameraResolution = (640, 480)

    allowedCrownAngle = (44, 140)
    allowedThroatAngle = (80, 170)

    magicNumberX = (allowedCrownAngle[1]-allowedCrownAngle[0]) / cameraResolution[0]
    magicNumberY = (allowedThroatAngle[1]-allowedThroatAngle[0]) / cameraResolution[1] 



    newCrownAngle = (x*magicNumberX)+ allowedCrownAngle[0] + 0.5*w*magicNumberX
    newThroatAngle = (allowedThroatAngle[1]-(y*magicNumberY)) -0.5*h*magicNumberY

    print("New CrownAngle: " + str(newCrownAngle))
    print("New ThroatAngle: " + str(newThroatAngle))

    return newCrownAngle, newThroatAngle

    
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


def face_rec():

    time.sleep(0.5)

    # Load the image from camera
    cap = cv2.VideoCapture(0)

    # display the image
    while True:
        ret, frame = cap.read()

        # get size of the image
        height, width = frame.shape[:2]
        print(width, height) # 640 480

        # JUST FINDING THE COORDINATES OF THE FACE
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # print the coordinates of the face
        print(faces) # [[x, y, w, h]]
        faceX = 0
        faceY = 0
        faceW = 0
        faceH = 0

        for (x,y,w,h) in faces:
            faceX = x
            faceY = y
            faceW = w
            faceH = h

        newC, newT = motorAngle(faceX, faceY, faceW, faceH)


        # for (x,y,w,h) in faces:
        #     cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)
        #     cv2.imshow('frame', frame)
        #     cv2.waitKey(0)
        #     cv2.destroyAllWindows()
        #     break

        return newC, newT

