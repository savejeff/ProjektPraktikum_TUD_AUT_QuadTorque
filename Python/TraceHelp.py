from Defines import *
from Help import *
from HelpMath import *
from StatisticHelp import *


def time2value(Group, t, TRACE, TIME_TRACE=TRACE_TIME, interpolate=True):
	if interpolate:
		return np.interp(t, Group[TIME_TRACE], Group[TRACE])
	else:
		return Group[TRACE][time2index(Group, t, TIME_TRACE)]

def index2time(Group, i, TIME_TRACE=TRACE_TIME):
	return Group[TIME_TRACE][i]

def time2index(Group, t, TIME_TRACE=TRACE_TIME):
	"""
	returns index closest to given time
	negative t to start from end of trace
	"""
	"""
	#return -1 if time == -1 to indicate last value
	if t == -1:
		return -1
	"""
	#if t < 0:
	#	t = t + Group[TIME_TRACE][-1]

	assert TIME_TRACE in Group

	TimeTrace = Group[TIME_TRACE]
	if len(TimeTrace) == 0:
		return 0

	ts = TimeTrace[0]
	#avg_dt = mean(diff(TimeTrace[0:(min(50, Group_Length(Group)))]))
	avg_dt = (TimeTrace[-1] - TimeTrace[0]) / len(TimeTrace)
	length = Group_Length(Group)

	index = 0
	if avg_dt != 0:
		index = int((t - ts) / avg_dt)
	if index >= length:
		index = length - 1
	last_dt = None
	last_index = index
	while True:
		if index < 0:
			return 0
		if index >= length:
			return length - 1

		dt = TimeTrace[index] - t
		# if old detla was better/lower then current
		if last_dt != None and abs(last_dt) <= abs(dt) and last_dt != dt:

			if abs(last_dt) > avg_dt * 2:
				pass
				#print("Time2Index Warning: dt avg: {} - but found closest has dt {}".format(avg_dt, last_dt))
			"""
			# makes no sense: might be error if last delta was much better/lower then current
			if abs(1.5 * last_dt) < abs(dt):
				if(last_index == index):
					print("")
				print("Time2Index error: t={} {} at index {}->{}s and {}->{}s".format(
					Time, last_dt, last_index, TimeTrace[last_index], index, TimeTrace[index]
					)
				)
				i_low = max(0, min(last_index, index) - 2)
				i_high = min(length, max(last_index, index) + 2)
				print(TimeTrace[i_low:i_high])
				print(np.diff(TimeTrace[i_low:i_high]))
				print()
			"""

			# return last index
			return last_index

		last_index = index
		if dt == 0:
			return index
		if dt > 0:
			index -= 1
		else:
			index += 1

		last_dt = dt

#TODO refactor
def GenerateTimeTrace(dt, t_end, t_start=0):
	"""
	Generates a Time Trace
	:param dt: [s] dt between Samples
	:param t_end: [s]
	:param t_start: [s]
	:return: [List of t]
	"""
	import numpy as np
	return np.linspace(t_start,t_end, int((t_end-t_start) / dt))


def getAVG_TimeDelta(Data, GROUP=None, Simple=True):
	""" Calculates avg dt between samples. Returns dt in s """
	if not GROUP:
		group = Data
	else:
		group = Data[GROUP]
	TimeTrace = group[TRACE_TIME]

	glen = Group_Length(group)
	i_start = 0
	i_end = glen - 1

	if Simple:
		dt = (TimeTrace[i_end] - TimeTrace[i_start]) / (i_end - i_start)
	else:
		#if long group : take 500 samples 25% into trace
		if glen > 1000:
			i_start = int(0.25 * glen)
			i_end = i_start + 500
		dt = mean(diff(TimeTrace[i_start:i_end]))
	if isNaN(dt):
		return None
	return dt


#################################################
#          Basic getter / Setter Functions      #
#################################################


def group_getTimeStartEnd(Group, TIME_TRACE=TRACE_TIME):
	"""
	calculates start and end time of trace
	:return: (t_start, t_end)
	"""
	if(TIME_TRACE in Group):
		return (Group[TIME_TRACE][0], Group[TIME_TRACE][-1])
	else:
		return None, None

def Group_getTimeStartEnd(Data, GROUP, TIME_TRACE=TRACE_TIME):
	"""
	calculates start and end time of trace
	:return: (t_start, t_end)
	"""
	return Trace_getValueStartEnd(Data, GROUP, TIME_TRACE)

def Trace_getValueStartEnd(Data, GROUP, TRACE):
	"""
	calculates start and end time of trace
	:return: (t_start, t_end)
	"""
	if(TRACE in Data[GROUP]):
		return (Data[GROUP][TRACE][0], Data[GROUP][TRACE][-1])
	else:
		return None, None

def Data_getTimeStartEnd(Data):

	times = [group_getTimeStartEnd(Data[GROUP]) for GROUP in Data_getAllGroupNames(Data)]
	t_start = min([s for s, e in times if not (s == None or e == None or s == e == 0)])
	t_end = max([e for s, e in times if not (s == None or e == None or s == e == 0)])
	return t_start, t_end
	"""
	t_end, t_start = None, None
	for GROUP in Data_getAllGroupNames(Data):
		if(t_start == None and t_end == None):
			t_start, t_end = timeStartEnd(Data[GROUP])
		else:
			new_t_start, new_t_end = timeStartEnd(Data[GROUP])
			if new_t_start == new_t_end == 0:
				continue
			t_start = min(t_start, new_t_start)
			t_end = max(t_end, new_t_end)

	return t_start, t_end
	"""


def Trace_getValue_atTime(Data, GROUP, TRACE, t, TIME_TRACE=TRACE_TIME, interpolate=True):
	if isinstance(TRACE, list):
		return tuple([Trace_getValue_atTime(Data, GROUP, T, t, TIME_TRACE, interpolate) for T in TRACE])

	return time2value(Data[GROUP], t, TRACE, TIME_TRACE, interpolate)

def Trace_getValues_TimeSegement(Data, GROUP, TRACE, t_start, t_end, TIME_TRACE=TRACE_TIME) -> list:
	""" get values as list between t_start and t_end """

	if isinstance(TRACE, list):
		return [Trace_getValues_TimeSegement(Data, GROUP, T, t_start, t_end, TIME_TRACE) for T in TRACE]

	i_start = time2index(Data[GROUP], t_start, TIME_TRACE)
	i_end = time2index(Data[GROUP], t_end, TIME_TRACE)

	return Data[GROUP][TRACE][i_start:i_end]


def Group_Time_2_Index(Data, Group, Time):
	""" returns index closest to given time """
	return time2index(Data[Group], Time)

def Group_Length(Data : dict, GROUP= None) -> int:
	"""
	Get length/sample count of Group
	:param Data: Data or Group
	:param GROUP:
	:return: length of group
	"""
	if GROUP:
		group = Data[GROUP]
	else:
		group = Data
	TRACE = TRACE_TIME # default use time trace
	if TRACE_TIME not in Data: # use first trace if time trace not found
		TRACE = list(group.keys())[0]
	return len(group[TRACE])

def Group_Duration(Data, GROUP):
	""" returns total duration in Seconds of Group """
	return Data[GROUP][TRACE_TIME][-1] - Data[GROUP][TRACE_TIME][0]

def Data_getAllGroupNames(Data):
	return list(Data.keys())

def Group_getAllTraceNames(Data, GROUP=None, TIME_TRACE=TRACE_TIME):
	""" returns every Trace Name in GROUP without TRACE_TIME"""
	group = Data
	if GROUP:
		group = Data[GROUP]
	return [t for t in list(group.keys()) if t != TIME_TRACE]

def Group_Add_Dataset(Data, GROUP, Dataset):
	for T in Data[GROUP]:
		if T not in Dataset:
			print("Group_Add_Dataset: Trace {} is missing in Dataset".format(T))
			return
	for T in Data[GROUP]:
		Data[GROUP][T].append(Dataset[T])

def Group_Remove_Dataset(Data, GROUP, index):
	"""
	Removes one or a list of samples/datasets
	:param index: can be one index (int) or a list of indexes
	"""
	if(Group_Length(Data, GROUP) == 0):
		print("Warning: Group {} has length 0 (Group_Remove_Dataset)".format(GROUP))
		return

	if(isinstance(index, list)):
		for i in sorted(index, reverse=True):
			Group_Remove_Dataset(Data, GROUP, i)
	else:
		for Trace in Data[GROUP]:
			if(isNPArray(Data[GROUP][Trace])):
				Data[GROUP][Trace] = np.delete(Data[GROUP][Trace], index)
			else:
				Data[GROUP][Trace].pop(index)




#################################################
#          Create Group, Trace                  #
#################################################

def Group_Create_fromGroup(Data, GROUP, GROUP_FROM, dt=None, copy_TRACES=None):
	if copy_TRACES == None:
		copy_TRACES = []

	if dt != None:
		t_start, t_end = Group_getTimeStartEnd(Data, GROUP_FROM)
		Group_Create_Tstartend(Data, GROUP, dt, t_start=t_start, t_end=t_end)
		for TRACE in copy_TRACES:
			Trace_Resample(Data, GROUP_FROM, TRACE, GROUP, TRACE)
	else:
		Group_Copy(Data, GROUP_FROM, GROUP, only_TRACES=copy_TRACES)


def Group_Create_dt(Data, GROUP, dt):
	t_start, t_end = Data_getTimeStartEnd(Data)

	Group_Create_Tstartend(Data, GROUP, dt, t_start=t_start, t_end=t_end)

def Group_Create_Tstartend(Data, GROUP, dt, t_end, t_start=0):
	if t_start < 0:
		print("WARNING - Group_Create_Tstartend: t_start < 0 (t_start={})".format(t_start))
		t_start = max(0, t_start)

	assert (t_end > t_start)
	#print("ERROR - Group_Create_Tstartend: t_start > t_end (maybe switched?)")

	Data[GROUP] = {TRACE_TIME: GenerateTimeTrace(dt, t_end, t_start)}

def CreateEmptyGroup(TRACES):
	"""
	Creates a empty group with the given Traces
	:param TRACES:
	:return: Group with given traces, all traces have length 0
	"""
	return {T:[] for T in TRACES}


def Group_Create_FromFeatureVectorList(Data, GROUP, FeatureVectorList, keys):
	"""
	Creates a Group from a given Feature Vector List / Dataset
	:param FeatureVectorList: list of dict like [{f1 : v1, f2 : v2, ...}, {f1 : v1, f2 : v2, ...}, ...]
	:param keys: list of features to convert to traces like [f1, f2, ...]
	"""

	Data[GROUP] = {key : [v[key] if key in v else nan for v in FeatureVectorList] for key in keys}


def Trace_Create_Func(Data, GROUP, TRACE_NEW, func=lambda d : 0):
	"""
	Create a Trace from a Function
	Input is the Datapoint at current time like { TRACE_TIME: 32, TRACE_ACCEL_X : 0.1, ...}
	:param Data:
	:param GROUP:
	:param TRACE_NEW:
	:param func: func(datasample) -> value
	"""
	trace_new = []
	for i in range(Group_Length(Data, GROUP)):
		d = {}
		for T in Data[GROUP]:
			d[T] = Data[GROUP][T][i]
		trace_new.append(func(d))

	Data[GROUP][TRACE_NEW] = trace_new

