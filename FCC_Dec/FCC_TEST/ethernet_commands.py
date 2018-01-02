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
	status = {'scard_ok':-1, 'eth_ok':-1}
	#print 'Please enter IP address: '
	dynaproIP = "10.57.22.103"

	dynaproPort = str(5000)

	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client_socket.connect((dynaproIP, int(dynaproPort)))

	buffer = bytearray.fromhex(u'C0 01 01 C1 01 01 C2 01 3F')
	buffer[5] = app
	buffer[8] = cmd

	client_socket.send(buffer)
	recvData = client_socket.recv(10000)

	data = struct.unpack(str(len(recvData))+'B', recvData)
	
	
	#ICC STATUS
	if app == 6:
		if data == []:
			status = {'scard_ok':0, 'eth_ok':-1}
		elif data[11] != 0:
			print "SC ETH FAILED!!!"
			print data[11]
			print hex(data[12])
			status = {'scard_ok':0, 'eth_ok':1}
		else:
			#print "SC ETH PASSED!!!"
			status = {'scard_ok':1, 'eth_ok':1}
	else:
		#TAMPER
		if data == []:
			status = {'tamper_ok':0, 'eth_ok':-1}
		elif data[11] != 0:
			print "USB FAILED!!!"
			status = {'tamper_ok':0, 'usb_ok':0}
		elif data[14] != 0x3F:
			print "USB FAILED (tamper not ON)!!!" + data[15]
			status = {'tamper_ok':0, 'usb_ok':1}
		elif data[15] != 0xF:
			print "USB FAILED (tamper not ON)!!!" + data[16]
			status = {'tamper_ok':0, 'usb_ok':1}
		elif data[16] != 0x0:
			print "USB FAILED EXT!!!" + data[17]
			status = {'tamper_ok':0, 'usb_ok':1}
		elif data[17] != 0x0:
			print "USB FAILED INT!!!" + data[18]
			status = {'tamper_ok':0, 'usb_ok':1}
		else:
			#print "TM ETH PASSED!!!"
			status = {'tamper_ok':1, 'eth_ok':1}
		
	time.sleep(1)
	client_socket.close()
	return status

if __name__=='__main__':
	print "ret is: " + str(eth_test(6,1))
	print "ret is: " + str(eth_test(1,0x3F))