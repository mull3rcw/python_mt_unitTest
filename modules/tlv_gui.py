#NOTE:
#For some reason it's not able to read when this script is run
#in the ubuntu VM (writing is fine).
#So please run it on your Windows host machine if you wish to
#test reading.
#By default, the pyserial module is not included in your
#python installation. You need to install it before you
#can run this script.
#For reference on the pyserial installation:
#http://www.instructables.com/id/The-Arduino-Internet-Gizmo/step19/Installing-the-software/

import serial, time
import binascii

#port = "/dev/ttyS0" #Linux com port format
port = "COM1"   #Windows com port format
baud = 9600                        #make sure it's the same for both side

ser = serial.Serial(port, baud, timeout=1) #Block for 10 second when read
if ser.isOpen():
     print(ser.name + ' is open...')


#sendCommand = bytearray.fromhex(u'c0 09 09 09 09 09 09 09 09 09 c0')
#sendCommand = bytearray.fromhex(u'C0 DB DC 01 01 C1 01 04 C2 01 12 C0') #simple MSR command
sendCommand = bytearray.fromhex(u'C0 01 01 C1 01 06 C2 01 01') #simple SC command
#sendCommand = bytearray.fromhex(u'C0 DB DC 01 01 C1 01 06 C2 01 01 C0') #simple SC command SLIP

# C0 = DB DC
# DB = DB DD


def convert_to_slip (raw):
	slip = bytearray(b'')
	#Add opening C0
	slip.append(0xC0)
	for i in raw:
		if i == 0xC0:
			slip.append(0xDB)
			slip.append(0xDC)
		elif i == 0xDB:
			slip.append(0xDB)
			slip.append(0xDD)
		else:
			slip.append(i)
	#Add closing C0
	slip.append(0xC0)

	return slip

def get_byte(val, index):
	return val[index*2:(index*2)+2]

def convert_to_raw (slip):
	raw = bytearray(b'')
	print "C2R %s" % (binascii.hexlify(bytearray(slip)))
	val = (binascii.hexlify(bytearray(slip)))
	#for i in binascii.hexlify(bytearray(slip)):
	skip = 0
	for j in range(0,len(slip)):
		#collect 8bits per time.
		#i = val[j*2:(j*2)+2]
		i = get_byte(val, j)


		if skip == 1:
			skip = 0
			continue

		if not i:
			continue
		#print i
		n = get_byte(val, j+1)
		if i == 'db':
			#print "FOUND DB n is " + n
			if n == 'dc':
			#	print "FOUND DC"
				raw.append(0xC0)
				skip =1
			elif n == 'dd':
				raw.append(0xDB)
				skip =1
			elif n == 'de':
				raw.append(0x11)
				skip =1
			elif n == 'df':
				raw.append(0x13)
				skip =1
			else:
				print "Issue!! ESCAPE invalid " + n
				exit()
		elif i != 'c0':
			raw.append(int(i,16))

	return raw


print "Sending %s" % (binascii.hexlify(sendCommand))

slip_data = convert_to_slip(sendCommand)
while True:
########## sending #######################
	ser.write(slip_data)
########## receiving #####################
	#out  = ser.readline()
	out  = ser.readline()
	raw_out = convert_to_raw(out)

#	for i in out:
#		print "-> " + binascii.hexlify(i)

	for i in raw_out:
		print "-> %x" % i

	time.sleep(10)
	print "write again\n"

