#!/usr/bin/python

#import usb.core
#import usb.util
import sys
import logging
import time, datetime
import os

from log_cm import set_log_info, set_log_level, get_log_cm
from serial_cm import ser_Init, get_ser, uart_self_test, serial_close


from sec_mon_hcr4 import read_tamper_count, read_rtc_count, set_tamper_trigger


##################################################
#Main Code Here
##################################################
if __name__=='__main__':

##############USER DEFINED########################
	##Overwrite Log location
	my_path = '..\\tam_log\\'
	my_name = 'tamper_monitor'
	tamper_flag = 0 	# 0-OFF, f-tamper 0,1,2,3 active, 3f-All Tampers and Latches (not this test) Active and triggered
							# 1 - Tamper1 armed
							# 2 - Tamper2 armed
							# 3 - Tampers 1&2 armed
							# 4 - Tamper3 armed
							# ... binary flag to enable each tamper.
##############USER DEFINED######################


##One time setup
	set_log_info(my_path, my_name, 0)

	while True:
		isCardP=[-1, -1]
		run 			= 1
		count 			= 0
########Passing Counters########
		uart_count 		= 0
		tamper_count 	= 0
		rtc_stamp 	= 0
		total_count 	= 0
		MAX_COM_RETRY	= 5
################################


##############INIT #################
		prev_dev = "Not Init"
		ser_Init()
		#Requires Serial init
		set_tamper_trigger(tamper_flag)
##############INIT END##############
		get_log_cm().info('Start TAMPER Monitor Test')

		while run:
			total_count+=1
			get_log_cm().debug( "Total Test Cycles = %d", total_count)


			#UART:####################################################################
			ret = uart_self_test()
			if ret == False:
				uart_count += 1
			get_log_cm().info( "UART Count = \t\t\t%d of %d", uart_count, total_count)
			#UART end:################################################################

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
				get_log_cm().error("\t\t\tTAMPER DISABLED\n")

			#TAMPER end:################################################################

			get_log_cm().info("\t\t\t==============================\n")
			time.sleep(5)

