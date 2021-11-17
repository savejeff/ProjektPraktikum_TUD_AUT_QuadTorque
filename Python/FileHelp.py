import os
import shutil
from pathlib import Path


#################################################
#
# link for encodings : https://docs.python.org/3/library/codecs.html
#
#
#
#################################################

ENCODING_ASCII = 'ascii'
ENCODING_UTF_8 = 'utf_8'
ENCODING_LATIN_1 = 'latin_1'

def file_get_filesize_human(bytes, units=[' bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB']):
	""" Returns a human readable string representation of bytes """
	return (str(bytes) if isinstance(bytes, int) else "{:.2f}".format(bytes)) + units[0] if bytes < 1024 else file_get_filesize_human(bytes / 1024, units[1:])

def file_name_swap_extension(filename : str, new_Ext : str) -> str:
	if(new_Ext[0] != "."):
		new_Ext = "." + new_Ext
	return file_name_remove_extension(filename) + new_Ext

def file_name_remove_extension(filename : str) -> str:
	"""
	Removes file extension from a file name like "test.txt"
	:param filename:
	:return:
	"""
	ext = file_name_get_extension(filename)
	return filename[:-len(ext)]


# Low Level Func
def file_get_filename(fullpath):
	import os.path
	path, filename = os.path.split(fullpath)
	return filename


def file_get_path(fullpath):
	"""
	Splits of filename and returns path without filename
	:param fullpath: filepath with filename
	:return: only path without filename
	"""
	import os.path
	path, filename = os.path.split(fullpath)
	return path



def get_files_Folder(path, ext="", withpath=False):
	import os
	Files = []
	for file in os.listdir(path):
		if len(ext) == 0 or file.endswith(ext):
			if(withpath):
				file = path_join(path, file)
			Files.append(file)
	return Files


# return file extension of filepath - zb.: '.mat'
def file_name_get_extension(path):
	if "." not in path:
		return ""

	import os
	filename = os.path.basename(path)
	return "." + (filename.split(".")[-1])


def isFile(path):
	path = fix_path(path)
	import os.path
	return os.path.isfile(path)


def isFolder(path):
	path = fix_path(path)
	import os.path
	return os.path.isdir(path)

def folder_exisits(path):
	return file_exists(path)

def file_exists(name, path=".\\"):
	import os.path
	if not isAbsolutPath(name):
		name = path_join(path, name)

	name = fix_path(name)
	return os.path.exists(name)



def file_find(name, path):
	""" Finds file with name in path. name can have wildcard character * in it to match pattern """
	import re
	pattern = name.replace(".", "\.").replace("*", ".*")
	filenames = get_files_Folder(path, withpath=False)
	for f in filenames:
		if(re.search(pattern, f)):
			return f

	return None



def fix_path(filepath):
	# return str(Path(filepath))
	return filepath.replace("\\", "/")


def isAbsolutPath(filepath):
	if (filepath.startswith("./")):
		return True
	return (os.path.isabs(fix_path(filepath)))

def getAbsolutePath(relpath):
	from os.path import abspath
	return abspath(relpath)

def getBasePath():
	""" returns path that corresponds to './'  """
	return getAbsolutePath("./")

def path_join(path, filename):
	"""
	Join Path and Filename/Foldername
	:param path: base path
	:param filename: filename/foldername or List of Foldernames
	:return: resulting path
	"""
	# if (path[-1] not in ["\\", "/"]):
	#	path += "\\"
	# return path + filename
	if isinstance(filename, list):
		if len(filename) == 0:
			return path
		else:
			return path_join(path_join(path, filename[0]), filename[1:])

	path = Path(fix_path(path))
	return str(path / filename)

#splits path to file to path and filename
def path_split(fullpath):
	import os
	return os.path.split(fullpath)

def path_go_up(path):
	return path_split(path)[0]

#returns absolute path to .py file that was executed to start this thread
def get_Basepath():
	import os
	import sys
	basepath = path_go_up(sys.argv[0])
	return os.path.abspath(basepath)

def get_files_in_Folder(path, ext="", withpath=False):
	path = fix_path(path)
	import os
	Files = []
	try:
		for file in os.listdir(path):
			if len(ext) == 0 or file.endswith(ext):
				if (withpath):
					file = os.path.join(path, file)
				Files.append(file)
	except:
		print("get_files_in_Folder: Error with access to '{}'".format(path))
		return []
	return Files


