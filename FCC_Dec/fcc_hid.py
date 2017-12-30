#Can send HID to device

import pywinusb.hid as hid
#import hid
import usb.core
import usb.util

##   usb device 
VId = 0x0801
PId = 0x001B
 
print('searching for device')
 
filter = hid.HidDeviceFilter(vendor_id = VId, product_id = PId)
dev = usb.core.find(idVendor=VId, idProduct=PId)

hid_device = filter.get_devices()
device = hid_device[0]
device.open()
##   Setup communication     ##
 # datapipe allowing 64 byte data of any format #
target_usage = hid.get_full_usage_id(0x00, 0x40)
#print(target_usage)
#print('1')
report = device.find_feature_reports()
#print(report)
#print(report[0])
#print('2')
buffer = bytearray.fromhex(u' 05 C0 01 01 C1 01 06 C2 01 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00')
buffer[0] = 05
print('3')
print str(buffer)
print('4')
report[0].set_raw_data(buffer)
CTRL_LOOPBACK_WRITE = 0x05
#dev.ctrl_transfer(0x05, CTRL_LOOPBACK_WRITE, 0, 0, buffer)
report[0].send()
print('5')
#dev.hid_get_feature_report(dev, msg)



 
def writer(x):
    buffer[0]=x
    report[0].set_raw_data(buffer)
    report.send()