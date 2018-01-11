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

port = "COM13"   #Windows com port format 
baud = 9600		#make sure it's the same for both side

ser = serial.Serial(port, baud, timeout=10) #Block for 10 second when read
if ser.isOpen():
	print(ser.name + ' is open...')
	print("Hello")

sendCommand = bytearray.fromhex(u'02 c0 01 01 c1 01 02 c2 01 0b c4 02 df 7c 0a')
#sendCommand = bytearray.fromhex(u'02 43 30 30 31 30 31 43 31 30 31 30 32 43 32 30 31 30 42 43 34 30 32 44 46 37 43 31 31 31 31 03 0a')

#while True:
########## sending #######################
ser.write(sendCommand + '\r\n')
#ser.write('hello')
########## receiving #####################
out  = ser.read(25) #how many bytes expect to read
#    print(out)   ##for outputing ascii characters
print "-> " + binascii.hexlify(out) #for outputing hex value
time.sleep(1)
ser.close()



def ser_test(app, cmd):
	status = {'scard_ok':-1, 'ser_ok':-1}
	#print 'Please enter IP address: '
	
	port = "COM13"   #Windows com port format 
	baud = 9600		#make sure it's the same for both side

	ser = serial.Serial(port, baud, timeout=10) #Block for 10 second when read
	if ser.isOpen():
		print(ser.name + ' is open...')
	
	buffer = bytearray.fromhex(u'C0 01 01 C1 01 01 C2 01 3F')
	buffer[5] = app
	buffer[8] = cmd

	ser.write(buffer + '\r\n')
	data  = ser.read(25) #how many bytes expect to read
	ser.close()
#    print(data)   ##for outputing ascii characters
	print "-> " + binascii.hexlify(data) #for outputing hex value
	time.sleep(1)
	

	
	#ICC STATUS
	if app == 6:
		if data == []:
			status = {'scard_ok':0, 'ser_ok':-1}
		elif data[11] != 0:
			print "SC ETH FAILED!!!"
			print data[11]
			print hex(data[12])
			status = {'scard_ok':0, 'ser_ok':1}
		else:
			#print "SC ETH PASSED!!!"
			status = {'scard_ok':1, 'ser_ok':1}
	else:
		#TAMPER
		if data == []:
			status = {'tamper_ok':0, 'ser_ok':-1}
		elif data[11] != 0:
			print "USB FAILED!!!"
			status = {'tamper_ok':0, 'ser_ok':0}
		elif data[14] != 0x3F:
			print "USB FAILED (tamper not ON)!!!" + data[15]
			status = {'tamper_ok':0, 'ser_ok':1}
		elif data[15] != 0xF:
			print "USB FAILED (tamper not ON)!!!" + data[16]
			status = {'tamper_ok':0, 'ser_ok':1}
		elif data[16] != 0x0:
			print "USB FAILED EXT!!!" + data[17]
			status = {'tamper_ok':0, 'ser_ok':1}
		elif data[17] != 0x0:
			print "USB FAILED INT!!!" + data[18]
			status = {'tamper_ok':0, 'ser_ok':1}
		else:
			#print "TM ETH PASSED!!!"
			status = {'tamper_ok':1, 'ser_ok':1}
		
	time.sleep(1)
	client_socket.close()
	return status

if __name__=='__main__':
	print "ret is: " + str(ser_test(6,1))
	print "ret is: " + str(ser_test(1,0x3F))


