from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import tkinter
import os
import cv2
import numpy as np
import notify2
import math

def notifier():
	app_name = 'HealthNotifier'
	notify2.init(app_name)
	cap = cv2.VideoCapture(0)
	ret, frame = cap.read()
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

			if angle > 20:
				notification = notify2.Notification(app_name, 'Your head is tilted to the left')
				notification.show()
			elif angle < -20:
				notification = notify2.Notification(app_name, 'Your head is tilted to the right')
				notification.show()

			with open('FirstRun', 'r') as f:
				specs = f.readlines()
				focal_length = float(specs[0])
				width = float(specs[1])
				original_distance = float(specs[2])
				distance = width * focal_length / w
				print(original_distance, distance)
				//notify accordingly

	#cap.release()
	cap.release()
	cv2.imshow('img',frame)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

def changeFrame(dir = 0):
	global index
	global cap
	global root
	ind = index
	if index == 0:
		index = 1
	elif index == 1:
		if dir == -1:
			index = 0
		else:
			index = 2
	elif index == 2:
		if dir == -1:
			index = 1
		else:
			try:
				var = int(distance_str.get()) / int(width_str.get())
			except:
				tkinter.messagebox.showerror('Error', 'Value of width and distance must be non zero number')
				return
			index = 3
	elif index == 3:
		index = 4
	elif index == 4:
		if dir == -1:
			index = 3
		else:
			focal_length = pixels * float(distance_str.get()) / float(width_str.get())
			with open('FirstRun', 'w') as f:
				f.write(str(focal_length))
				f.write('\n')
				f.write(str(float(width_str.get())))
				f.write('\n')
				f.write(str(float(distance_str.get())))
				f.write('\n')
			index = 5
	elif index == 5:
		cap.release()
		root.quit()

	if not ind == 5:
		frames[ind].grid_forget()
		frames[index].grid(sticky='news')
	if index == 3:
		if cap == None:
			cap = cv2.VideoCapture(0)
			cap.set(cv2.CAP_PROP_FRAME_WIDTH, 550)
			cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)
		show_frame(cap, frames[index].winfo_children()[0])
	elif index == 4:
		takeSnap(frames[index].winfo_children()[0])

