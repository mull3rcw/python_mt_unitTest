import socket
import array
import time
import binascii

#print 'Please enter IP address: '
#dynaproIP = raw_input('IP address [10.57.10.133]: ')
#if dynaproIP == "":
dynaproIP = "10.57.10.120"

#dynaproPort = raw_input('Port [26]: ')
#if dynaproPort == "":
dynaproPort = str(5000)

print "Attempting to connect to DynaPro at " + dynaproIP + " on " + dynaproPort

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((dynaproIP, int(dynaproPort)))

sendCommand = bytearray.fromhex(u'C0 DB DC 01 01 C1 01 04 C2 01 12 C0')       # End Session command

print "-> " + binascii.hexlify(sendCommand)
client_socket.send(sendCommand)
recvData = client_socket.recv(128)
print "<- " + binascii.hexlify(recvData)
#print

client_socket.close()
