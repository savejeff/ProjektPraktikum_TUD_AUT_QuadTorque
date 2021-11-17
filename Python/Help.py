from Defines import *
#from FileHelp import *
#from StatisticHelp import *
#from HelpMath import *
#from UserHelp import *

#import numpy
import numpy as np
#import scipy.io as sio
from pprint import pprint

OS_LINUX = "Linux"
OS_MAC = "Darwin"
OS_WINDOWS = "Windows"
def getOS_Name():
	import platform
	return platform.system()

def isLinux():
	return getOS_Name() == OS_LINUX

def isWindows():
	return getOS_Name() == OS_WINDOWS

def isMac():
	return getOS_Name() == OS_MAC

def all_in(elements : list, all_elements : list) -> bool:
	"""
	Checks if all elements are in all_elements
	:param elements: list of elements to search for
	:param all_elements: list of elements to search in
	:return:
	"""
	return all(x in all_elements for x in elements)

def any_in(elements : list, all_elements : list) -> bool:
	"""
	Checks if any elements are in all_elements
	:param elements: list of elements to search for
	:param all_elements: list of elements to search in
	:return:
	"""
	return any(x in all_elements for x in elements)

def shuffle(x):
	""" returns a shuffled version of the given list x"""
	import random
	y = x[:]
	random.shuffle(y)
	return y

def chunks(lst, n, force_len=False):
	"""Yield successive n-sized chunks from lst."""
	l = len(lst)
	if force_len:
		l -= len(lst) % n
	for i in range(0, l, n):
		yield lst[i:i + n]

from copy import deepcopy

def LIMIT(LOWER, value, UPPER):
	return min(max(value, LOWER), UPPER)


def getHash(data):
	"""
	Returns given data as a has
	:param data: bytes or string
	:return: (bytes, hex string)
	"""
	if isinstance(data, str):
		data = data.encode('utf-8')

	import hashlib
	m = hashlib.sha256()
	m.update(data)
	return m.digest(), m.hexdigest()


def getTimeStampString():
	import datetime
	return str(datetime.datetime.utcnow()).replace(" ", "_").replace(":", "")
def between(minv, val, maxv):
	return minv if val < minv else maxv if val > maxv else val

# intersection of two lists
def intersection(lst1, lst2):
	return list(set(lst1) & set(lst2))

def delay(ms):
	from time import sleep
	sleep(ms / 1000)

_millis0 = None
def millis():
	"""
	mimics behavior of Arduino millis function.
	returns milliseconds since start of system.
	can only be used differencial
	"""
	import time
	global _millis0
	if _millis0 == None:
		_millis0 = int(time.time() * 1000)

	return int(time.time() * 1000) - _millis0


def beep():
	import winsound
	duration = 1000  # millisecond
	freq = 666  # Hz
	winsound.Beep(freq, duration)

def filter_string_f(s, bfunc):
	return ''.join([c for c in s if bfunc(c)])

def filter_string(text, unwanted):
	res = ""
	for c in text:
		if(c not in unwanted):
			res += c
	return c


def split_at_func(s, func):
	res = []
	buff = ""
	for c in s:
		if (not func(c)):
			buff += c
		else:
			res += [buff]
			buff = ""
			res += [c]

	if (buff != ""):
		res += [buff]
	return res

def delKey(dict, key):
	if(key in dict):
		dict.pop(key)


def SubDict(listofkeys, localDict):
	newdict = {}
	for key in listofkeys:
		if(key in localDict):
			newdict[key] = localDict[key]
	return newdict


def getRange(count, offset=0):
	return list([i + offset for i in range(count)])


def endswith(str, end):
	return str[-(len(end)):] == end

def getRandomRange(min=0, max=1):
	return getRandom(max - min) + min

def getRandom(max=1):
	return np.random.random() * max

def shuffleArray(arr):
	np.random.shuffle(arr)

def getRandomInt(min=0, max=1):
	return int(np.random.random_integers(min, max))

def getRandomIntRange(range):
	return getRandomInt(range[0], range[1])


