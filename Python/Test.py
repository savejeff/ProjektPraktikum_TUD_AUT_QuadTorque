from ImportsBase import *

def getLogfileFolder(datestring):
	return path_join(PATH.DIR_LOGFILES, datestring)

def getAllOsciLogfiles(datestring):
	return get_files_in_Folder(getLogfileFolder(datestring), ".csv", withpath=False)

if __name__ == '__main__':
	# Load Osci Logging
	if True:
		datestring = "2021-11-11"
		#logfilename = "bldc_throttle_10.csv"

		logfilefolder = getLogfileFolder(datestring)

		for logfilename in getAllOsciLogfiles(datestring):

			data = load_csv_wHeader(logfilename, logfilefolder, mode = 1, sample_func=lambda x : float(x))

			#print(data)

			logfilename_out = file_name_swap_extension(logfilename, ".mat")

			store_mat({"Osci" : data}, path_join(logfilefolder, logfilename_out))