def get_subFolders(path, withpath=False):
	path = fix_path(path)
	import os
	Files = []
	for file in os.listdir(path):
		filepath = os.path.join(path, file)
		if os.path.isdir(filepath):
			if (withpath):
				Files.append(filepath)
			else:
				Files.append(file)
	return Files


def load_filesystemdict(path_base):
	"""
	load_filesystemdict("C:/abc")
	{
		"file1.txt" : "C:/abc/file1.txt"
		"folder1" : {
						"file2.txt" : "C/abc/folder1/file2.txt"
					}
	}
	:param path_base:
	:return:
	"""

	filesdict = {}
	for file in get_files_in_Folder(path_base):
		filesdict[file] = path_join(path_base, file)

	for dir in get_subFolders(path_base):
		filesdict[dir] = load_filesystemdict(path_join(path_base, dir))

	return filesdict


def mkdir(path):
	path = fix_path(path)
	import os
	if not os.path.exists(path):
		os.makedirs(path)


def delete_filesinfolder(folderpath):
	for file in get_files_in_Folder(folderpath, withpath=True):
		file_delete(file)


def file_delete(filename):
	filename = fix_path(filename)
	if (file_exists(filename)):
		os.remove(filename)
	else:
		print("file_delete: File '{}' does not exists")


def folder_delete(folderpath):
	from pathlib import Path

	if not file_exists(folderpath):
		print("folder_delete: folder does not exists")
		return

	def rmdir(directory):
		directory = Path(directory)
		for item in directory.iterdir():
			if item.is_dir():
				rmdir(item)
			else:
				item.unlink()
		directory.rmdir()

	rmdir(Path(folderpath))

	#shutil.rmtree(folderpath)

def folder_copy(dir_src, dir_dst):
	import shutil, errno
	try:
		shutil.copytree(dir_src, dir_dst)
	except OSError as exc: # python >2.5
		if exc.errno == errno.ENOTDIR:
			shutil.copy(dir_src, dir_dst)
		else: raise

def file_move(src, dst_dir, override=True, newFileName=None):
	if (not newFileName):
		newFileName = file_get_filename(src)

	dst = path_join(dst_dir, newFileName)

	if (file_exists(newFileName, dst_dir)):
		if (not override):
			return
		file_delete(dst)

	shutil.move(src, path_join(dst_dir, newFileName))

	if (not override):
		print("File copyed {}".format(file_get_filename(src)))


def file_copy(src, dst_dir, override=True, newFileName=None):
	"""
	Copys file from src-path to dst_dir
	:param src:
	:param dst_dir:
	:param override: override file if exists in dst_dir
	:param newFileName: optional new filename in dst_dir
	:return: None if not copyed - else path to new file in dst_dir
	"""
	src = fix_path(src)

	if (not newFileName):
		newFileName = file_get_filename(src)

	if (not override and file_exists(newFileName, dst_dir)):
		return

	dst = path_join(dst_dir, newFileName)

	from shutil import copy
	copy(src, dst)

	if (not override):
		print("File copyed {}".format(file_get_filename(src)))

	return dst


def file_copy_folder(src_dir, dst_dir, override=True, extonly=""):
	src_dir = fix_path(src_dir)

	for filepath in get_files_in_Folder(src_dir, withpath=True):
		if (filepath.endswith(extonly)):
			file_copy(filepath, dst_dir, override)



"""
def store_txt(text, filename, path=""):
	if ("." not in filename):
		filename += '.txt'

	if (isAbsolutPath(filename)):
		filename = filename
	else:
		filename = path_join(path, filename)

	path = fix_path(filename)

	with open(path, "w", encoding=ENCODING_UTF_8) as text_file:
		print(text, file=text_file)
"""

