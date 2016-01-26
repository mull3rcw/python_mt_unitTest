#! python
import sys, serial, time, sched, threading, msvcrt, datetime, time, logging, os

#from msvcrt import getch is for keyboard polling while not blocking.

# Set up Serial	  
##################################################
#Machine SPECIFIC, change UART to MATCH YOURS


port = "COM1"
#hdlr = logging.FileHandler('C:\MagTek\HCR-4\check_card_log.txt','w')
path = 'C:\Users\Christim.MAGTEK\workspace'
hdlr = logging.FileHandler('C:\Users\Christim.MAGTEK\workspace\check_card_log.txt', 'w')
log_file = open('C:\Users\Christim.MAGTEK\workspace\card_check.log','w')

log_name = 'check_card_log'

##################################################
baud = 57600
isCardP=[False, False]
ser = 0
logger = logging.getLogger('check_card')

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
#logger.setLevel(logging.WARNING)
logger.setLevel(logging.DEBUG)
old_stdout = sys.stdout
#sys.stdout = log_file

#Initialize Access
def Init():
	global ser 
	try:
		ser = serial.Serial(port, baud, timeout=1)
	except serial.SerialException:
		print "Oops! Is the serial port %s available" % port
		exit()
		
	if ser.isOpen():
		print(ser.name + ' is open...')
		logging.info(ser.name + 'Logging: is open...')
	else:
		print 'Another UART blocking %s' % (ser.name)
		
	print "Path : "+ log_name
	if not os.path.exists(path):
		os.mkdir(path)
	filename = path + '.log'
	with open(os.path.join(path, filename), 'wb') as temp_file:
		temp_file.write(" ")
	become_root()

# ReadInput
def readInput( caption, default, timeout = 5):
    start_time = time.time()
    sys.stdout.write('%s(%s):'%(caption, default));
    input = ''
    while True:
        if msvcrt.kbhit():
            chr = msvcrt.getche()
            if ord(chr) == 13: # enter_key
                break
            elif ord(chr) >= 32: #space_char
                input += chr
        if len(input) == 0 and (time.time() - start_time) > timeout:
            break

    print ''  # needed to move to next line
    if len(input) > 0:
        return input
    else:
        return default

def isCardPresent (num):
	# check list for NOK or OK
	global ser
	input = './sci_basic /dev/sc 3'
	index = input.find(' 3')
	input2 = input[:index] + str(num) + input[index:]
	#print input2
	ser.write(input2.encode('ascii')+'\n')
	out = ser.readlines()
	if "NOK" in str(out):
#		print "Card Empty"
		return False
	elif " OK" in str(out):
#		print "Card Detected"
		return True
	else:
		print "Failed to read"
		return -1

def detect_boot_complete():
	global ser
	
	out = ser.readlines()
	
	if "jibe-eek login" in str(out):
		print("Boot up Complete")
		return False
	elif "" in str(out):
		print ("Awaiting Bootup")
		# Send some data to get new printouts
		input = '.'
		ser.write(input.encode('ascii')+'\n')
		time.sleep(2)
		ser.write(input.encode('ascii')+'\n')
		time.sleep(10)
		
		return True

def become_root ():
	# check list for NOK or OK
	global ser
	
	check = True
	while check:
		check = detect_boot_complete()
	
	input = 'root'
	ser.write(input.encode('ascii')+'\n')
	
	time.sleep(3)
	input = 'cd /opt/maxim-ic/basic/examples'
	ser.write(input.encode('ascii')+'\n')
	
	time.sleep(1)
	input = 'ls'
	ser.write(input.encode('ascii')+'\n')
	time.sleep(1)
	
	wait = 1
	wait_count = 0
	
	
	out = ser.readlines()
		
	if "sci_basic" in str(out):
		print "Logged in OK: sci_basic detected"
	
		return True
	else:
		print "Logged in Fail: CNTL-C and restart"
		return False	
	


##################################################
#Main Code Here
##################################################
	
while True:
	run = 1
	count = 0
	Init()

	while run:
	
		time.sleep(1)
		ts = time.time()
	
		for i in range(0,2):
			x = isCardPresent(i)
			# if -1, then it failed to read (maybe reset).
			if(x < 0):
				count+=1
				#if 5 failed reads in a row, the system may have reset.
				if count > 5:
					print ("Wait 20 seconds, maybe rebooted")
					time.sleep(20)
					run = 0
			else:	
				count = 0
				if isCardP[i] != x:
					isCardP[i] = x
					st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
					if isCardP[i] == True:
						print "%s Card %d Present" % (st, i)
					else:
						print "%s Card %d Removed" % (st, i)
		
#   if cmd == 'exit':
#	ser.close()
#	exit()
		
		

	 
