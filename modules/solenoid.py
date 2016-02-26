#! python

import time
from serial_cm import ser_Init, get_ser, serial_close
from log_cm import set_log_info, set_log_level, get_log_cm

PULL_ON = 2		#mean card latched
PULL_OFF = 3	#means card free
POWER_ON = 6
POWER_DOWN = 7
LATCHED_OPEN = 8
LATCHED_CLOSE = 9

def latch_config (num):
	ser = get_ser()
	input = './solenoid /dev/sol0 '
	index = input.find('sol0 ')
	input2 = input[:index+5] + str(num)
	ser.write(input2.encode('ascii')+'\n')
	out = ser.readlines()
	return True

def latched_open ():
	latch_config(LATCHED_OPEN)
	get_log_cm().debug("\n latched_open\n")
	return True
	
def latched_close ():
	latch_config(LATCHED_CLOSE)
	get_log_cm().debug("\n latched_close\n")
	return True
	
	
	
def pull_on ():
	latch_config(PULL_ON)
	get_log_cm().debug("pull_on")
	return True

def pull_off ():
	latch_config(PULL_OFF)
	get_log_cm().debug("pull_off")
	return True

def power_on ():
	latch_config(POWER_ON)
	get_log_cm().debug("power_on")
	return True

def power_off ():
	latch_config(POWER_DOWN)
	get_log_cm().debug("power_off")
	return True

def card_bay_open():
	power_on()
	pull_off()
	time.sleep(1)
	power_off()
	#print "card_bay_open -Plunger pushed forward, locked by magnet"
	get_log_cm().debug(" ---card_bay_open---")

def card_bay_locked():
	power_on()
	pull_on()
	time.sleep(1)
	power_off()
	#print "card_bay_locked -Plunger pulled back"
	get_log_cm().debug(" ---card_bay_lock---")

def card_bay_init():
	power_on()
	pull_off()
	power_off()
	
	
if __name__=='__main__':
##############USER DEFINED##################################################################################			
##Overwrite Log location	
	my_path = '..\\solenoid_log\\'
	my_name = 'solendoid_test'
	test_count = 10
##############USER DEFINED##################################################################################

##One time setup
	while True:
		test_count 			= 0
########Passing Counters########
		total_count 	= 0
		run = 1
################################		
	

##############INIT #################					
		set_log_info(my_path, my_name)
		ser_Init()
		#card_bay_init()
##############INIT END##############		
		get_log_cm().info('Start %s Test', my_name)
		get_log_cm().info('Test :\n Solenoid')

		while run:
			#Total Test Cycles
			#get_log_cm().info( "\n")
			total_count+=1
			get_log_cm().debug( "Total Test Cycles = %d", total_count)
			time.sleep(1)
			