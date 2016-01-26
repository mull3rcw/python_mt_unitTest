#! python
import sys, serial, time, sched, threading, msvcrt

#from msvcrt import getch is for keyboard polling while not blocking.

# Set up Serial	  
port = "COM5"
baud = 57600
isCardP=False

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



ser = serial.Serial(port, baud, timeout=1)

def isCardPresent ():
	# check list for NOK or OK
	input = './sci_basic /dev/sc1 3'
	ser.write(input.encode('ascii')+'\n')
	out = ser.readlines()
	if "NOK" in str(out):
		print "Card Empty"
		return False
	elif " OK" in str(out):
		print "Card Detected"
		return True
	

if ser.isOpen():
	print(ser.name + ' is open...')

while True:
#	cmd = raw_input("Enter command or 'exit':")
#	cmd = readInput("Enter command or 'exit':", "nuthin")
	cmd = readInput(" ", " ")
	print "The Command is %s" % cmd
	
#	time.sleep(1)
	if isCardP != isCardPresent():
		isCardP = isCardPresent()
		print "isCP is ",isCardP

#   if cmd == 'exit':
#	ser.close()
#	exit()
		
		

	 
