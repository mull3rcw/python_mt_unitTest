#!/usr/bin/python

import usb.core
import usb.util
import sys
import logging
import time, datetime
import os


from serial_cm import ser_Init, get_ser, log, set_log_info, uart_self_test
from smart_card import isCardPresent, getEnvData
from ping import find_ip_addr, can_addr_ping
from sec_mon_hcr4 import read_tamper_count, read_rtc_count, set_tamper_trigger, check_secdiag



#Time delay when possible reboot detected.
wait_time = 30

##################################################
#Main Code Here
##################################################
if __name__=='__main__':
	
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
################################		
	
##############USER DEFINED##################################################################################			
	##Overwrite Log location	
		my_path = '..\\fcc_log\\'
		my_name = 'fcc_test'
		tamper_flag = '0' 	# 0-OFF, f-tamper 0,1,2,3 active, 3f-All Tampers Active and triggered
							# 1 - Tamper1 armed
							# 2 - Tamper2 armed
							# 3 - Tampers 1&2 armed
							# 4 - Tamper3 armed
							# ... binary flag to enable each tamper.
		
##############USER DEFINED##################################################################################

##############INIT #################					
		prev_dev = "Not Init"
		log = ser_Init(my_path, my_name)
		#Requires Serial init
		hostname = find_ip_addr('eth0')
		set_tamper_trigger(tamper_flag)
##############INIT END##############		
		log.info('Start FCC Test')
		log.info('Test :\n UART, Ethernet, USB, SmartCard')

		while run:
			#Total Test Cycles
			#log.info( "\n")
			#print( "\n")
			total_count+=1
			log.debug( "Total Test Cycles = %d", total_count)
			
			#Ethernet Test:###########################################################
			###Find HCR-4 IP Address####
			if hostname != -1:
				ret = can_addr_ping(hostname)
				if ret == True:
					ethernet_count+=1
					
			log.info( "Ethernet Count = \t\t%d of %d", ethernet_count, total_count)
			print 'Ethernet Count = \t\t%d of %d' % (ethernet_count, total_count)
			#Ethernet Test end:#######################################################
			
			#UART:####################################################################
			ret = uart_self_test()
			if ret == False:
				uart_count += 1
			log.info( "UART Count = \t\t\t%d of %d", uart_count, total_count)
			print 'UART Count = \t\t\t%d of %d' % (uart_count, total_count)
			#UART end:################################################################

			#USB:####################################################################
			dev = usb.core.find(idVendor=0x0525, idProduct=0xA4AC) #HCR-4 	
			if dev is None:
				#raise ValueError('Device not found')
				print('USB Device not found')
			elif dev is 'NoneType':
				print('USB Device noneType found')
			elif prev_dev == "Not Init":
				#First time is free
				usb_count += 1
				prev_dev = dev
			else:	
				#print "PREV VENDOR %s" % prev_dev.idVendor
				#print "DEV VENDOR %s" % dev.idVendor
				if prev_dev.idVendor == dev.idVendor and prev_dev.idProduct == dev.idProduct:
					usb_count += 1
				prev_dev = dev	

			log.info( "USB Count = \t\t\t%d of %d", usb_count, total_count)
			print 'USB Count = \t\t\t%d of %d' % (usb_count, total_count)
			#USB end:################################################################

			#SMARTCARD Test:##########################################################
			#Per Smart Card(2)
			#2 card, clear flag each time
			c_present = 1		#changed 1,2 from 0,2 and c_present as 1, ignoring SAM card.
			for i in range(1,2):
				x = isCardPresent(i)
				time.sleep(1)
				if(x < 0):
					print "Failed Present %d" % i
					count+=1
					#if 5 failed reads in a row, the system may have reset.
					if count > 5:
						log.error("Reading stopped, Reboot suspected")
						get_ser().close()
						run = 0
						break
				elif x == 0:
					print "card %d is Missing" % (x)
					log.error("card %d is Missing" % (x))
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
							#print("Card %d ATR %s" % (i, emv_data))
							if "No EMV Support" not in str(emv_data):
								characters = emv_data.replace(' ', '')
								log.debug("Card %d ATR string %s" % (i, characters.decode('hex')))
								# check each card ATR
								c_present+=1
								#when both cards pass
								if c_present == 2:
									smart_card_count += 1
						else:
							log.info( "%s Card %d Removed" % (st, i))
							print( "%s Card %d Removed" % (st, i))
				else:
					print "x is %d UNKNOWN" % (x)
			log.info( "SmartCard Count = \t%d of %d", smart_card_count, total_count)
			print 'SmartCard Count = \t\t%d of %d' % (smart_card_count, total_count)	
			#SMARTCARD Test end:#######################################################
			
			#TAMPER:####################################################################
			ret = read_tamper_count()
			if ret < 0: #Read Failure
				log.info("TAMPER Read Failed")
				print "TAMPER Read Failed"
			elif ret > 0:
				log.info("TAMPER Found")
				print "TAMPER Found"
			else:	
				tamper_count += 1
			log.info( "TAMPER Count = \t\t%d of %d", tamper_count, total_count)
			print 'TAMPER Count = \t\t\t%d of %d' % (tamper_count, total_count)
			
			#RTC
			rtc_stamp = read_rtc_count()
			log.info( "last RTC Event = \t\t%d", rtc_stamp)
			print 'last RTC Event = \t\t%d' % (rtc_stamp)
			if rtc_stamp is not '0':
				check_secdiag()
			
			#TAMPER end:################################################################
			
			log.info("\n")
			print '\n'
			
			
