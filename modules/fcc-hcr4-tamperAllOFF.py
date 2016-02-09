#!/usr/bin/python

import usb.core
import usb.util
import sys
import logging
import time, datetime
import os

from serial_cm import ser_Init, get_ser, set_log_info, uart_self_test, serial_close, log
from smart_card import isCardPresent, getEnvData
from ping import find_ip_addr, can_addr_ping
from sec_mon_hcr4 import read_tamper_count, read_rtc_count, set_tamper_trigger, check_secdiag



#Time delay when possible reboot detected.
wait_time = 30

##################################################
#Main Code Here
##################################################
if __name__=='__main__':

##############USER DEFINED##################################################################################			
	##Overwrite Log location	
	my_path = '..\\fcc_log\\'
	my_name = 'fcc_test'
	tamper_flag = '0' 	# 0-OFF, f-tamper 0,1,2,3 active, 3f-All Tampers and Latches (not this test) Active and triggered
							# 1 - Tamper1 armed
							# 2 - Tamper2 armed
							# 3 - Tampers 1&2 armed
							# 4 - Tamper3 armed
							# ... binary flag to enable each tamper.
##############USER DEFINED##################################################################################


##One time setup
	log = set_log_info(my_path, my_name)


	
	while True:
		isCardP=[-1, -1]
		run 			= 1
		count 			= 0
########Passing Counters########
		ethernet_count 	= 0
		uart_count 		= 0
		usb_count 		= 0
		smart_card_count 	= 0
		tamper_count 	= 0
		rtc_stamp 	= 0
		total_count 	= 0
		MAX_COM_RETRY	= 5	
################################		
	

##############INIT #################					
		prev_dev = "Not Init"
		ser_Init()
		#Requires Serial init
		hostname = find_ip_addr('eth0')
		set_tamper_trigger(tamper_flag)
##############INIT END##############		
		log.info('Start FCC Test')
		log.info('Test :\n UART, Ethernet, USB, SmartCard')

		while run:
			#Total Test Cycles
			#log.info( "\n")
			total_count+=1
			log.debug( "Total Test Cycles = %d", total_count)
			
			#Ethernet Test:###########################################################
			###Find HCR-4 IP Address####
			if hostname != -1:
				ret = can_addr_ping(hostname)
				if ret == True:
					ethernet_count+=1
					
			log.info( "Ethernet Count = \t\t%d of %d", ethernet_count, total_count)
			#Ethernet Test end:#######################################################
			
			#UART:####################################################################
			ret = uart_self_test()
			if ret == False:
				uart_count += 1
			log.info( "UART Count = \t\t\t%d of %d", uart_count, total_count)
			#UART end:################################################################

			#USB:####################################################################
			dev = usb.core.find(idVendor=0x0525, idProduct=0xA4AC) #HCR-4 	
			if dev is None:
				#raise ValueError('Device not found')
				log.error('\t\t\tUSB Device not found')
			elif dev is 'NoneType':
				log.error('\t\t\tUSB Device noneType found')
			elif prev_dev == "Not Init":
				#First time is free
				usb_count += 1
				prev_dev = dev
			else:	
				log.debug( "PREV VENDOR %s" % prev_dev.idVendor)
				log.debug("DEV VENDOR %s" % dev.idVendor)
				if prev_dev.idVendor == dev.idVendor and prev_dev.idProduct == dev.idProduct:
					usb_count += 1
				prev_dev = dev	

			log.info( "USB Count = \t\t\t%d of %d", usb_count, total_count)

			#USB end:################################################################

			#SMARTCARD Test:##########################################################
			#Per Smart Card(2)
			#2 card, clear flag each time
			c_present = 1		#changed 1,2 from 0,2 and c_present as 1, ignoring SAM card.
			for i in range(1,2):
				x = isCardPresent(i)
				time.sleep(1)
				if(x < 0):
					count+=1
					log.error("\t\t\tFailed %d for Card %d", count, i)
					#if 5 failed reads in a row, the system may have reset.
					if count > MAX_COM_RETRY:
						log.error("\t\t\tReading stopped, Reboot restarting script.\n\n\n")
						serial_close()
						
						run = 0
						break
				elif x == 0:
					log.error("\t\t\tcard %d is Missing" % (i))
				elif x == 1:
					#Get ATR
					count = 0
					if x > 0:
						isCardP[i] = x
						ts = time.time()
						st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
						if isCardP[i] == True:
							emv_data = getEnvData(i)
							log.debug("Card %d ATR %s" % (i, emv_data))
							if "No EMV Support" not in str(emv_data):
								characters = emv_data.replace(' ', '')
								log.debug("Card %d ATR string %s" % (i, characters.decode('hex')))
								# check each card ATR
								c_present+=1
								#when both cards pass
								if c_present == 2:
									smart_card_count += 1
						else:
							log.warn( "%s Card %d Removed" % (st, i))
				else:
					log.error("x is %d UNKNOWN") % (x)
			log.info( "SmartCard Count = \t\t%d of %d", smart_card_count, total_count)
			#SMARTCARD Test end:#######################################################
			
			#TAMPER:####################################################################
			ret = read_tamper_count()
			if ret < 0: #Read Failure
				log.error("\t\t\tTAMPER Read Failed")
			elif ret > 0:
				log.warn("TAMPER Found")
			else:	
				tamper_count += 1
			log.info( "TAMPER Count = \t\t%d of %d", tamper_count, total_count)
			
			#RTC
			rtc_stamp = read_rtc_count()
			if rtc_stamp < 0:
				log.error("\t\t\tPossible reset RTC")
                        else:
                                log.info( "last RTC Event = \t\t%d", rtc_stamp)
			if rtc_stamp > 0:
				check_secdiag()
			
			#TAMPER end:################################################################
			log.info("\t\t\t==============================\n")
			
			
