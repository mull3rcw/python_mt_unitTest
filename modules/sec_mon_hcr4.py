#! python
import time, datetime
from log_cm import get_log_cm
from serial_cm import ser_Init, get_ser, _ser_init

secmon_dev_name = 0

def set_secmon_devnm(new):
	global secmon_dev_name
	secmon_dev_name = new

def get_secmon_devnm():
	global secmon_dev_name
	return secmon_dev_name 



def get_bit(byteval,idx):
#	get_log_cm().info( "byteval %x" % (byteval))
	return ((byteval&(1<<idx))!=0);

def read_tamper_count_old():
	input = '/opt/maxim-ic/basic/examples/secmon /dev/secmon0 3'
	if (get_ser().isOpen()==False):
		get_log_cm().error("serial not available")
		return -1

	get_ser().write(input.encode('ascii')+'\n')
	time.sleep(1)
	out = get_ser().readlines()
	count = -1
	print out
	if not out:
		get_log_cm().error("\t\t\t(read_tamper_count)Possible reset")
	elif len(out) < 10:
		get_log_cm().error( "\t\t\t(read_tamper_count)Possible reset too short")
	elif 'Error Getting SEC_GET_STATUS' in out:
		get_log_cm().error( "\t\t\t(read_tamper_count)secmon read error")
	elif 'TMP' in out[10]:
		#print "length"
		#print len(out)
		# Brute force index values
		count = int(out[10][7:])#TMP1
		count += int(out[11][7:])#TMP2
		count += int(out[12][7:])#TMP3
		count += int(out[13][7:])#TMP4
		count += int(out[14][7:])#TMP5
		count += int(out[15][7:])#TMP6
	else:	
		get_log_cm().error( "\t\t\tTamper ret not found")
	return count

def read_tamper_count():
	if (get_ser().isOpen()==False):
		get_log_cm().error("serial not available")
		return -1
		
	# send UART request	
	input = '/opt/maxim-ic/basic/examples/secmon /dev/secmon0 3'
	get_ser().write(input.encode('ascii')+'\n')
	time.sleep(1)

	out = get_ser().readlines()
	#generator: creates "matches list" only if parsed TMP info present.
	matches = [x for x in out if "TMP" in x]
	if not matches:
		get_log_cm().error("\t\t\t(read_tamper_count)Possible reset")
		return -1
	else:
		count = 0
		for y in matches:
			count += int(y[7:])
	return count

def find_dev_secmon_name():
	if (get_ser().isOpen()==False):
		get_log_cm().info( "\t\t\tserial not available")
		return -1
	input = 'ls /dev/secm*'
	get_ser().write(input.encode('ascii')+'\n')
	time.sleep(2)
	out = get_ser().readlines()

	if not out:
		get_log_cm().error( "\t\t\t(find_dev_secmon_name)Possible Reset")
	elif "ls" is out:
		get_log_cm().error( "\t\t\t/dev/secmon not found")
	else:
		print out
		s_index = out[1].find('dev')+4
		e_index = out[1].find(r"\x1b", s_index)
		print  out[1][s_index:e_index]
		#set_secmon_devnm


def read_secdiag_val_old():
	if (get_ser().isOpen()==False):
		get_log_cm().info( "\t\t\t(read_secdiag_val)serial not available")
		return -1

	print "read_secdiag_val Here"    
	input = '/opt/maxim-ic/basic/examples/secmon /dev/secmon0 5 ffe0200c'
	get_ser().write(input.encode('ascii')+'\n')
	time.sleep(1)
	out = get_ser().readlines()
	
	print out
	count = -1
	if not out:
		get_log_cm().error("\t\t\t(read_secdiag_val)Possible reset")
	elif len(out) < 15:
		get_log_cm().error("\t\t\t(read_secdiag_val)Possible reset, too short")
	elif 'Error reading' in out:
		get_log_cm().error("\t\t\t(read_secdiag_val)secdiag read error")
	elif 'fee0200c =' in out[15]:
		# Brute force index values
		print out[15][11:]
		count = int(out[15][11:], 16)
	else:	
		get_log_cm().error("Tamper secdiag return not found.")
	return count
	
	
def read_secdiag_val():
	if (get_ser().isOpen()==False):
		get_log_cm().info( "\t\t\t(read_secdiag_val)serial not available")
		return -1

	input = '/opt/maxim-ic/basic/examples/secmon /dev/secmon0 5 ffe0200c'
	get_ser().write(input.encode('ascii')+'\n')
	time.sleep(1)
	out = get_ser().readlines()

	#Filter all out for ifstatement
	matches = [x for x in out if "fee0200c" in x]
	conv =  matches[0][12:]

	if not out:
		get_log_cm().error("\t\t\t(read_secdiag_val)Possible reset")
		val = -1
	else:
		val = int(conv, 16)
	return val

