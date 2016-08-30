#! python
import time, datetime
from log_cm import set_log_info, set_log_level, get_log_cm
from serial_cm import ser_Init, get_ser, Hcr4SendCMD, _ser_init

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

def read_stest_count():
	if (get_ser().isOpen()==False):
		get_log_cm().error("serial not available")
		return -1

	# send UART request
	input = '/opt/maxim-ic/basic/examples/ucl_example'
	get_ser().write(input.encode('ascii')+'\n')
	time.sleep(1)

	out = get_ser().readlines()
	#generator: creates "matches list" only if parsed TMP info present.
	#print "Out is %s" % out
	valid = [v for v in out if "DES" in v]
	passed = [x for x in out if "PASSED" in x]
	fails = [z for z in out if "FAILED" in z]
	#if not matches:
	if not valid:
		get_log_cm().error("\t\t\t(read_stest_count)Possible reset")
		return -1
	elif not fails:	
		#Passes
		count = 0
	else:
		count = 0
		#Count each Failure detected
		for y in fails:
			count += 1
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

##One time setup
	my_path = '..\\sec_mon_log\\'
	my_name = 'sec_mon_test'
	set_log_info(my_path, my_name, 0)

#	ser_Init()
	_ser_init()
	get_log_cm().info("Crypto Test")
	get_log_cm().info(read_stest_count())
	print read_stest_count()
	#print test1()