def Trace_Create_Func_byTime(Data, GROUP, TRACE_NEW, func=lambda t : 0, TIME_TRACE=TRACE_TIME):
	"""
	Create a Trace from a Function
	Input is the current time
	:param Data:
	:param GROUP:
	:param TRACE_NEW:
	:param func: func(datasample) -> value
	"""
	#trace_new = []
	#for i in range(Group_Length(Data, GROUP)):
	#    trace_new.append(func(Data[GROUP][TIME_TRACE][i]))
	#Data[GROUP][TRACE_NEW] = trace_new

	Data[GROUP][TRACE_NEW] = [func(Data[GROUP][TIME_TRACE][i]) for i in range(Group_Length(Data, GROUP))]



def Trace_Create_Const(Data, GROUP, TRACE_NEW, value=0):
	if isinstance(TRACE_NEW, list):
		for T in TRACE_NEW:
			Trace_Create_Const(Data, GROUP, T, value)
		return


	trace_new = []
	for i in range(Group_Length(Data, GROUP)):
		d = {}
		for T in Data[GROUP]:
			d[T] = Data[GROUP][T][i]
		trace_new.append(value)

	Data[GROUP][TRACE_NEW] = trace_new



def Trace_Create_byFunc(Data, GROUP, TRACE, func=lambda t: 0, INPUT_TRACE=TRACE_TIME):
	""" Creates a Trace in the Given Group using the function given """
	Trace_ApplyFunc(Data, GROUP, INPUT_TRACE, func, TRACE_RES=TRACE)



def CreateGroup_FromSignals(Data, GROUP, SIGNALS : list, dt=None, LOOKUP_SIGNAL_TO_TRACE: dict = None, delete_signal=False):
	"""
	Creates a Group from Multiple "Signal"-Groups
	Signal Groups are groups with only TRACE_TIME and (TRACE_VALUE or Group name as Trace name)
	:param Data:
	:param GROUP:
	:param SIGNALS: list of Signals
	:param dt: [s] force sample rate. if not given it is automaticly determined by signal groups
	:param LOOKUP_SIGNAL_TO_TRACE: lookup {Signal -> Trace Name}
	:param delete_signal: if true all source signal groups are deleted
	"""

	if LOOKUP_SIGNAL_TO_TRACE == None:
		LOOKUP_SIGNAL_TO_TRACE = {}

	t_start, t_end, dts = None, None, []
	for SIGNAL in SIGNALS:
		t_s, t_e = Group_getTimeStartEnd(Data, SIGNAL)
		dt = (t_e - t_s) / Group_Length(Data, SIGNAL)

		if t_start == None or t_s < t_start:
			t_start = t_s
		if t_end == None or t_e > t_end:
			t_end = t_e

		dts.append(dt)

	if dt == None:
		dt = median(dts)

	Group_Create_Tstartend(Data, GROUP, dt, t_end, t_start)
	for i, SIGNAL in enumerate(SIGNALS):


		if SIGNAL in LOOKUP_SIGNAL_TO_TRACE:
			TRACE = LOOKUP_SIGNAL_TO_TRACE[SIGNAL]
		elif SIGNAL in Data[GROUP]:
			TRACE = SIGNAL
		elif TRACE_VALUE in Data[GROUP]:
			TRACE = TRACE_VALUE
		else:
			print(f"Warning: CreateGroup_FromSignals - Trace for Signal {SIGNAL}")
			continue

		Trace_Resample(Data, SIGNAL, SIGNAL, GROUP, TRACE_NEW=TRACE)

		if delete_signal:
			Group_Delete(Data, SIGNAL)



#################################################
#          Rename/Copy/Remove/sort              #
#################################################


def Group_Rename(Data, GROUP, GROUP_NEW):
	""" Renames Group. If GROUP_NEW does exist it will be overwritten """
	Data[GROUP_NEW] = Data[GROUP]
	Group_Delete(Data, GROUP)


def Trace_Rename(Data, GROUP, TRACE, TRACE_NEW):
	""" Renames Group. If GROUP_NEW does exist it will be overwritten """
	if isinstance(TRACE, list):
		for T_IN, T_OUT in zip(TRACE, TRACE_NEW):
			Trace_Rename(Data, GROUP, T_IN, T_OUT)
	else:
		Data[GROUP][TRACE_NEW] = Data[GROUP].pop(TRACE)
		#Data[GROUP][TRACE_NEW] = Data[GROUP][TRACE]
		#Trace_Delete(Data, GROUP, TRACE)


def Group_Switch_Traces(Data, GROUP, TRACEA, TRACEB):
	Trace_Rename(Data, GROUP, TRACEA, TRACE_TMP)    # A   -> TMP
	Trace_Rename(Data, GROUP, TRACEB, TRACEA)       # B   -> A
	Trace_Rename(Data, GROUP, TRACE_TMP, TRACEB)    # TMP -> B

#deletes Trace and returns it
def Group_Delete(Data, GROUP):
	if isinstance(GROUP, list):
		for G in GROUP:
			Group_Delete(Data, G)
		return

	if(GROUP in Data):
		return Data.pop(GROUP)
	else:
		print("Group not found: {}".format(GROUP))

def Group_Exists(Data, GROUP):
	if(isinstance(GROUP, list)):
		return all([Group_Exists(Data, G) for G in GROUP])
	return (GROUP in Data)

def Trace_Exists(Data, GROUP, TRACE):
	if not Group_Exists(Data, GROUP):
		return False

	if(isinstance(TRACE, list)):
		return all([Trace_Exists(Data, GROUP, T) for T in TRACE])

	return TRACE in Data[GROUP]


def Trace_Copy(Data, GROUP, TRACE, TRACE_NEW, GROUP_NEW=None, override=True):
	if not GROUP_NEW:
		GROUP_NEW = GROUP

	if isinstance(TRACE, list):
		for T_FROM, T_TO in zip(TRACE, TRACE_NEW):
			Trace_Copy(Data, GROUP, T_FROM, T_TO)
		return

	if GROUP_NEW not in Data:
		print("Trace_Copy: Dst GroupName not found: {}".format(GROUP_NEW))
		return

	if GROUP_NEW == GROUP and TRACE_NEW == TRACE:
		print("Trace_Copy: Copy to same Group->Trace - '{}->{}'".format(GROUP, TRACE))
		return

	if TRACE_NEW in Data[GROUP_NEW]:

		if override:
			Trace_Delete(Data, GROUP_NEW, TRACE_NEW)
		else:
			print("Warning: Trace_Copy - Dst-Trace already exists found: {}->{}".format(GROUP_NEW, TRACE_NEW))
			return

	if not Trace_Exists(Data, GROUP, TRACE):
		print("Warning: Trace_Copy - Trace {}/{} does not exist".format(GROUP, TRACE))
		return

	Data[GROUP_NEW][TRACE_NEW] = Data[GROUP][TRACE].copy()



def Trace_Delete(Data, GROUP, TRACE):
	""" deletes Trace and returns it """
	if GROUP in Data:
		if isinstance(TRACE, list):
			for T in TRACE:
				Trace_Delete(Data, GROUP, T)
			return

		if TRACE in Data[GROUP]:
			return Data[GROUP].pop(TRACE)
		else:
			print("Trace_Delete: TraceName not found: {}->{}".format(GROUP, TRACE))
	else:
		pass
		#print("Trace_Delete: Group not found: {}".format(GROUP))




def Group_Copy(Data, GROUP, GROUP_NEW, only_TRACES=[]):
	"""
	Copys a Group
	:param onlyTrace: list of Traces that should be copied. if not given all is copied
	"""
	Group = {}
	for trace in Data[GROUP]:
		if only_TRACES and trace not in only_TRACES:
			continue
		Group[trace] = np.array(Data[GROUP][trace])
	Data[GROUP_NEW] = Group


def Group_sortTraces(Data, GROUP):
	group = {}
	TRACES = list(Data[GROUP].keys())
	nTRACES = []

	def addTrace(TRACE):
		if TRACE in TRACES and TRACE not in nTRACES:
			nTRACES.append(TRACE)
			return True
		return False

	if addTrace(TRACE_TIME):
		addTrace(TRACE_DELTA_TIME)
	addTrace(TRACE_PROGRESS)

	for T in sorted(TRACES):
		addTrace(T)

	for T in nTRACES:
		group[T] = Data[GROUP][T]

	Data[GROUP] = group


def Datas_Copy_Group(DataFrom, GROUP_FROM, DataTo, GROUP_TO=None):
	"""
	Copies a group from one Data to another
	:param DataFrom:
	:param GROUP_FROM:
	:param DataTo:
	:return:
	"""
	if not GROUP_TO:
		GROUP_TO = GROUP_FROM

	if isinstance(GROUP_FROM, list):
		for G_FROM, G_TO in zip(GROUP_FROM, GROUP_TO):
			Datas_Copy_Group(DataFrom, G_FROM, DataTo, G_TO)
		return


	DataTo[GROUP_TO] = deepcopy(DataFrom[GROUP_FROM])


#################################################
#          Time / Resample                      #
#################################################


def Trace_Resample(Data, GROUP, TRACE, GROUP_TARGET, TRACE_NEW="", TIME_TRACE=TRACE_TIME, order=1):
	"""
	takes the trace and resamples it to the Time Trace of the TargetGroup
	:param Data:
	:param GROUP: Source Group
	:param TRACE: Group to resample
	:param GROUP_TARGET: Group to resample trace to
	:param TRACE_NEW: New Trace name
	:param TIME_TRACE:
	:param order: order of resampling (not yet used)
	"""

	if isinstance(TRACE, list):
		if isinstance(TRACE_NEW, list):
			assert len(TRACE) == len(TRACE_NEW)
			for i in range(len(TRACE)):
				Trace_Resample(Data, GROUP, TRACE[i], GROUP_TARGET, TRACE_NEW[i], TIME_TRACE=TIME_TRACE, order=order)
		else:
			for T in TRACE:
				Trace_Resample(Data, GROUP, T, GROUP_TARGET, TRACE_NEW, TIME_TRACE=TIME_TRACE, order=order)
	else:
		if not TRACE_NEW:
			TRACE_NEW = TRACE

		if not Group_Exists(Data, GROUP) or not Trace_Exists(Data, GROUP, TRACE):
			print("Trace_Resample: Group or Trace does not exist {}->{}".format(GROUP, TRACE))
			return

		t_new = Data[GROUP_TARGET][TIME_TRACE]

		from HelpMath import interpolate
		Data[GROUP_TARGET][TRACE_NEW] = interpolate(Data[GROUP][TIME_TRACE], Data[GROUP][TRACE], t_new, order=order)
		#Data[GROUP_TARGET][TRACE_NEW] = np.interp(t_new, Data[GROUP][TIME_TRACE], Data[GROUP][TRACE])


