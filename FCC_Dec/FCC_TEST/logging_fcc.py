#! python
import time, datetime, logging, os

##################################################
#USER/Machine SPECIFIC, change UART to MATCH YOURS!!!!
path = '..\log\\'
brk = '\\'
log_name = 'check_card_log'

##################################################
# Get timestamp of Python call:
myts = time.time()	
myst = datetime.datetime.fromtimestamp(myts).strftime('%Y-%m-%d+%H_%M_%S')
#myst = datetime.datetime.fromtimestamp(myts).strftime('%Y-%m-%d+%H_%M')


##formatter = logging.Formatter('%(asctime)s:  %(message)s')
##hdlr.setFormatter(formatter)
##log.addHandler(hdlr) 
#log.setLevel(logging.DEBUG)
##log.setLevel(logging.INFO)

########################

def log_date(n):
	#t = datetime.datetime.fromtimestamp(myts).strftime('%Y-%m-%d+%H_%M_%S')
	t = datetime.datetime.fromtimestamp(myts).strftime("%Y-%m-%d %H:%M:%S")
	n.info(t)
	return t


def set_logger_name(new):
	global logger_name
	logger_name = new
	return logging.getLogger(logger_name)

def set_log_path(new, rootLogger):
	global log_path_name
	log_path_name = new
	#logFormatter = logging.Formatter('%(asctime)s:  %(message)s')
	logFormatter = logging.Formatter('%(message)s')
	filename = log_path_name+brk+logger_name+str(myst)+'.log'
	print 'LOGGING new PATH is: ' + filename
	
	fileHandler = logging.FileHandler(filename,'wb')
	fileHandler.setFormatter(logFormatter)
	rootLogger.addHandler(fileHandler) 	
	
	consoleHandler = logging.StreamHandler()
	consoleHandler.setFormatter(logFormatter)
	rootLogger.addHandler(consoleHandler) 
	
	return fileHandler

def set_log_info(path, name):
	print "Log Path : "+ path
	if not os.path.exists(path):
		os.mkdir(path)
	print "Log Name : "+ name
	log = set_logger_name(name)
	hdlr2 = set_log_path(path,log)
	#log.addHandler(hdlr2) move to set log
	log.setLevel(logging.INFO)
	set_log(log)
	return log
	
def set_log(new):
	global my_log
	my_log = new

def get_log():
	global my_log
	return my_log

#def log_Init(my_path, my_name):
#	return set_log_info(my_path, my_name)	


