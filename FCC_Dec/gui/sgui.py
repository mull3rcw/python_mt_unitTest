from Tkinter import *
import urllib
import re
import time	

from serial_cm import ser_Init
from serial_cm import log
from smart_card import isCardPresent
from smart_card import getEnvData

		
				
class MyApp(object):
    def __init__(self, parent):
        print "__init__"
		
        self.myParent = parent
        self.myContainer1 = Frame(parent)
        self.myContainer1.pack()
        self.createWidgets()
        #button1 = Button(self.myContainer1, command = self.addStockToTrack)
        button1 = Button(self.myContainer1, command = isCardPresent(1))
        self.myContainer1.bind("<Return>", isCardPresent(1))
        button1.configure(text = "Type in PIN")
        button1.pack()  


    def createWidgets(self):
        print "createWidgets"
        # title name
        root.title("Stock App")
        # creates a frame inside myContainer1
        self.widgetFrame = Frame(self.myContainer1)
        self.widgetFrame.pack()
        # User enters stock symbol here:
        self.symbol = Entry(self.widgetFrame) 
        self.symbol.pack()
        self.symbol.focus_set()

    def addStockToTrack(self):
		print "addStockToTrack"
		s = self.symbol.get()
		labelName = str(s) + "Label"
		self.symbol.delete(0, END)
		stockPrice = get_quote(s)
		self.labelName = Label(self.myContainer1, text = s.upper() + ": " + str(stockPrice))
		self.labelName.pack()
		self.myContainer1.after(5, self.get_quote)
		
    def updateStock(self):
        print "updateStock"
        while True:
            print "updateStock2"
            labelName = str(s) + "Label"
            stockPrice = get_quote(s)
            self.labelName = Label(self.myContainer1, text = s.upper() + ": " + str(stockPrice))
            self.labelName.pack()
            self.after(10, self.updateStock)

def get_quote(symbol):
	print "symbol is:" + symbol
	base_url = 'http://finance.google.com/finance?q='
	content = urllib.urlopen(base_url + symbol).read()
	m = re.search('id="ref_\d*_l".*?>(.*?)<', content)
	if m:
		quote = m.group(1)
	else:
		quote = 'Not found: ' + symbol
	return quote

root = Tk()
ser_Init()
myapp = MyApp(root)
root.mainloop()