def ArrayRemoveAt(Array, position):
	return [Array[i] for i in range(len(Array)) if i != position]

#bearbeitet arr nicht
def subArray(arr, val):

	if(isinstance(val, list)):
		if(len(arr) == len(val)):
			res = arr[:]
			for i in range(len(res)):
				if(isinstance(res[i], list) and isinstance(val[i], list)):
					res[i] = subArray(res[i], val[i])
				else:
					res[i] -= val[i]
			return res
		else:
			print("ERROR: arrays musst have same length")
			return None

	return list([v - val for v in arr])


def addArray(arr, val):
	if (isinstance(val, list)):
		if (len(arr) == len(val)):
			for i in range(len(arr)):
				arr[i] = arr[i] + val[i]
				return arr
		else:
			print("ERROR: arrays musst have same length")
			return None

	return list([v + val for v in arr])

#Array-of-Dict to Dict-of-Array
def ArrayofDict_2_DictofArray(ArrayofDicts):
	Tags = ArrayofDicts[0].keys()
	DictofArrays = {}
	for t in Tags:
		DictofArrays[t] = [Stat[t] for Stat in ArrayofDicts if t in Stat]
	return DictofArrays

#Dict-of-Array to Array-of-Dict
def DictofArray_2_ArrayofDict(Dict_of_Arrays):
	Tags = list(Dict_of_Arrays.keys())
	arr_len = len(Dict_of_Arrays[Tags[0]])
	Array_of_Dicts = []
	for i in range(arr_len):
		Array_of_Dicts.append(
			{tag : Dict_of_Arrays[tag][i] for tag in Tags}
		)
	return Array_of_Dicts

def switchArrayDim(array):
	if(isinstance(array, np.ndarray)):
		return np.transpose(array)

	res = []
	for x in range(len(array)):
		for y in range(len(array[x])):
			if (len(res) - 1 < y):
				res.append([])
			res[y].append(array[x][y])

	return res

	#alternative implemenation
	"""
	res = []
	for x in range(len(array)):
		for y in range(len(array[x])):
			if (len(res) - 1 < y):
				res.append([])
			res[y].append(array[x][y])

	return res
	"""



def isNPArray(array):
	return isinstance(array, np.ndarray)


def removeEndbevorChar(text, char='.'):
	res = text

	while (len(res) > 0 and res[-1] != char):
		res = res[:-1]

	if (len(res) == 0):
		return text

	return res[:-1]



def addDict(dict1, dict2):
	for key in dict1:
		if(key in dict2):
			if isinstance(dict1[key], dict):
				addDict(dict1[key], dict2[key])
			else:
				dict1[key] += dict2[key]
	for key in dict2:
		if(key not in dict1):
			dict1[key] = dict2[key]

def appendDict(dict1, dict2):
	for key in dict1:
		if(key in dict2):
			if isinstance(dict1[key], dict):
				appendDict(dict1[key], dict2[key])
			else:
				if(not isinstance(dict1[key], list)):
					dict1[key] = [dict1[key]]

				dict1[key].append(dict2[key])
	for key in dict2:
		if(key not in dict1):
			dict1[key] = dict2[key]

def divDict(dict1, devider):
	for key in dict1:
		if isinstance(dict1[key], dict):
			divDict(dict1[key], devider)
		else:
			dict1[key] /= devider


#Takes List of Dict(Key->Value) and returns avg of every key
def avgDicts(ListofDicts):
	ResDict = {}
	for d in ListofDicts:
		addDict(ResDict, d)

	divDict(ResDict, len(ListofDicts))
	return ResDict

#applies func to every key of Dict
def funcDict(dict1, func=lambda x : x):
	if isinstance(dict1, list):
		return [funcDict(d, func) for d in dict1]
	for key in dict1:
		if isinstance(dict1[key], dict):
			funcDict(dict1[key], func)
		else:
			dict1[key] = func(dict1[key])

