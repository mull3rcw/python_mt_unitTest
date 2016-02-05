#! python
import time
from serial_cm import get_ser

def getEnvData (num):
	#load num into sc* cmd line
	ser = get_ser()
	input = '/opt/maxim-ic/basic/examples/sci_basic /dev/sc 10'
	#input = './sci_basic /dev/sc 10'
	index = input.find(' 10')
	input2 = input[:index] + str(num) + input[index:]
	ser.write(input2.encode('ascii')+'\n')
	#Wait 2 seconds for Sam card
	if num == 0: time.sleep(2)
	#Parse Output
	out = str(ser.readlines())
	if 'Card mute' not in out:
		s_index = out.find('ATR[')+10
		e_index = out.find(r"\r\n", s_index)
		return out[s_index:e_index]
	elif 'Card mute' in out:
		return "No EMV Support"


def isCardPresent (num):
	# check list for NOK or OK
	ser = get_ser()
	input = '/opt/maxim-ic/basic/examples/sci_basic /dev/sc 3'
	index = input.find(' 3')
	input2 = input[:index] + str(num) + input[index:]
	#print input2
	ser.write(input2.encode('ascii')+'\n')
	out = ser.readlines()
	if "NOK" in str(out):
		#print "Card Missing"
		return False
	elif " OK" in str(out):
		#print "Card Present"
		return True
	else:
		#print "Failed to read"
		return -1


def setCardFacilitator ():
	#This statys running until completes
	ser = get_ser()
	input = '/opt/maxim-ic/basic/examples/card_facilitator'
	ser.write(input.encode('ascii')+'\n')
	#Wait 2 seconds for Sam card
	print "Pull out MSR read within 10 seconds"
	out = str(ser.readlines())
	print out
	time.sleep(10)
	#Control-C
	input = '\x03'
	ser.write(input.encode('ascii')) #+'\n')
	print "DONE"
	
