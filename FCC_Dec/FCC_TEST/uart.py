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
import struct
from serial import SerialException

#convert string to hex
def toHex2(text):
	s=binascii.unhexlify(text)
	#print s
	return [hex(ord(x)) for x in s]	

def ser_test(app, cmd):
	#Compares need to be against strings, and lower case apparently
	status = {'scard_ok':-1, 'ser_ok':-1}
	#print 'Please enter IP address: '
	
	port = "COM13"   #Windows com port format was 13
	baud = 9600		#make sure it's the same for both side

	try:
		ser = serial.Serial(port, baud, timeout=10) #Block for 10 second when read
	except SerialException:
		return status

	if not ser.isOpen():
		print(ser.name + ' is NOT open...')

	buffer = bytearray.fromhex(u'C0 01 01 C1 01 01 C2 01 3F')
	buffer[5] = app
	buffer[8] = cmd
		
	#ser.write(binascii.hexlify(buffer) + '\r\n')
	ser.write(binascii.hexlify(buffer) + '\n')
	
	if app == 6:
		out  = ser.read(24) #how many bytes expect to read
	else:
		out  = ser.read(36) #how many bytes expect to read
	ser.close()
	time.sleep(1)
	
	#ICC STATUS
	data = toHex2(out)
	#print data
	if app == 6:
		#print "SC"
		if data == []:
			status = {'scard_ok':0, 'ser_ok':-1}
		elif data[11] != '0x0':
			print "SC SER FAILED!!! " + str(int(data[11], 16))
			#for i in range(12):
			#	print data[i]
			status = {'scard_ok':0, 'ser_ok':1}
		else:
			#print "SC SER PASSED!!!"
			status = {'scard_ok':1, 'ser_ok':1}
	else:
		#TAMPER
		#print "Tamper"
		if data == []:
			status = {'tamper_ok':0, 'ser_ok':-1}
		elif data[11] != '0x0':
			print "SER FAILED!!!"
			status = {'tamper_ok':0, 'ser_ok':0}
		elif data[14] != '0x3f':
			print "SER FAILED (tamper not ON)!" + data[14]
			status = {'tamper_ok':0, 'ser_ok':1}
		elif data[15] != '0xf':
			print "SER FAILED (tamper not ON)!!!" + data[15]
			status = {'tamper_ok':0, 'ser_ok':1}
		elif data[16] != '0x0':
			print "SER FAILED EXT!!!" + data[16]
			status = {'tamper_ok':0, 'ser_ok':1}
		elif data[17] != '0x0':
			print "SER FAILED INT!!!" + data[17]
			status = {'tamper_ok':0, 'ser_ok':1}
		else:
			#print "TM SER PASSED!!!"
			status = {'tamper_ok':1, 'ser_ok':1}
		
	time.sleep(1)
	return status

if __name__=='__main__':
	#print "ret is: " + str(ser_test(6,1))
	print "ret is: " + str(ser_test(1,0x3F))


