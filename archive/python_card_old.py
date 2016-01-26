#! python
import serial, time	
x = int(raw_input("Please enter an integer: "))
if x < 0:
    x = 0
    print 'Negative changed to zero'
elif x == 0:
    print 'Zero'
elif x == 1:
    print 'Single'
else:
    print 'More'
	  
	  
#ser = serial.Serial('/dev/tty.usbserial', 57600, timeout=0.5)
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
	elif cmd == 'hi':
		ser.write(cmd.encode('ascii')+'\n')
		out = ser.readlines()
		print('Receiving...'+str(out))
	else:
		with open ("./sci_basic /dev/sc1 3", "r") as myfile:
			 data="".join(line.rstrip() for line in myfile)
			 ##data=myfile.read()
		#print('read:...'+str(data))
		print myfile.read()

	 
