import socket
import array
import time
import binascii
import struct


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
	status = -1
	#print 'Please enter IP address: '
	#dynaproIP = raw_input('IP address [10.57.10.133]: ')
	#if dynaproIP == "":
	dynaproIP = "10.57.22.123"

	#dynaproPort = raw_input('Port [26]: ')
	#if dynaproPort == "":
	dynaproPort = str(5000)

	print "Attempting to connect to DynaPro at " + dynaproIP + " on " + dynaproPort

	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client_socket.connect((dynaproIP, int(dynaproPort)))


	buffer = bytearray.fromhex(u'C0 01 01 C1 01 01 C2 01 3F')
	#sendCommand_icc_read = bytearray.fromhex(u'C0 01 01 C1 01 06 C2 01 01')

	
	buffer[5] = app
	buffer[8] = cmd
	
#	counter = 0
#	while (1):
#		counter += 1
#		if counter > 500:
#			break

	print "-> " + binascii.hexlify(buffer)
	client_socket.send(buffer)
	recvData = client_socket.recv(10000)
	
	print len(recvData)

	#data_list = map(ord, recvData)
	#print data_list
	
	data_list = struct.unpack(str(len(recvData))+'B', recvData)
	print data_list

	if data_list[11] != 0:
		print "ETHER FAILED!!!"
		status = 1
	print "ETH PASSED!!!"
	status = 0

	
	print "<- " + binascii.hexlify(recvData)

#		print "-> " + binascii.hexlify(sendCommand_icc_read)
#		client_socket.send(sendCommand_icc_read)
#		recvData = client_socket.recv(10000)
#		print "<- " + binascii.hexlify(recvData)
#		print counter
		
	time.sleep(1)
	client_socket.close()
	return status

if __name__=='__main__':
	print "ret is: " + str(eth_test(6,1))
	print "ret is: " + str(eth_test(1,0x3F))