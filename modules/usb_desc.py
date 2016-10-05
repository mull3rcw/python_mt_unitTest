import usb.core
import usb.util

# find our device
dev = usb.core.find(idVendor=0x0801, idProduct=0x3003)

# was it found?
if dev is None:
    raise ValueError('Device not found')
else:
	print "Found it"
	
#print dev
# set the active configuration. With no arguments, the first
# configuration will be the active one
dev.set_configuration()

# get an endpoint instance
cfg = dev.get_active_configuration()
intf = cfg[(0,0)]

ep_o = usb.util.find_descriptor(
    intf,
    # match the first OUT endpoint
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_OUT)

assert ep_o is not None

ep_i = usb.util.find_descriptor(
    intf,
    # match the first OUT endpoint
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_IN)

assert ep_i is not None



# write the data
output = '124365'
ep_o.write(output)
print "write " + output
rd =  ep_i.read(0x81)
print "read"
#print str(rd)
conv = (chr(w) for w in rd)
print ', '.join(map(str, conv))
print "done"