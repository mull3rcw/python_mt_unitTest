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

#sendCommand = bytearray.fromhex(u'C0 DB DC 01 01 C1 01 04 C2 01 12 C0')	# with SLIP
sendCommand_1 = bytearray.fromhex(u'C0 01 01 C1 01 01 C2 01 10 c4 04 09 00 00 00')	
sendCommand_2 = bytearray.fromhex(u'C0 01 01 C1 01 01 C2 01 10 c4 09 C0 01 01 C1 01 04 C2 01 12')	

sendCommand_3 = bytearray.fromhex(u'C0 01 01 C1 01 01 C2 01 3F')

#sendCommand_2 = bytearray.fromhex(u'C0 01 01 C1 01 04 C2 01 12 ')	

#sendCommand = bytearray.fromhex(u'C0 C0 C0 C0 C0 C0 C0 C0 C0 C0')	# random data
#sendCommand = bytearray.fromhex(u'C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0 C0 DB DC 01 01 C1 01 04 C2 01 12 C0') # MSR data


####################################################################
#client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client_socket.connect((dynaproIP, int(dynaproPort)))

print "-> " + binascii.hexlify(sendCommand_3)
client_socket.send(sendCommand_3)
recvData = client_socket.recv(10000)
print "<- " + binascii.hexlify(recvData)

#print "-> " + binascii.hexlify(sendCommand_2)
#client_socket.send(sendCommand_2)
#recvData = client_socket.recv(10000)
#print "<- " + binascii.hexlify(recvData)
#client_socket.close()

#recvData = client_socket.recv(10000)
#print "<- " + binascii.hexlify(recvData)
#client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client_socket.connect((dynaproIP, int(dynaproPort)))
#client_socket.send(sendCommand)
#recvData = client_socket.recv(10000)
#print "<- " + binascii.hexlify(recvData)
#client_socket.close()
#recvData = client_socket.recv(10000)
#print "<- " + binascii.hexlify(recvData)
#client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client_socket.connect((dynaproIP, int(dynaproPort)))
#client_socket.send(sendCommand)
#recvData = client_socket.recv(10000)
#print "<- " + binascii.hexlify(recvData)
#client_socket.close()
#recvData = client_socket.recv(10000)
#print "<- " + binascii.hexlify(recvData)


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