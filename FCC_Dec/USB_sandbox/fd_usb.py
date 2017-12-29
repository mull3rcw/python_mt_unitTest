import usb.core
import usb.util

#http://www.craftedge.com/products/libusb.html needed for Windows USB

# find our device
#dev = usb.core.find(idVendor=0xfffe, idProduct=0x0001)
#VendorID:0525 ProductID:a4ac rev:0310 is HCR-4
#dev = usb.core.find(find_all=True)
dev = usb.core.find(idVendor=0x0525, idProduct=0xA4AC)

# was it found?
if dev is None:
    raise ValueError('Device not found')
	
print( "dev is %s" % dev)

# set the active configuration. With no arguments, the first
# configuration will be the active one
dev.set_configuration()

# get an endpoint instance
cfg = dev.get_active_configuration()
intf = cfg[(0,0)]

ep = usb.util.find_descriptor(
    intf,
    # match the first OUT endpoint
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_OUT)

assert ep is not None

# write the data
#print ep.write('test')

# read the data
#data = ep.read()

msg = 'test'
#print ep.write(1, msg, 100)
ret = ep.read(0x81,4,10)

print("%s" % ret)
