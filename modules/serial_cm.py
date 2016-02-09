#! python
import serial, time, datetime, logging, os

##################################################
#USER/Machine SPECIFIC, change UART to MATCH YOURS!!!!
port = 'COM1'
path = '..\log\\'
brk = '\\'
log_name = 'check_card_log'

##################################################
baud = 57600
isCardP=[-1, -1]
# Get timestamp of Python call:
myts = time.time()	
myst = datetime.datetime.fromtimestamp(myts).strftime('%Y-%m-%d+%H_%M_%S')
fH = 0
cH = 0
#log = 0

##formatter = logging.Formatter('%(asctime)s:  %(message)s')
##hdlr.setFormatter(formatter)
##log.addHandler(hdlr) 
#log.setLevel(logging.DEBUG)
##log.setLevel(logging.INFO)

########################
ser = 0
log_path_name = path
logger_name = 'check_card'

def set_logger_name(new):
	global logger_name
	logger_name = new
	return logging.getLogger(logger_name)

def set_log_path(new):
	global log_path_name
	log_path_name = new
	filename = log_path_name+logger_name+str(myst)+'.log'
	print('LOGGING new PATH is: %s' % filename)
	return logging.FileHandler(filename,'wb')
	
def set_log_info(path, name):
	global fH, cH
	print "Log Path :\n"+ path
	if not os.path.exists(path):
		os.mkdir(path)

	# Configure Path/Create handles
	log = set_logger_name(name)
	fH = set_log_path(path)
	cH = logging.StreamHandler()
	
	#Overall logging mask, leave alone.
	log.setLevel(logging.DEBUG)
	
	# Logging to File	
	log_formatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")
	fH.setFormatter(log_formatter)
	fH.setLevel(logging.DEBUG)
	log.addHandler(fH) 
	
	# Logging to Console
	console_formatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")
	cH.setFormatter(console_formatter)
	cH.setLevel(logging.INFO)
	log.addHandler(cH)
	return log
	
def set_ser(new):
	global ser
	ser = new

def get_ser():
	global ser
	return ser 


###################################################
### LOGGING
###################################################
filename = path+log_name+str(myst)+'.log'
log = set_log_info(path, 'check_card')

########################
#Initialize Access

def _ser_init():

	wait4ser=True

	while wait4ser:
		try:
			set_ser(serial.Serial(port, baud, timeout=1))
			get_ser().close()
			get_ser().open()
			wait4ser=False
		except serial.SerialException:
			log.info("Oops! waiting 15 seconds. Is the serial port %s available" % port)
			wait4ser=True
			set_ser(0)
			time.sleep(15)
		
	if get_ser().isOpen():
		print(get_ser().name + ' is open...')
	else:
		print('Another UART blocking '+get_ser().name)	

def _ser_end():		
	global fH, cH
	get_ser().close()
	#cH.handlers = []
	#fH.handlers = []
	#log.handlers = []
		
def serial_close():
	_ser_end()
		
#def ser_Init2(my_path, my_name):
#	_ser_init()
#	if become_root() == True:
#		log.info("Logged in OK: sci_basic detected")
#	else:
#		log.info("Failure: CNTL-C and restart")
#		
#	return set_log_info(my_path, my_name)	

def ser_Init():
	_ser_init()

	while become_root() == False:
		print("\t\t\t\tChecking for ROOT\n")
	print("\tROOT Detected!!")
	#return set_log_info(my_path, my_name)

def ser_Init_old_with_logging(my_path, my_name):
	_ser_init()

	while become_root() == False:
		print("\t\t\t\tChecking for ROOT\n")
	print("\tROOT Detected!!")
	return set_log_info(my_path, my_name)

	
def uart_self_test():
	input = 'ls'
	get_ser().write(input.encode('ascii')+'\n')
	time.sleep(1)
	out = str(get_ser().readlines())
#	log.info("%s" % out)
	if out is None:
		return True
	elif out == "[]":
		return True
	else:
		return False
	
	
def await_boot_complete():
	input = 'ls'
	get_ser().write(input.encode('ascii')+'\n')
	time.sleep(3)
	out = str(get_ser().readlines())

	if "jibe-eek login" in out:
		log.info("Boot up Complete")
		return "BootDone"
	elif "root@jibe-eek examples" in out:
		log.info("Root up Complete")
		return "RootDone"
	elif "root@jibe-eek /root" in out:
		log.info("Root Log Complete")
		return "RootDone"	
	elif "Password" in out:
		input = 'ls'
		get_ser().write(input.encode('ascii')+'\n')
		time.sleep(5)
		log.info("Boot up Complete:PW")
		return "BootDone"
	else:
		log.info("Awaiting Bootup")
		input = 'cd /root'
		get_ser().write(input.encode('ascii')+'\n')
		time.sleep(2)
		log.info("Awaiting Bootup")
		log.info("%s" % out)
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
		input = 'root'
		get_ser().write(input.encode('ascii')+'\n')

    #Make all passes go through this (move out of if)
	time.sleep(3)
	input = 'cd /opt/maxim-ic/basic/examples'
	get_ser().write(input.encode('ascii')+'\n')
    # end
	time.sleep(1)

	#Check if in the correct directory
	input = 'ls'
	get_ser().write(input.encode('ascii')+'\n')
	time.sleep(2)
	out = get_ser().readlines()
		
	if "sci_basic" in str(out):
		return True
	else:
		log.debug("FAIL to find SCIBASIC")
		input = 'pwd'
		get_ser().write(input.encode('ascii')+'\n')
		time.sleep(1)
		log.info("%s" % str(get_ser().readlines()))
		return False	

if __name__=='__main__':
	log.info("serial_cm.py")
	that_path = '..\\fcc_log\\'
	that_name = 'fcc_test'
	log = ser_Init(that_path, that_name)
	log.debug('DEBUG: Quick zephyrs daft.')
	log.info('INFO:How jumping zebras vex.')
