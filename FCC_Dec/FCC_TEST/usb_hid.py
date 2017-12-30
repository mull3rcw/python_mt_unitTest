#Use this one


import usb.core
import usb.util
import pywinusb.hid as hid
import time

# find our device
# dev = usb.core.find(idVendor=0xfffe, idProduct=0x0001)

status = -1

def TM_readData(data):
	global status
#	print "RX->: "
#	print [hex (l) for l in data]
	if data[12] != 0:
		print "USB FAILED!!!"
		status = 1
		return None

	if data[15] != 0x3F:
		print "USB FAILED (tamper not ON)!!!" + data[15]
		status = 1
		return None

	if data[16] != 0xF:
		print "USB FAILED (tamper not ON)!!!" + data[16]
		status = 1
		return None

	if data[17] != 0x0:
		print "USB FAILED EXT!!!" + data[17]
		status = 1
		return None

	if data[18] != 0x0:
		print "USB FAILED INT!!!" + data[18]
		status = 1
		return None
		
	print "TM_USB PASSED!!!"
	status = 0
	return None

def SC_readData(data):
	global status
	#print "RX->: "
	#print [hex (l) for l in data]
	if data[12] != 0:
		print "SC USB FAILED!!!"
		status = 1
		return None
	print "SC USB PASSED!!!"
	status = 0
	return None


def usb_hid_test(app, cmd):
	cvendor_id=0x0801
	cproduct_id=0x001B
	#print app
	#print cmd
	#dev = usb.core.find(idVendor=cvendor_id, idProduct=cproduct_id)
	dev = hid.HidDeviceFilter(vendor_id = 0x0801, product_id = 0x001B).get_devices()[0]
	# was it found?
	if dev is None:
		raise ValueError('Device not found')

	#hid.set_configuration()
	dev.open()
	
	report = dev.find_feature_reports()[0]

	#ICC STATUS
	if app == 6:
		dev.set_raw_data_handler(SC_readData)
	else:
		dev.set_raw_data_handler(TM_readData)	

	buffer = bytearray.fromhex(u' 05 C0 01 01 C1 01 06 C2 01 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00')
	buffer[0] = 05
	buffer[6] = app
	buffer[9] = cmd
	
	report.set_raw_data(buffer)
	report.send()

	time.sleep(1)


	#TAMPER
	
#	buffer = bytearray.fromhex(u' 05 C0 01 01 C1 01 01 C2 01 3F 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00')
#	buffer[0] = 05
#	report.set_raw_data(buffer)
#	report.send()

#	time.sleep(1)
	
	
	
	dev.close()
	return status

if __name__=='__main__':
	print "ret is: " + str(usb_hid_test(6,1))
	print "ret is: " + str(usb_hid_test(1,0x3F))