def Group_Resample(Data, GROUP, dt=0, samplecount=0, GROUP_RES=None, only_TRACE=[], TIME_TRACE=TRACE_TIME):
	"""
	Resamples a Group to a new SampleRate
	:param dt: Time Delta between Samples in seconds
	:param samplecount: instrad of dt, sample count can be given
	:param only_TRACE: if given only these Traces are carryed over
	"""
	if not GROUP_RES:
		GROUP_RES = GROUP

	if not only_TRACE:
		only_TRACE = Group_getAllTraceNames(Data, GROUP, TIME_TRACE=TIME_TRACE)


	Group = Data[GROUP]
	t_start, t_end= group_getTimeStartEnd(Group, TIME_TRACE=TIME_TRACE)

	if samplecount:
		dt = (t_end - t_start) / samplecount

	if not dt:
		print("Group_Resample: Error - dt or samplecount must be given")
		return

	Data["_"] = {TIME_TRACE : GenerateTimeTrace(dt, t_end, t_start)}

	Trace_Resample(Data, GROUP, only_TRACE, "_", TIME_TRACE=TIME_TRACE)
	Group_Rename(Data, "_", GROUP_RES)


def Group_TimeShift(Data, GROUP, dt, clock_speed_correction=1, GROUP_RES=None):
	"""
	Shifts Group in Time by given delta t
	:param dt: Time Shift in [s]
	"""
	if GROUP_RES != None:
		Group_Copy(Data, GROUP, GROUP_RES)
	else:
		GROUP_RES = GROUP

	Trace_Scale(Data, GROUP_RES, TRACE_TIME, Offset=dt, ScaleFactor=clock_speed_correction)
	#Trace_Scale(Data, GROUP, TRACE_TIME, Offset=dt)
	#Trace_Scale(Data, GROUP, TRACE_TIME, ScaleFaktor=clock_speed_correction)

def Data_TimeShift(Data, dt, clock_speed_correction=1):
	"""
	Shifts all Groups by given delta t
	:param dt: Time Shift in [s]
	"""
	for GROUP in Data:
		Group_TimeShift(Data, GROUP, dt, clock_speed_correction)


def Data_RemoveOffset_TimeTrace(Data):
	"""
	Shifts time so that Data starts at time == 0
	"""
	t_start = None
	for GROUP in Data:
		if t_start == None:
			t_start = Data[GROUP][TRACE_TIME][0]
		else:
			t_start = min(Data[GROUP][TRACE_TIME][0], t_start)
		print("{}: {}".format(GROUP, Data[GROUP][TRACE_TIME][0]))

	print("RemoveOffset TimeTrace: t_start={}s".format(t_start))
	#for GROUP in Data:
	#    Trace_Scale(Data,GROUP,TRACE_TIME, Offset=-t_start)
	Data_TimeShift(Data, -t_start)



#################################################
#          Data Group and Trace func            #
#################################################


def Data_Crop_FromTo(Data, TimeSegment, Zero_Time=False):
	"""
	Crops out Data at given Time Segments
	:param Data: Data of complete recording
	:param TimeSegment: (t_start, t_end) or  list of (t_start, t_end)
	:param Zero_Time: remove offset in time trace so that Segement starts at time 0
	:return: DataSegment or list of DataSegments
	"""

	# if no laps found
	if not TimeSegment:
		return

	if isinstance(TimeSegment, list):
		return [Data_Crop_FromTo(Data, tSeg, Zero_Time) for tSeg in TimeSegment]

	t_start, t_end = TimeSegment
	assert t_end > t_start

	DataSegment = Data_Split(Data, t_start, t_end, TimeZero=Zero_Time)

	#for GROUP in Data:
	#    Trace_CreateProgressTrace(DataSegment, GROUP)

	return DataSegment


def Data_Split(Data, t_start, t_end=-1, TimeZero=False, RemoveEmptyGroups=False):
	"""
	Splits Data at timestamp and returns
	- (Data1, Data2)  if only t_start is given
	- DataSegment    if t_start and t_end was given
	:param t_start:
	:param t_end:
	:param TimeZero: make Time of Data2 start at 0 (relative to t_start)
	:param RemoveEmptyGroups: remove groups that are empty after split (because split was before or after end of data in group)
	:return: (Data1, Data2) or DataSegment
	"""

	if t_end > t_start:
		Data, DRest = Data_Split(Data, t_end)

	D1 = {}
	D2 = {}
	for GROUP in Data:
		#D1[GROUP], D2[GROUP] = Group_Split(Data, GROUP, t_start)
		G1, G2 = Group_Split(Data, GROUP, t_start)
		if Group_Length(G1) or not RemoveEmptyGroups:
			D1[GROUP] = G1
		if Group_Length(G2) or not RemoveEmptyGroups:
			D2[GROUP] = G2

		if TimeZero:
			Trace_Scale(D2, GROUP, TRACE_TIME, Offset=-t_start)

	if t_end > t_start:
		return D2
	else:
		return D1, D2


def Data_Join(Data1, Data2, deep_copy=False):
	"""
	Joints two Data to one
	if Group exists in both Data -> "GROUP_1" and "GROUP_2" is used
	:param Data1:
	:param Data2:
	:param deep_copy: deep copy's Groups
	:return: Data joint
	"""
	Data = {}


	for GROUP in Data1:
		GROUP_NEW = GROUP if GROUP not in Data2 else GROUP + "_1"
		#GROUP_NEW = GROUP
		if deep_copy:
			Data[GROUP_NEW] = deepcopy(Data1[GROUP])
		else:
			Data[GROUP_NEW] = Data1[GROUP]

	for GROUP in Data2:
		GROUP_NEW = GROUP if GROUP not in Data1 else GROUP + "_2"
		if deep_copy:
			Data[GROUP_NEW] = deepcopy(Data2[GROUP])
		else:
			Data[GROUP_NEW] = Data2[GROUP]

	return Data


def Group_SplitStartEnd(Data, GROUP, t_start = 0, t_end = -1, TIME_TRACE=TRACE_TIME):
	i_start = time2index(Data[GROUP], t_start, TIME_TRACE)
	i_end = time2index(Data[GROUP], t_end, TIME_TRACE)
	group = {}
	for T in Data[GROUP]:
		group[T] = Data[GROUP][T][i_start:i_end + 1]

	return group

def Group_Crop(Data, GROUP, t_start = 0, t_end = -1, GROUP_RES=None):
	if not GROUP_RES:
		GROUP_RES = GROUP
	Data[GROUP_RES] = Group_SplitStartEnd(Data, GROUP, t_start, t_end)

def Group_Split(Data, GROUP, t_split):
	"""
	Splits a Group at timestamp t and returns G1,G2 as tuple
	G2 does not contain timestamps before t_split
	"""

	if Group_Length(Data, GROUP) == 0:
		return Data[GROUP], Data[GROUP]

	i_split = Group_Time_2_Index(Data, GROUP, t_split)
	t_selected = index2time(Data[GROUP], i_split)


	#make sure split second part does not include sample before t_split
	if t_selected < t_split:
		i_split += 1
	G1 = {}
	G2 = {}
	for TRACE in Data[GROUP]:
		G1[TRACE], G2[TRACE] = Trace_Split(Data, GROUP, TRACE, i_split)
	return G1, G2

def Trace_Split(Data, GROUP, TRACE, i_split):
	"""
	Splits a Trace at index i and returns t1,t2 as tuple
	t1 excludes i_split, t2 includes i_split
	trace = [0, 1, 2, 3, 4]
	i_split = 2
	t1 = [0, 1], t2 = [2, 3, 4]
	"""
	trace = np.array(Data[GROUP][TRACE])

	try:
		if i_split == 0:
			return np.array([]), np.array(trace, copy=True)
		if(trace.size > i_split):
			return np.array(trace[:i_split], copy=True), np.array(trace[i_split:], copy=True)
		else:
			return np.array(trace, copy=True), np.array([])
	except:
		print("Trace_Split: Error")



#################################################
#          Trace Apply Func                     #
#################################################

def Trace_ApplyFunc(Data, GROUP, TRACE=None, func=lambda x: x, TRACE_RES=None):
	"""
	Applies Func to every element of Trace
	:param func: must be a func with one parameter (value)
	"""
	if not TRACE:
		TRACE = Group_getAllTraceNames(Data, GROUP)

	if isinstance(TRACE, list):
		if TRACE_RES != None:
			TRACE_IN_OUT = zip(TRACE, TRACE_RES)
		else:
			TRACE_IN_OUT = zip(TRACE, TRACE)

		for T_IN, T_OUT in TRACE_IN_OUT:
			Trace_ApplyFunc(Data, GROUP, T_IN, func, TRACE_RES=T_OUT)
	else:
		if not TRACE_RES:
			TRACE_RES = TRACE
		trace = Data[GROUP][TRACE]
		Data[GROUP][TRACE_RES] = [func(trace[i]) for i in range(Group_Length(Data, GROUP))]


def Trace_ApplyFunc_ValueIndex(Data, GROUP, TRACE=None, func=lambda i, x: x, TRACE_RES=None):
	"""
	Applies Func to every element of Trace
	:param func: must be a func with two parameter (index, value)
	"""
	if not TRACE:
		TRACE = Group_getAllTraceNames(Data, GROUP)

	if isinstance(TRACE, list):
		if TRACE_RES != None:
			TRACE_IN_OUT = zip(TRACE, TRACE_RES)
		else:
			TRACE_IN_OUT = zip(TRACE, TRACE)

		for T_IN, T_OUT in TRACE_IN_OUT:
			Trace_ApplyFunc(Data, GROUP, T_IN, func, TRACE_RES=T_OUT)
	else:
		if not TRACE_RES:
			TRACE_RES = TRACE
		trace = Data[GROUP][TRACE]
		Data[GROUP][TRACE_RES] = [func(i, trace[i]) for i in range(Group_Length(Data, GROUP))]


def Trace_ApplyFunc_ValueTime(Data, GROUP, TRACE=None, func=lambda t, x: x, TRACE_RES=None, TIME_TRACE=TRACE_TIME):
	"""
	Applies Func to every element of Trace
	:param func: must be a func with two parameter (time, value)
	"""
	if not TRACE:
		TRACE = Group_getAllTraceNames(Data, GROUP)

	if isinstance(TRACE, list):
		if TRACE_RES != None:
			TRACE_IN_OUT = zip(TRACE, TRACE_RES)
		else:
			TRACE_IN_OUT = zip(TRACE, TRACE)

		for T_IN, T_OUT in TRACE_IN_OUT:
			Trace_ApplyFunc_ValueTime(Data, GROUP, T_IN, func, TRACE_RES=T_OUT, TIME_TRACE=TRACE_TIME)
	else:
		if not TRACE_RES:
			TRACE_RES = TRACE
		trace = Data[GROUP][TRACE]
		time_trace = Data[GROUP][TIME_TRACE]
		Data[GROUP][TRACE_RES] = [func(time_trace[i], trace[i]) for i in range(Group_Length(Data, GROUP))]



