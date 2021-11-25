FILENAME_PATH_JSON = "paths.json"
class paths:

	DIR_LOGFILES = "../../Logdaten"
	DIR_TMP = "./tmp"
	PATH_DIADEM = r"C:\Program Files\National Instruments\DIAdem 2019\DIAdem.exe"
	#PATH_DIADEM_DOCUMENTS = r"C:\Users\Public\Documents\National Instruments\DIAdem 2019\Documents"
	PATH_DIADEM_DOCUMENTS = "../Diadem"

	def __init__(self):
		from FileHelp import load_json, file_exists, mkdir, folder_exisits
		if(file_exists(FILENAME_PATH_JSON)):
			self.__dict__.update(load_json(FILENAME_PATH_JSON))
			print("paths.json loaded")

		from FileHelp import path_join

		self.PATH_TDV_OVERVIEW = path_join(self.PATH_DIADEM_DOCUMENTS, "View_Overview.TDV")
		self.PATH_TDV_DEFAULT = path_join(self.PATH_DIADEM_DOCUMENTS, "View_Log_Default.TDV")
		self.PATH_TDV_TMP = path_join(self.PATH_DIADEM_DOCUMENTS, "TMP.TDV")

		if not folder_exisits(self.DIR_TMP):
			mkdir(self.DIR_TMP)




PATH = paths()


def Script_Configure_pathjson():

	paths_dict = {}

	from FileHelp import OpenFolderPickerDialog, OpenFilePickerDialog, store_json
	paths_dict["DIR_LOGFILES"] = OpenFolderPickerDialog(titel="Select Folder all Logfiles are stored")
	paths_dict["PATH_DIADEM"] = OpenFilePickerDialog(r"C:\Program Files\National Instruments", fileextentions=[".exe"], titel="Select Diadem.exe in installation Folder")
	paths_dict["PATH_DIADEM_DOCUMENTS"] = OpenFolderPickerDialog(r"C:\Users\Public\Documents\National Instruments", titel="Select Diadem Documents Folder containing Views")

	store_json(paths_dict, FILENAME_PATH_JSON)


if __name__ == '__main__':
	from FileHelp import store_json
	#store_json(PATH.__dict__, FILENAME_PATH_JSON)
	Script_Configure_pathjson()