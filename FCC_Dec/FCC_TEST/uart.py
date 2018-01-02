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
def toHex(s):
	lst = []
	for ch in s:
		hv = hex(ord(ch)).replace('0x', ' ')
		if len(hv) == 1:
			hv = '0'+hv
		lst.append(hv)
	return reduce(lambda x,y:x+y, lst)

#convert string to hex
def toHex2(text):
	s=binascii.unhexlify(text)
	#print s
	return [hex(ord(x)) for x in s]	

	
	
#convert hex repr to string
def toStr(s):
	return s and chr(int(s[:2], base=16)) + toStr(s[2:]) or ''
	
def mHex(s):
	
	return " ".join(hex(ord(n)) for n in text)

def ser_test(app, cmd):
	status = {'scard_ok':-1, 'ser_ok':-1}
	#print 'Please enter IP address: '
	
	port = "COM13"   #Windows com port format 
	baud = 9600		#make sure it's the same for both side

	try:
		ser = serial.Serial(port, baud, timeout=10) #Block for 10 second when read
	except SerialException:
		return status

	if ser.isOpen():
		print(ser.name + ' is open...')
		

	buffer = bytearray.fromhex(u'C0 01 01 C1 01 01 C2 01 3F')
	buffer[5] = app
	buffer[8] = cmd

	ser.write(buffer + '\r\n')
	#ser.write(buffer)
	print "write->"
	print binascii.hexlify(buffer)
	#print buffer
	if app == 6:
		out  = ser.read(24) #how many bytes expect to read
	else:
		out  = ser.read(30) #how many bytes expect to read
	ser.close()
	print "<-read"
	#print(out)   ##for outputing ascii characters
	print "toHex2->"
	print toHex2(out)

	time.sleep(1)
	
	#ICC STATUS
	data = toHex2(out)
	print data
	if app == 6:
		print "SC"
		if data == []:
			status = {'scard_ok':0, 'ser_ok':-1}
		elif data[11] != '0x0':
			print "SC SER FAILED!!"
			print "data[11] is ->"
			print data[11]
			for i in range(12):
				print data[i]
			
			status = {'scard_ok':0, 'ser_ok':1}
		else:
			#print "SC SER PASSED!!!"
			status = {'scard_ok':1, 'ser_ok':1}
	else:
		#TAMPER
		print "Tamper"
		if data == []:
			status = {'tamper_ok':0, 'ser_ok':-1}
		elif data[11] != 0:
			print "SER FAILED!!!"
			status = {'tamper_ok':0, 'ser_ok':0}
		elif data[14] != 0x3F:
			print "SER FAILED (tamper not ON)!!!" + data[15]
			status = {'tamper_ok':0, 'ser_ok':1}
		elif data[15] != 0xF:
			print "SER FAILED (tamper not ON)!!!" + data[16]
			status = {'tamper_ok':0, 'ser_ok':1}
		elif data[16] != 0x0:
			print "SER FAILED EXT!!!" + data[17]
			status = {'tamper_ok':0, 'ser_ok':1}
		elif data[17] != 0x0:
			print "SER FAILED INT!!!" + data[18]
			status = {'tamper_ok':0, 'ser_ok':1}
		else:
			#print "TM SER PASSED!!!"
			status = {'tamper_ok':1, 'ser_ok':1}
		
	time.sleep(1)
	return status

if __name__=='__main__':
	print "ret is: " + str(ser_test(6,1))
	#print "ret is: " + str(ser_test(1,0x3F))

