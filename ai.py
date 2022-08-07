import cv2

# Load the image from camera
cap = cv2.VideoCapture(0)

# display the image
while True:
    ret, frame = cap.read()

    # get size of the image
    height, width = frame.shape[:2]
    print(width, height) # 640 480

    # JUST FINDING THE COORDINATES OF THE FACE
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # print the coordinates of the face
    print(faces) # [[x, y, w, h]]

    for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)
        cv2.imshow('frame', frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        break



    # # ANOTHER OPTION...
    # # seperate the image into squares
    # for i in range(0, width, 100): # change the 100 according to the size of the image
    #     for j in range(0, height, 100):
    #         # get the square
    #         square = frame[j:j+100, i:i+100]

    #         # TODO: see if there is a face in this frame

    #         # display the square
    #         cv2.imshow("Square", square)
    #         cv2.waitKey(0)
    #         cv2.destroyAllWindows()
