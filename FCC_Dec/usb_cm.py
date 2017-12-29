import hid
import time

count=0
vendor_id=0x0801
product_id=0x001B

#for d in hid.enumerate(vendor_id=2049, product_id=12292):
#    count+=1
#    print ("enum #%d" % count)
#    keys = d.keys()
#    keys.sort()

#    for key in keys:
#        print " %s : %s" % (key, d[key])
#    print ""
#    print "hid.enum"
#    print d

try:
    print "Opening device"
    h = hid.device(vendor_id, product_id)
    print "hid.device"
#    print h
    h.open(vendor_id, product_id)
    #h.open_path("/dev/hidg0")
    #h.open_path("\\?\hid#vid_0801&pid_3004#6&355df3ea&1&0000#{4d1e55b2-f16f-11cf-88cb-001111000030}")
    #h.open(1267, 4369) #ELAN
    #h.open(0x1941, 0x8021) # Fine Offset USB Weather Station

    print "Manufacturer: %s" % h.get_manufacturer_string()
    print "Product: %s" % h.get_product_string()
    print "Serial No: %s" % h.get_serial_number_string()
    GET_REP_REQ = [0xa1, 0x01, 0x09, 0x03, 0x00 , 0x00, 0x09]
    GET_DESC_STR = [0x80, 0x06, 0x02, 0x03, 0x09 , 0x04, 0x83]
    #SET_CNF_REQ = [0x00, 0x09, 0x01, 0x00, 0x00 , 0x00, 0x00]
    SET_CNF_REQ = [0x21, 0x09, 0x02, 0x03, 0x00 , 0x00, 0x02]
	
    sendCommand_tamper = \
	bytearray.fromhex(u'05 C0 01 01 C1 01 01 C2 01 3F 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00')
	

    get_ip = bytearray.fromhex(u'05 c0 01 01 c1 01 00 c2 01 18 c3 01 00 c4 0d 01 31 30 2e 35 37 2e 32 32 2e 31 32 33 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00')
	
    # try non-blocking mode by uncommenting the next line
    #h.set_nonblocking(1)

    # try writing some data to the device
	
    #h.write(sendCommand_tamper)
    #done()
	
	
    for k in range(2):
        #for i in [0x20, 0x21, 0x23, 0x80, 0x81, 0x82, 0xB0, 0xB2]:
        for i in [0,1]:
            for j in [2, 5]: 
                #a = 0x80
                a = 0x02
                print "%x %x" % (i,  j)
                #print "SET_CNF_REQ"
                #print SET_CNF_REQ
                h.write([j, 2, j])
                #h.write([a, 0x0a, 0x00])
                h.write(SET_CNF_REQ)
                #d = h.read(5)
                d = 0
                print "read"
                if d:
                    print d
                time.sleep(1)

    print "Closing device"
    h.close()

except IOError, ex:
    print ex
    print "You probably don't have the hard coded test hid. Update the hid.device line"
    print "in this script with one from the enumeration list output above and try again."

print "Done"