def load_file_lines(filename, path="", encoding=ENCODING_UTF_8):
	if ("." not in filename):
		filename += '.txt'

	if (isAbsolutPath(filename)):
		filename = filename
	else:
		filename = path_join(path, filename)

	path = fix_path(filename)

	if not file_exists(path):
		print("load_file_lines: file {} does not exist".format(path))
		return []


	def fix_end_of_line(l):
		""" you may also want to remove whitespace characters like `\n` at the end of each line """

		if l.startswith("\ufeff"):
			return l[len("\ufeff"):]

		if l.endswith("\r\n"):
			return l[:-2]
		elif l.endswith("\n"):
			return l[:-1]
		return l

	content = []
	line_num = 0
	with open(path, encoding=encoding) as f:
		content = f.readlines()

		#Read line by line for debug
		"""
		while True:
			try:
				l = f.readline()
				if l:
					content.append(l)
					line_num += 1
				else:
					break
			except:
				print("Error with File line {} after line '{}'".format(line_num, content[-1]))
				break
		"""




	# content = [x[:-2] + x[-2:].strip() for x in content]
	return [fix_end_of_line(l) for l in content]

def load_file_lines_robust(filename, path="", encoding=ENCODING_UTF_8) -> 'list[str]':
	"""
	Loads lines of file
	-> as binary and removes all lines what can not be encoded
	:param filename:
	:param path:
	:param encoding:
	:return:
	"""
	if ("." not in filename):
		filename += '.txt'

	if (isAbsolutPath(filename)):
		filename = filename
	else:
		filename = path_join(path, filename)

	path = fix_path(filename)

	if not file_exists(path):
		print("load_file_lines: file {} does not exist".format(path))
		return []


	def fix_end_of_line(l):
		""" you may also want to remove whitespace characters like `\n` at the end of each line """
		if l.startswith("\ufeff"):
			return l[len("\ufeff"):]

		if l.endswith("\r\n"):
			return l[:-2]
		elif l.endswith("\n"):
			return l[:-1]
		return l

	content = []
	line_num = 0

	data = load_file_bytes(path)
	start = 0
	while(True):
		end = data.find(bytes('\n', encoding='ascii'), start) + 1
		if(end < 0 or end <= start):
			break

		line_num += 1
		line = ""
		try:
			line = data[start:end].decode("ascii")
		except:
			print("load_file_lines_robust: error in line {}".format(line_num))
			print("line bytes: {}".format(data[start:end]))
			line = ""

		line = fix_end_of_line(line)
		#print(line)
		content.append(line)
		start = end

		if(line_num % 100 == 0):
			print("\r{} / {}".format(start, len(data)), end="")
	print()

	return content


def store_file_lines(Lines : '[str]', filename : str, path=""):
	if ("." not in filename):
		filename += '.txt'

	if (isAbsolutPath(filename)):
		filename = filename
	else:
		filename = path_join(path, filename)

	path = fix_path(filename)
	with open(path, 'w', encoding=ENCODING_UTF_8) as outputfile:
		for line in Lines:
			outputfile.write("%s\n" % line)


def load_file_text_recure(filename):
	data = load_file_bytes(filename)
	#for i in range(len(data)):
	#	if data[i]
	return "".join([chr(b) for b in data])
	#return data.decode("ascii")

def load_file_bytes(filepath, n=-1):
	if not file_exists(filepath):
		print("load_file_bytes: file {} does not exist".format(filepath))
		return []


	ifile = open(filepath, 'rb')
	data = ifile.read(n)
	ifile.close()
	return data


def store_file_bytes(filepath, data):
	ofile = open(filepath, 'wb')
	ofile.write(data)
	ofile.close()


def File_write_Data(path, data):
	path = fix_path(path)
	print("File write Data to: '{}'".format(path))
	file_ = open(path, 'wb')
	file_.write(data)
	file_.close()



def zipFolder(folderpath, switch_ext=[]):
	folderpath = fix_path(folderpath)
	import zipfile
	import os
	zipfilepath = '{}.zip'.format(folderpath)
	zipf = zipfile.ZipFile(zipfilepath, 'w', zipfile.ZIP_DEFLATED)

	for root, dirs, files in os.walk(folderpath):
		for file in files:
			if (file_name_get_extension(file) in switch_ext):
				continue
			zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), root))
	zipf.close()
	return zipfilepath


##############################
#	   load/store txt	   #
##############################


def load_txt(filename : str, path="", encoding=ENCODING_UTF_8) -> str:
	if ("." not in filename):
		filename += '.txt'

	if (isAbsolutPath(filename)):
		filename = filename
	else:
		filename = path_join(path, filename)

	path = fix_path(filename)

	if not file_exists(path):
		print("load_txt: file {} does not exist".format(path))
		return ""

	with open(path, encoding=encoding) as f:
		content = f.read()

	return content


