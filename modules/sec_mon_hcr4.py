#! python
import time, datetime
from serial_cm import ser_Init, get_ser, log, _ser_init


def get_bit(byteval,idx):
#	print "byteval %x" % (byteval)
	return ((byteval&(1<<idx))!=0);

def read_tamper_count():
	input = '/opt/maxim-ic/basic/examples/secmon /dev/secmon 3'
        if (get_ser().isOpen()==False):
                print "serial not available"
                return -1

	get_ser().write(input.encode('ascii')+'\n')
	time.sleep(1)
	out = get_ser().readlines()
	count = -1
#	print out
#	print out[10]
	if not out:
                print "\t\t\tPossible reset"
                log.info( "\t\t\tPossible Reset")
        elif len(out) < 10:
                print "\t\t\tPossible reset too short"
                log.info( "\t\t\tPossible reset too short")
        elif 'Error Getting SEC_GET_STATUS' in out:
		print "\t\t\tsecmon read error"
		log.info( "\t\t\tssecmon read error")
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
		print "\t\t\tTamper return not found."
		log.info( "\t\t\tTamper ret not found")
	return count

def read_secdiag_val():
	input = '/opt/maxim-ic/basic/examples/secmon /dev/secmon 5 ffe0200c'
	if (get_ser().isOpen()==False):
                print "serial not available"
                log.info( "\t\t\tserial not available")
                return -1
        
	get_ser().write(input.encode('ascii')+'\n')
	time.sleep(1)
	out = get_ser().readlines()
	#print out
	count = -1
	if not out:
                print "\t\t\tPossible reset"
        elif len(out) < 15:
                print "\t\t\tPossible reset too short"
        elif 'Error reading' in out:
		print "\t\t\tsecdiag read error"
	elif 'fee0200c =' in out[15]:
		# Brute force index values
		#print out[15][11:]
		count = int(out[15][11:], 16)
	else:	
		print "Tamper secdiag return not found."
	return count

def print_secdiag(flag):
	DRS=0; KW=1;SHEILD=2;LOTEMP=3;
	HITEMP=4
	BATLO=5
	BATHI=6
	EXTF=7
	TMP1=16;TMP2=17;TMP3=18;TMP4=19;TMP5=20;TMP6=21;
	if get_bit(flag, DRS) == 1:
                log.info( "DRS")
		print "DRS"
	if get_bit(flag, KW) == 1:
                log.info( "KW")
		print "KW"
	if get_bit(flag, SHEILD) == 1:
                log.info( "SHEILD")
		print "SHEILD"
	if get_bit(flag, LOTEMP) == 1:
                log.info( "LOTEMP")
		print "LOTEMP"	
	if get_bit(flag, HITEMP) == 1:
                log.info( "HITEMP")
		print "HITEMP"
	if get_bit(flag, BATLO) == 1:
                log.info( "BATLO")
		print "BATLO"
	if get_bit(flag, BATHI) == 1:
                log.info( "BATHI")
		print "BATHI"
	if get_bit(flag, EXTF) == 1:
                log.info( "EXTF")
		print "EXTF"		
	if get_bit(flag, TMP1) == 1:
                log.info( "TMP1")
		print "TMP1"		
	if get_bit(flag, TMP2) == 1:
                log.info( "TMP2")
		print "TMP2"		
	if get_bit(flag, TMP3) == 1:
                log.info( "TMP3")
		print "TMP3"		
	if get_bit(flag, TMP4) == 1:
                log.info( "TMP4")
		print "TMP4"		
	if get_bit(flag, TMP5) == 1:
                log.info( "TMP5")
		print "TMP5"		
	if get_bit(flag, TMP6) == 1:
                log.info( "TMP6")
		print "TMP6"		
	

def check_secdiag():
	flag = read_secdiag_val()
	print_secdiag(flag)
	
	
def set_tamper_trigger(num):
	input = '/opt/maxim-ic/basic/examples/secmon /dev/secmon 4 ' + str(num)
	if (get_ser().isOpen()==False):
                log.info( "\t\t\tserial not available")
                print "\t\t\tserial not available"
                return
	get_ser().write(input.encode('ascii')+'\n')
	time.sleep(1)
	out = get_ser().readlines()
	if 'Error Getting SEC_GET_STATUS' in out:
		print "\t\t\tsecmon read error"
	
def read_rtc_count():
	input = '/opt/maxim-ic/basic/examples/secmon /dev/secmon 3'
        if (get_ser().isOpen()==False):
                print "\t\t\tserial not available"
                log.info( "\t\t\tserial not available")
                return -1

	get_ser().write(input.encode('ascii')+'\n')
	time.sleep(2)
	out = get_ser().readlines()
	count = -1
	if not out:
                print "\t\t\tPossible reset"
                log.info( "\t\t\tPossible Reset")
        elif len(out) < 16:
                print "\t\t\tPossible reset too short"
                log.info( "\t\t\tToo Short Possible reset")
        elif 'Error Getting SEC_GET_STATUS' in out:
		print "\t\t\tsecmon read error"
	elif 'RTC' not in out[16]:
		print "secmon cmd not found"
	else:	
		count = int(out[16][6:]) #RTC
	return count

##################################################
#Main Code Here
##################################################

if __name__=='__main__':
	_ser_init()
	print "Tamper Readings"
	#print read_tamper_count()
	#print read_rtc_count()
	#print "RTC Above"
	#print set_tamper_trigger("f")
	flag = read_secdiag_val()
	print_secdiag(flag)
	
