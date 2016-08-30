#! python


from Tkinter import *
import time, datetime

import Tkinter

from serial_cm import ser_Init
from serial_cm import log
from smart_card import isCardPresent
from smart_card import getEnvData



root = Tk()
def hello(event): print 'Got tag event'



def InitShowText(mytext):
	text = Text()
	text.config(font=('courier', 15, 'normal'))                 
	text.config(width=20, height=12)
	text.pack(expand=YES, fill=BOTH)
	text.insert(END, mytext+'\n')  
	
	text.tag_add('demo', '1.5', '1.7')                      
	text.tag_add('demo', '3.0', '3.3')                      
	text.tag_add('demo', '5.3', '5.7')                      
	text.tag_bind('demo', '<Double-1>', hello)              
	root.mainloop()




##################################################
#Main Code Here
##################################################

if __name__=='__main__':
	
	while True:
		isCardP=[-1, -1]
		run = 1
		count = 0
		
		InitShowText("Insert Card Please")
		ser_Init()
		

		while run:
			time.sleep(1)
			ts = time.time()
	
			for i in range(0,2):
				x = isCardPresent(i)
				# if -1, then it failed to read (maybe reset).
				if(x < 0):
					count+=1
					#if 5 failed reads in a row, the system may have reset.
					if count > 5:
						print ("Wait 60 seconds, maybe rebooted")
						time.sleep(60)
						run = 0
				else:	
					#Get Transition Change
					count = 0
					if isCardP[i] != x:
						isCardP[i] = x
						st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
						if isCardP[i] == True:
							print "%s Card %d Present" % (st, i)
							log.info("%s Card %d Present" % (st, i))
							emv_data = getEnvData(i)
							print emv_data
							log.info(emv_data)
						else:
							print "%s Card %d Removed" % (st, i)
							log.info("%s Card %d Removed" % (st, i))
		
		
		

	 
