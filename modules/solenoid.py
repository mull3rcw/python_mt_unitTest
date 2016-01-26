#! python

import time
from serial_cm import get_ser

PULL_ON = 2		#mean card latched
PULL_OFF = 3	#means card free
POWER_ON = 6
POWER_DOWN = 7

def latch_config (num):
	ser = get_ser()
	input = './solenoid /dev/sol0 '
	index = input.find('sol0 ')
	input2 = input[:index+5] + str(num)
	ser.write(input2.encode('ascii')+'\n')
	out = ser.readlines()
	return True

def pull_on ():
	latch_config(PULL_ON)
	#print "pull_on"
	return True

def pull_off ():
	latch_config(PULL_OFF)
	#print "pull_off"
	return True

def power_on ():
	latch_config(POWER_ON)
	#print "power_on"
	return True

def power_off ():
	latch_config(POWER_DOWN)
	#print "power_off"
	return True

def card_bay_open():
	power_on()
	pull_off()
	time.sleep(2)
	power_off()
	print "card_bay_open -Plunger pushed forward, locked by magnet"

def card_bay_locked():
	power_on()
	pull_on()
	time.sleep(2)
	power_off()
	print "card_bay_locked -Plunger pulled back"

def card_bay_init():
	power_on()
	pull_off()
	power_off()