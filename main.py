from tkinter import *
from tkinter import ttk
import os

def checkAgreement():
	if flag.get():
		next.config(bg='green')
		next.config(state=NORMAL)
	else:
		next.config(bg='gray')
		next.config(state=DISABLED)


#installer
if not os.path.exists('FirstRun'):
	#open('FirstRun', '+w')
	#close('FirstRun')

	#root
	root = Tk()
	root.title('HealthNotifier')
	root.resizable(0, 0)
	root.geometry("%dx%d%+d%+d" % (550, 400, 450, 150))
	root.rowconfigure(0, weight=1)
	root.columnconfigure(0, weight=1)
	#root.bind("<KeyPress>", keydown)

	#main
	mainframe = ttk.Frame(root)
	mainframe.grid(row=0, column=0, sticky="nwes")
	mainframe.rowconfigure(0, weight=1)
	mainframe.columnconfigure(0, weight=1)

	#frames
	frames = []

	#frame 0
	page = ttk.Frame(mainframe)
	page.rowconfigure(0, weight=1)
	page.columnconfigure(0, weight=1)
	text = Label(page, text='Welcome to HealthNotifier!!', font=("Helvetica", 16), fg='blue')
	text.grid()
	next = Button(page, text='Next', activebackground='blue', activeforeground='white', bg='green')
	next.grid(sticky='es')
	frames.append(page)

	#frame 1
	page = ttk.Frame(mainframe)
	page.rowconfigure(0, weight=2)
	page.columnconfigure(0, weight=1)
	page.rowconfigure(1, weight=2)
	page.columnconfigure(0, weight=1)
	page.rowconfigure(1, weight=1)
	page.columnconfigure(0, weight=1)
	labelFrame = ttk.LabelFrame(page, text='Terms & Conditions:', borderwidth=5, relief=SUNKEN)
	labelFrame.grid(sticky='e')
	term1 = Label(labelFrame, text='1. This application assumes that it is being used in a brightly lit up space.',
	 wraplength=450)
	term1.grid(row=0, pady=10, sticky='w')
	term2 = Label(labelFrame, text='2. Next step involves callibration, for proper functioning of the application please do the callibration step minutely.',
	 wraplength=450)
	term2.grid(row=1, pady=10, sticky='w')
	flag = IntVar(0)
	checkbox = Checkbutton(page, variable=flag, text='I agree', command=checkAgreement)
	checkbox.grid(sticky='n')
	next = Button(page, text='Next', bg='gray', relief=RAISED, state=DISABLED)
	next.grid(row=2, column=1, sticky='es', padx=5, pady=5)
	back = Button(page, text='Back', bg='green', relief=RAISED)
	back.grid(row=2, column=0, sticky='es', padx=5, pady=5)
	frames.append(page)

	#frame 2
	page = ttk.Frame(mainframe)
	frames.append(page)

	frames[2].grid(row=0, column=0, sticky="nwes")

	#root configuration
	root.mainloop()