def Trace_ApplyFuncPrev(Data, GROUP, TRACE, func, TRACE_NEW=None, update_while_running=False):
	"""
	Applies Func to every element of Trace, and also gives previous value
	:param func: func(x_prev, x) - x_prev is None for first x
	"""
	if not TRACE_NEW:
		TRACE_NEW = TRACE
	if not update_while_running:
		trace = Data[GROUP][TRACE]
		Data[GROUP][TRACE_NEW] = func(nan, trace[0]) + [func(trace[i - 1], trace[i]) for i in range(Group_Length(Data, GROUP)) if i != 0]
	else:
		Trace_Copy(Data, GROUP, TRACE, TRACE_NEW)
		for i in range(Group_Length(Data, GROUP)):
			x = Data[GROUP][TRACE_NEW][i]
			if i == 0:
				#x_prev = Data[GROUP][TRACE_NEW][i]
				x_prev = nan
			else:
				x_prev = Data[GROUP][TRACE_NEW][i - 1]

			Data[GROUP][TRACE_NEW][i] = func(x_prev, x)

def Trace_ApplyFunc2Trace(Data, GROUP, TRACE1, TRACE2, func, TRACE_RES=None):
	"""
	Applies Func to every element of Traces like out = func(trace1, trace2)

	:param func: like lambda x, y : x + y
	"""

	if TRACE_RES == None:
		TRACE_RES = TRACE1

	trace1 = Data[GROUP][TRACE1]
	trace2 = Data[GROUP][TRACE2]
	Data[GROUP][TRACE_RES] =  [func(trace1[i], trace2[i]) for i in range(Group_Length(Data, GROUP))]

def Trace_ApplyFunc3Trace(Data, GROUP, TRACE1, TRACE2, TRACE3, func, TRACE_RES=None):
	"""
	Applies Func to every element of Traces like out = func(trace1, trace2, trace3)
	:param func: like lambda x, y, z : x + y + z
	"""

	if TRACE_RES == None:
		TRACE_RES = TRACE1

	trace1 = Data[GROUP][TRACE1]
	trace2 = Data[GROUP][TRACE2]
	trace3 = Data[GROUP][TRACE3]
	Data[GROUP][TRACE_RES] = [func(trace1[i], trace2[i], trace3[i]) for i in range(Group_Length(Data, GROUP))]

def Trace_ApplyFunc4Trace(Data, GROUP, TRACE1, TRACE2, TRACE3, TRACE4, func, TRACE_RES=None):
	"""
	Applies Func to every element of Traces like out = func(trace1, trace2, trace3, trace4)
	:param func: like lambda x, y, z, w : x + y + z + w
	"""

	if TRACE_RES == None:
		TRACE_RES = TRACE1

	trace1 = Data[GROUP][TRACE1]
	trace2 = Data[GROUP][TRACE2]
	trace3 = Data[GROUP][TRACE3]
	trace4 = Data[GROUP][TRACE4]
	Data[GROUP][TRACE_RES] = [func(trace1[i], trace2[i], trace3[i], trace4[i]) for i in range(Group_Length(Data, GROUP))]


def Trace_ApplyFuncMultiTrace(Data, GROUP, TRACES_IN, TRACES_OUT, func, param_as_array=False):
	"""
	Runs function with Multiple input values and multiple output values
	Example
		TRACE_IN = [TRACE_A, TRACE_B, TRACE_C]
		TRACE_OUT = [TRACE_AB, TRACE_AC]
		def func(a, b, c):
			return (a + b, a + c)

	:param TRACES_IN: list of func input parameter
	:param TRACES_OUT: list of func output values
	:param func: input parameter must match length of TRACE_IN. output must match length of TRACE_OUT
	"""

	INS_Data_In = np.array([Data[GROUP][TRACE] for TRACE in TRACES_IN])
	ins_length = INS_Data_In.shape[1]
	INS_Data_Out = np.empty([len(TRACES_OUT), ins_length], dtype=float)
	for i in range(ins_length):

		data_in = INS_Data_In[:, i]

		if param_as_array:
			data_out = func(data_in)
		else:
			data_out = func(*data_in)

		INS_Data_Out[:, i] = np.append([], data_out)

	for i, TRACE in enumerate(TRACES_OUT):
		Data[GROUP][TRACE] = INS_Data_Out[i, :]


def Trace_ApplyFuncMultiTraceDataGen(Data, GROUP, TRACES_IN, TRACES_OUT, func, replace_group=False):
	"""
	Runs function with Multiple input values and multiple output values
	Example
		TRACE_IN = [TRACE_A, TRACE_B, TRACE_C]
		TRACE_OUT = [TRACE_AB, TRACE_AC]
		def func(a, b, c):
			return (a + b, a + c)

	:param TRACES_IN: list of func input parameter
	:param TRACES_OUT: list of func output values
	:param func: input parameter must match length of TRACE_IN. output must match length of TRACE_OUT
	:param replace_group: replaces group and only keep trace out
	"""

	INS_Data_In = np.array([Data[GROUP][TRACE] for TRACE in TRACES_IN])
	ins_length = INS_Data_In.shape[1]
	INS_Data_Out = np.empty([len(TRACES_OUT), ins_length], dtype=float)
	def data_gen():
		for i in range(ins_length):

			data_in = INS_Data_In[:, i]
			yield data_in

	for i, data_out in enumerate(func(data_gen())):
		INS_Data_Out[:, i] = np.append([], data_out)

	if replace_group:
		Data[GROUP] = {}
	for i, TRACE in enumerate(TRACES_OUT):
		Data[GROUP][TRACE] = INS_Data_Out[i, :]




#################################################
#          General Trace Func                   #
#################################################


def Trace_Scale(Data, GROUP, TRACE, ScaleFactor=1.0, Offset=0.0, TRACE_RES=""):
	if isinstance(TRACE, list):
		for i in range(len(TRACE)):
			Trace_Scale(Data, GROUP, TRACE[i], ScaleFactor, Offset,
						TRACE_RES=(None if (not TRACE_RES or not isinstance(TRACE_RES, list) or not len(TRACE_RES) == len(TRACE)) else TRACE_RES[i]))
		return
	if not TRACE_RES:
		TRACE_RES = TRACE
	#else:
	#    Trace_Copy(Data, GROUP, TRACE, TRACE_RES)
	#for i in range(len(Data[GROUP][TRACE])):
	#    Data[GROUP][TRACE_RES][i] = (Data[GROUP][TRACE_RES][i] * ScaleFactor) + Offset

	if not Trace_Exists(Data, GROUP, TRACE):
		print("Warning - Trace_Scale: {}/{} not found".format(GROUP, TRACE))
		return

	Data[GROUP][TRACE_RES] = list((np.array(Data[GROUP][TRACE]) * ScaleFactor) + Offset)



def Trace_Smooth_func(Data, GROUP, TRACE="", TRACE_RES="", i_range=3, t_range=None, Itterations=1, smooth_func=smooth_moving_avg):
	"""
	smoothes trace with moving avg filter.
	:param i_range: index width of moving avg filter
	:param t_range: time range in seconds: if this is set -> not index range is used but T_Range
	:param Itterations: times to apply filter
	:param smooth_func: function that takes an array and a index range and returns the filtered version of the array
	"""
	if not TRACE:
		TRACE = Group_getAllTraceNames(Data, GROUP)

	if not TRACE_RES:
		TRACE_RES = TRACE

	if t_range:
		dt = getAVG_TimeDelta(Data[GROUP])
		i_range = int(t_range / dt)
		if(i_range < 2):
			print("Trace_Smooth: Samplerate to small. t_range is less then 3 samples")
			Trace_Copy(Data, GROUP, TRACE, TRACE_RES, override=True) #copy with no modification
			return

	if isinstance(TRACE, list):
		if TRACE_RES != None:
			TRACE_IN_OUT = zip(TRACE, TRACE_RES)
		else:
			TRACE_IN_OUT = zip(TRACE, TRACE)

		for T_IN, T_OUT in TRACE_IN_OUT:
			Trace_Smooth_func(Data, GROUP, T_IN, T_OUT, i_range=i_range, Itterations=Itterations, smooth_func=smooth_func)
	else:
		if TRACE_RES != TRACE:
			Trace_Copy(Data, GROUP, TRACE, TRACE_RES, override=True)
		for i in range(Itterations):
			Data[GROUP][TRACE_RES] = smooth_func(Data[GROUP][TRACE_RES], i_range)

def Trace_Smooth_Median(Data, GROUP, TRACE="", TRACE_RES="", i_range=3, t_range=None, Itterations=1):
	Trace_Smooth_func(Data, GROUP, TRACE, TRACE_RES, i_range, t_range, Itterations, smooth_func=smooth_median)

def Trace_Smooth_Box(Data, GROUP, TRACE="", TRACE_RES="", func=mean, i_range=3, t_range=None, Itterations=1):
	Trace_Smooth_func(Data, GROUP, TRACE, TRACE_RES, i_range, t_range, Itterations, smooth_func=lambda arr, i_range: smooth_box(arr, i_range, func))

def Trace_Smooth(Data, GROUP, TRACE=None, TRACE_RES=None, i_range=3, t_range=None, Itterations=1):
	"""
	smoothes trace with moving avg filter.
	:param i_range: index width of moving avg filter
	:param t_range: time range in seconds: if this is set -> not index range is used but T_Range
	:param itterations: times to apply filter
	"""
	if not TRACE:
		TRACE = Group_getAllTraceNames(Data, GROUP)

	if not TRACE_RES:
		TRACE_RES = TRACE

	if t_range:
		dt = getAVG_TimeDelta(Data[GROUP])
		if not dt:
			return
		i_range = int(round(t_range / dt))
		print("Trace_Smooth({}, {}): i_range={}".format(GROUP, TRACE, i_range))
		if(i_range < 2):
			print("Trace_Smooth: Samplerate to small. t_range is less then 3 samples")
			if TRACE != TRACE_RES:
				Trace_Copy(Data, GROUP, TRACE, TRACE_RES, override=True)
			return

	if (isinstance(TRACE, list)):
		#for i, T in enumerate(TRACE):
		#    T_RES = TRACE_RES[i]
		for T, T_RES in zip(TRACE, TRACE_RES):
			Trace_Smooth(Data, GROUP, T, T_RES, i_range=i_range, Itterations=Itterations)
		return

	if TRACE_RES != TRACE:
		Trace_Copy(Data, GROUP, TRACE, TRACE_RES, override=True)

	for i in range(Itterations):
		Data[GROUP][TRACE_RES] = smooth_moving_avg(Data[GROUP][TRACE_RES], i_range)


def Filter_movingaverage(Data, GROUP, i_range=3, t_range=None, TRACE_NEW="", itterations=1):
	"""
	does a moving avg filter
	:param i_range: index range to define width of moving avg
	:param t_range: time range in seconds: if this is set -> not index range is used but T_Range
	:param itterations: how many times this filter is applyed
	:return:
	"""

	Group = Data[GROUP]
	if(len(TRACE_NEW) == 0):
		TRACE_NEW = list(Group.keys())
	else:
		TRACE_NEW = [TRACE_NEW]

	if t_range:
		dt = getAVG_TimeDelta(Group)
		i_range = t_range / dt
	for Trace in TRACE_NEW:
		if(Trace != "Time"):
			for i in range(itterations):
				Group[Trace] = smooth_moving_avg(Group[Trace], i_range)

