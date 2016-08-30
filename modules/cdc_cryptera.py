#!/usr/bin/python

import time
import os
from log_cm import set_log_info, set_log_level, get_log_cm
from serial_cm import get_ser, ser_Init, uart_self_test


def find_cdc_rsp_data ():
	input = '/opt/maxim-ic/hcr4/apps/cdc_host_test'
	get_ser().write(input.encode('ascii')+'\n')
	time.sleep(2)
	out = str(get_ser().readlines())
	if out:
		#print out
		s_index = out.find("errno = 0")
		if s_index != -1:
			s_index = s_index + 16
		else:
			return -1
		e_index = out.find(r"#", s_index) - 8
		#print "s-index %d" % s_index
		#print "e-index %d" % e_index
		#print out[s_index:e_index]
		#print e_index - s_index
		return out[s_index:e_index]
	else:
		return -1

##################################################
#Main Code Here
##################################################
if __name__=='__main__':
	while True:
		run = 1
		cdc_count = 0
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
			if find_cdc_rsp_data() != -1:
				cdc_count = cdc_count+1
			get_log_cm().info( "CDC Count = \t\t%d of %d", cdc_count, total_count)
			#Ethernet Test end:#######################################################

