#! python
import time, datetime, logging, os


myst = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d+%H_%M_%S')
#fH = 0
#cH = 0
logg = 0
log_level = 0		#sets default log setting

########################

#API to other fails
def set_log_cm(new):
	global lg
	lg = new

def get_log_cm():
	global lg
	if 'lg' not in globals():
		print "Error: lg not init"
		lg=-1
	return lg

def set_logger_name(new):
	global logger_name
	logger_name = new
	return logging.getLogger(logger_name)

def set_log_path(new):
	global log_path_name
	log_path_name = new
	filename = log_path_name+logger_name+str(myst)+'.log'
	print('>Setting Log to %s' % filename)
	return logging.FileHandler(filename,'wb')

def set_log_info(path, name, debugINFO=1):
	global fH, cH

	if not os.path.exists(path):
		os.mkdir(path)

	# Configure Path/Create handles
	set_log_cm(set_logger_name(name))

	#Remove prior cf handlers.
	if 'fH'  in globals():
		get_log_cm().removeHandler(fH)

	if 'cH'  in globals():
		get_log_cm().removeHandler(cH)

	fH = set_log_path(path)
	cH = logging.StreamHandler()

	#Overall logging mask, leave alone.
	if debugINFO == 0:
		get_log_cm().setLevel(logging.DEBUG)
		print ">>DEBUG Log Enabled"
	else:
		get_log_cm().setLevel(logging.INFO)
		print "INFO Log Enabled"

	# Logging to File
	log_formatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")
	fH.setFormatter(log_formatter)
	if debugINFO == 0:
		fH.setLevel(logging.DEBUG)
	else:
		fH.setLevel(logging.INFO)
	get_log_cm().addHandler(fH)

	# Logging to Console
	console_formatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")
	cH.setFormatter(console_formatter)
	if debugINFO == 0:
		cH.setLevel(logging.DEBUG)
	else:
		cH.setLevel(logging.INFO)
	get_log_cm().addHandler(cH)
	return get_log_cm()

def set_log_level(new):
	global log_level
	log_level = new

def get_log_level():
	global log_level
	if 'log_level' not in globals():
		print "Error: log_level not init"
		log_level=-1
	return log_level

########################
#Initialize Access
if __name__=='__main__':
	that_path = '..\\my_log\\'
	that_name = 'my_log_test'
	DEBUG_PRINT=0
	INFO_PRINT=1
	count=4

	set_log_level(DEBUG_PRINT)

	for i in range(0,count):
		#Show that set_log_info clears previous log.
		set_log_info(that_path, that_name, get_log_level())
		get_log_cm().debug('DEBUG: Quick zephyrs daft.')
		get_log_cm().info('INFO:How jumping zebras vex.')
		val = get_log_level()
		val = not val
		set_log_level(val)
