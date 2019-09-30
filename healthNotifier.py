import numpy as np
import cv2
import notify2
import math

app_name = 'HealthNotifier'
notify2.init(app_name)
#cap = cv2.VideoCapture(0)
#ret, frame = cap.read()
ret = True
frame = cv2.imread('k.jpg')
if ret:
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
	left_eye_cascade = cv2.CascadeClassifier('haarcascade_left_eye_2splits.xml')
	right_eye_cascade = cv2.CascadeClassifier('haarcascade_right_eye_2splits.xml')
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	if len(faces) == 1:
		left_eye_x = left_eye_y = right_eye_x = right_eye_y = 0
		for (x,y,w,h) in faces:
		    img = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
		    roi_gray = gray[y:y+h, x:x+w]
		    roi_color = frame[y:y+h, x:x+w]
		    left_eye = left_eye_cascade.detectMultiScale(roi_gray, 1.3, 6)
		    right_eye = right_eye_cascade.detectMultiScale(roi_gray, 1.3)

		    for (ex,ey,ew,eh) in left_eye:
		    	left_eye_x = ex + ew / 2
		    	left_eye_y = ey + eh / 2
		    	cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

		    for (ex,ey,ew,eh) in right_eye:
		    	right_eye_x = ex + ew / 2
		    	right_eye_y = ey + eh / 2
		    	cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,0,255),2)

		slope = (right_eye_y - left_eye_y) / (right_eye_x - left_eye_x)
		angle = math.atan(slope)
		print(slope, angle)

	elif len(faces) == 0:
		#check if someone there or not and then notify this
		notification = notify2.Notification(app_name, 'Your current line of sight is not correct for your body')
		notification.show()

#cap.release()

cv2.imshow('img',frame)
cv2.waitKey(0)
cv2.destroyAllWindows()