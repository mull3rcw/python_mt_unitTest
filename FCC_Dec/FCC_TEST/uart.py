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

import sys
import serial, time
import binascii
import struct
from serial import SerialException
from logging_fcc import log_date, get_log, get_mode


def set_com(new):
	global my_com
	my_com = new

def get_com():
	global my_com
	return my_com	


def serial_ports():
	""" Lists serial port names
		:raises EnvironmentError:
			On unsupported or unknown platforms
		:returns:
			A list of the serial ports available on the system
    """
	if sys.platform.startswith('win'):
		ports = ['COM%s' % (i + 1) for i in range(256)]
	elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
		# this excludes your current terminal "/dev/tty"
		ports = glob.glob('/dev/tty[A-Za-z]*')
	elif sys.platform.startswith('darwin'):
		ports = glob.glob('/dev/tty.*')
	else:
		raise EnvironmentError('Unsupported platform')

	result = []
	for port in ports:
		try:
			s = serial.Serial(port)
			s.close()
			result.append(port)
		except (OSError, serial.SerialException):
			pass
	return result

#convert string to hex
def toHex2(text):
	if len(text) % 2 == 0:
		s=binascii.unhexlify(text)
		#log.info( s )
		return [hex(ord(x)) for x in s]	
	else:
		return[]

def ser_open_port(port):
	#print(serial_ports())
	#Compares need to be against strings, and lower case apparently
	status = {'scard_ok':-1, 'ser_ok':-1}
	#print 'Please enter IP address: '
	log = get_log()
	baud = 9600		#make sure it's the same for both side

	try:
		ser = serial.Serial(port, baud, timeout=3) #Block for 10 second when read
	except SerialException:
		log.info(log_date(get_log()) + ' SerialException...')
		return -1

	if not ser.isOpen():
		log.info(ser.name + ' is NOT open...')

	return ser
		
def ser_close_port(ser):
	ser.close()
	
def ser_find_com():
	ports = serial_ports()
	#print ports
	for i in ports:
		ser = ser_open_port(i)
		buffer = bytearray.fromhex(u'C0 01 01 C1 01 01 C2 01 3F')
		ser.write(binascii.hexlify(buffer) + '\n')	
		out  = ser.read(36) #how many bytes expect to read
		ser.close()
		data = toHex2(out)
		if data != []:
			#print "Port OK " + i
			set_com(i)
			return i

def ser_test(app, cmd):

	#print(serial_ports())
	
	#Compares need to be against strings, and lower case apparently
	status = {'scard_ok':-1, 'ser_ok':-1}
	#print 'Please enter IP address: '
	log = get_log()

	#if get_com() == "laptop":
	#	port = "COM1"   #Windows com port format was 13
	#else:
	#	port = "COM9"   #Windows com port format was 13
	port = get_com()
	baud = 9600		#make sure it's the same for both side

	try:
		ser = serial.Serial(port, baud, timeout=3) #Block for 10 second when read
	except SerialException:
		log.info(log_date(get_log()) + ' SerialException...')
		return status

	if not ser.isOpen():
		log.info(ser.name + ' is NOT open...')

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
			log.info( "SC SER EMPTY!!! ")
		elif data[11] != '0x0':
			log.info( "SC SER FAILED!!! " + str(int(data[11], 16)))
			#for i in range(12):
			#	print data[i]
			status = {'scard_ok':0, 'ser_ok':1}
		else:
			#log.info( "SC SER PASSED!!!")
			status = {'scard_ok':1, 'ser_ok':1}
	else:
		#TAMPER
		#print "Tamper"
		if data == []:
			status = {'tamper_ok':0, 'ser_ok':-1}
		elif data[11] != '0x0':
			log.info( "SER FAILED!!!")
			status = {'tamper_ok':0, 'ser_ok':-1}
		elif data[14] != '0x3f':
			log.info( "SER FAILED (tamper not ON)!" + data[14])
			status = {'tamper_ok':0, 'ser_ok':1}
		elif data[15] != '0xf':
			log.info( "SER FAILED (tamper not ON)!!!" + data[15])
			status = {'tamper_ok':0, 'ser_ok':1}
		elif data[16] != '0x0':
			log.info( "SER FAILED EXT!!!" + data[16])
			status = {'tamper_ok':0, 'ser_ok':1}
		elif data[17] != '0x0':
			log.info( "SER FAILED INT!!!" + data[17])
			status = {'tamper_ok':0, 'ser_ok':1}
		else:
			#log.info( "TM SER PASSED!!!")
			status = {'tamper_ok':1, 'ser_ok':1}
		
	time.sleep(1)
	return status


if __name__=='__main__':
	#print "ret is: " + str(ser_test(6,1))
	print "ret is: " + str(ser_test(1,0x3F))