def addList(l1, l2):
	for i in range(len(l1)):
		if(isinstance(l2, list)):
			l1[i] += l2[i]
		else:
			l1[i] += l2
	return l1

def subList(l1, l2):
	for i in range(len(l1)):
		if(isinstance(l2, list)):
			l1[i] -= l2[i]
		else:
			l1[i] -= l2
	return l1

def absList(l1):
	for i in range(len(l1)):
		l1[i] = abs(l1[i])
	return l1

def divList(list, devider):
	for i in range(len(list)):
		list[i] /= devider
	return list

def getSubDict(Dic, keys):
	subDic = {}
	for key in keys:
		if key in Dic:
			subDic[key] = Dic[key]
	return subDic




def getTimeString(Seconds):
	""" returns timesting for minutes and seconds and microseconds like 01:36:123 """
	return "{:02}:{:02}:{:03}".format(int(Seconds / 60), int(Seconds % 60), int((Seconds * 100) % 100))

def getTimeString_hhmmss(Seconds):
	hh = int(Seconds / (60*60))
	Seconds = Seconds % (60*60)
	mm = int(Seconds / 60)
	Seconds = int(Seconds % 60)
	ss = Seconds
	return "{:02}:{:02}:{:02}".format(hh,mm,ss)


def Time_split_HHMMSS(hhmmss):
	"""
	Splits "083015.350" into hour=8, minute=30, second=15, millisec=350
	:param hhmmss:
	:return: hh, mm, ss, ms
	"""
	ms = int((hhmmss % 1) * 1000)
	hhmmss = int(hhmmss)
	hh = int(hhmmss / 10000)
	hhmmss = hhmmss % 10000
	mm = int(hhmmss / 100)
	hhmmss = hhmmss % 100
	ss = hhmmss

	return hh, mm, ss, ms

def Time_split_DDMMYY(ddmmyy):
	"""
	Splits "300394" into day=30, month=03, year=94
	:param hhmmss: like 300394
	:return: dd, mm, yy
	"""

	dd = int(ddmmyy / 10000)
	ddmmyy = ddmmyy % 10000
	mm = int(ddmmyy / 100)
	ddmmyy = ddmmyy % 100
	yy = int(ddmmyy)

	return dd, mm, yy

def getTime_HHMMSSCCC(daytime_s):
	""" Converts Time of day in Seconds since 00:00 into format HHMMSS.CCC like 123001.120 for 12:30:01:120"""
	time = daytime_s
	h = int(time / 3600 % 3600)
	m = int(time / 60 % 60)
	s = int((time % 60) * 1000) / 1000
	return h * 10000 + m * 100 + s

def getTimeString_hhmmssccc(Seconds):
	""" Converts Time of day in Seconds since 00:00 into format HHMMSS.CCC like "123001.120" for 12:30:01:120"""
	return "{:06.3f}".format(getTime_HHMMSSCCC(Seconds))

def IntValueFromString(dataline, signed=True, isBigEndian=False):
	if isinstance(dataline, bytes):
		line_bytes = dataline
	else:
		line_bytes = bytes(dataline, encoding='ascii')
	#print(line_bytes)
	res = int.from_bytes(line_bytes, byteorder=('big' if isBigEndian else 'little'), signed=signed)
	#print(res)
	return res


def FloatValueFromString(dataline, isBigEndian=False):
	#https://docs.python.org/3/library/struct.html

	if isinstance(dataline, bytes):
		line_bytes = dataline
	else:
		line_bytes = bytes(dataline, encoding='ascii')
	#print(line_bytes)
	from struct import unpack
	res = unpack('>f' if isBigEndian else '<f', line_bytes)[0]
	# print(res)
	return res

def DoubleValueFromString(dataline, isBigEndian=False):
	if isinstance(dataline, bytes):
		line_bytes = dataline
	else:
		line_bytes = bytes(dataline, encoding='ascii')
	#print(line_bytes)
	from struct import unpack
	res = unpack('>d' if isBigEndian else '<d', line_bytes)[0]
	# print(res)
	return res


if __name__ == "__main__":
	pass