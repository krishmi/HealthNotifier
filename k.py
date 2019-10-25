import cv2
import numpy as np

cap = cv2.VideoCapture(0)
ret, cimg = cap.read()
img = cv2.cvtColor(cimg,cv2.COLOR_BGR2GRAY)
img = cv2.medianBlur(img,5)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
faces = face_cascade.detectMultiScale(img, 1.3, 5)
if len(faces) == 1:
    #frame = increase_brightness(frame, 20)
    left_eye_x = left_eye_y = right_eye_x = right_eye_y = 0
    (x,y,w,h) = faces[0]
    img = cv2.rectangle(cimg,(x,y),(x+w,y+h),(255,0,0),2)
    roi_gray = img[y:y+h, x:x+w]
    roi_color = cimg[y:y+h, x:x+w]
    eyes = eye_cascade.detectMultiScale(roi_gray, 1.3, 6)

    circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=0,maxRadius=0)

    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        # draw the outer circle
        cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
        cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

    cv2.imshow('detected circles',cimg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()