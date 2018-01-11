import usb.core
import usb.util

# find our device
dev = usb.core.find(idVendor=0x0801, idProduct=0x3004)

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
#output = 1,2,4,3,6,5
scout = 'C0 01 01 C1 01 06 C2 01 01'
#sendCommand = bytearray.fromhex(u'C0 01 01 C1 01 06 C2 01 01') #simple SC command
sendCommand = bytearray.fromhex(scout) #simple SC command
output = '987643'
#ep_o.write(output)
ep_o.write(sendCommand)
print "write " 
#print output
print scout

rd =  ep_i.read(0x81)
print "read"
#print rd
#print str(rd)
#conv = (str(w) for w in rd)
for w in rd:
	print hex(w)
#print ', '.join(map(hex, conv))
#print ', '.join(conv)
print "done"