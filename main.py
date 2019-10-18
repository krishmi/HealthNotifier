from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import os
import cv2

def changeFrame(dir = 0):
	global index
	global cap
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
			index = 3
	elif index == 3:
		index = 4
	elif index == 4:
		if dir == -1:
			index = 3
		else:
			index = 5
	elif index == 5:
		cap.release()
		#os.system('python healthNotifier.py')

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
			cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
			img = Image.fromarray(cv2image)
			imgtk = ImageTk.PhotoImage(image=img)
			lmain.imgtk = imgtk
			lmain.configure(image=imgtk)

#installer
if not os.path.exists('FirstRun'):
	#file = open('FirstRun', '+w')
	#file.close()
	frames = []
	id = 0
	index = 0
	cap = None
	defineFrames(frames)
	
else:
	os.system('python healthNotifier.py')