def store_txt(text : str, filename : str, path="", encoding=ENCODING_UTF_8):

	#if not filename.endswith('.txt'):
	if "." not in filename:
		filename += '.txt'

	if (isAbsolutPath(filename)):
		filename = filename
	else:
		filename = path_join(path, filename)

	filename = fix_path(filename)

	# If the file name exists, write a JSON string into the file.
	if filename:
		# Writing text
		with open(filename, "w", encoding=encoding) as text_file:
			print(text, file=text_file)

##############################
#	   load/store bin	   #
##############################


def load_bin(filename : str, path="") -> bytes:
	if ("." not in filename):
		filename += '.bin'

	if (isAbsolutPath(filename)):
		filename = filename
	else:
		filename = path_join(path, filename)

	path = fix_path(filename)

	if not file_exists(path):
		print("load_bin: file {} does not exist".format(path))
		return bytes()

	with open(path, mode="rb") as f:
		content = f.read()

	return content


def store_bin(data : bytes, filename : str, path=""):

	#if not filename.endswith('.txt'):
	if "." not in filename:
		filename += '.bin'

	if (isAbsolutPath(filename)):
		filename = filename
	else:
		filename = path_join(path, filename)

	filename = fix_path(filename)

	# If the file name exists, write a JSON string into the file.
	if filename:
		# Writing text
		with open(filename, "wb") as text_file:
			text_file.write(data)


##############################
#	   load/store json	  #
##############################

def json_string(s):
	import json
	return json.loads(s)


def json_dump(data, compact=False, ensure_ascii=False):
	import json
	if (compact):
		return json.dumps(data, ensure_ascii=ensure_ascii)
	else:
		return json.dumps(data, indent=4, sort_keys=True, ensure_ascii=ensure_ascii)


def update_json(newdata, filename : str, path=""):
	data = load_json(filename, path)
	data.update(newdata)
	store_json(data, filename, path)


def exits_json(filename : str, path="") -> bool:
	if not filename.endswith(".json"):
		filename += '.json'

	if not isAbsolutPath(filename):
		filename = path_join(path, filename)

	filename = fix_path(filename)
	return file_exists(filename)


def store_json(data : dict, filename : str, path="", compact=False, ensure_ascii=False):
	import json

	if not filename.endswith(".json"):
		filename += '.json'

	if not isAbsolutPath(filename):
		filename = path_join(path, filename)

	filename = fix_path(filename)

	# If the file name exists, write a JSON string into the file.
	if filename:
		# Writing JSON data
		with open(filename, 'w', encoding=ENCODING_UTF_8) as f:
			if (compact):
				json.dump(data, f, ensure_ascii=ensure_ascii)
			else:
				json.dump(data, f, indent=4, sort_keys=True, ensure_ascii=ensure_ascii)


def load_json(filename : str, path="") -> dict:
	import json
	if not filename.endswith(".json"):
		filename += '.json'

	if not isAbsolutPath(filename):
		filename = path_join(path, filename)

	if (not file_exists(filename)):
		print("load_json: File not found - '{}'".format(filename))
		return {}

	filename = fix_path(filename)

	# TODO very dirty check for utf-8 endocding
	#try:
	#	return json.load(open(filename))
	#except:
	#	# print("load failed. retry with utf-8 encoding")
	#	pass
	return json.load(open(filename, encoding=ENCODING_UTF_8))




##############################
#	 load/store PICKLE	  #
##############################


# PICKLE
#https://docs.python.org/3/library/pickle.html

def store_pkl(data, filename : str, path=""):
	"""Saves an object in pickle format."""
	import pickle

	if not filename.endswith(".pkl"):
		filename += '.pkl'

	if not isAbsolutPath(filename):
		filename = path_join(path, filename)

	filename = fix_path(filename)

	pickle.dump(data, open(filename, 'wb'))

def load_pkl(filename : str, path=""):
	"""Restores an object from a pickle file."""
	import pickle

	if not filename.endswith(".pkl"):
		filename += '.pkl'

	if not isAbsolutPath(filename):
		filename = path_join(path, filename)

	if (not file_exists(filename)):
		print("load_pkl: File not found - '{}'".format(filename))
		return None

	filename = fix_path(filename)
	try:
		data = pickle.load(open(filename, 'rb'))
	except FileNotFoundError:
		data = None
	return data


##############################
#	 load/store numpy	  #
##############################



