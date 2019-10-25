from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from math import sin, cos, radians
import tkinter
import os
import cv2
import numpy as np
import notify2
import math
import time
import threading

def rotate_image(image, angle):
    if angle == 0: return image
    height, width = image.shape[:2]
    rot_mat = cv2.getRotationMatrix2D((width/2, height/2), angle, 0.9)
    result = cv2.warpAffine(image, rot_mat, (width, height), flags=cv2.INTER_LINEAR)
    return result

def rotate_point(pos, img, angle):
    if angle == 0: return pos
    x = pos[0] - img.shape[1]*0.4
    y = pos[1] - img.shape[0]*0.4
    newx = x*cos(radians(angle)) + y*sin(radians(angle)) + img.shape[1]*0.4
    newy = -x*sin(radians(angle)) + y*cos(radians(angle)) + img.shape[0]*0.4
    return int(newx), int(newy), pos[2], pos[3]

def notifier(cap):
	app_name = 'HealthNotifier'
	notify2.init(app_name)
	global flag
	flag = True

	while flag:
		ret, frame = cap.read()
		if ret:
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')
			for angle in [0, -25, 25]:
				rimg = rotate_image(frame, angle)
				faces = face_cascade.detectMultiScale(rimg, 1.3, 5)
				if len(faces):
					faces = [rotate_point(faces[-1], frame, -angle)]
					break

			if len(faces) == 1:
				if angle == 25:
					notification = notify2.Notification(app_name, 'Your head is tilted to the left')
					notification.show()
				elif angle == -25:
					notification = notify2.Notification(app_name, 'Your head is tilted to the right')
					notification.show()
				else:
					with open('FirstRun', 'r') as f:
						specs = f.read()
						top_distance = float(specs)
						(x, y, w, h) = faces[0]
						if y > top_distance + 20:
							notification = notify2.Notification(app_name, 'Your body is slouching')
							notification.show()

		t_end = time.time() + 5
		while time.time() < t_end and flag:
			ret, frame = cap.read()

	cap.release()
	root.quit()

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
		index = 3
	elif index == 3:
		if dir == -1:
			index = 2
		else:
			index = 4
	elif index == 4:
		if finish.get() == 'Finish':
			finish.set('Stop Notifier')
			thread = threading.Thread(target=notifier, args=[cap])
			thread.start()
		else:
			global flag
			flag = False

	if not ind == 4:
		frames[ind].grid_forget()
		frames[index].grid(sticky='news')
	if index == 2:	
		show_frame(cap, frames[index].winfo_children()[0])
	elif index == 3:
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
		bg='green', command=changeFrame, relief=RAISED).grid(sticky='es', padx=5, pady=5)
	frames.append(page)

	#frame 1
	page = ttk.Frame(mainframe)
	page.rowconfigure(0, weight=2)
	page.rowconfigure(1, weight=2)
	page.columnconfigure(0, weight=1)
	labelFrame = ttk.LabelFrame(page, text='Guidelines:', borderwidth=5, relief=SUNKEN)
	labelFrame.grid(sticky='e')
	Label(labelFrame, text='1. This application assumes that it is being used in a brightly lit up space.',
	 wraplength=450).grid(pady=10, sticky='w')
	Label(labelFrame, text='2. Next step involves callibration, so please sit in front of webcam in your preferred posture which you will consider healthy for your body',
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
	page.columnconfigure(0, weight=1)
	Label(page).grid()
	Button(page, text='Take snapshot', bg='blue', relief=RAISED, 
		command=changeFrame).grid(padx=5, pady=5)
	frames.append(page)

	#frame 3
	page = ttk.Frame(mainframe)
	page.rowconfigure(0, weight=1)
	page.columnconfigure(0, weight=1)
	Label(page).grid(columnspan=2)
	Button(page, text='Accept', bg='green', relief=RAISED,
		command=lambda: changeFrame(1)).grid(row=1, column=1, sticky='es', padx=5, pady=5)
	Button(page, text='Discard', bg='green', relief=RAISED,
		command=lambda: changeFrame(-1)).grid(row=1, column=0, sticky='es', padx=5, pady=5)
	frames.append(page)

	#frame 4
	page = ttk.Frame(mainframe)
	page.rowconfigure(0, weight=1)
	page.columnconfigure(0, weight=1)
	Label(page, text='HealthNotifier is all setup to\n keep your body posture perfect :)',
		font=("Helvetica", 16), fg='blue').grid()
	global finish
	finish = StringVar()
	finish.set('Finish')
	Button(page, textvariable=finish, activebackground='blue', activeforeground='white', 
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
				with open('FirstRun', 'w') as f:
					f.write(str(float(y)))
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
	if tkinter.messagebox.askokcancel("Quit", "You want to quit now?"):
		cap.release()
		root.quit()


id = 0
index = 0
cap = None
focal_length = 0
pixels = 0

frames = []
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 550)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)
for i in range(30):
	cap.read()
	
defineFrames(frames)