import pywinusb.hid as hid
##   usb device 
VId = 0x0801
PId = 0x001B
 
#def sample_handler(data):
 #   print("Raw data: {0}".format(data))
def readData(data):
	print "Over here"
	print(data)
	return None
 
 
 
print('searching for device')
 
filter = hid.HidDeviceFilter(vendor_id = VId, product_id = PId)
hid_device = filter.get_devices()
device = hid_device[0]
device.open()
##   Setup communication     ##
 # datapipe allowing 64 byte data of any format #
target_usage = hid.get_full_usage_id(0x00, 0x40)
#device.set_raw_data_handler(sample_handler)
print(target_usage)
print('1')
report = device.find_feature_reports()
print(report)
print(report[0])
print('2')
buffer = [0xFF]*64
buffer[0] = 05
print('3')
print(buffer)
print('4')
report[0].set_raw_data(buffer)
report[0].send()
print('5')
 
def writer(x):
    buffer[0]=x
    report[0].set_raw_data(buffer)
    report.send()