def store_numpy(data, filename : str, path=""):
	"""Saves an object in npy format."""
	import numpy

	if not filename.endswith(".npy"):
		filename += '.npy'

	if (isAbsolutPath(filename)):
		filename = filename
	else:
		filename = path_join(path, filename)

	filename = fix_path(filename)

	numpy.save(filename, data)

def load_numpy(filename : str, path=""):
	"""Restores an object from a npy file."""
	import numpy

	if not filename.endswith(".npy"):
		filename += '.npy'

	if not isAbsolutPath(filename):
		filename = path_join(path, filename)

	if (not file_exists(filename)):
		print("load_numpy: File not found - '{}'".format(filename))
		return None

	filename = fix_path(filename)
	try:
		data = numpy.load(filename)
	except FileNotFoundError:
		data = None
	return data


##############################
#	 load/store mat files   #
##############################


def store_mat(data : dict, filename : str):
	import scipy.io as sio

	if not filename.endswith(".mat"):
		filename += '.mat'

	print("file storing: {}".format(filename))

	sio.savemat(fix_path(filename), data)
	return
	#old version
	"""
	data_mod = {}
	for group in data:
		for trace in data[group]:
			VarName = "{}__{}".format(group, trace)
			data_mod[VarName] = data[group][trace]
	sio.savemat(filename, data_mod)
	"""


def load_mat(filename : str) -> dict:
	import scipy.io as sio
	import numpy as np

	if not filename.endswith(".mat"):
		filename += '.mat'

	if not file_exists(filename):
		print("load_mat: file not found {}".format(filename))
		return {}

	print("file loading: {}".format(filename))

	file = sio.loadmat(filename)

	Data = {}
	for k in file: #for every group
		if ("__" in k):
			continue
		group = file[k][0][0]
		Data[k] = {}
		try:
			for c in group.dtype.names: #for every channel
				if len(group[c]) == 0:
					continue
				if group[c].dtype.type == np.str_:
					#Data[k][c] = group[c]
					Data[k][c] = [s.rstrip() for s in group[c]]
				#convert to python native

				#elif group[c][0].dtype == "int32":
				elif group[c].dtype.type == np.int32:
					Data[k][c] = group[c][0]
					#Data[k][c] = [int(f) for f in group[c][0]]
				#elif group[c][0].dtype == "float64":
				elif group[c].dtype.type == np.float64:
					Data[k][c] = group[c][0]
					#Data[k][c] = [float(f) for f in group[c][0]]
				else:
					Data[k][c] = group[c][0]

		except Exception as ex:
			raise ex

		if not Data[k]:
			Data.pop(k)


	#old version
	"""
	for key in file:
		if(len(str(key).split("__")) != 2):
			continue

		[group, name] = str(key).split("__")

		trace = file[key]
		trace = np.reshape(trace, len(trace))
		Group = {group:{name:trace}}
		appendDict(Data, Group)
	"""
	return Data


##############################
#	 load/store yaml files  #
##############################


def store_yaml(data, filename : str, path=""):
	import yaml

	if not filename.endswith(".yaml"):
		filename += '.yaml'

	if not isAbsolutPath(filename):
		filename = path_join(path, filename)

	filename = fix_path(filename)

	# If the file name exists, write a YAML string into the file.
	if filename:
		# Writing YAML data
		with open(filename, 'w', encoding='utf8') as f:
			yaml.dump(data, f, default_flow_style=False, allow_unicode=True)


def load_yaml(filename, path=""):
	# https://stackoverflow.com/questions/1773805/how-can-i-parse-a-yaml-file-in-python
	import yaml



	if not filename.endswith(".yaml"):
		filename += '.yaml'

	if not isAbsolutPath(filename):
		filename = path_join(path, filename)

	if (not file_exists(filename)):
		print("load_yaml: File not found - '{}'".format(filename))
		return {}

	filename = fix_path(filename)

	with open(filename, 'r') as f:
		try:
			return yaml.safe_load(f)
		except yaml.YAMLError as exc:
			print(exc)
			return None

##############################
#	 load/store hdf5 files  #
##############################


def store_hdf5(data, filename, path=""):
	"""
	stores a dict of numpy matrixes
	:param data: dict {string_key -> numpy matrix}
	"""
	import h5py

	if not filename.endswith(".hdf5"):
		filename += '.hdf5'

	if not isAbsolutPath(filename):
		filename = path_join(path, filename)

	filename = fix_path(filename)

	# Write data to HDF5
	with h5py.File(filename, "w") as data_file:
		for key, mat in data.items():
			data_file.create_dataset(key, data=mat)

