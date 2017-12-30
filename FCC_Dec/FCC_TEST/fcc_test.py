#Use this one


from ethernet_commands import eth_test
from usb_hid import usb_hid_test

if __name__=='__main__':
	print "ret is: " + str(usb_hid_test(6,1))
	print "ret is: " + str(usb_hid_test(1,0x3F))
	print "ret is: " + str(eth_test(6,1))
	print "ret is: " + str(eth_test(1,0x3F))