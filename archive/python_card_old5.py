#! python
import sys, serial, time, sched, threading, msvcrt, datetime, time

#from msvcrt import getch is for keyboard polling while not blocking.

# Set up Serial	  
##################################################
#Machine SPECIFIC, change UART to MATCH YOURS

port = "COM1"

##################################################
baud = 57600
isCardP=[False, False]
ser = 0


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
	else:
		print 'Another UART blocking %s' % ser.name
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
		return False

def become_root ():
	# check list for NOK or OK
	global ser
	input = 'root'
	ser.write(input.encode('ascii')+'\n')
	
	time.sleep(3)
	input = 'cd /opt/maxim-ic/basic/examples'
	ser.write(input.encode('ascii')+'\n')
	
	time.sleep(1)
	input = 'ls'
	ser.write(input.encode('ascii')+'\n')
	time.sleep(1)
	out = ser.readlines()
	
	if "sci_basic" in str(out):
		print "Logged in OK: sci_basic detected"
		#print str(out)
		return True
	else:
		print "Logged in Fail: CNTL-C and restart"
		#print str(out)
		return False	
	


##################################################
#Main Code Here
##################################################
	
Init()

while True:
#	cmd = raw_input("Enter command or 'exit':")
#	cmd = readInput("Enter command or 'exit':", "nuthin")
#	cmd = readInput(" ", " ")
#	print "The Command is %s" % cmd
	
	time.sleep(1)
	ts = time.time()
	
	for i in range(0,2):
		x = isCardPresent(i)
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
		
		

	 
