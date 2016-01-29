#! python
import time, datetime
from serial_cm import ser_Init, get_ser, log, _ser_init


def read_tamper_count():
	input = './secmon /dev/secmon 3'
	get_ser().write(input.encode('ascii')+'\n')
	time.sleep(2)
	out = get_ser().readlines()
	count = int(out[9][7:]) #TMP0
	count = int(out[10][7:]) #TMP1
	count += int(out[11][7:])#TMP2
	count += int(out[12][7:])#TMP3
	count += int(out[13][7:])#TMP4
	count += int(out[14][7:])#TMP5
	return count

##################################################
#Main Code Here
##################################################

if __name__=='__main__':
	_ser_init()
	print "Tamper Readings"
	print read_tamper_count()
		