def defineFrames(frames):
	#root
	global root
	root = Tk()
	root.title('HealthNotifier')
	root.resizable(0, 0)
	root.geometry("%dx%d%+d%+d" % (550, 400, 450, 150))
	root.rowconfigure(0, weight=1)
	root.columnconfigure(0, weight=1)

	#main
	mainframe = ttk.Frame(root)
	mainframe.grid(row=0, column=0, sticky="nwes")
	mainframe.rowconfigure(0, weight=1)
	mainframe.columnconfigure(0, weight=1)

	#frame 0
	page = ttk.Frame(mainframe)
	page.rowconfigure(0, weight=1)
	page.columnconfigure(0, weight=1)
	Label(page, text='Welcome to HealthNotifier!!', font=("Helvetica", 16), fg='blue').grid()
	Button(page, text='Next', activebackground='blue', activeforeground='white', 
		bg='green', command=changeFrame).grid(sticky='es')
	frames.append(page)

	#frame 1
	page = ttk.Frame(mainframe)
	page.rowconfigure(0, weight=2)
	page.rowconfigure(1, weight=2)
	page.columnconfigure(0, weight=1)
	labelFrame = ttk.LabelFrame(page, text='Terms & Conditions:', borderwidth=5, relief=SUNKEN)
	labelFrame.grid(sticky='e')
	Label(labelFrame, text='1. This application assumes that it is being used in a brightly lit up space.',
	 wraplength=450).grid(pady=10, sticky='w')
	Label(labelFrame, text='2. Next step involves callibration, for proper functioning of the application please do the callibration step minutely.',
	 wraplength=450).grid(pady=10, sticky='w')
	global flag 
	flag = IntVar(0)
	next = Button(page, text='Next', bg='gray', relief=RAISED, state=DISABLED,
		command= lambda: changeFrame(1))
	checkbox = Checkbutton(page, variable=flag, text='I agree', 
		command=lambda: checkAgreement(flag, next)).grid(sticky='n')
	next.grid(row=2, column=1, sticky='es', padx=5, pady=5)
	Button(page, text='Back', bg='green', relief=RAISED,
		command= lambda: changeFrame(-1)).grid(row=2, column=0, sticky='es', padx=5, pady=5)
	frames.append(page)

	#frame 2
	page = ttk.Frame(mainframe)
	page.rowconfigure(0, weight=2)
	page.rowconfigure(1, weight=2)
	page.columnconfigure(0, weight=1)
	labelFrame = ttk.LabelFrame(page, text='Width of object')
	Label(labelFrame, text='Enter the width of the object whose snapshot is to be taken', wraplength=450).grid(
		row=0, column=0, pady=10, padx=10, sticky='w')
	global width_str, distance_str
	width_str = StringVar()
	Entry(labelFrame, textvariable=width_str).grid(row=1, column=0, padx=10, pady=10, rowspan=2, sticky='w')
	labelFrame.grid(sticky="nw", padx=15, pady=10)
	labelFrame = ttk.LabelFrame(page, text='Distance of object')
	Label(labelFrame, text='Enter the distance of the object from webcam', wraplength=450).grid(
		pady=10, padx=10, sticky='w')
	distance_str = StringVar()
	Entry(labelFrame, textvariable=distance_str).grid(padx=10, pady=10, sticky='w')
	labelFrame.grid(sticky="nw", padx=15, pady=10)
	Button(page, text='Next', bg='green', relief=RAISED, 
		command=lambda: changeFrame(1)).grid(row=2, column=1, sticky='es', padx=5, pady=5)
	Button(page, text='Back', bg='green', relief=RAISED,
		command=lambda: changeFrame(-1)).grid(row=2, column=0, sticky='es', padx=5, pady=5)
	frames.append(page)

	#frame 3
	page = ttk.Frame(mainframe)
	page.columnconfigure(0, weight=1)
	Label(page).grid()
	Button(page, text='Take snapshot', bg='blue', relief=RAISED, 
		command=changeFrame).grid(padx=5, pady=5)
	frames.append(page)

	#frame 4
	page = ttk.Frame(mainframe)
	page.rowconfigure(0, weight=1)
	page.columnconfigure(0, weight=1)
	Label(page).grid(columnspan=2)
	Button(page, text='Accept', bg='green', relief=RAISED,
		command=lambda: changeFrame(1)).grid(row=1, column=1, sticky='es', padx=5, pady=5)
	Button(page, text='Discard', bg='green', relief=RAISED,
		command=lambda: changeFrame(-1)).grid(row=1, column=0, sticky='es', padx=5, pady=5)
	frames.append(page)

	#frame 5
	page = ttk.Frame(mainframe)
	page.rowconfigure(0, weight=1)
	page.columnconfigure(0, weight=1)
	Label(page, text='HealthNotifier is all setup to\n keep your body posture perfect :)',
		font=("Helvetica", 16), fg='blue').grid()
	Button(page, text='Finish', activebackground='blue', activeforeground='white', 
		bg='green', command=changeFrame).grid(sticky='es')
	frames.append(page)
	
	frames[0].grid(sticky='news')
	root.protocol("WM_DELETE_WINDOW", ask_quit)
	root.mainloop()


def checkAgreement(flag, next):
	if flag.get():
		next.config(bg='green')
		next.config(state=NORMAL)
	else:
		next.config(bg='gray')
		next.config(state=DISABLED)

def show_frame(cap, lmain):
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    global id
    id = lmain.after(10, lambda: show_frame(cap, lmain))

def takeSnap(lmain):
	ret = False
	while not ret:
		global cap
		ret, frame = cap.read()
		if ret:
			global id
			lmain.after_cancel(id)
			frame = cv2.flip(frame, 1)
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
			faces = face_cascade.detectMultiScale(gray, 1.3, 5)
			if len(faces) == 1:
				(x,y,w,h) = faces[0]
				global pixels
				pixels = w
			else:
				tkinter.messagebox.showerror('Error', 'Error in detecting face!')
				changeFrame(-1)
				return

			cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
			img = Image.fromarray(cv2image)
			imgtk = ImageTk.PhotoImage(image=img)
			lmain.imgtk = imgtk
			lmain.configure(image=imgtk)

def ask_quit():
	if not index == 5:
		os.remove('FirstRun')

	if tkinter.messagebox.askokcancel("Quit", "You want to quit now?"):
		root.quit()


id = 0
index = 0
cap = None
focal_length = 0
pixels = 0

#installer
if not os.path.exists('FirstRun'):
	file = open('FirstRun', '+w')
	file.close()
	frames = []
	defineFrames(frames)
	
else:
	notifier()