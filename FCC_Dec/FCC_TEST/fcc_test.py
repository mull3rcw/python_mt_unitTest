#Use this one
from ethernet_commands import eth_test
from usb_hid import usb_hid_test


iterate = 3
usb_pass = 0
usb_fail = 0
sc_pass = 0
sc_fail = 0
eth_pass = 0
eth_fail = 0
tm_pass = 0
tm_fail = 0
sc_pass = 0
sc_fail = 0


def run_fcc():
	global usb_pass
	global usb_fail
	global sc_pass
	global sc_fail
	global eth_pass
	global eth_fail
	global tm_pass
	global tm_fail
	global sc_pass
	global sc_fail
	ret = 0

	#USB SC
	ret = usb_hid_test(6,1)
	if ret['usb_ok'] != -1:
		usb_pass += ret['usb_ok']
		usb_fail += not ret['usb_ok']
		sc_pass += ret['scard_ok']
		sc_fail += not ret['scard_ok']
	else:
		usb_fail +=1

	#USB Tamper
	ret = usb_hid_test(1, 0x3F)
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

	print "usb_pass is : " + str(usb_pass)
	print "usb_fail is : " + str(usb_fail)
	print "eth_pass is : " + str(eth_pass)
	print "eth_fail is : " + str(eth_fail)
	print "tm_pass is : " + str(tm_pass)
	print "tm_fail is : " + str(tm_fail)
	print "sc_pass is : " + str(sc_pass)
	print "sc_fail is : " + str(sc_fail)

if __name__=='__main__':

	for i in range(iterate):
		run_fcc()
