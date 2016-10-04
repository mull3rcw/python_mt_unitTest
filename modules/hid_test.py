from pywinusb import hid

filter = hid.HidDeviceFilter(vendor_id = 0x0525, product_id = 0xA4AC)
hid_device = filter.get_devices()
#device = hid_device[0]
#hid_device.open()
#print(hid_device)






filter = hid.HidDeviceFilter(vendor_id = 0x0801, product_id = 0x3004)
devices = filter.get_devices()
print devices


if devices:
    device = devices[0]
    print "success"

device.open()
out_report = device.find_output_reports()[0]

buffer= [0x00]*65
buffer[0]=0x0
buffer[1]=0x01
buffer[2]=0x00
buffer[3]=0x01

out_report.set_raw_data(buffer)
out_report.send()
dev.close()