def Trace_Limit(Data, GROUP, TRACE, LOWER_LIMIT=None, UPPER_LIMIT=None, TRACE_NEW=None):
	if(LOWER_LIMIT == None and UPPER_LIMIT == None):
		print("Trace_Limit: Error - No Limit given")
		return
	func = lambda x : min(max(LOWER_LIMIT, x), UPPER_LIMIT)
	if(LOWER_LIMIT != None and UPPER_LIMIT == None): #only Limit low
		func = lambda x : max(LOWER_LIMIT, x)
	if(LOWER_LIMIT == None and UPPER_LIMIT != None): #only Limit up
		func = lambda x : min(UPPER_LIMIT, x)

	Trace_ApplyFunc(Data, GROUP, TRACE, func, TRACE_NEW)

def Trace_Devide(Data, GROUP, TRACE1, TRACE2, TRACE_RES=None, devidezero_theshold=0, devidezero_value=0):
	"""
	Creates new trace that contains (TRACE1 / TRACE2) element wise
	:param devidezero_theshold: with this lower threshold can be defined for TRACE2 at with all resulting values are :param devidezero_value
	:param devidezero_value: if true devide zero is replaced with this value
	"""
	if not TRACE_RES:
		TRACE_RES = TRACE1

	Data[GROUP][TRACE_RES] = arr_divide(Data[GROUP][TRACE1], Data[GROUP][TRACE2])

	if(devidezero_theshold > 0):
		Trace_ApplyFunc2Trace(Data, GROUP, TRACE2, TRACE_RES, func=lambda t2, tr : devidezero_value if t2 < devidezero_theshold else tr, TRACE_RES=TRACE_RES)
		#for i in range(Group_Length(Data[GROUP])):
		#    if Data[GROUP][TRACE2][i] < devidezero_theshold:
		#        Data[GROUP][TRACE_RES][i] = devidezero_value

def Trace_AVG(Data, GROUP, TRACE1, TRACE2, TRACE_RES=None):
	""" Creates a Trace that is the avg between Trace1 and Trace 2 """
	if not TRACE_RES:
		TRACE_RES = TRACE1
	Data[GROUP][TRACE_RES] = np.divide(np.add(Data[GROUP][TRACE1], Data[GROUP][TRACE2]), 2)

def Trace_Add(Data, GROUP, TRACE1, TRACE2, TRACE_RES=None):
	"""
	Creates new trace that contains (TRACE1 + TRACE2) element wise
	:param TRACE2: can be a TRACE or a list of TRACE
	:param TRACE_RES: if not given Res is stored in TRACE1
	"""
	if not TRACE_RES:
		TRACE_RES = TRACE1

	if isinstance(TRACE2, list):
		res = Data[GROUP][TRACE1]
		for T in TRACE2:
			res = np.add(res, Data[GROUP][T])
	else:
		res = np.add(Data[GROUP][TRACE1], Data[GROUP][TRACE2])

	Data[GROUP][TRACE_RES] = res

def Trace_Sub(Data, GROUP, TRACE1, TRACE2, TRACE_RES=None):
	"""
	Creates new trace that contains (TRACE1 - TRACE2) element wise
	"""
	if not TRACE_RES:
		TRACE_RES = TRACE1
	Data[GROUP][TRACE_RES] = np.subtract(Data[GROUP][TRACE1], Data[GROUP][TRACE2])

def Trace_Mul(Data, GROUP, TRACE1, TRACE2, TRACE_RES=None):
	"""
	Creates new trace that contains (TRACE1 * TRACE2) element wise
	"""
	if not TRACE_RES:
		TRACE_RES = TRACE1
	Data[GROUP][TRACE_RES] = np.multiply(Data[GROUP][TRACE1], Data[GROUP][TRACE2])


def Trace_Diff(Data, GROUP, TRACE, TRACE_RES=None):
	""" Calculates diff between values of the trace (time independet)
	:returns fist value """
	if not TRACE_RES:
		TRACE_RES = TRACE

	Data[GROUP][TRACE_RES] = diff(Data[GROUP][TRACE])
	return Data[GROUP][TRACE][0]


def Trace_Sum(Data, GROUP, TRACE, TRACE_RES=None, StartValue=0):
	""" Calculates itterative sum between values of the trace (like integrate but time independet) """
	if not TRACE_RES:
		TRACE_RES = TRACE
	Data[GROUP][TRACE_RES] = sum_integrate(Data[GROUP][TRACE], start_value=StartValue)



def Trace_Integrate(Data, GROUP, TRACE, TRACE_INTEGRATE=None, TIME_TRACE=TRACE_TIME):
	if not TRACE_INTEGRATE:
		TRACE_INTEGRATE = TRACE
	Data[GROUP][TRACE_INTEGRATE] = integrate(Data[GROUP][TIME_TRACE], Data[GROUP][TRACE])



def Trace_Integrate_Fuse(Data, GROUP, TRACE, TRACE_INTEGRATE, TRACE_FUSE, alpha, TIME_TRACE=TRACE_TIME):
	"""
	Integrates Trace with Fuse Trace to compensate Drift
	:param GROUP: Group of Trace to integrate
	:param TRACE: Trace to Integrate
	:param TRACE_INTEGRATE: Trace to store integrated trace to
	:param TRACE_FUSE: Trace to compensate Drift
	:param alpha: fuse alpha. higher alphas increase influence of TRACE_FUSE
	:param TIME_TRACE: Trace Time to integrate over
	"""
	Data[GROUP][TRACE_INTEGRATE] = integrate_fuse(Data[GROUP][TIME_TRACE], Data[GROUP][TRACE], Data[GROUP][TRACE_FUSE], alpha)



def Trace_Derivative(Data, GROUP, TRACE, TRACE_RES=None, TIME_TRACE=TRACE_TIME):
	if isinstance(TRACE, list):
		if TRACE_RES != None:
			TRACE_IN_OUT = zip(TRACE, TRACE_RES)
		else:
			TRACE_IN_OUT = zip(TRACE, TRACE)

		for T_IN, T_OUT in TRACE_IN_OUT:
			Trace_Derivative(Data, GROUP, T_IN, T_OUT, TIME_TRACE=TRACE_TIME)
	else:
		if not TRACE_RES:
			TRACE_RES = TRACE
		Data[GROUP][TRACE_RES] = derivative(Data[GROUP][TIME_TRACE], Data[GROUP][TRACE])







#################################################
#          Specific Functions                   #
#################################################


def Trace_Fuse(Data, GROUP, TRACE1, TRACE2, alpha, TRACE_RES=None):
	""" Fuses two Traces by applying trace_res = trace2 * alpha + trace1 * (1 - alpha) """
	Trace_ApplyFunc_ValueIndex(Data, GROUP, TRACE1, lambda i, x : Data[GROUP][TRACE2][i] * alpha + x * (1 - alpha), TRACE_RES)

def Trace_Fuse_Diff(Data, GROUP, TRACE1, TRACE2, alpha, TRACE_RES=None, start_value = None):
	"""
	Fuses two Traces by Differentiating and Integrating TRACE1 and using TRACE2 as Guiding Trace while integrating.
	This can be used to reduce drift in Trace1 by guiding it with Trace2
	with higher alpha resulting Trace does follow Trace2 more closely but reduces effect off original Trace1
	:param TRACE2 Guiding Trace. Can be ether Trace or constant value
	"""

	#def Trace_Integrate_Fuse(Data, GROUP, TRACE, TRACE_INTEGRATE, TRACE_FUSE, alpha, TIME_TRACE=TRACE_TIME):
	if not TRACE_RES:
		TRACE_RES = TRACE1

	alpha = alpha / getAVG_TimeDelta(Data, GROUP)
	trace1_diff = derivative(Data[GROUP][TRACE_TIME], Data[GROUP][TRACE1])
	if not isinstance(TRACE2, str):
		trace2 = TRACE2
	else:
		trace2 = Data[GROUP][TRACE2]

	if start_value == None:
		start_value = Data[GROUP][TRACE2][0]

	Data[GROUP][TRACE_RES] = integrate_fuse(Data[GROUP][TRACE_TIME],
											trace1_diff, trace2, alpha,
											start_value=start_value
											)

	"""
	#Alt. Version
	#def Trace_Integrate_Fuse(Data, GROUP, TRACE, TRACE_INTEGRATE, TRACE_FUSE, alpha, TIME_TRACE=TRACE_TIME):
	if not TRACE_RES:
		TRACE_RES = TRACE1

	trace1_diff = diff(Data[GROUP][TRACE1])
	Data[GROUP][TRACE_RES] = sum_integrate_fuse(trace1_diff, Data[GROUP][TRACE2], alpha, start_value=Data[GROUP][TRACE1][0])
	"""






def Group_Filter_Index(Data, GROUP, indexs):
	for Trace in Data[GROUP]:
		if(isinstance(Data[GROUP][Trace], np.ndarray)):
			Data[GROUP][Trace] = list(Data[GROUP][Trace])
		Data[GROUP][Trace] = np.array([Data[GROUP][Trace][i] for i in range(len(Data[GROUP][Trace])) if i in indexs])

def Group_Filter_byTrace(Data, GROUP, TRACE, func_filter=lambda x: x, GROUP_RES=None):
	if GROUP_RES == None:
		GROUP_RES = GROUP

	group = {}
	for T in Data[GROUP]:
		group[T] = [v for i, v in enumerate(Data[GROUP][T]) if func_filter(Data[GROUP][TRACE][i])]

	Data[GROUP_RES] = group

def Group_Remove_OverSampling(Data, GROUP, UPDATE_TRACE, GROUP_RES=None):
	"""
	Removes Double Samples like [1], 1, 1, 1, [2], 2, 2, 2, [3], 3, 3, 3
	This is caused by forced sample rate higher then underlying data is updated slower
	this causes traces be delayed if smoothed or resampled.

	Resulting group only holds samples where the value in UPDATE_TRACE changes
	:param UPDATE_TRACE: Trace used for resampling.
	:param GROUP_RES: Resulting Group
	"""

	if not GROUP_RES:
		GROUP_RES = GROUP

	TRACES = list(Data[GROUP].keys())
	group_new = {T : [] for T in TRACES}

	val_prev = None
	for i in range(Group_Length(Data, GROUP)):
		val = Data[GROUP][UPDATE_TRACE][i]
		if i == 0:
			val_prev = val
			continue

		#Add Datasample if value has changed
		if val_prev != val:
			for TRACE in TRACES:
				group_new[TRACE].append(Data[GROUP][TRACE][i])

			val_prev = val

	Data[GROUP_RES] = group_new


