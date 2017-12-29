import pywinusb.hid as hid
import time

count=0
target_vendor_id=0x0801
product_id=0x001B

try:
	print "Opening device"
	all_devices = hid.HidDeviceFilter(vendor_id = target_vendor_id).get_devices()
    #h = hid.device(vendor_id, product_id)
	print "hid.device"
#    print h

	if not all_devices:
		print("Can't find target device (vendor_id = 0x%04x)!" % target_vendor_id)
	else:
		for device in all_devices:
			try:
				device.open()

		print "Manufacturer: %s" % h.get_manufacturer_string()
		print "Product: %s" % h.get_product_string()
		print "Serial No: %s" % h.get_serial_number_string()
		GET_REP_REQ = [0xa1, 0x01, 0x09, 0x03, 0x00 , 0x00, 0x09]
		GET_DESC_STR = [0x80, 0x06, 0x02, 0x03, 0x09 , 0x04, 0x83]
		#SET_CNF_REQ = [0x00, 0x09, 0x01, 0x00, 0x00 , 0x00, 0x00]
		SET_CNF_REQ = [0x21, 0x09, 0x02, 0x03, 0x00 , 0x00, 0x02]

		# try writing some data to the device
		for k in range(2):
			#for i in [0x20, 0x21, 0x23, 0x80, 0x81, 0x82, 0xB0, 0xB2]:
			for i in [0,1]:
				for j in [0, 1]: 
					a = 0x80
					print "%x %x" % (i,  j)
					#print "SET_CNF_REQ"
					#print SET_CNF_REQ
					#h.write([i, 2, j])
					h.write([a, 0x0a, 0x00])
					#h.write(SET_CNF_REQ)
					d = h.read(5)
					#d = 0
					print "read"
					if d:
						print d
					time.sleep(0.05)

		print "Closing device"
		h.close()

except IOError, ex:
    print ex
    print "You probably don't have the hard coded test hid. Update the hid.device line"
    print "in this script with one from the enumeration list output above and try again."

print "Done"
