#!/usr/bin/python
import usb.core
import usb.util
import sys
import logging
import time, datetime
import os

from log_cm import set_log_info, set_log_level, get_log_cm
from serial_cm import ser_Init, get_ser, uart_self_test, serial_close
from smart_card import isCardPresent, getEnvData, read_smart_card
from ping import find_ip_addr, can_addr_ping
from sec_mon_hcr4 import read_tamper_count, read_rtc_count, set_tamper_trigger
from ucl import read_stest_count

##################################################
#Main Code Here
##################################################
if __name__=='__main__':

##############USER DEFINED########################
	##Overwrite Log location
	my_path = '..\\fcc_log\\'
	my_name = 'Thermal_test'
	tamper_flag = 0 	# 0-OFF, f-tamper 0,1,2,3 active, 3f-All Tampers and Latches (not this test) Active and triggered
							# 1 - Tamper1 armed
							# 2 - Tamper2 armed
							# 3 - Tampers 1&2 armed
							# 4 - Tamper3 armed
							# ... binary flag to enable each tamper.

	DELAY_PER_CYCLE = 3
##############USER DEFINED######################


##One time setup
	set_log_info(my_path, my_name)
	#DEBUG set_log_info(my_path, my_name, 0)

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
		crypto_count = 0
		total_count 	= 0
		MAX_COM_RETRY	= 5
		SECONDS_PMIN = 60
		MINUTES_DELAY = (SECONDS_PMIN * DELAY_PER_CYCLE)
################################


##############INIT #################
		prev_dev = "Not Init"
		ser_Init()
		#Requires Serial init
		hostname = find_ip_addr('eth0')
		set_tamper_trigger(tamper_flag)
##############INIT END##############
		get_log_cm().info('Start FCC Test')
		get_log_cm().info('Test :\n UART, Ethernet, USB, SmartCard')

		while run:
			#Total Test Cycles
			#get_log_cm().info( "\n")
			total_count+=1
			get_log_cm().debug( "Total Test Cycles = %d", total_count)

			#Ethernet Test:###########################################################
			###Find HCR-4 IP Address####
			if hostname != -1:
				ret = can_addr_ping(hostname)
				if ret == True:
					ethernet_count+=1

			get_log_cm().info( "Ethernet Count = \t\t%d of %d", ethernet_count, total_count)
			#Ethernet Test end:#######################################################

			#UART:####################################################################
			ret = uart_self_test()
			if ret == False:
				uart_count += 1
			get_log_cm().info( "UART Count = \t\t\t%d of %d", uart_count, total_count)
			#UART end:################################################################

			#USB:####################################################################

			dev = usb.core.find(find_all=True)
			time.sleep(1)
			if prev_dev == "Not Init":
				for cfg in dev:
					if cfg.idVendor == 0x0525:
						prev_dev = cfg
						usb_count += 1
			elif prev_dev != "Not Init":
				for cfg in dev:
					if cfg is None:
						get_log_cm().error('\t\t\tUSB Device not found')
					elif cfg is 'NoneType':
						get_log_cm().error('\t\t\tUSB Device noneType found')
					else:
						if prev_dev.idVendor == cfg.idVendor and prev_dev.idProduct == cfg.idProduct:
							#get_log_cm().debug( "PREV VENDOR %s\n" % prev_dev.idVendor)
							#get_log_cm().debug("cfg VENDOR %s\n" % cfg.idVendor)
							usb_count += 1
			get_log_cm().info( "USB Count = \t\t\t%d of %d", usb_count, total_count)

			#USB end:################################################################

			#SMARTCARD Test:##########################################################
			#Only testing card 1 in range below
			for i in range(1,2):
					val = read_smart_card(i)
					if val == -1:
						run = 0
						break
					if val == 0:
						smart_card_count+=1
			get_log_cm().info( "SmartCard Count = \t\t%d of %d", smart_card_count, total_count)
			#SMARTCARD Test end:#######################################################

			#TAMPER:####################################################################
			if tamper_flag != 0:
				get_log_cm().debug("\t\t\t Tamper Flag is %X\n\n", tamper_flag)
				ret = read_tamper_count()
				if ret < 0: #Read Failure
					get_log_cm().error("\t\t\tTAMPER Read Failed")
				elif ret > 0:
					get_log_cm().info("TAMPER Found")
				else:
					tamper_count += 1
				get_log_cm().info( "TAMPER Count = \t\t%d of %d", tamper_count, total_count)

				#RTC
				rtc_stamp = read_rtc_count()
				if rtc_stamp < 0:
					get_log_cm().error("\t\t\tPossible reset RTC")
				else:
					get_log_cm().info( "last RTC Event = \t\t%d", rtc_stamp)
			else:
				get_log_cm().debug("\t\t\t No Tamper nodes enabled\n")

			#TAMPER end:################################################################
			#CRYPTO:####################################################################
			ret = 0
			#Read Crypto 5 times to exercise Crypto block
			for i in range(0,5):
				ret += read_stest_count()
			if ret < 0: #Read Failure
				get_log_cm().error("\t\t\t Crypto Read Failed")
			elif ret > 0:
				get_log_cm().info("Crypto Found")
			else:
				crypto_count += 1
			get_log_cm().info( "Crypto Count = \t\t%d of %d", crypto_count, total_count)
			#CRYPTO end:################################################################
			get_log_cm().info("\t\t\t======SLEEP %d Minutes ========================\n", DELAY_PER_CYCLE)
			time.sleep(MINUTES_DELAY)