def Trace_FlatOut_StartEnding(Data, GROUP, TRACE, TRACE_NEW="", t_begin=0, t_end=-1):
	"""
	This sets every value before t_begin and after t_end to the value at t_begin/t_end
	:param t_begin:
	:param t_end:
	"""

	if not TRACE_NEW:
		TRACE_NEW = TRACE
	if TRACE_NEW != TRACE:
		Trace_Copy(Data, GROUP, TRACE, TRACE_NEW)

	i_begin = time2index(Data[GROUP], t_begin)
	i_end = time2index(Data[GROUP], Data[GROUP][TRACE_TIME][-1] - t_end)
	i_last = Group_Length(Data, GROUP)
	for i in range(i_begin):
		Data[GROUP][TRACE_NEW][i] = Data[GROUP][TRACE][i_begin]
	for i in range(i_last - i_end):
		Data[GROUP][TRACE_NEW][i_last - i - 1] = Data[GROUP][TRACE][i_end]


def Trace_RemoveStartOffset(Data, GROUP, TRACE):
	""" Moves Trace that it starts with Value 0 """
	if GROUP not in Data:
		print("Warning - Trace_RemoveStartOffset: Group {} does not exist".format(GROUP))
		return

	if isinstance(TRACE, list):
		for T in TRACE:
			Trace_RemoveStartOffset(Data, GROUP, T)
		return


	if not Trace_Exists(Data, GROUP, TRACE):
		print("Warning - Trace_RemoveStartOffset: {}/{} not found".format(GROUP, TRACE))
		return

	Trace_Scale(Data, GROUP, TRACE, Offset=-Data[GROUP][TRACE][0])


def Trace_OffsetCorrection(Data, GROUP, TRACE, First_i_Values=1, offset_mapping=lambda x: x, TRACE_RES=None):
	""" removes offset from Trace. Offset is Calculated by param First_i_Values """

	if not TRACE_RES:
		TRACE_RES = TRACE

	if(not GROUP in Data or not TRACE in Data[GROUP]):
		print("Trace_OffsetCorrection: Group or Trace not found 'Data[{}][{}]'".format(GROUP, TRACE))
		return


	#if -1 -> avg over all values
	if(First_i_Values == -1):
		offset = mean(Data[GROUP][TRACE][:First_i_Values])
	else:
		First_i_Values = min(First_i_Values, Group_Length(Data, GROUP))
		offset = mean(Data[GROUP][TRACE][:First_i_Values])

	Trace_Scale(Data, GROUP, TRACE, Offset=-offset_mapping(offset), TRACE_RES=TRACE_RES)



def Trace_Drift_Remove(Data, GROUP, TRACE, TRACE_RES=None):
	"""
	Removes Linear Drift of Trace using end value
	"""
	if TRACE_RES == None:
		TRACE_RES = TRACE

	v_start, v_end = Data[GROUP][TRACE][0], Data[GROUP][TRACE][-1]

	Trace_FitStartEnd(Data, GROUP, TRACE, v_start, v_start, TRACE_RES)


def Trace_FitStartEnd(Data, GROUP, TRACE, v_start_ref, v_end_ref, TRACE_RES=None):
	"""
	Changes Trace to match given start value and end value
	"""
	if TRACE_RES == None:
		TRACE_RES = TRACE

	t_start, t_end = Group_getTimeStartEnd(Data, GROUP)

	v_start, v_end = Data[GROUP][TRACE][0], Data[GROUP][TRACE][-1]

	TMP_TRACE = TRACE + "_CORR"

	Data[GROUP_TMP] = {
		TRACE_TIME: [t_start, t_end],
		TMP_TRACE: [v_start - v_start_ref, v_end - v_end_ref]
	}

	Trace_Resample(Data, GROUP_TMP, TMP_TRACE, GROUP, TMP_TRACE)
	Trace_Sub(Data, GROUP, TRACE, TMP_TRACE, TRACE_RES)

	#Trace_Delete(Data, GROUP, TRACE_TMP)
	Group_Delete(Data, GROUP_TMP)


def getSampleKernel(a= 3/8):
	""" Creates a 5x5 Filterkernel
	:param a: a = 3/8 -> Binomialfilter | a = 2/5 -> Gaußfilter
	:return: [c, b, a, b, c]
	"""

	b = 1 / 4
	c = 1 / 4 - (a / 2)
	return [c, b, a, b, c]

def Group_DownSample_x2(Data, GROUP, Kernel=[1, 2, 1], GROUP_RES=None):
	"""
	This Function downsamples the Given Group SampleRate by half. That means every other sample will be removed
	:param Kernel: Kernel for Downsampling operator. Must be list of unenven length like 1, 3, 5 ..
	:return:
	"""
	if len(Kernel) % 2 == 0:
		print("Group_DownSample_x2: Error - Kernel Length must be uneven")
		return

	if not GROUP_RES:
		GROUP_RES = GROUP

	group_res = {}
	for T in Data[GROUP]:
		group_res[T] = []

	glen = Group_Length(Data, GROUP)
	k_center = int(len(Kernel) / 2)
	k_sum = sum(Kernel)
	def sample(i, arr):
		return sum([Kernel[r] * arr[between(0, i - k_center + r, glen - 1)] for r in range(len(Kernel))]) / k_sum


	for i in range(glen):
		if i % 2 == 0: #only even index
			for T in Data[GROUP]:
				group_res[T].append(Data[GROUP][T][i] if T == TRACE_TIME else sample(i, Data[GROUP][T]))

	Data[GROUP_RES] = group_res


def Group_Remove_ZeroTdelta_Samples(Data, GROUP):
	"""
	Removes every sample that has the same Time value t as its previous sample
	"""
	indexes_remove = [i for i in range(Group_Length(Data, GROUP)) if i != 0 and index2time(Data[GROUP], i) == index2time(Data[GROUP], i - 1)]
	Group_Remove_Dataset(Data, GROUP, indexes_remove)

def Group_SplitMerge_ByTraceValue(Data, GROUP, SPLIT_TRACE, GROUP_NEW=None, Val2Name_func=lambda x : str(int(x))):

	#Split Group by Value
	_Data = Group_Split_ByTraceValue(Data[GROUP], SPLIT_TRACE, Val2Name_func=Val2Name_func)
	GroupValue_Names = Data_getAllGroupNames(_Data)

	# Get Time Trace from first SPLIT GROUP as Stuetzchannel
	Time_Trace = _Data[GroupValue_Names[0]][TRACE_TIME]
	# Create New Group from Time_TRACE
	_Data[GROUP_TMP] = {TRACE_TIME: Time_Trace}

	# Resample All SPLIT_GROUPS into new Group with Trace names to "TRACE_VAL" like "TempObj_1"
	for G in GroupValue_Names:  # G like 0, 1, 2, 3
		for T in Group_getAllTraceNames(_Data, G):  # T like TempObj
			Trace_Resample(_Data, G, T, GROUP_TMP, "{}_{}".format(T, G))

	# Remove Old Group in Data and Copy New Group over
	if not GROUP_NEW:
		GROUP_NEW = GROUP
		Group_Delete(Data, GROUP)

	Data[GROUP_NEW] = _Data[GROUP_TMP]

def Group_Split_ByTraceValue(Group, SPLIT_TRACE, Val2Name_func=lambda x : str(x)):
	"""
	Splits up given Group by the values in SPLIT_TRACE
	Example: SPLIT_TRACE = SensorID
	:param Val2Name_func: split_value -> name of group
	:returns dict of {Split_Value:Split_Group}
	"""
	Groups = {}
	_Group = {}
	for TRACE in Group:
		if TRACE != SPLIT_TRACE:
			_Group[TRACE] = Group[TRACE]
	for i in range(Group_Length(_Group)):
		v = Group[SPLIT_TRACE][i]
		if v not in Groups:
			Groups[v] = CreateEmptyGroup(_Group.keys())
		for TRACE in _Group:
			Groups[v][TRACE].append(_Group[TRACE][i])

	return {Val2Name_func(v) : Groups[v] for v in Groups}


def Trace_FindFirst(Data, GROUP, TRACE, func=lambda x : True):
	"""
	Finds first Datapoint fullfilling given function.
	Goes over every datapoint until function returns True
	:param Data:
	:param GROUP:
	:param TRACE:
	:param func:
	:return: index of first datapoint where func returns true
	"""

	for i in range(Group_Length(Data, GROUP)):
		if func(Data[GROUP][TRACE][i]):
			return i

	return None


def Trace_FindExtrema(Data, GROUP, TRACE, comparator=np.less):
	"""
	Finds extrema like Maxima and Minima
	:param Data:
	:param GROUP:
	:param TRACE:
	:param comparator: np.less for low points. np.greater for high points
	:return: list of index's of extrema points like [2, 10, 640, ...]
	"""

	from scipy.signal import argrelextrema

	indexes = list(argrelextrema(np.array(Data[GROUP][TRACE]), comparator)[0])

	return indexes


def Trace_Find_CmpFunc(Group, TRACE, t_start=0, t_end=-1, cmp_func=lambda x, y: x > y):
	"""
	Searches for value that returns true for every comparison of cmp_func -> can be used for finding max value, min value usw
	:param cmp_func: function that takes 2 arguments and returns bool value
	:return: (t_value, value)
	"""

	i_start = time2index(Group, t_start)
	i_end = time2index(Group, t_end)

	v_max = Group[TRACE][i_start]
	i_max = i_start
	for i in range(i_end - i_start - 1):
		new_i = i_start + 1 + i
		new_v = Group[TRACE][i_start + 1 + i]
		if(cmp_func(new_v, v_max)):
			v_max = new_v
			i_max = new_i

	return (index2time(Group, i_max), v_max)

def Trace_FindMinmum(Group, TRACE, t_start=0, t_end=-1):
	""" returns index and value of minimum in given trace"""
	i_start = time2index(Group, t_start)
	i_end = time2index(Group, t_end)

	vmin = min(Group[TRACE][i_start:i_end])
	imin = list(Group[TRACE][i_start:i_end]).index(vmin)

	return (imin + i_start, vmin)


def Trace_FindNextMaximum(Group, TRACE, t_start, mindelta=0, dir=1):
	""" returns index and value of maximum after t_start"""
	trace = Group[TRACE]
	i_start = time2index(Group, t_start)
	i = i_start + dir
	max_value = trace[i_start]
	max_i = i_start
	while i < len(trace) and i >= 0:
		new_value = trace[i]
		#found new max value
		if(max_value < new_value):
			max_value = new_value
			max_i = i
		#return value because min delta was not overcome
		elif(max_value >= new_value + mindelta):
			"""
			import matplotlib.pyplot as plt
			plot_setup("")
			plt.plot(
				Group[TRACE_TIME],
				Group[Trace],
				'k'
			)
			plt.plot(t_start, trace[i_start], COLOR_GREEN, marker="*")
			plt.plot(index2time(Group, max_i), trace[max_i], COLOR_RED, marker="*")
			plot_show()
			"""
			return max_i, max_value

		i += dir
	return i_start, max_value


