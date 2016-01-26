#! python
import serial, time	

# Set up Serial	  
port = "COM5"
baud = 57600

ser = serial.Serial(port, baud, timeout=1)



if ser.isOpen():
	print(ser.name + ' is open...')

while True:
	cmd = raw_input("Enter command or 'exit':")
	if cmd == 'exit':
		ser.close()
		exit()
	elif cmd == '1':
		input = './sci_basic /dev/sc1 3'
		ser.write(input.encode('ascii')+'\n')
		out = ser.readlines()
		if "NOK" in str(out):
			print "Card Empty"
		elif " OK" in str(out):
			print "Card Detected"
			
		#print('Receiving...'+str(out))
	else:
		with open ("./sci_basic /dev/sc1 3", "r") as myfile:
			 data="".join(line.rstrip() for line in myfile)
			 ##data=myfile.read()
		#print('read:...'+str(data))
		print myfile.read()

	 
