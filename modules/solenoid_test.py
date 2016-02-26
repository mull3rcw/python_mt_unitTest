#!/usr/bin/python

import time

print "solenoid_test"
from log_cm import set_log_info, set_log_level, get_log_cm
from serial_cm import ser_Init, get_ser, uart_self_test, serial_close
from smart_card import isCardPresent, getEnvData, read_smart_card
from solenoid import card_bay_open, card_bay_locked, card_bay_init, latched_open, latched_close



##################################################
#Main Code Here
##################################################
if __name__=='__main__':
##############USER DEFINED##################################################################################			
##Overwrite Log location	
	my_path = '..\\solenoid_test\\'
	my_name = 'solenoid_test_file'
	set_log_level(1)
	test_count = 100
	DEBUG_LOG = 0
	set_log_info(my_path, my_name, 1)
##############USER DEFINED##################################################################################

##One time setup

	SLEEP_DURATION		=	2
	CUSTOMER_DELAY		=	5
	
	
	while True:
########Passing Counters########
		total_count 		=	0
		smart_card_count 	=	0
		run 				=	1
################################		

##############INIT #################
		
		ser_Init()
		card_bay_init()
##############INIT END##############		
		get_log_cm().info('Start %s Test', my_name)
		while run:
			total_count+=1
			if total_count >= test_count:
				card_bay_init() # 
				run = 0
				
			get_log_cm().info( "Total Test Cycles = %d Sleep for %d seconds!", total_count, CUSTOMER_DELAY)
			time.sleep(CUSTOMER_DELAY)
			#card_bay_locked()
			latched_close()
			#SMARTCARD Test:##########################################################
			for i in range(1,2):
					val = read_smart_card(i)
					if val == -1:
						run = 0
						break
					if val == 0:
						smart_card_count+=1
			
			get_log_cm().info( "SmartCard Count = %d\\%d -- Sleeping for %d ", smart_card_count, total_count, SLEEP_DURATION)
			time.sleep(SLEEP_DURATION)
			
			#SMARTCARD Test:##########################################################			
			#card_bay_open()
			latched_open()
			
			get_log_cm().info("==============================\n")

					
	
	