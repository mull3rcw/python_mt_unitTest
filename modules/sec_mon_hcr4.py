#! python
import time, datetime
from serial_cm import ser_Init, get_ser, log, _ser_init

secmon_dev_name = 0

def set_secmon_devnm(new):
	global secmon_dev_name
	secmon_dev_name = new

def get_secmon_devnm():
	global secmon_dev_name
	return secmon_dev_name 



def get_bit(byteval,idx):
#	log.info( "byteval %x" % (byteval))
	return ((byteval&(1<<idx))!=0);

def read_tamper_count_old():
	input = '/opt/maxim-ic/basic/examples/secmon /dev/secmon0 3'
	if (get_ser().isOpen()==False):
		log.error("serial not available")
		return -1

	get_ser().write(input.encode('ascii')+'\n')
	time.sleep(1)
	out = get_ser().readlines()
	count = -1
	print out
	if not out:
		log.error("\t\t\t(read_tamper_count)Possible reset")
	elif len(out) < 10:
		log.error( "\t\t\t(read_tamper_count)Possible reset too short")
	elif 'Error Getting SEC_GET_STATUS' in out:
		log.error( "\t\t\t(read_tamper_count)secmon read error")
	elif 'TMP' in out[10]:
		test()
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
		log.error( "\t\t\tTamper ret not found")
	return count

def read_tamper_count():
	if (get_ser().isOpen()==False):
		log.error("serial not available")
		return -1
		
	# send UART request	
	input = '/opt/maxim-ic/basic/examples/secmon /dev/secmon 3'
	get_ser().write(input.encode('ascii')+'\n')
	time.sleep(1)

	out = get_ser().readlines()
	#generator: creates "matches list" only if parsed TMP info present.
	matches = [x for x in out if "TMP" in x]
	if not matches:
		log.error("\t\t\t(read_tamper_count)Possible reset")
		return -1
	else:
		count = 0
		for y in matches:
			count += int(y[7:])
	return count

def find_dev_secmon_name():
	if (get_ser().isOpen()==False):
		log.info( "\t\t\tserial not available")
		return -1
	input = 'ls /dev/secm*'
	get_ser().write(input.encode('ascii')+'\n')
	time.sleep(2)
	out = get_ser().readlines()

	if not out:
		log.error( "\t\t\t(find_dev_secmon_name)Possible Reset")
	elif "ls" is out:
		log.error( "\t\t\t/dev/secmon not found")
	else:
		print out
		s_index = out[1].find('dev')+4
		e_index = out[1].find(r"\x1b", s_index)
		print  out[1][s_index:e_index]
		#set_secmon_devnm


	
	
def read_secdiag_val():
	input = '/opt/maxim-ic/basic/examples/secmon /dev/secmon0 5 ffe0200c'
	if (get_ser().isOpen()==False):
		log.info( "\t\t\t(read_secdiag_val)serial not available")
        return -1
        
	get_ser().write(input.encode('ascii')+'\n')
	time.sleep(1)
	out = get_ser().readlines()
	print out
	count = -1
	if not out:
		log.error("\t\t\t(read_secdiag_val)Possible reset")
	elif len(out) < 15:
		log.error("\t\t\t(read_secdiag_val)Possible reset, too short")
	elif 'Error reading' in out:
		log.error("\t\t\t(read_secdiag_val)secdiag read error")
	elif 'fee0200c =' in out[15]:
		# Brute force index values
		#print out[15][11:]
		count = int(out[15][11:], 16)
	else:	
		log.error("Tamper secdiag return not found.")
	return count

def print_secdiag(flag):
	DRS=0; KW=1;SHEILD=2;LOTEMP=3;
	HITEMP=4
	BATLO=5
	BATHI=6
	EXTF=7
	TMP1=16;TMP2=17;TMP3=18;TMP4=19;TMP5=20;TMP6=21;
	if get_bit(flag, DRS) == 1:
		log.info("DRS")
	if get_bit(flag, KW) == 1:
		log.info("KW")
	if get_bit(flag, SHEILD) == 1:
		log.info( "SHEILD")
	if get_bit(flag, LOTEMP) == 1:
		log.info( "LOTEMP")
	if get_bit(flag, HITEMP) == 1:
		log.info( "HITEMP")
	if get_bit(flag, BATLO) == 1:
		log.info( "BATLO")
	if get_bit(flag, BATHI) == 1:
		log.info( "BATHI")
	if get_bit(flag, EXTF) == 1:
		log.info( "EXTF")
	if get_bit(flag, TMP1) == 1:
		log.info( "TMP1")
	if get_bit(flag, TMP2) == 1:
		log.info( "TMP2")
	if get_bit(flag, TMP3) == 1:
		log.info( "TMP3")
	if get_bit(flag, TMP4) == 1:
		log.info( "TMP4")
	if get_bit(flag, TMP5) == 1:
		log.info( "TMP5")
	if get_bit(flag, TMP6) == 1:
		log.info( "TMP6")
	
def check_secdiag():
	flag = read_secdiag_val()
	print_secdiag(flag)

def set_tamper_trigger(num):
	input = '/opt/maxim-ic/basic/examples/secmon /dev/secmon0 4 ' + str(num)
	if (get_ser().isOpen()==False):
		log.info( "\t\t\tserial not available")
		return
	get_ser().write(input.encode('ascii')+'\n')
	time.sleep(1)
	out = get_ser().readlines()
	if 'Error Getting SEC_GET_STATUS' in out:
		log.info("\t\t\tsecmon read error")
	
def read_rtc_count():
	input = '/opt/maxim-ic/basic/examples/secmon /dev/secmon0 3'
	if (get_ser().isOpen()==False):
		log.info( "\t\t\tserial not available")
		return -1

	get_ser().write(input.encode('ascii')+'\n')
	time.sleep(2)
	out = get_ser().readlines()
	count = -1
	if not out:
		log.error( "\t\t\t(read_rtc_count)Possible Reset")
	elif len(out) < 16:
		log.error( "\t\t\t(read_rtc_count)Too Short Possible reset")
	elif 'Error Getting SEC_GET_STATUS' in out:
		log.error("\t\t\t(read_rtc_count)secmon read error")
	elif 'RTC' not in out[16]:
		log.error("(read_rtc_count)secmon cmd not found")
	else:	
		count = int(out[16][6:]) #RTC
	return count

##################################################
#Main Code Here
##################################################

if __name__=='__main__':
	_ser_init()
	#find_dev_secmon_name()
	log.info("Tamper Readings")
	#log.info(read_tamper_count())
	#log.info(read_rtc_count())
	#log.info("RTC Above")
	#log.info(set_tamper_trigger("f"))
	#flag = read_secdiag_val()
	#print_secdiag(flag)
	read_tamper_count()
	
