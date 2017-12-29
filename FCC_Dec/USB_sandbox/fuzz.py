#!/usr/bin/python
import usb.core
import usb.util
import sys
 
# find our device
#VendorID:0525 ProductID:a4ac rev:0310 is HCR-4
#dev = usb.core.find(idVendor=0x05AC, idProduct=0x12A8)
dev = usb.core.find(idVendor=0x0525, idProduct=0xA4AC)
print dev 

if dev is None:
    raise ValueError('Device not found')

#try: 
#	dev.detach_kernel_driver(0)
#except Exception, e:
#	pass # already unregistered
dev.set_configuration()

# Let's fuzz around! 
 
# Lets start by Reading 1 byte from the Device using different Requests
# bRequest is a byte so there are 255 different values
for bRequest in range(255):
	try:
		ret = dev.ctrl_transfer(0xC0, bRequest, 0, 0, 1)
		print "bRequest ",bRequest
		print ret
	except:
       # failed to get data for this request
		print("Fail %x" % bRequest)  
		pass
