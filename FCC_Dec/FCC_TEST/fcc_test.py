#Use this one
import sys, time, datetime
#logging
from logging_fcc import set_log_info, log_date, get_log
from ethernet_commands import eth_test
from usb_hid import usb_hid_test
#from serial_fcc import ser_Init, get_ser, log, set_log_info, uart_self_test
from uart import ser_test

#Logging setup
myts = time.time()	
myst = datetime.datetime.fromtimestamp(myts).strftime('%Y-%m-%d+%H_%M_%S')

my_path = 'fcc_log\\'
my_name = 'fcc_test'
my_file = my_path+my_name+str(myst)+'.log'

iterate = 100

usb_pass = 0
usb_fail = 0
ser_pass = 0
ser_fail = 0
eth_pass = 0
eth_fail = 0
tm_pass = 0
tm_fail = 0
sc_pass = 0
sc_fail = 0
test_count = 0

def run_fcc():
	global test_count
	global usb_pass
	global usb_fail
	global ser_pass
	global ser_fail
	global eth_pass
	global eth_fail
	
	global tm_pass
	global tm_fail
	global sc_pass
	global sc_fail
	ret = 0

	#ser SC
	ret = ser_test(6,1)
	if ret['ser_ok'] != -1:
		ser_pass += ret['ser_ok']
		ser_fail += not ret['ser_ok']
		sc_pass += ret['scard_ok']
		sc_fail += not ret['scard_ok']
	else:
		ser_fail +=1

	#ser Tamper
	ret = ser_test(1, 0x3F)
	if ret['ser_ok'] != -1:
		ser_pass += ret['ser_ok']
		ser_fail += not ret['ser_ok']
		tm_pass += ret['tamper_ok']
		tm_fail += not ret['tamper_ok']
	else:
		ser_fail +=1
	
	#USB SC
	ret = usb_hid_test(6,1)
	if ret['usb_ok'] != -1:
		usb_pass += ret['usb_ok']
		usb_fail += not ret['usb_ok']
		try:
			sc_pass += ret['scard_ok']
			sc_fail += not ret['scard_ok']
		except:
			log.info("Don't Update")
	else:
		usb_fail +=1

	#USB Tamper
	ret = usb_hid_test(1, 0x3F)
	#log.info ret
	if ret['usb_ok'] != -1:
		usb_pass += ret['usb_ok']
		usb_fail += not ret['usb_ok']
		tm_pass += ret['tamper_ok']
		tm_fail += not ret['tamper_ok']
	else:
		usb_fail +=1

	#ETH SC
	ret = eth_test(6,1)
	if ret['eth_ok'] != -1:
		eth_pass += ret['eth_ok']
		eth_fail += not ret['eth_ok']
		sc_pass += ret['scard_ok']
		sc_fail += not ret['scard_ok']
	else:
		eth_fail +=1

	#ETH Tamper
	ret = eth_test(1, 0x3F)
	if ret['eth_ok'] != -1:
		eth_pass += ret['eth_ok']
		eth_fail += not ret['eth_ok']
		tm_pass += ret['tamper_ok']
		tm_fail += not ret['tamper_ok']
	else:
		eth_fail +=1

	test_count+=1
	log_date(log)
	log.info("/*** \t\tTEST NUMBER " + str(test_count) + '\t\t\t ***/')
	log.info ("\t\t\tpass \t	fail")
	log.info ("usb interface\t\t" + str(usb_pass) + "\t\t" + str(usb_fail))
	log.info ("eth interface\t\t" + str(eth_pass) + "\t\t" + str(eth_fail))
	log.info ("ser interface\t\t" + str(ser_pass) + "\t\t" + str(ser_fail))
	log.info ("Tamper\t\t\t" + str(tm_pass) + "\t\t" + str(tm_fail))
	log.info ("SmartCard\t\t" + str(sc_pass) + "\t\t" + str(sc_fail) + "\n")
	
	#print ("/*** \t\tTEST NUMBER " + str(test_count) + '\t\t\t ***/')
	#print ("\t\t\tpass \t	fail")
	#print ("usb interface\t\t" + str(usb_pass) + "\t\t" + str(usb_fail) + "\n")
	#print ("eth interface\t\t" + str(eth_pass) + "\t\t" + str(eth_fail) + "\n")
	#print ("ser interface\t\t" + str(ser_pass) + "\t\t" + str(ser_fail) + "\n")
	#print ("Tamper\t\t" + str(tm_pass) + "\t\t" + str(tm_fail) + "\n")
	#print ("SmartCard\t\t" + str(sc_pass) + "\t\t" + str(sc_fail) + "\n")

	
if __name__=='__main__':

	
	#uart_self_test()
	for arg in sys.argv[1:]:
		if not arg:
			log.info("no arg")
			iterate = 100
		else:
			print("get arg")
			iterate = int(sys.argv[1])
			for arg in sys.argv[1:]:
				print(arg)

	log = set_log_info(my_path, my_name)
	log.info(iterate)
	for i in range(iterate):
		run_fcc()
