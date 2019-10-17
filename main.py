from tkinter import *
from tkinter import ttk
import os

def callibrate():
	global page
	page.destroy()
	page = ttk.LabelFrame(mainframe)
	page.grid(row=0, column=0, sticky="nwe", padx=15, pady=15)
	term1 = Label(page, text='1. This application assumes that it is being used in a brightly lit up space.',
	 wraplength=500, font=('Arial', 10))
	term1.grid(row=0, pady=5, sticky='e')
	term2 = Label(page, text='2. Next step involves callibration, for proper functioning of the application please do the callibration step minutely.', wraplength=500)
	term2.grid(row=1, pady=5, sticky='e')

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

#welcome page
if not os.path.exists('FirstRun'):
	#open('FirstRun', '+w')
	#close('FirstRun')
	page = ttk.Frame(mainframe)
	page.grid(row=0, column=0, sticky="nwes")
	page.rowconfigure(0, weight=1)
	page.columnconfigure(0, weight=1)
	text = Label(page, text='Welcome to HealthNotifier!!', font=("Helvetica", 16), fg='blue')
	text.grid()
	button = Button(page, text='Next', activebackground='blue', activeforeground='white', bg='green'
		, command=callibrate)
	button.grid(sticky='es')


#root configuration
root.mainloop()