def load_hdf5(filename, path=""):
	"""
	load a hdf5 file
	:return: dict {string_key -> numpy matrix}
	"""
	# https://stackoverflow.com/questions/28170623/how-to-read-hdf5-files-in-python/41586571#41586571
	import h5py

	if not filename.endswith(".hdf5"):
		filename += '.hdf5'

	if not isAbsolutPath(filename):
		filename = path_join(path, filename)

	if (not file_exists(filename)):
		print("load_hdf5: File not found - '{}'".format(filename))
		return {}

	filename = fix_path(filename)

	with h5py.File(filename, "r") as f:
		# List all groups
		#print("Keys: %s" % f.keys())
		data = {k: f[k] for k in f.keys()}
		return data


##############################
#	 load/store csv files  #
##############################

def load_csv_wHeader(filename, path="", mode=0, sample_func=lambda x: x):
	"""
	reads csv file and returns as
	list of dict/samples
	[
		{ trace1: 0, trace2: 2 },
		{ trace1: 1, trace2: 2 },
		{ trace1: 2, trace2: 2 },
		{ trace1: 3, trace2: 2 },
		{ trace1: 4, trace2: 2 }
	]
	:param filename:
	:return:
	"""
	import csv

	if not filename.endswith(".csv"):
		filename += '.csv'

	if not isAbsolutPath(filename):
		filename = path_join(path, filename)

	if (not file_exists(filename)):
		print("load_csv: File not found - '{}'".format(filename))
		return {}

	filename = fix_path(filename)
	data_raw = []

	with open(filename, encoding=ENCODING_UTF_8) as csvfile:
		csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for row in csv_reader:
			data_raw.append([l.replace("\ufeff", "") for l in row])

	if (len(data_raw) == 0):
		return {}

	header = []
	rows = []
	for i, line in enumerate(data_raw):
		if len(line) == 0:
			continue
		if line[0].startswith("#"):
			continue

		header = line
		rows = data_raw[i + 1:]
		break

	if not rows:
		return {}

	del data_raw



	# mode0: list of dicts/samples (every line is a sample)
	if mode == 0:
		res = []

		for row in rows:
			sample = row

			assert len(sample) == len(header)

			dic = {}
			for col, tag in enumerate(header):
				try:
					dic[header[col]] = sample_func(sample[col])
				except:
					print("load_csv_wHeader mode2: Error with {} : {}".format(tag, sample[col]))

			res.append(dic)

		return res

	# mode1: dict of lists/traces (every column is a trace)
	elif mode == 1:

		last_ghost_sample = False #every line ends with ',' and causes empty sample for every line at end
		if len(header[-1]) == 0:
			last_ghost_sample = True
			header = header[:-1]

		res = {tag : [] for tag in header}
		for row in rows:
			sample = row
			if last_ghost_sample:
				sample = sample[:-1]

			assert len(sample) == len(header)

			for col, tag in enumerate(header):
				try:
					res[tag].append(sample_func(sample[col]))
				except:
					print("load_csv_wHeader mode1: Error with {} : {}".format(tag, sample[col]))


		return res

	return None

def load_csv(filename, path=""):
	"""
	reads csv file and returns as
	list of dict/samples
	[
		{ trace1: 0, trace2: 2 },
		{ trace1: 1, trace2: 2 },
		{ trace1: 2, trace2: 2 },
		{ trace1: 3, trace2: 2 },
		{ trace1: 4, trace2: 2 }
	]
	:param filename:
	:return:
	"""
	import csv

	if not filename.endswith(".csv"):
		filename += '.csv'

	if not isAbsolutPath(filename):
		filename = path_join(path, filename)

	if (not file_exists(filename)):
		print("load_csv: File not found - '{}'".format(filename))
		return {}

	filename = fix_path(filename)
	data_raw = []

	with open(filename, encoding=ENCODING_UTF_8) as csvfile:
		csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for row in csv_reader:
			data_raw.append([l.replace("\ufeff", "") for l in row])

	if (len(data_raw) == 0):
		return {}

	header = []
	rows = []
	for i, line in enumerate(data_raw):
		if len(line) == 0:
			continue
		if line[0].startswith("#"):
			continue

		header = line
		rows = data_raw[i + 1:]
		break

	if not rows:
		return {}

	del data_raw

	res = []
	for row in rows:
		dic = {}
		for col in range(len(row)):
			try:
				dic[header[col]] = row[col]
			except:
				pass
		res.append(dic)

	return res

