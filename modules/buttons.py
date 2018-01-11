import Tkinter
import tkMessageBox

top = Tkinter.Tk()

def helloCallBack():
	   tkMessageBox.showinfo( "Hello Python", "Hello World")

B = Tkinter.Button(top, text ="Over here in the corner", command = helloCallBack)

B.pack()
top.mainloop()