def print_secdiag(flag):
	DRS=0; KW=1;SHEILD=2;LOTEMP=3;
	HITEMP=4; BATLO=5; BATHI=6;	EXTF=7;
	TMP1=16;TMP2=17;TMP3=18;TMP4=19;TMP5=20;TMP6=21;
	
	if get_bit(flag, DRS) == 1:
		get_log_cm().info("DRS")
	if get_bit(flag, KW) == 1:
		get_log_cm().info("KW")
	if get_bit(flag, SHEILD) == 1:
		get_log_cm().info( "SHEILD")
	if get_bit(flag, LOTEMP) == 1:
		get_log_cm().info( "LOTEMP")
	if get_bit(flag, HITEMP) == 1:
		get_log_cm().info( "HITEMP")
	if get_bit(flag, BATLO) == 1:
		get_log_cm().info( "BATLO")
	if get_bit(flag, BATHI) == 1:
		get_log_cm().info( "BATHI")
	if get_bit(flag, EXTF) == 1:
		get_log_cm().info( "EXTF")
	if get_bit(flag, TMP1) == 1:
		get_log_cm().info( "TMP1")
	if get_bit(flag, TMP2) == 1:
		get_log_cm().info( "TMP2")
	if get_bit(flag, TMP3) == 1:
		get_log_cm().info( "TMP3")
	if get_bit(flag, TMP4) == 1:
		get_log_cm().info( "TMP4")
	if get_bit(flag, TMP5) == 1:
		get_log_cm().info( "TMP5")
	if get_bit(flag, TMP6) == 1:
		get_log_cm().info( "TMP6")
	
def check_secdiag():
	flag = read_secdiag_val()
	print_secdiag(flag)

def set_tamper_trigger(num):
	input = '/opt/maxim-ic/basic/examples/secmon /dev/secmon0 4 ' + str(num)
	if (get_ser().isOpen()==False):
		get_log_cm().info( "\t\t\tserial not available")
		return
	get_ser().write(input.encode('ascii')+'\n')
	time.sleep(1)
	out = get_ser().readlines()
	if 'Error Getting SEC_GET_STATUS' in out:
		get_log_cm().info("\t\t\tsecmon read error")
	
def read_rtc_count_old():
	if (get_ser().isOpen()==False):
		get_log_cm().info( "\t\t\tserial not available")
		return -1

	# send UART request			
	input = '/opt/maxim-ic/basic/examples/secmon /dev/secmon0 3'
	get_ser().write(input.encode('ascii')+'\n')
	time.sleep(1)
	
	out = get_ser().readlines()
	count = -1
	if not out:
		get_log_cm().error( "\t\t\t(read_rtc_count)Possible Reset")
	elif len(out) < 16:
		get_log_cm().error( "\t\t\t(read_rtc_count)Too Short Possible reset")
	elif 'Error Getting SEC_GET_STATUS' in out:
		get_log_cm().error("\t\t\t(read_rtc_count)secmon read error")
	elif 'RTC' not in out[15]:
		#print out
		#print out[15]
		get_log_cm().error("(read_rtc_count)secmon cmd not found")
	else:	
		print "out[16][6:] is %s" % out[15][6:]
		count = int(out[15][6:]) #RTC
		
	return count

	
def read_rtc_count():
	if (get_ser().isOpen()==False):
		get_log_cm().error("serial not available")
		return -1
		
	# send UART request	
	input = '/opt/maxim-ic/basic/examples/secmon /dev/secmon0 3'
	get_ser().write(input.encode('ascii')+'\n')
	time.sleep(1)

	out = (get_ser().readlines())
	#generator: creates "matches list" only if parsed TMP info present.
	lRtc = [x for x in out if "RTC:" in x]
	
	#s_index = 5 #smatch.find('RTC:\\t\\t')+8
	#print("lRtc is %s\n" % lRtc)
	#print("lRtc[s_index:] is %s\n" % lRtc[0][5:])
	count = -1	
	
	try:
		if not lRtc:
			get_log_cm().error("\t\t\t(read_rtc_count)Possible reset")
		else:
			count = int(lRtc[0][5:])
	except ValueError:
		get_log_cm().error("\t\t\t(read_rtc_count)Possible reset error")
	return count

def test1():
	aList = [123, 'xyz', 'zara', 'abc'];
	print "Index for xyz : ", aList.index( 'xyz' ) 
	print "Index for zara : ", aList.index( 'zara' ) 
	try:
		print "Index for chris : ", aList.index( 'chris' ) 
	except ValueError:
		print "No Chris found"
	
	
##################################################
#Main Code Here
##################################################

if __name__=='__main__':
	_ser_init()
	#find_dev_secmon_name()
	#get_log_cm().info("Tamper Readings")
	#get_log_cm().info(read_tamper_count())
	get_log_cm().info("Read RTC %d" % read_rtc_count())
	#get_log_cm().info("RTC Above")
	#get_log_cm().info(set_tamper_trigger("f"))
	#flag = read_secdiag_val()
	#print("Flag is %x" % flag)
	#print_secdiag(flag)
	#print read_tamper_count()
	#print test1()
	
