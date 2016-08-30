#! python

import serial, time, datetime, os
from log_cm import get_log_cm, set_log_info

##################################################
#USER/Machine SPECIFIC, change UART to MATCH YOURS!!!!
port = 'COM1'
baud = 57600
base_app_dir = '/opt/maxim-ic/hcr4/apps/'
########################

def set_ser(new):
	global ser
	ser = new

def get_ser():
	global ser
	if 'ser' not in globals():
		get_log_cm().error("Error: ser not init")
		return -1
	return ser

########################
#Initialize Access

def Hcr4SendCMD(cmd):
	input = base_app_dir+cmd
	get_log_cm().debug("SendHCR4 : %s" % input)
	get_ser().write(input.encode('ascii')+'\n')
	time.sleep(1)
	return get_ser().readlines()

def _ser_init():

	wait4ser=True

	while wait4ser:
		try:
			set_ser(serial.Serial(port, baud, timeout=1))
			get_ser().close()
			get_ser().open()
			wait4ser=False
		except serial.SerialException:
			get_log_cm().info("Oops! waiting 15 seconds. Is the serial port %s available" % port)
			wait4ser=True
			set_ser(0)
			time.sleep(15)

	if get_ser().isOpen():
		get_log_cm().info(get_ser().name + ' is open...')
	else:
		get_log_cm().error('Another UART blocking '+get_ser().name)

def _ser_end():
	global fH, cH
	get_ser().close()

def serial_close():
	_ser_end()

def ser_Init():
	_ser_init()

	while become_root() == False:
		get_log_cm().debug("\t\t\t\tChecking for ROOT\n")
	get_log_cm().info("\tROOT Detected!!")

def uart_self_test():
	input = 'ls'
	get_ser().write(input.encode('ascii')+'\n')
	time.sleep(1)
	out = str(get_ser().readlines())
	if out is None:
		return True
	elif out == "[]":
		return True
	elif "SecureBoot" in out:
		return True
	else:
		return False

def await_boot_complete():
	input = 'root'
	get_ser().write(input.encode('ascii')+'\n')
	time.sleep(3)
	out = str(get_ser().readlines())

	if "jibe-eek login" in out:
		get_log_cm().info("Boot up Complete")
		return "BootDone"
	elif "root@jibe-eek examples" in out:
		get_log_cm().info("Root up Complete")
		return "RootDone"
	elif "SecureBoot/disabled (EvKit-revC-B5)>" in out:
		get_log_cm().info("U-Boot detected, reset u-boot and wait 40 seconds")
		input = 'reset'
		get_ser().write(input.encode('ascii')+'\n')
		time.sleep(40)
		get_log_cm().info("Go Back to listening")
		return "Pending"
	elif "root@jibe" in out:
		get_log_cm().info("Root Log Complete")
		return "RootDone"
	elif "#" in out:
		get_log_cm().info("Root Log Complete")
		return "RootDone"
	elif "Password" in out:
		input = 'ls'
		get_ser().write(input.encode('ascii')+'\n')
		time.sleep(5)
		get_log_cm().info("Boot up Complete:PW")
		return "BootDone"
	else:
		get_log_cm().info("%s: Awaiting Bootup", port )
		input = 'cd /root'
		get_ser().write(input.encode('ascii')+'\n')
		time.sleep(2)
		get_log_cm().info("Awaiting2 Bootup")
		get_log_cm().info("%s" % out)
		return "Pending"

def become_root ():
	# check list for NOK or OK
	rootDone = False
	check = True

	while check:
		state = await_boot_complete()
		if "Pending" in state:
			rootDone = False
			check = True
		elif "BootDone" in state:
			rootDone = False
			check = False
		else:
			rootDone = True
			check = False

	if rootDone == False:
		out = str(get_ser().readlines())
		get_log_cm().info("Out is %s", out)
		get_log_cm().info("Send Password")
		input = 'root'
		get_ser().write(input.encode('ascii')+'\n')
		time.sleep(1)
		get_ser().write(input.encode('ascii')+'\n')

    #Make all passes go through this (move out of if)
	time.sleep(3)
	input = 'cd /opt/maxim-ic/hcr4/apps'
	get_ser().write(input.encode('ascii')+'\n')
    # end
	time.sleep(1)

	#Check if in the correct directory
	input = 'ls'
	get_ser().write(input.encode('ascii')+'\n')
	time.sleep(2)
	out = get_ser().readlines()

	if "sci" in str(out):
		return True
	else:
		get_log_cm().debug("FAIL to find SCIBASIC")
		input = 'pwd'
		get_ser().write(input.encode('ascii')+'\n')
		time.sleep(1)
		get_log_cm().info("%s" % str(get_ser().readlines()))
		return False

if __name__=='__main__':

	my_path = '..\\serial_log\\'
	my_name = 'serial_test'

	set_log_info(my_path, my_name, 0)
	ser_Init()

	get_log_cm().info("serial_cm.py")
	get_log_cm().debug('DEBUG: Quick zephyrs daft.')
	get_log_cm().info('INFO:How jumping zebras vex.')