def Trace_FindNextMinimum(Group, TRACE, t_start, mindelta=0, dir=1):
	""" returns index and value of maximum after t_start"""
	trace = Group[TRACE]
	i_start = time2index(Group, t_start)
	i = i_start + dir
	min_value = trace[i_start]
	min_i = i_start
	while i < len(trace) and i >= 0:
		new_value = trace[i]
		#found new max value
		if(min_value > new_value):
			min_value = new_value
			min_i = i
		#return value because min delta was not overcome
		elif(min_value <= new_value + mindelta):
			"""
			import matplotlib.pyplot as plt
			plot_setup("")
			plt.plot(
				Group[TRACE_TIME],
				Group[Trace],
				'k'
			)
			plt.plot(t_start, trace[i_start], COLOR_GREEN, marker="*")
			plt.plot(index2time(Group, max_i), trace[max_i], COLOR_RED, marker="*")
			plot_show()
			"""
			return min_i, min_value

		i += dir
	return i_start, min_value


def Group_Remove_Equal_Value(Data, GROUP, TRACE, GROUP_RES=None):
	"""
	Creates a new Group that contains only samples where the given TRACE does change
	:returns: New Group
	"""
	if GROUP_RES == None:
		GROUP_RES = GROUP


	# Create empty group
	group_new = {T:[] for T in Data[GROUP]}

	def copy_datum(i):
		for TRACE in group_new:
			group_new[TRACE].append(Data[GROUP][TRACE][i])

	v_prev = None
	for i in range(Group_Length(Data, GROUP)):
		v = Data[GROUP][TRACE][i]
		if v_prev == None or v != v_prev: # only copy samples where ref trace changes
			copy_datum(i)
		v_prev = v

	#for trace in group_new:
	#    group_new[trace] = np.array(group_new[trace])

	Data[GROUP_RES] = group_new


def Trace_RemoveAusreisser(Data, GROUP, TRACE, std_faktor=5, delete=False):
	""" removes values that are outside of std_faktor times the standard deviation """
	std = np.std(Data[GROUP][TRACE])
	avg = mean(Data[GROUP][TRACE])
	listi = []
	for i in range(Group_Length(Data, GROUP)):
		v = Data[GROUP][TRACE][i]
		if not (avg - std_faktor*std < v < avg + std_faktor*std):
			listi.append(i)

	if(delete):
		Group_Remove_Dataset(Data, GROUP, listi)
	return listi

def Trace_getAvg(Data, GROUP, TRACE, t_start=0, t_end=-1, func_ignore=lambda x, i: True):
	"""
	Calculates Avg over Function
	:param Data:
	:param GROUP:
	:param TRACE:
	:param t_start:
	:param t_end:
	:param func_ignore: function is given values from trace. if this func returns false, value is ignored for avg calculation
	:return: avarage value of trace
	"""
	i_start = time2index(Data[GROUP], t_start)
	i_end = time2index(Data[GROUP], t_end)
	c = 0
	acc = 0
	for i in range(i_end - i_start):
		v = Data[GROUP][TRACE][i_start + i]
		if isNaN(v):
			#print("v is nan")
			continue
		if(func_ignore(v, i + i_start)):
			acc += v
			c += 1
	if c == 0:
		print("Trace_GetAVG: no values were counted - returning nan")
		return nan
	return acc / c



###################################
#        Rotation Functions       #
###################################


def Trace_rotateVector_ByTrace(Data, GROUP, TRACE_VECX, TRACE_VECY, TRACE_ANLGE, TRACE_VECX_OUT=None, TRACE_VECY_OUT=None):
	"""

	:param Data:
	:param GROUP:
	:param TRACE_VECX:
	:param TRACE_VECY:
	:param Angle:
	:param TRACE_VECX_OUT:
	:param TRACE_VECY_OUT:
	:return:
	"""


	if not TRACE_VECX_OUT:
		TRACE_VECX_OUT = TRACE_VECX
	if not TRACE_VECY_OUT:
		TRACE_VECY_OUT = TRACE_VECY


	tracex = []
	tracey = []
	for i in range(Group_Length(Data, GROUP)):
		x = Data[GROUP][TRACE_VECX][i]
		y = Data[GROUP][TRACE_VECY][i]
		theta = Data[GROUP][TRACE_ANLGE][i]

		tracex.append(x * cos(theta) - y * sin(theta))
		tracey.append(x * sin(theta) + y * cos(theta))

	Data[GROUP][TRACE_VECX_OUT] = tracex
	Data[GROUP][TRACE_VECY_OUT] = tracey

def Trace_rotateVector_ByConstant(Data, GROUP, TRACE_VECX, TRACE_VECY, Angle, TRACE_VECX_OUT=None, TRACE_VECY_OUT=None):
	"""
	Rotates the Vector (VecX, VecY) around the Z Axis by Angle
	:param TRACE_VECX: Vector X
	:param TRACE_VECY: Vector Y
	:param Angle: Rotation Angle in rad
	"""

	if not TRACE_VECX_OUT:
		TRACE_VECX_OUT = TRACE_VECX
	if not TRACE_VECY_OUT:
		TRACE_VECY_OUT = TRACE_VECY

	tracex = []
	tracey = []
	for i in range(Group_Length(Data, GROUP)):
		x = Data[GROUP][TRACE_VECX][i]
		y = Data[GROUP][TRACE_VECY][i]
		theta = Angle

		tracex.append(x * cos(theta) - y * sin(theta))
		tracey.append(x * sin(theta) + y * cos(theta))

	Data[GROUP][TRACE_VECX_OUT] = tracex
	Data[GROUP][TRACE_VECY_OUT] = tracey


def Trace_Rotate2D(Data, GROUP, TRACE_X, TRACE_Y, TRACE_ANGLE, TRACE_X_RES=None, TRACE_Y_RES=None, in_degree=False):
	"""
	Rotates two Traces around a given angle trace
	:param in_degree: if angle trace is in degree not rad
	"""


	if not TRACE_X_RES:
		TRACE_X_RES = TRACE_X
	if not TRACE_Y_RES:
		TRACE_Y_RES = TRACE_Y

	tracex_res = []
	tracey_res = []
	for i in range(Group_Length(Data, GROUP)):
		x = Data[GROUP][TRACE_X][i]
		y = Data[GROUP][TRACE_Y][i]
		a = Data[GROUP][TRACE_ANGLE][i]

		xr, yr = Vec2_rotate((x, y), a, is_degree=in_degree)

		tracex_res.append(xr)
		tracey_res.append(yr)

	Data[GROUP][TRACE_X_RES] = tracex_res
	Data[GROUP][TRACE_Y_RES] = tracey_res

def Trace_Rotate3D(Data, GROUP, TRACE_X, TRACE_Y, TRACE_Z, TRACE_ANGLE_X, TRACE_ANGLE_Y, TRACE_ANGLE_Z, TRACE_X_RES=None, TRACE_Y_RES=None, TRACE_Z_RES=None, angle_in_degree=False):
	"""
	Rotates 3 Traces around a 3 given angle trace
	:param angle_in_degree: if angle trace is in degree not rad
	"""

	if not TRACE_X_RES:
		TRACE_X_RES = TRACE_X
	if not TRACE_Y_RES:
		TRACE_Y_RES = TRACE_Y
	if not TRACE_Z_RES:
		TRACE_Z_RES = TRACE_Z



	tracex_res = []
	tracey_res = []
	tracez_res = []
	for i in range(Group_Length(Data, GROUP)):
		x = Data[GROUP][TRACE_X][i]
		y = Data[GROUP][TRACE_Y][i]
		z = Data[GROUP][TRACE_Z][i]
		rot_x = Data[GROUP][TRACE_ANGLE_X][i]
		rot_y = Data[GROUP][TRACE_ANGLE_Y][i]
		rot_z = Data[GROUP][TRACE_ANGLE_Z][i]

		RotMount = getRotMat(rot_x, rot_y, rot_z, isdegrees=angle_in_degree)

		x_rot, y_rot, z_rot = RotMount.apply((x, y, z))

		tracex_res.append(x_rot)
		tracey_res.append(y_rot)
		tracey_res.append(z_rot)

	Data[GROUP][TRACE_X_RES] = tracex_res
	Data[GROUP][TRACE_Y_RES] = tracey_res
	Data[GROUP][TRACE_Z_RES] = tracez_res


###################################
#        Plot Functions           #
###################################

def Trace_Plot(Data, GROUP, TRACE, TIME_TRACE=TRACE_TIME, title="", marker=""):
	"""
	Plots given Trace
	:param title: title of plot
	"""
	from PlotData import plot_setup, plot_Trace, plot_show, plot_getLabel_fromTag

	plot_setup(title,
			   plot_getLabel_fromTag(TRACE),
			   plot_getLabel_fromTag(TIME_TRACE)
			   )
	plot_Trace(Data, GROUP, TRACE, TIME_TRACE, marker=marker)
	plot_show()

def Trace_Plot_Select_Sample(Data, GROUP, TRACE, TIME_TRACE=TRACE_TIME, onTrace=True, title="",
							 t_start=None, t_end=None
							 ):
	"""
	Plots given Trace and User can select a datapoint by clicking on the Plot
	:param onTrace: if True the Datapoint is selected closes to clicked position
	:param title: title of plot
	:return: (time, value)
	"""
	from PlotHelp import plot_setup, plot_show_onClick, FIGSIZE_BIG_UW
	from PlotData import plot_Trace, plot_getLabel_fromTag

	plot_setup(title,
			   plot_getLabel_fromTag(TRACE),
			   plot_getLabel_fromTag(TIME_TRACE),
			   figsize=FIGSIZE_BIG_UW)
	plot_Trace(Data, GROUP, TRACE, TIME_TRACE, t_start=t_start, t_end=t_end)
	p = plot_show_onClick()
	if not p:
		return None

	t, v = p
	if onTrace:
		v = time2value(Data[GROUP], t, TRACE, TIME_TRACE)
	return (t, v)


def Trace_PlotAllanVerivation(Data, GROUP, TRACE, dt):
	rate = 1 / dt

	import allantools
	import numpy as np
	b = allantools.Plot()
	a = allantools.Dataset(data=Data[GROUP][TRACE], rate=rate)
	a.compute("mdev")
	b.plot(a)
	b.show()




###################################
#        Datas Functions        #
###################################


