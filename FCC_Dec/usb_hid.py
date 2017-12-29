import usb.core
import usb.util
import pywinusb.hid as hid

# find our device
# dev = usb.core.find(idVendor=0xfffe, idProduct=0x0001)

def readData(data):
    print(data)
    return None




cvendor_id=0x0801
cproduct_id=0x001B
#dev = usb.core.find(idVendor=cvendor_id, idProduct=cproduct_id)
dev = hid.HidDeviceFilter(vendor_id = 0x0801, product_id = 0x001B).get_devices()[0]
# was it found?
if dev is None:
    raise ValueError('Device not found')

#dev.set_configuration()
#dev.set_raw_data_handler(readData)

report = dev.find_output_reports()[0]

buffer= [0xFF]*33 # 33 = report size + 1 byte (report id)
buffer[0]=0x0 # report id
buffer[1]=0xFE
buffer[2]=0x00
buffer[3]=0xFF
out_report.set_raw_data(buffer)
out_report.send()
dev.close()




cfg=dev[0]
intf=cfg[(0,0)]
ep=intf[0]




#dev.write(ep.bEndpointAddress, [0x00, 0x00,0x04,0x04,0xFF,0xFF,0xFF,0x00, 0x00], 1000)
#dev.ctrl_transfer(bmRequestType, bRequest, wValue=0, wIndex=0, data_or_wLength=None, timeout=None)

print("print ep")
print(ep)
print("print cfg")
print(cfg)
print("print intf")
print(intf)