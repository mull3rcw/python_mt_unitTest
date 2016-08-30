#!/usr/bin/python
 
import os
import sys
import time
 
import usb.core
import usb.util
 
 
 
packet_len = 64
 
# Packing a request. Please see HexWax documentation for the list of all commands
# Packets are 64 bytes long, most of the commands are 4 bytes long. So up to 18
# can be batched into a packet. For example command with bytes [0x94, 0x0, 0x0, 0x0]
# is getting firmware id
def pack_request(*arguments):
    packet = [0x0] * packet_len
    i = 0
    for arg in arguments:
        packet[i] = arg
        i += 1
    #packet[0:4] = [0x94, 0x0, 0x0, 0x0] #get firmware id
    return ''.join([chr(c) for c in packet])
 
# Logs error to the error output
def log_error(functionName, ret):
    sys.stderr.write(functionName + (" failed with return code %d\n" % ret))
 
# Logs result onto standard output. Result is 64 bytes as decimal numbers
# Response is 64 bytes long
def show_result(bytes):
    sys.stdout.write("Result:")
    sys.stdout.write(''.join(['%d ' % abyte for abyte in bytes]))
 
# Turns LED on the bord on or off depending on input parameter on. 0 is turning
# the led on 1 is turning it off. The command is 0x9F set port bit (set output
# pin value), port is 0x03 (port C), 0x06 is bit index (so this is 7th bit),
# and the last bit is 0 for clear, 1 for set
def set_led(on, dev):
    if on:
        param = 0x00
    else:
        param = 0x01
 
    raw = pack_request(0x9F, 0x03, 0x06, param) #set port bit - 0 to turn it on 1 to turn it off
 
    dev.write(1, raw, 0, 100)
 
    bytes = dev.read(0x81, packet_len, 0, 100)
    show_result(bytes)
 
 
 
def main():
    #initialising debuging - don't have a clue if this will work
    #os.environ['PYUSB_LOG_FILENAME'] = 'debug'
	
	#dev = usb.core.find(idVendor=0x0525, idProduct=0xA4AC)
	dev = usb.core.find(idVendor=0x05AC, idProduct=0x12A8)
	#VendorID:05AC ProductID:12a8 rev:0702 is Apple

	if dev is None:
		raise ValueError('Device not found')
	try:
		dev.detach_kernel_driver(0)
	except: # this usually mean that kernel driver has already been dettached
		pass
 
    # set the active configuration, the device has 2 configurations you can see them
    # by using: lsusb -vvv -d 0x0b40:
    # this device has configurations 1 and 2 I'm using the first one, not sure at the
    # moment if 2nd would work the same
	dev.set_configuration(1)
 
 
    #removed following lines if you're running this from command line
    #my netbeans didn't want to show standard output so I had to redirect it to
    #a file
	fsock = open('out.log', 'w')
	sys.stdout = fsock
	fsock2 = open('out.err', 'w')
	sys.stderr = fsock2
 
 
    #prepare our own command - this is get firmware id, only the first byte is
    #significant
	raw = pack_request(0x94)
	
	#send the packet
	#dev.write(1,raw,0,100)
	#dev.write(1,raw,0,10)
		
    #then read the result
	#bytes = dev.read(0x81, packet_len, 0, 100)
	#show_result(bytes)
 
    #prepare another request
    #set register TRISC bit 6 - port C bit 6 to be output
    #mind though 0x9B command can be used to write any register, so check the
    #microcontroller's datasheet
	raw = pack_request(0x9B, 0x94, 0x06, 0x00)
 
	#dev.write(1,raw,0,100)
	#dev.write(1,raw,0,100)
	
	msg = 'test'
	#print len(dev.write(1, msg, 100)) == len(msg)
	print dev.write(1, msg, 100)
	ret = dev.read(0x81, len(msg), 100)
 
	print ret
 
	#bytes = dev.read(0x81, packet_len, 0, 100)
	#show_result(bytes)
 
 
    #once we have our bit set as output we can control it. Here, LED is turned
    #on and then turned off after a second and it's done 10 times
	#for i in range(10):
	#	set_led(True, dev)
	#	time.sleep(1)
	#	set_led(False, dev)
	#	time.sleep(1)
 
    #done
 
 
if __name__ == '__main__':
	main()