import socket
import array
import time
import binascii
import struct
from logging_fcc import log_date, get_log, get_mode
from usb_hid import get_ip

#convert string to hex
def toHex(s):
	lst = []
	for ch in s:
		hv = hex(ord(ch)).replace('0x', ' ')
		if len(hv) == 1:
			hv = '0'+hv
		lst.append(hv)
	return reduce(lambda x,y:x+y, lst)
	
#convert hex repr to string
def toStr(s):
	return s and chr(int(s[:2], base=16)) + toStr(s[2:]) or ''

def eth_test(app, cmd):
	status = {'scard_ok':-1, 'eth_ok':-1}
	#if get_mode() == "laptop":
	#	dynaproIP = "192.168.56.4"
	#else:
	#	dynaproIP = "10.57.22.118"
	dynaproIP = str(get_ip())
	dynaproPort = str(5000)
	log = get_log()

	try:
		client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client_socket.settimeout(3.0)
		client_socket.connect((dynaproIP, int(dynaproPort)))
		#print "Socket obtained"
	except socket.error as err:
		print dynaproIP
		log.info(log_date(get_log()) + ' ETH Failure to resolve...' + str(dynaproIP))
		status = {'scard_ok':-1, 'eth_ok':-1}
		return status

	buffer = bytearray.fromhex(u'C0 01 01 C1 01 01 C2 01 3F')
	buffer[5] = app
	buffer[8] = cmd

	client_socket.send(buffer)
	recvData = client_socket.recv(10000)

	data = struct.unpack(str(len(recvData))+'B', recvData)
	
	#ICC STATUS
	if app == 6:
		#log.info( data)
		if data == []:
			status = {'scard_ok':0, 'eth_ok':-1}
		elif data[11] != 0:
			log.info( "SC ETH FAILED!!! " + str(data[11]))
			status = {'scard_ok':0, 'eth_ok':-1}
		else:
			#log.info( "SC ETH PASSED!!!"
			status = {'scard_ok':1, 'eth_ok':1}
	else:
		#TAMPER
		if data == []:
			status = {'tamper_ok':0, 'eth_ok':-1}
		elif data[11] != 0:
			log.info( "ETH FAILED!!!")
			status = {'tamper_ok':0, 'eth_ok':-1}
		elif data[14] != 0x3F:
			log.info( "ETH FAILED (tamper not ON)!!!" + data[15])
			status = {'tamper_ok':0, 'eth_ok':1}
		elif data[15] != 0xF:
			log.info( "ETH FAILED (tamper not ON)!!!" + data[16])
			status = {'tamper_ok':0, 'eth_ok':1}
		elif data[16] != 0x0:
			log.info( "ETH FAILED EXT!!!" + data[17])
			status = {'tamper_ok':0, 'eth_ok':1}
		elif data[17] != 0x0:
			log.info( "ETH FAILED INT!!!" + data[18])
			status = {'tamper_ok':0, 'eth_ok':1}
		else:
			#log.info( "TM ETH PASSED!!!")
			status = {'tamper_ok':1, 'eth_ok':1}
		
	time.sleep(1)
	client_socket.close()
	return status

if __name__=='__main__':
	print "ret is: " + str(eth_test(6,1))
	print "ret is: " + str(eth_test(1,0x3F))