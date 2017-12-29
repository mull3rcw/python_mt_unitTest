#Use this one


import usb.core
import usb.util
import pywinusb.hid as hid
import time

# find our device
# dev = usb.core.find(idVendor=0xfffe, idProduct=0x0001)

def readData(data):
	#print "RX->: "
	#print [hex (l) for l in data]
	if data[12] != 0:
		print "USB FAILED!!!"
		return None
	print "USB PASSED!!!"
	
	return None


cvendor_id=0x0801
cproduct_id=0x001B
#dev = usb.core.find(idVendor=cvendor_id, idProduct=cproduct_id)
dev = hid.HidDeviceFilter(vendor_id = 0x0801, product_id = 0x001B).get_devices()[0]
# was it found?
if dev is None:
    raise ValueError('Device not found')

#hid.set_configuration()
dev.open()
dev.set_raw_data_handler(readData)

report = dev.find_feature_reports()[0]

#ICC STATUS
buffer = bytearray.fromhex(u' 05 C0 01 01 C1 01 06 C2 01 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00')
buffer[0] = 05
report.set_raw_data(buffer)
report.send()

time.sleep(1)
dev.close()