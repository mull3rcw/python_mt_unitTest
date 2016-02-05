#!/usr/bin/python
import time
import os
import logging
from serial_cm import get_ser, log, _ser_init, uart_self_test

def find_ip_addr (node):
	input = 'ifconfig'
	get_ser().write(input.encode('ascii')+'\n')
	time.sleep(2)
	out = str(get_ser().readlines())
	if node in out:
		s_index = out.find('inet addr:')+10
		e_index = out.find(r"Bcast", s_index)
		return out[s_index:e_index]
	else:
		return -1

def can_addr_ping(addr):		
        #print addr
	response = os.system('ping -n 1 %s > temp.txt' % addr)
	time.sleep(1)
	ret = False
	if response != 0:
		log.info("Ping to %s Failed" % (addr))
		print 'Ping to %s Failed' % addr
		return ret
	txt = open("temp.txt")
	out = txt.readlines()
	if "Destination host unreachable" in str(out):
		print 'Ping Dest Unreachable'
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

		_ser_init()
		
		while run:
			#Total Test Cycles
			print( "\n")
			total_count+=1
		
			#Ethernet Test:###########################################################
			###Find HCR-4 IP Address####
			
			#print uart_self_test()
			#print "FALSE is pass"
			hostname = find_ip_addr('eth0')
			if hostname != -1:
				ret = can_addr_ping(hostname)
				if ret == True:
					ethernet_count+=1
					
			log.info( "Ethernet Count = \t\t%d of %d", ethernet_count, total_count)
			print 'Ethernet Count = \t\t%d of %d' % (ethernet_count, total_count)
			#Ethernet Test end:#######################################################
			
