from Help import *
from FileHelp import *



#################################################
#               specific functions              #
#################################################

def StoreData_toPath(Data : dict, filename : str, path="", sort_alphabetic=False):
	if path:
		filename = path_join(path, filename)
	if sort_alphabetic:
		Data = sortData_Alphabetic(Data)

	store_mat(Data, filename)

def StoreData(Data : dict, datestring : str, logname : str, postfix="", sort_alphabetic=False):
	"""
	Stores given Data
	:param Data: Data to Store
	:param datestring:
	:param lognum: Lognum or Filename to store to
	:param postfix: Postfix to append like LogXX_POSTFIX
	:param sort_alphabetic:
	"""

	filename = logname
	if postfix:
		filename += "_" + postfix

	filepath = path_join(getLogfilefolder(datestring), filename)

	if sort_alphabetic:
		Data = sortData_Alphabetic(Data)

	store_mat(Data, filepath)

def sortData_Alphabetic(Data : dict) -> dict:
	from TraceHelp import Group_Exists, Group_sortTraces

	def addgroup(GROUP):
		if (Group_Exists(Data, GROUP)):
			nData[GROUP] = Data[GROUP]
			Group_sortTraces(nData, GROUP)
		else:
			from TraceHelp import Group_Create_Tstartend
			Group_Create_Tstartend(nData, GROUP, 1, t_end=1)

	nData = {}

	for GROUP in sorted(list(Data.keys())):
		addgroup(GROUP)


	#nData.update(Data)
	return nData




def LoadData_byPath(path : str) -> dict:
	return load_mat(path)


def getLogfilefolder(datestring : str):
	return path_join(PATH.DIR_LOGFILES, datestring)

def getAllOsciLogfiles(datestring : str):
	return get_files_in_Folder(getLogfilefolder(datestring), ".csv", withpath=False)


def LoadData(datestring : str, logname : str) -> dict:
	"""
	Load Data from datestring
	:param datestring:
	:param logname: filename of log without extension
	:param RAW: if true unprocessed logfile is loaded.
	:return: Data
	"""

	filename = path_join(getLogfilefolder(datestring), logname)
	if not filename.endswith(".mat"):
		filename += ".mat"

	if not file_exists(filename):
		print("LoadData: Logfile '{}' not found".format(filename))
		return {}

	return LoadData_byPath(filename)



def OpenDiadem_Data(Data, tdv_path=None, block=True, name="tmp"):
	"""
	Opens Diadem with given Data
	:param Data:
	:param tdv_path:
	:return:
	"""
	path = path_join(PATH.DIR_TMP, "diadem_{}.mat".format(name))
	StoreData_toPath(Data, path, sort_alphabetic=True)
	OpenDiadem(path, tdv_path, block)

def OpenDiadem(logfile_path, tdv_path=None, block=True):
	# Open in Diadem
	if not isAbsolutPath(logfile_path):
		logfile_path = getAbsolutePath(logfile_path)

	if tdv_path and not isAbsolutPath(tdv_path):
		tdv_path = getAbsolutePath(tdv_path)


	args = [PATH.PATH_DIADEM, logfile_path]

	if tdv_path:
		args.append(tdv_path)

	import subprocess
	if block:
		subprocess.call(args)
	else:
		subprocess.Popen(args)

def OpenExplorer(path):
	if not isAbsolutPath(path):
		path = getAbsolutePath(path)

	import subprocess
	subprocess.call("explorer {}".format(path), shell=True)


def DEBUG_Store(Data, tag=None):
	if tag == None:
		filename = FILENAME_TMP_JSON
	else:
		filename = FILENAME_TMP_JSON_TAG.format(tag)

	store_json(Data, filename, PATH.DIR_TMP)


def DEBUG_Load(tag=None):
	if tag == None:
		filename = FILENAME_TMP_JSON
	else:
		filename = FILENAME_TMP_JSON_TAG.format(tag)

	return load_json(filename, PATH.DIR_TMP)



def DEBUG_StoreData(Data, tag=None):
	if tag == None:
		filename = FILENAME_TMP_DATA
	else:
		filename = FILENAME_TMP_DATA_TAG.format(tag)

	#save_json(Data, filename, PATH.DIR_TMP)
	path = path_join(PATH.DIR_TMP, filename)
	StoreData_toPath(Data, path, sort_alphabetic=True)


def DEBUG_LoadData(tag=None):
	if tag == None:
		filename = FILENAME_TMP_DATA
	else:
		filename = FILENAME_TMP_DATA_TAG.format(tag)

	#return load_json(filename, PATH.DIR_TMP)
	path = path_join(PATH.DIR_TMP, filename)
	return LoadData_byPath(path)




if __name__ == '__main__':
	pass