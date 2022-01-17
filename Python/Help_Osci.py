from Defines import *
from Help import *
from HelpMath import *
from PlotHelp import *
from PlotData import *
from TraceHelp import *

from FileHelp import *
from FileModule import *
#from Lookup_Logfiles import *
#import os



def ExtractFeatureVector_OsciSnapshot(datestring, logfilename, enable_offset_correct=False) -> "list[dict]":
	"""
	Take a osci snapshot (in .mat) and extracts a feature vector for every period
	:param datestring:
	:param logfilename:
	:return:
	"""

	Data = LoadData(datestring, logfilename)



	Trace_Rename(Data, GROUP_OSCI, TRACE_CHANNEL2_V, TRACE_VOLTAGE)

	# Conversion from Shunt Voltage to Phase current
	Trace_Rename(Data, GROUP_OSCI, TRACE_CHANNEL1_V, TRACE_PHASE_CURRENT)
	Trace_Scale(Data, GROUP_OSCI, TRACE_PHASE_CURRENT, ScaleFactor=100)

	TRACE_PHASE_CURRENT_SMOOTH = TRACE_PHASE_CURRENT + TRACE_POSTFIX_SMOOTH

	# Moving Avg filter to get a clean sinus/zero crossing
	Trace_Smooth(Data, GROUP_OSCI, TRACE_PHASE_CURRENT, TRACE_PHASE_CURRENT_SMOOTH, t_range=0.0001)
	Trace_Smooth(Data, GROUP_OSCI, TRACE_PHASE_CURRENT_SMOOTH, TRACE_PHASE_CURRENT_SMOOTH, t_range=0.00012)

	# Find zero Crossings by detect sign change
	Trace_ApplyFunc(Data, GROUP_OSCI, TRACE_PHASE_CURRENT_SMOOTH, func=lambda x : 1 if x >= 0 else 0, TRACE_RES=TRACE_TEST)
	Trace_Diff(Data, GROUP_OSCI, TRACE_TEST, TRACE_TEST2)

	list_index_period_start = []
	list_index_period_half = []
	for i in range(Group_Length(Data, GROUP_OSCI)):
		v = Data[GROUP_OSCI][TRACE_TEST2][i]

		if v < -0.1: # Check if negative flank -> period start
			list_index_period_start.append(i)
		if v > 0.1: # Check if negative flank -> period start
			list_index_period_half.append(i)

	print(f"list_index_period_start: {list_index_period_start}")

	# list_index_period_start like [ 1, 5, 7, 8 ]
	# list_index_period_half like [ 2, 6, 7.5, 9 ]


	# Split Complete Trace into seperate periods
	GROUPS_PERIOD = []
	GROUP_PERIOD_FORMAT = "Periode_{}"
	for period_num, (i_start, i_end) in enumerate(zip(list_index_period_start, list_index_period_start[1:])):

		print(f"period#{period_num}: i_start={i_start}, i_end={i_end}")

		GROUP_NAME = GROUP_PERIOD_FORMAT.format(period_num)


		Group_Crop(Data, GROUP_OSCI,
				   t_start=index2time(Data[GROUP_OSCI], i_start),
				   t_end=index2time(Data[GROUP_OSCI], i_end),
				   GROUP_RES=GROUP_NAME
				   )

		GROUPS_PERIOD.append(GROUP_NAME)

	print(f"Analyse_PhaseCurrent : found {len(GROUPS_PERIOD)} Periods in total")



	# Go over all periods and extract values
	results = [] # collect all feature vectors for every period
	for GROUP in GROUPS_PERIOD:

		res = {}

		# Remove timeoffset of Period
		Trace_Scale(Data, GROUP, TRACE_TIME, Offset=-Data[GROUP][TRACE_TIME][0], TRACE_RES = TRACE_TIME + "_noOffset")

		# Find First and second half of period (negative first, positive second)
		index_period_half = None
		for i in range(Group_Length(Data, GROUP)):
			v = Data[GROUP][TRACE_TEST2][i]

			if v > 0.1: # Check if negative flank -> period start
				index_period_half = i
				break
		print(f"index_period_half: {index_period_half}")

		#assert index_period_half != None
		if index_period_half == None:
			print("Error: Period half detection failed/not found")
			continue


		if enable_offset_correct:
			a = list_index_period_start[0]
			b = list_index_period_start[-1]
			current_offset = mean(Data[GROUP][TRACE_PHASE_CURRENT][a:b])
		else:
			current_offset = 0

		Trace_Copy(Data, GROUP, TRACE_PHASE_CURRENT, TRACE_PHASE_CURRENT + TRACE_POSTFIX_CORRECTED)

		# extract values for specific part of period
		def Analyse_PeriodHalf(i_start, i_end, is_neg=False):

			# Get Avg Current in this part of period
			current_avg = mean(Data[GROUP][TRACE_PHASE_CURRENT][i_start:i_end])
			current_avg -= current_offset

			if is_neg:
				current_avg *= -1
				Trace_ApplyFunc_ValueIndex(Data, GROUP, TRACE_PHASE_CURRENT + TRACE_POSTFIX_CORRECTED,
										   lambda i, x: x * -1 if i_start <= i <= i_end else x
										   )
		#Trace_Scale(Data, GROUP_OSCI, TRACE_PHASE_CURRENT + TRACE_POSTFIX_CORRECTED, ScaleFactor=-1)

		#print(f"{GROUP}: current_avg={current_avg}")


		Analyse_PeriodHalf(0, index_period_half, is_neg=True)
		Analyse_PeriodHalf(index_period_half, Group_Length(Data, GROUP), is_neg=False)

		period_current = mean(Data[GROUP][TRACE_PHASE_CURRENT + TRACE_POSTFIX_CORRECTED])

		period_current *= 3.0 / 2.0

		#print(f"period_current: {period_current}")

		period_duration = Data[GROUP][TRACE_TIME][-1] - Data[GROUP][TRACE_TIME][0]


		#res[TAG_T_START] = Data[GROUP][TRACE_TIME][0]
		#res[TAG_T_END] = Data[GROUP][TRACE_TIME][-1]
		res[FEATURE_AC_CURRENT] = period_current
		res[FEATURE_AC_PERIOD] = period_duration

		results.append(res)


	#OpenDiadem_Data(Data, PATH.PATH_TDV_ALANYSIS_PERIODS)

	#store_json(results, f"results_{datestring}_{logfilename}", PATH.DIR_TMP)
	return results




