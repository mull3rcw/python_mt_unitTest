#Use this one


from ethernet_commands import eth_test
from usb_hid import usb_hid_test

if __name__=='__main__':
	usb_pass = 0
	sc_pass = 0
	eth_pass = 0
	tm_pass = 0

	ret = usb_hid_test(6,1)
	if ret == 0:
		usb_pass +=1
		sc_pass+=1
	elif ret == 1:
		usb_pass+=1
	elif ret == 2:
		usb_pass+=1


	print "ret is: " + str(usb_hid_test(6,1))
	print "ret is: " + str(usb_hid_test(1,0x3F))
	print "ret is: " + str(eth_test(6,1))
	print "ret is: " + str(eth_test(1,0x3F))
	print "usb_pass is : " + str(usb_pass)
