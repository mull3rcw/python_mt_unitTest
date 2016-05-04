#!/usr/bin/python
import sys
import usb.core, time
from log_cm import set_log_info, set_log_level, get_log_cm


# find USB devices
dev = usb.core.find(find_all=True)
# loop through devices, printing vendor and product ids in decimal and hex
for cfg in dev:
	sys.stdout.write('Decimal VendorID=' + str(cfg.idVendor) + ' & ProductID=' + str(cfg.idProduct) + '\n')
	sys.stdout.write('Hexadecimal VendorID=' + hex(cfg.idVendor) + ' & ProductID=' + hex(cfg.idProduct) + '\n\n')
  
 
prev_dev = "Not Init"
known_val = "Hexadecimal VendorID=0x525 & ProductID=0xa4ac"

usb_count = 0;


while (1):
	dev = usb.core.find(find_all=True)
	time.sleep(1)
	if prev_dev == "Not Init":
		for cfg in dev:
			sys.stdout.write("idVendor %s\n\n" % cfg.idVendor)
			if cfg.idVendor == 0x0525:
				prev_dev = cfg
				usb_count += 1
	elif prev_dev != "Not Init":
		for cfg in dev:
			if cfg is None:
				get_log_cm().error('\t\t\tUSB Device not found')
			elif cfg is 'NoneType':
				get_log_cm().error('\t\t\tUSB Device noneType found')
			else:
				sys.stdout.write( "PREV VENDOR %s\n" % prev_dev.idVendor)
				sys.stdout.write("cfg VENDOR %s\n" % cfg.idVendor)
				if prev_dev.idVendor == cfg.idVendor and prev_dev.idProduct == cfg.idProduct:
					usb_count += 1
					
	sys.stdout.write("count %d\n\n" % usb_count)

  
  
  