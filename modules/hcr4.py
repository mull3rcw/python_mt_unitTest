#! python

import time, datetime

import Tkinter

from serial_cm import ser_Init, get_ser, log
from smart_card import isCardPresent, getEnvData
from solenoid import card_bay_locked, card_bay_open, card_bay_init, power_off

#Time delay when possible reboot detected.
wait_time = 30

##################################################
#Main Code Here
##################################################

if __name__=='__main__':
	
	while True:
		isCardP=[-1, -1]
		run = 1
		count = 0
##############USER DEFINED##############			
##Overwrite Log location	
		my_path = 'C:\MagTek\HCR-4\\fcc_log\\'
		my_name = 'fcc_test'
##############USER DEFINED##############				
		
		log = ser_Init(my_path, my_name)
		#log = set_log_info(my_path, my_name)
		card_bay_init()

		while run:
			for i in range(0,2):
				x = isCardPresent(i)
				# if -1, then it failed to read (maybe reset).
				if(x < 0):
					count+=1
					#if 5 failed reads in a row, the system may have reset.
					if count > 5:
						print ("Reading stopped, Reboot suspected")
						get_ser().close()
						run = 0
						break
				else:	
					#Get Transition Change
					count = 0
					if isCardP[i] != x:
						isCardP[i] = x
						ts = time.time()
						st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
						if isCardP[i] == True:
							if i == 1:
								card_bay_locked() #plunger is pulled
								print "%s Card %d Present & Locked" % (st, i)
								log.info("%s Card %d Present & Locked" % (st, i))
							else:
								print "%s Card %d Present" % (st, i)
								log.info("%s Card %d Present" % (st, i))
							emv_data = getEnvData(i)
							print ("%s Card %d ATR %s" % (st, i, emv_data))
							log.info("%s Card %d ATR %s" % (st, i, emv_data))
							#Print ASCII, if data is available
							if "No EMV Support" not in str(emv_data):
								characters = emv_data.replace(' ', '')
								print "%s Card %d ATR string %s" % (st, i, characters.decode('hex'))
							if i == 1:
								card_bay_open() #Plunger goes forward
								print "%s Card %d Bay opened, Remove Card Quickly!!" % (st, i)
								log.info("%s Card %d Bay opened, Remove Card Quickly!!" % (st, i))
						else:
							print "%s Card %d Removed" % (st, i)
							log.info("%s Card %d Removed" % (st, i))
