#!/usr/bin/env python
import Tkinter as tk 

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
		self.grid_location(20,20)
        self.createWidgets()

    def createWidgets(self):
        self.quitButton = tk.Button(self, text='Quit', command=self.quit)
        self.quitButton.grid()

app = Application()
app.master.title('HCR-4 Tester')
app.mainloop()                