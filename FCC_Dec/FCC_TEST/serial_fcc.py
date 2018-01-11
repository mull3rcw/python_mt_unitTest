#! python
import serial, time, datetime, logging, os

##################################################
#USER/Machine SPECIFIC, change UART to MATCH YOURS!!!!
port = 'COM13'
path = '..\log\\'
brk = '\\'
log_name = 'check_card_log'

##################################################
baud = 9600
isCardP=[-1, -1]
# Get timestamp of Python call:
myts = time.time()	
myst =  "test" #datetime.datetime.fromtimestamp(myts).strftime('%Y-%m-%d+%H_%M_%S')


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
	print 'LOGGING new PATH is: ' + filename
	hdlr = logging.FileHandler(filename,'wb')
	formatter = logging.Formatter('%(asctime)s:  %(message)s')
	hdlr.setFormatter(formatter)
	return hdlr

def set_log_info(path, name):
	print "Log Path :\n"+ path
	if not os.path.exists(path):
		os.mkdir(path)
		
	log = set_logger_name(name)
	hdlr2 = set_log_path(path)
	log.addHandler(hdlr2) 
	log.setLevel(logging.INFO)
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
			print "Oops! waiting 15 seconds. Is the serial port %s available" % (port)
			log.info("Oops! waiting 15 seconds. Is the serial port %s available" % port)
			wait4ser=True
			set_ser(0)
			time.sleep(15)
		
	if get_ser().isOpen():
		print(get_ser().name + ' is open...')
		log.info(get_ser().name + ' is open...')
	else:
		print 'Another UART blocking %s' % (get_ser().name)
		log.info('Another UART blocking '+get_ser().name)	



def ser_Init2(my_path, my_name):
	_ser_init()
	if become_root() == True:
		print "Logged in OK: sci_basic detected"
	else:
		print "Failure: CNTL-C and restart"
		
	return set_log_info(my_path, my_name)	

def ser_Init(my_path, my_name):
	_ser_init()
	
	while become_root() == False:
		print "\t\t\t\tChecking for ROOT\n"
	
	print "\tROOT Detected!!"
		
	return set_log_info(my_path, my_name)	

	
def uart_self_test():
	print "uart_self_test"
	sendCommand_1 = bytearray.fromhex(u'C0 01 01 C1 01 01 C2 01 10 c4 04 09 00 00 00')	
	get_ser().write(sendCommand_1.encode('ascii')+'\n')
	time.sleep(1)
	out = str(get_ser().readlines())
	print out
	if out is None:
		return True
	elif out == "[]":
		return True
	else:
		return False
	
	
def await_boot_complete():
	print "Write ascci"
	input = bytearray.fromhex(u'C0 01 01 C1 01 01 C2 01 10 c4 04 09 00 00 00')
	input = 'C 0 0 1 0 1 C 1 0 1 0 1 C 2 0 1 1 0 c 4 0 4 0 9 0 0 0 0 0 a'
	get_ser().write(input.encode('ascii')+'\n')
	time.sleep(2)
	out = str(get_ser().readlines())
	raw_val = get_ser().readlines()

	print raw_val
	print ("CM Awaiting Bootup")
		#input = 'C00101C10101C2013F'
		
	sendCommand_1 = bytearray.fromhex(u'C0 01 01 C1 01 01 C2 01 10 c4 04 09 00 00 0a')	
		
	input = 'C0 01 01 C1 01 01 C2 01 10 c4 04 09 00 00 0a'
	input = '43 30 30 31 30 32 43 31 30 31 30 36 43 32 30 31 30 34 43 33 30 31 30 30 43 34 30 31 30 30 a'
	get_ser().write(input.encode('ascii')+'\n')
	#get_ser().write(sendCommand_1)
	time.sleep(2)
	log.info("Awaiting Bootup")
	print out
	raw_val = get_ser().readlines()
	print "raw: "
	print raw_val

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
                print "FAIL SCIBASIC"
                print out
                print "FAIL SCIBASIC"
		input = 'pwd'
		get_ser().write(input.encode('ascii')+'\n')
		time.sleep(1)
		print str(get_ser().readlines())
		return False	