def load_csv2(filename, path="", sample_func=lambda x: x):
	"""
	reads csv file and returns as dict of traces
	every line must contain value for every tag from header
	example:
	{
		trace1: [0, 1, 2, 3, 4],
		trace2: [2, 2, 2, 2, 2]
	}


	:param filename:
	:param sample_func: modifier function that is applied to every value of every trace. usefull for converting all values to int/float
	:return:
	"""
	import csv

	if not filename.endswith(".csv"):
		filename += '.csv'

	if not isAbsolutPath(filename):
		filename = path_join(path, filename)

	if (not file_exists(filename)):
		print("load_csv: File not found - '{}'".format(filename))
		return {}

	filename = fix_path(filename)
	data_raw = []

	with open(filename, encoding=ENCODING_UTF_8) as csvfile:
		csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for row in csv_reader:
			data_raw.append([l.replace("\ufeff", "") for l in row])

	if (len(data_raw) == 0):
		return []

	header = data_raw[0]

	last_ghost_sample = False #every line ends with ',' and causes empty sample for every line at end
	if len(header[-1]) == 0:
		last_ghost_sample = True
		header = header[:-1]

	res = {tag : [] for tag in header}
	for row in data_raw[1:]:
		sample = row
		if last_ghost_sample:
			sample = sample[:-1]

		assert len(sample) == len(header)

		for i, tag in enumerate(header):
			try:
				res[tag].append(sample_func(sample[i]))
			except:
				print("read_csv2: Error with {} : {}".format(tag, sample[i]))

	del data_raw
	return res

def store_csv(data : list, filename : str, path=""):
	"""
	stores a list of dicts to a csv file
	:param data: list of dicts | [{string_key -> value}]
	"""
	import csv

	if not filename.endswith(".csv"):
		filename += '.csv'

	if not isAbsolutPath(filename):
		filename = path_join(path, filename)

	filename = fix_path(filename)
	keys = list(data[0].keys())
	writer = csv.writer(open(filename, 'w', newline=''))
	writer.writerow(keys)
	for d in data:
		writer.writerow([d[k] for k in keys])

def store_csv2(data : dict, filename : str, path=""):
	"""
	stores a dict of lists to a csv file
	:param data: dict of lists | {string_key -> [values]}
	"""
	import csv

	if not filename.endswith(".csv"):
		filename += '.csv'

	if not isAbsolutPath(filename):
		filename = path_join(path, filename)

	filename = fix_path(filename)
	keys = list(data.keys())
	count = len(data[keys[0]])
	writer = csv.writer(open(filename, 'w', newline=''))
	writer.writerow(keys)
	for i in range(count):
		writer.writerow([data[k][i] for k in keys])

##########################################
#			  Dialogs				   #
##########################################

def OpenFilePickerDialog(basepath="", fileextentions=[], titel="Select a File"):
	"""

	:param basepath:
	:param fileextentions: list of extensions
	:return:
	"""
	from tkinter import Tk	 # from tkinter import Tk for Python 3.x
	from tkinter import filedialog

	Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing

	# show an "Open" dialog box and return the path to the selected file
	"""
	if basepath:
		filename = filedialog.askopenfilename(initialdir = basepath)
	else:
		filename = filedialog.askopenfilename()
	"""

	# https://stackoverflow.com/questions/44403566/add-multiple-extensions-in-one-filetypes-mac-tkinter-filedialog-askopenfilenam
	#filetypes=[("Excel files", ".xlsx .xls")]

	if isinstance(fileextentions, str):
		fileextentions = [fileextentions]

	filetypes = [(ext, ext) for ext in fileextentions]


	filename = filedialog.askopenfilename(
		title=titel,
		initialdir = basepath,
		filetypes=filetypes
	)

	return filename

