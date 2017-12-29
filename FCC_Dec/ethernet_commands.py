import socket
import array
import time
import binascii

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

sendCommand_tamper = bytearray.fromhex(u'C0 01 01 C1 01 01 C2 01 3F')
sendCommand_icc_read = bytearray.fromhex(u'C0 01 01 C1 01 06 C2 01 01')

counter = 0
while (1):
	counter += 1
	if counter > 500:
		break

	print "-> " + binascii.hexlify(sendCommand_tamper)
	client_socket.send(sendCommand_tamper)
	recvData = client_socket.recv(10000)
	print "<- " + binascii.hexlify(recvData)

	print "-> " + binascii.hexlify(sendCommand_icc_read)
	client_socket.send(sendCommand_icc_read)
	recvData = client_socket.recv(10000)
	print "<- " + binascii.hexlify(recvData)
	print counter
	
	time.sleep(5)

client_socket.close()






#while(1):
#	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#	client_socket.connect((dynaproIP, int(dynaproPort)))
#	print "-> " + binascii.hexlify(sendCommand)
#	client_socket.send(sendCommand)
#	time.sleep(1)
#	recvData = client_socket.recv(10000)
#	print "<- " + binascii.hexlify(recvData)
	
#	client_socket.send(sendCommand)
#	recvData = client_socket.recv(10000)
#	print "<- " + binascii.hexlify(recvData)

	
	#client_socket.close()
#time.sleep(1)
#recvData = client_socket.recv(10000)
#print "<- " + binascii.hexlify(recvData)

#print

#client_socket.close()