def Datas_Avg_Traces_byProgress(Datas, GROUP, TRACES):
	"""
	Takes a list of Data's and averages traces in a given group using the progress trace
	Example: DataAvg = Datas_Avg_Traces_byProgress(DataSegments, GROUP_VDY_REF, TRACES=[TRACE_POSI_X_NAV, TRACE_POSI_Y_NAV])
		Result: Data=	{
							GROUP_VDY_REF: {
								TRACE_PROGRESS: [0, ..., 1],
								TRACE_POSI_X_NAV: [ ... ],
								TRACE_POSI_Y_NAV: [ ... ],
							}
						}


	:param Datas: list of Data
	:param GROUP: Group to Average
	:param TRACES: Trace or List of Traces to average
	:return: new Data with Group containing averaged Traces
	"""
	Data = {}
	Group_Create_Tstartend(Data, GROUP, 0.001, t_start=0, t_end=1)
	Trace_Rename(Data, GROUP, TRACE_TIME, TRACE_PROGRESS)

	if not isinstance(TRACES, list):
		TRACES = [TRACES]

	for TRACE in TRACES:
		TRACES_NEW = []
		for i, DataSeg in enumerate(Datas):
			Data[GROUP_TMP] = DataSeg[GROUP]
			TRACE_NEW = TRACE + "_{}".format(i)
			Trace_Resample(Data, GROUP_TMP, TRACE, GROUP, TRACE_NEW, TIME_TRACE=TRACE_PROGRESS)
			TRACES_NEW.append(TRACE_NEW)
			Group_Delete(Data, GROUP_TMP)
		Trace_ApplyFuncMultiTrace(Data, GROUP, TRACES_NEW, TRACES_OUT=[TRACE], func=lambda x : mean(x), param_as_array=True)
		Trace_Delete(Data, GROUP, TRACES_NEW)

	return Data




###################################
#        Complex Functions        #
###################################


def Datas_SyncTime_byTimestamp(Data1, Data2,
							   PARAM_GROUP_SYNC = GROUP_TIMESTAMP,
							   PARAM_TRACE_SYNC = TRACE_UNIX_TIMESTAMP,
							   PARAM_SAMPLE_POINT = 0.5 #[%] into data
							   ):
	"""
	Syncs to Data using Timestamps
	:param Data1:
	:param Data2:
	:param PARAM_GROUP_SYNC:
	:param PARAM_TRACE_SYNC:
	:param PARAM_SAMPLE_POINT: [0-1] - Sample Point to use for Sync. 0= Start, 1= End. 0.5=in the middle
	"""

	if not Group_Exists(Data1, [PARAM_GROUP_SYNC]):
		print("Group Sync missing in Data1")
		return
	if not Group_Exists(Data2, [PARAM_GROUP_SYNC]):
		print("Group Sync missing in Data2")
		return

	index1 = int(Group_Length(Data1, PARAM_GROUP_SYNC) * PARAM_SAMPLE_POINT)
	t1 = Data1[PARAM_GROUP_SYNC][TRACE_TIME][index1]
	v1 = Data1[PARAM_GROUP_SYNC][PARAM_TRACE_SYNC][index1]

	index2 = int(Group_Length(Data2, PARAM_GROUP_SYNC) * PARAM_SAMPLE_POINT)
	t2 = Data2[PARAM_GROUP_SYNC][TRACE_TIME][index2]
	v2 = Data2[PARAM_GROUP_SYNC][PARAM_TRACE_SYNC][index2]

	#t_shift = - (v2 - v1 + t1 - t2)
	t_shift = (t1 - t2) + (v2 - v1)


	Data_TimeShift(Data2, t_shift)


	#from PlotHelp import plot_setup, plotTrace, plot_show, plotPoint
	#plotTrace(Data1, PARAM_GROUP_SYNC, PARAM_TRACE_SYNC)
	#plotTrace(Data2, PARAM_GROUP_SYNC, PARAM_TRACE_SYNC)
	#plot_show()

	return t_shift


def Datas_SyncTime_byTrace(Data1, Data2,
						   PARAM_GROUP_SYNC,
						   PARAM_TRACE_SYNC,
						   PARAM_SAMPLE_TIME = 0.010,
						   PARAM_MAX_TIME_SHIFT = 5,
						   remove_starttimeoffset = False
						   ):
	"""
	Synchronizes two Datas by using a Group and Trace.
	Traces of Both Data are shifted against each other to find closes match
	:param PARAM_GROUP_SYNC: Group used for sync
	:param PARAM_TRACE_SYNC: Trace used for sync
	:param PARAM_SAMPLE_TIME: [s] minimum Step size for shift. small values increase calculation time and precession
	:param PARAM_MAX_TIME_SHIFT: [s] maximum shift possible. if set to small possibly no solution can be found
	:param remove_starttimeoffset: if set to True both Data times are shifted to start at t=0
	:return: time Group2 was shifted by
	"""

	if remove_starttimeoffset:
		Data_RemoveOffset_TimeTrace(Data1)
		Data_RemoveOffset_TimeTrace(Data2)


	#Create new Data to compare data
	GROUP_SYNC = "sync"
	GROUP_SYNC1 = "sync1"
	GROUP_SYNC2 = "sync2"
	TRACE_SYNC1 = "sync1"
	TRACE_SYNC2 = "sync2"
	DataCMP = {
		GROUP_SYNC1 : deepcopy(Data1[PARAM_GROUP_SYNC]),
		GROUP_SYNC2 : deepcopy(Data2[PARAM_GROUP_SYNC]),
	}


	#find start and end of sync group and create sync group. copy sync traces to sync group
	t_start1, t_end1 = group_getTimeStartEnd(DataCMP[GROUP_SYNC1])
	t_start2, t_end2 = group_getTimeStartEnd(DataCMP[GROUP_SYNC2])
	t_start = max(t_start1, t_start2)
	t_end = min(t_end1, t_end2)
	t_start = max(0, t_start) #avoid starting bevore t0
	Group_Create_Tstartend(DataCMP, GROUP_SYNC, PARAM_SAMPLE_TIME, t_end, t_start)
	Trace_Resample(DataCMP, GROUP_SYNC1, PARAM_TRACE_SYNC, GROUP_SYNC, TRACE_SYNC1)
	Trace_Resample(DataCMP, GROUP_SYNC2, PARAM_TRACE_SYNC, GROUP_SYNC, TRACE_SYNC2)


	index_shift_best = 0

	#Search for Best Time Shift
	if True:
		glen = Group_Length(DataCMP, GROUP_SYNC)
		group_loss_curve = {
			TRACE_TIME : [],
			TRACE_VALUE : []
		}
		err_min_val = None

		#Go Over all possible index shifts
		shift_count = int(PARAM_MAX_TIME_SHIFT / PARAM_SAMPLE_TIME)
		for index_shift in [i - shift_count for i in range(2 * shift_count)]:

			count = 0
			total_err = 0
			for i in range(Group_Length(DataCMP, GROUP_SYNC)):

				if not abs(index_shift) < i < glen - abs(index_shift):
					continue

				if(index_shift > 0):
					diff = DataCMP[GROUP_SYNC][TRACE_SYNC1][i] - DataCMP[GROUP_SYNC][TRACE_SYNC2][i + index_shift]
				else:
					diff = DataCMP[GROUP_SYNC][TRACE_SYNC1][i - index_shift] - DataCMP[GROUP_SYNC][TRACE_SYNC2][i]

				total_err += abs(diff)
				count += 1

			mean_err = total_err / count

			if err_min_val == None:
				err_min_val = mean_err
				index_shift_best = index_shift
			elif err_min_val > mean_err:
				err_min_val = min(err_min_val, mean_err)
				index_shift_best = index_shift

			group_loss_curve[TRACE_TIME].append(index_shift)
			group_loss_curve[TRACE_VALUE].append(mean_err)


		t_shift = -PARAM_SAMPLE_TIME * index_shift_best
		print("t_shift: {}".format(t_shift))

		Group_TimeShift(DataCMP, GROUP_SYNC2, t_shift, GROUP_RES=GROUP_SYNC2 + "_shifted")
		Trace_Resample(DataCMP, GROUP_SYNC2 + "_shifted", PARAM_TRACE_SYNC, GROUP_SYNC, TRACE_SYNC2 + "_shifted")

		DataCMP["OPTIMUM"] = group_loss_curve

		#from PlotData import plot_setup, plot_Trace, plot_show, plot_point
		#plot_Trace(DataCMP, "OPTIMUM", TRACE_VALUE)
		#plot_point((index_shift_best, err_min_val))
		#plot_show()


	#Debug Result
	if False:
		index_shift = index_shift_best
		glen = Group_Length(DataCMP, GROUP_SYNC)
		trace_delta = []
		count = 0
		total_err = 0
		for i in range(Group_Length(DataCMP, GROUP_SYNC)):

			if not abs(index_shift) < i < glen - abs(index_shift):
				trace_delta.append(0)
				continue

			if(index_shift > 0):
				diff = DataCMP[GROUP_SYNC][TRACE_SYNC1][i] - DataCMP[GROUP_SYNC][TRACE_SYNC2][i + index_shift]
			else:
				diff = DataCMP[GROUP_SYNC][TRACE_SYNC1][i - index_shift] - DataCMP[GROUP_SYNC][TRACE_SYNC2][i]

			trace_delta.append(diff + 1)
			total_err += abs(diff)
			count += 1

		DataCMP[GROUP_SYNC][TRACE_TMP] = trace_delta

		Trace_Sub(DataCMP, GROUP_SYNC, TRACE_SYNC1, TRACE_SYNC2, TRACE_DELTA)
		mean_err2 = arr_absmean(DataCMP[GROUP_SYNC][TRACE_DELTA])
		mean_err = total_err / count

		print("mean_err: {}".format(mean_err))
		print("mean_err2: {}".format(mean_err2))

		from PlotData import plot_setup, plot_Trace, plot_show, plot_point, plot_setup_legend
		#plotTrace(Data1, GROUP_BASIC_NAV, TRACE_VELOCITY)
		#plotTrace(Data2, GROUP_BASIC_NAV, TRACE_VELOCITY)
		plot_Trace(DataCMP, GROUP_SYNC, TRACE_SYNC1)
		plot_Trace(DataCMP, GROUP_SYNC, TRACE_SYNC2)
		plot_Trace(DataCMP, GROUP_SYNC, TRACE_DELTA)
		plot_Trace(DataCMP, GROUP_SYNC, TRACE_TMP)


		#Trace_Scale(DataCMP, GROUP_SYNC2, TRACE_TIME, Offset=2.8)
		Trace_Scale(DataCMP, GROUP_SYNC2, TRACE_TIME, Offset=-PARAM_SAMPLE_TIME * index_shift)
		plot_Trace(DataCMP, GROUP_SYNC2, PARAM_TRACE_SYNC)

		plot_setup_legend()
		plot_show()


	Data_TimeShift(Data2, t_shift)


	from FileModule import OpenDiadem_Data
	#OpenDiadem_Data(DataCMP)

	#Data = Data_Join(Data1, Data2)
	#OpenDiadem_Data(Data)

	#from PlotHelp import plot_setup, plotTrace, plot_show, plotPoint
	#plotTrace(Data1, PARAM_GROUP_SYNC, PARAM_TRACE_SYNC)
	#plotTrace(Data2, PARAM_GROUP_SYNC, PARAM_TRACE_SYNC)
	#plot_show()

	return t_shift


if __name__ == '__main__':
	Data = {
		GROUP_TMP : {
			TRACE_TIME:[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
			TRACE_VALUE:[nan, nan, 1, nan, 0, 1, 0, 1, 0, 1]
		}
	}

	pprint(Data[GROUP_TMP][TRACE_VALUE])
	Trace_Smooth(Data, GROUP_TMP, TRACE_VALUE)
	pprint(Data[GROUP_TMP][TRACE_VALUE])