def OpenFolderPickerDialog(basepath="", titel="Select a Folder"):
	"""

	:param basepath:
	:param fileextentions: list of extensions
	:return:
	"""
	from tkinter import Tk	 # from tkinter import Tk for Python 3.x
	from tkinter import filedialog

	Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing

	"""
	filename = filedialog.askopenfilename(
		title=titel,
		initialdir = basepath,
		filetypes=filetypes
	)
	"""
	folder_selected = filedialog.askdirectory(
		title=titel,
		initialdir = basepath
	)

	return folder_selected



"""				   FUNC FROM HELP -- TODO integrate """


#File Functions


def save_string(data, name, path=".\\"):
	if (not path):
		path = ""
	elif (path[-1] != '\\'):
		path += '\\'

	filename = path + name + '.txt'

	# Writing JSON data
	with open(filename, 'w') as f:
		f.write(data)

"""
def save_json(data, filename, path=None, compact=False, ensure_ascii=False):
	import json
	if path != None:
		filename = path_join(path, filename)

	if not filename.endswith(".json"):
		print("Warning: save_json - filename does not end in .json '{}'".format(filename))
		#filename += '.json'

	assert filename.endswith(".json")

	if filename:
		# Writing JSON data
		with open(filename, 'w', encoding='utf8') as f:
			if(compact):
				json.dump(data, f, ensure_ascii=ensure_ascii)
			else:
				json.dump(data, f, indent=4, sort_keys=True, ensure_ascii=ensure_ascii)


def load_json(filename, path=None):
	import json
	if path != None:
		filename = path_join(path, filename)

	if not filename.endswith(".json"):
		print("Warning: save_json - filename does not end in .json '{}'".format(filename))
		#filename += '.json'

	assert filename.endswith(".json")

	#return json.load(open(filename))
	return json.load(open(filename, encoding='utf-8'))
"""

def path_get_filename(fullpath, remove_ext=False):
	import os.path
	path, filename = os.path.split(fullpath)
	if remove_ext:
		filename = file_name_remove_extension(filename)
	return filename

	#alternative implementation
	"""
	import os
	res = os.path.basename(path)
	while (remove_ext and len(res) > 0 and res[-1] != '.'):
		res = res[:-1]

	if (len(res) == 0):
		return os.path.basename(path)

	return res[:-1]
	"""


"""
def file_exists(name, path=""):
	import os.path
	return os.path.exists(path + name)


def get_files_Folder(path, ext="", withpath=False):
	import os
	Files = []
	for file in os.listdir(path):
		if len(ext) == 0 or file.endswith(ext):
			if(withpath):
				file = os.path.join(path, file)
			Files.append(file)
	return Files

def get_subFolders(path, withpath=False):
	import os
	Files = []
	for file in os.listdir(path):
		filepath = os.path.join(path, file)
		if os.path.isdir(filepath):
			if (withpath):
				Files.append(filepath)
			else:
				Files.append(file)
	return Files

def mkdir(path):
	import os
	if not os.path.exists(path):
		os.makedirs(path)
		return True
	return False

def file_copy(src, dst_dir, override=True):
	if(not override and file_exists(file_get_filename(src), dst_dir)):
		return

	from shutil import copy
	copy(src, dst_dir)

	if (not override):
		print("File copyed {}".format(file_get_filename(src)))


def file_copy_folder(src_dir, dst_dir, override=True):
	for filepath in get_files_Folder(src_dir, withpath=True):
		file_copy(filepath, dst_dir, override)
"""


if __name__ == '__main__':

	if False:
		"""loop read from rx queue and write to file"""
		file = open('./tmp/test.txt', 'w')
		for rx_data in ["hallo", "world", "blabla"]:
				print(">>>{}".format(rx_data.encode("ascii")))
				file.write(rx_data)

		file.write("\nXXXCLOSINGXXX")
		file.close()

	#data = load_yaml("../tmp/out.yaml")
	#print(data)
	#store_yaml(data, "./tmp/test.yaml")

	if False:
		data = [
			{"a" : 0, "b" : "c", "c": 0.1},
			{"a" : 1, "b" : "d", "c": 0.2},
			{"a" : 2, "b" : "e", "c": 0.3},
		]
		path = "./tmp/test.csv"
		store_csv(data, path)
		print(load_csv(path))

	if False:
		data = {
			"a" : [0, 1, 2],
			"b": ["c", "d", "e"],
			"c": [0.1, 0.2, 0.3],
		}
		path = "./tmp/test.csv"
		store_csv2(data, path)
		print(load_csv(path))