def Execute_ForAllOsci(datestring):

	logfilefolder = getLogfilefolder(datestring)

	# Use this to convert complete folder
	logfilenames = getAllOsciLogfiles(datestring)

	for logfilename_csv in logfilenames:

		logfilename = file_name_swap_extension(logfilename_csv, ".mat")

		Plot_Osci_Logging(datestring, logfilename)

def ConvertOsciLoggingAll(datestring):
	logfilefolder = getLogfilefolder(datestring)

	# Use this to convert complete folder
	logfilenames = getAllOsciLogfiles(datestring)

	# Use this to convert specific file
	#logfilenames = ["bldc_phase_current_phase_to_ground_voltage_throttle_100"]

	for logfilename in logfilenames:

		data = load_csv_wHeader(logfilename, logfilefolder, mode = 1, sample_func=lambda x: float(x))

		Data = {GROUP_OSCI: data}

		# Rename Channel Names to defined names
		Trace_Rename(Data, GROUP_OSCI, "Time (s)", TRACE_TIME)
		Trace_Rename(Data, GROUP_OSCI, "Channel 1 (V)", TRACE_CHANNEL1_V)
		if Trace_Exists(Data, GROUP_OSCI, "Channel 2 (V)"):
			Trace_Rename(Data, GROUP_OSCI, "Channel 2 (V)", TRACE_CHANNEL2_V)

		#OpenDiadem_Data(Data)

		# Store unmodified data
		logfilename_out = file_name_swap_extension(logfilename, ".mat")
		store_mat(Data, path_join(logfilefolder, logfilename_out))




def Plot_Osci_Logging(datestring, logfilename):

	logfilefolder = getLogfilefolder(datestring)

	Data = LoadData(datestring, logfilename)

	plot_setup("Channels", ylable="Spannung in [V]")
	from PlotData import plot_Trace
	plot_Trace(Data, GROUP_OSCI, TRACE_CHANNEL1_V, label=TRACE_CHANNEL1_V)
	plot_Trace(Data, GROUP_OSCI, TRACE_CHANNEL2_V, label=TRACE_CHANNEL2_V)

	plot_setup_legend(LEGEND_LOC_TOP_RIGHT)

	plot_tofile(path_join(logfilefolder, f"{logfilename}.png"))
	#plot_show()
	plot_close()

