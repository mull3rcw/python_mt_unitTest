#!/usr/bin/python
import time
import os
from log_cm import set_log_info, set_log_level, get_log_cm
from serial_cm import get_ser, ser_Init, uart_self_test


def find_ip_addr (node):
	input = 'ifconfig'
	get_ser().write(input.encode('ascii')+'\n')
	time.sleep(2)
	out = str(get_ser().readlines())
	if node in out:
		s_index = out.find('inet addr:')+10
		e_index = out.find(r"Bcast", s_index)
		#print "e-index %d" % e_index
		return out[s_index:e_index]
	else:
		return -1

def can_addr_ping(addr):		
	response = os.system('ping -n 1 %s > temp.txt' % addr)
	time.sleep(1)
	ret = False
	if response != 0:
		get_log_cm().info("Ping to %s Failed" % (addr))
		return ret
	txt = open("temp.txt")
	out = txt.readlines()
	if "Destination host unreachable" in str(out):
		get_log_cm().error("Ping Dest Unreachable")
		return ret
	elif "Lost = 0" not in str(out):
		print 'Ping Lost'
		return ret
	else:	
		ret = True
	txt.close()			
	response = os.remove('temp.txt')
	return ret

##################################################
#Main Code Here
##################################################
if __name__=='__main__':
	
	while True:
		run = 1
		ethernet_count = 0
		total_count = 0
		my_path = '..\\ping_log\\'
		my_name = 'ping_test'
		set_log_info(my_path, my_name, 0)
		ser_Init()
		
		while run:
			#Total Test Cycles
			get_log_cm().info("\n")
			total_count+=1
		
			#Ethernet Test:###########################################################
			###Find HCR-4 IP Address####
			hostname = find_ip_addr('eth0')
			if hostname != -1:
				ret = can_addr_ping(hostname)
				if ret == True:
					ethernet_count+=1
					
			get_log_cm().info( "Ethernet Count = \t\t%d of %d", ethernet_count, total_count)
			#Ethernet Test end:#######################################################
			
