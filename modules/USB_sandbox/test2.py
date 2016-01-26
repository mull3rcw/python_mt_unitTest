#!/usr/bin/python
import usb.core
import usb.core
import usb.util
import sys
import time
 
# find our device
#VendorID:0525 ProductID:a4ac rev:0310 is HCR-4
#dev = usb.core.find(idVendor=0x05AC, idProduct=0x12A8) #iPhone
dev = usb.core.find(idVendor=0x0525, idProduct=0xA4AC) #HCR-4 
#dev = usb.core.find(idVendor=0x0403, idProduct=0x6001) #HCR-4 FTDI
#dev = usb.core.find(idVendor=0x0423, idProduct=0x0107) #Teledyne

#print dev 

if dev is None:
    raise ValueError('Device not found')


try: 
	dev.detach_kernel_driver(0)
except Exception, e:
	pass # already unregistered
dev.set_configuration()

usb_count = 0
total_count = 0
prev_dev = dev
while True:
		#dev = usb.core.find(idVendor=0x0525, idProduct=0xA4AC) #HCR-4 
		#dev = usb.core.find()
		#if dev is None:
		#	raise ValueError('Device not found')
		if dev != "Not Init":
			#if prev_dev eq dev:
			if prev_dev.idVendor == dev.idVendor and prev_dev.idProduct == dev.idProduct:
				usb_count += 1
				print "  idVendor: %d (0x%04x)" % (dev.idVendor, dev.idVendor)
				print "  idProduct: %d (0x%04x)" % (dev.idProduct, dev.idProduct)
			else:
				print "No Match %s" % dev.idVendor
		#else:
		prev_dev = dev 
		print "Update prev_dev"
			
		print( "USB Count = \t\t\t%d of %d", usb_count, total_count)
		print 'USB Count = %d of %d' % (usb_count, total_count)
		time.sleep(2)