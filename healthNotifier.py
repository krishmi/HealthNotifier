import numpy as np
import cv2
import notify2
import math

app_name = 'HealthNotifier'
notify2.init(app_name)
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
ret = True
#frame = cv2.imread('k.jpg')
if ret:
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
	eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	if len(faces) == 1:
		left_eye_x = left_eye_y = right_eye_x = right_eye_y = 0
		(x,y,w,h) = faces[0]
		img = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
		roi_gray = gray[y:y+h, x:x+w]
		roi_color = frame[y:y+h, x:x+w]
		eyes = eye_cascade.detectMultiScale(roi_gray, 1.3, 6)

		if len(eyes) > 1:
			(ex,ey,ew,eh) = eyes[0]
			left_eye_x = ex + ew / 2
			left_eye_y = ey + eh / 2
			cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

			(ex,ey,ew,eh) = eyes[1]
			right_eye_x = ex + ew / 2
			right_eye_y = ey + eh / 2
			cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,0,255),2)

		if right_eye_x - left_eye_x != 0:
			slope = (right_eye_y - left_eye_y) / (right_eye_x - left_eye_x)
			angle = math.atan(slope) * 180 / math.pi
		else:
			angle = 0

		print(angle)

		if angle > 20:
			notification = notify2.Notification(app_name, 'Your head is tilted to the left')
			notification.show()
		elif angle < -20:
			notification = notify2.Notification(app_name, 'Your head is tilted to the right')
			notification.show()

		distance = math.sqrt(y*y + w*w)
		measured_distance = 250
		tolerance = .05

		print(distance)

		if distance < tolerance*measured_distance or distance > tolerance*measured_distance:
			notification = notify2.Notification(app_name, 'Your body is slouching')
			notification.show()			

	elif len(faces) == 0:
		#check if someone there or not and then notify this
		notification = notify2.Notification(app_name, 'Your current posture is not good for your body')
		notification.show()

#cap.release()

cv2.imshow('img',frame)
cv2.waitKey(0)
cv2.destroyAllWindows()