#!/usr/bin/python

import usb.core
import usb.core
import usb.util
import sys

import time, datetime
import Tkinter
import os
import usb.core

from serial_cm import ser_Init, get_ser, log, set_log_info
from smart_card import isCardPresent, getEnvData
from solenoid import card_bay_locked, card_bay_open, card_bay_init, power_off

import logging

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
		#Passing Counters
		ethernet_count = 0
		uart_count = 0
		usb_count = 0
		smart_card_count = 0
		total_count = 0
		prev_dev = "Not Init"
		
		dev = usb.core.find(idVendor=0x0525, idProduct=0xA4AC) #HCR-4 
		dev = usb.core.find()
		prev_dev = dev
##############USER DEFINED##############			
##Overwrite Log location	
		my_path = 'C:\MagTek\HCR-4\\fcc_log\\'
		my_name = 'fcc_test'
##############USER DEFINED##############				
		log = ser_Init(my_path, my_name)
		#log = set_log_info(my_path, my_name)

		card_bay_init()
		
		log.info('Start FCC Test')
		log.info('Test :\n UART, Ethernet, USB, SmartCard')

		while run:
			#Total Test Cycles
			log.info( "\n")
			print( "\n")
			total_count+=1
			log.debug( "Total Test Cycles = %d", total_count)
			
			#Ethernet Test:###########################################################
			temp_f = "temp.txt"
			hcr_4_hostname = "10.57.10.169"

			response = os.system('ping -n 1 %s > temp.txt' % hcr_4_hostname)
			txt = open(temp_f)
			out = txt.readlines()
			if "Lost = 0" in str(out):
				ethernet_count+=1
			txt.close()			
			response = os.remove('temp.txt')
			log.info( "Ethernet Count = \t\t%d of %d", ethernet_count, total_count)
			print 'Ethernet Count = \t\t%d of %d' % (ethernet_count, total_count)
			#Ethernet Test end:#######################################################
			
			#UART:####################################################################
			uart_count += 1
			log.info( "UART Count = \t\t\t%d of %d", uart_count, total_count)
			print 'UART Count = \t\t\t%d of %d' % (uart_count, total_count)
			#UART end:################################################################

			#USB:####################################################################
			
			if dev is None:
				raise ValueError('Device not found')
			else:
				if prev_dev.idVendor == dev.idVendor: # and prev_dev.idProduct == dev.idProduct:
					usb_count += 1
			log.info( "USB Count = \t\t\t%d of %d", usb_count, total_count)
			print 'USB Count = \t\t\t%d of %d' % (usb_count, total_count)
			#USB end:################################################################

			
			#SMARTCARD Test:##########################################################
			#Per Smart Card(2)
			for i in range(0,2):
				x = isCardPresent(i)
				# if -1, then it failed to read (maybe reset).
				time.sleep(1)
				if(x < 0):
					count+=1
					#if 5 failed reads in a row, the system may have reset.
					if count > 5:
						log.error("Reading stopped, Reboot suspected")
						get_ser().close()
						run = 0
						break
				else:	
					#Get ATR
					count = 0
					if x > 0:
						isCardP[i] = x
						ts = time.time()
						st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
						if isCardP[i] == True:
							emv_data = getEnvData(i)
							log.debug("Card %d ATR %s" % (i, emv_data))
							#Print ASCII, if data is available
							if "No EMV Support" not in str(emv_data):
								characters = emv_data.replace(' ', '')
								log.debug("Card %d ATR string %s" % (i, characters.decode('hex')))
								smart_card_count += 1
								log.info( "SmartCard Count = \t%d of %d", smart_card_count, total_count)
								print 'SmartCard Count = \t\t%d of %d' % (smart_card_count, total_count)
						else:
							log.info( "%s Card %d Removed" % (st, i))

			#SMARTCARD Test end:#######################################################
			
