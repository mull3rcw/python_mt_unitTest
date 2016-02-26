#! python
import time
from serial_cm import ser_Init, get_ser, serial_close
from log_cm import set_log_info, set_log_level, get_log_cm

def getEnvData (num):
	#load num into sc* cmd line
	ser = get_ser()
	input = '/opt/maxim-ic/basic/examples/sci_basic /dev/sc 10'
	#input = './sci_basic /dev/sc 10'
	index = input.find(' 10')
	input2 = input[:index] + str(num) + input[index:]
	ser.write(input2.encode('ascii')+'\n')
	#Wait 2 seconds for Sam card
	if num == 0: time.sleep(2)
	#Parse Output
	out = str(ser.readlines())
	if 'Card mute' not in out:
		s_index = out.find('ATR[')+10
		e_index = out.find(r"\r\n", s_index)
		return out[s_index:e_index]
	elif 'Card mute' in out:
		return "No EMV Support"


def isCardPresent (num):
	# check list for NOK or OK
	ser = get_ser()
	input = '/opt/maxim-ic/basic/examples/sci_basic /dev/sc 3'
	index = input.find(' 3')
	input2 = input[:index] + str(num) + input[index:]
	#print input2
	ser.write(input2.encode('ascii')+'\n')
	out = ser.readlines()
	if "NOK" in str(out):
		#print "Card Missing"
		return False
	elif " OK" in str(out):
		#print "Card Present"
		return True
	else:
		#print "Failed to read"
		return -1


def setCardFacilitator ():
	#This statys running until completes
	ser = get_ser()
	input = '/opt/maxim-ic/basic/examples/card_facilitator'
	ser.write(input.encode('ascii')+'\n')
	#Wait 2 seconds for Sam card
	print "Pull out MSR read within 10 seconds"
	out = str(ser.readlines())
	print out
	time.sleep(10)
	#Control-C
	input = '\x03'
	ser.write(input.encode('ascii')) #+'\n')
	print "DONE"

def set_fail_count(new):
	global fail_count
	fail_count = new

def get_fail_count():
	global fail_count
	if 'fail_count' not in globals():
		print "Error: fail_count not init"
		fail_count=0
	return fail_count

def handle_failed_card_read():
	count=get_fail_count()
	set_fail_count(count+1)
	ret = True
	get_log_cm().error("\t\t\tFailed %d for Card", count)
	#if 5 failed reads in a row, the system may have reset.
	if get_fail_count() > MAX_COM_RETRY:
		get_log_cm().error("\t\t\tReading stopped, Reboot restarting script.\n\n\n")
		serial_close()
		ret = False
	return ret

def read_smart_card(card_id):
	x = isCardPresent(card_id)
	time.sleep(1)
	if(x < 0):
		#Card failed to read
		get_log_cm().error("\t\t\tcard %d failed to read" % (card_id))
		run = handle_failed_card_read()
		if run == False:
			return -1
		return 1
	elif x == 0:
		get_log_cm().error("\t\t\tcard %d is Missing" % (card_id))
		return 1
	elif x == 1:
		#Get ATR
		set_fail_count(0)
		if x > 0:
			if x == True:
				emv_data = getEnvData(card_id)
				get_log_cm().debug("Card %d ATR %s" % (card_id, emv_data))
				if "No EMV Support" not in str(emv_data):
					characters = emv_data.replace(' ', '')
					get_log_cm().debug("Card %d ATR string %s" % (card_id, characters.decode('hex')))
					return 0
				else:
					get_log_cm().error("x is %d UNKNOWN") % (x)
					return 1


if __name__=='__main__':
##############USER DEFINED##################################################################################
##Overwrite Log location
	my_path = '..\\smart_card_log\\'
	my_name = 'smart_card_test'
	test_count = 100
	log = set_log_info(my_path, my_name)
##############USER DEFINED##################################################################################

##One time setup
	while True:
		test_count 			= 0
########Passing Counters########
		total_count 	= 0
		smart_card_count = 0
		MAX_COM_RETRY	= 5

################################

##############INIT #################
		ser_Init()
		run = 1
		#card_bay_init()
##############INIT END##############
		get_log_cm().info('Start %s Test', my_name)
		get_log_cm().info('Test :\n Smart Card')

		while run:
			total_count+=1
			get_log_cm().debug( "Total Test Cycles = %d", total_count)

			#SMARTCARD Test:##########################################################
			for i in range(1,2):
					val = read_smart_card(i)
					if val == -1:
						run = 0
						break
					if val == 0:
						smart_card_count+=1
			#SMARTCARD Test:##########################################################
			get_log_cm().info( "SmartCard Count = \t\t%d of %d", smart_card_count, total_count)
			get_log_cm().info("\==============================\n")
