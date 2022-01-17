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


def ExtractFeatureVector_ArduinoLog(datestring, logfilename, time : float) -> dict:
	"""
	Extracts Feature Values of Arduino Log at given time.
	:param datestring:
	:param logfilename:
	:param time: [s] timestamp center of steady state
	:return: samplevectoor with dc_current, dc_voltage, ...
	"""

	#### alle Traces fürs Auslesen vorbereiten

	# TODO move to dataset definition
	offset = -244498  # [1]
	offset_factor = 1148.709  # [1/g]
	leverarm = 0.025  # [m]

	# Load Data from File
	path_out = getLogfilefolder(datestring)
	Data = LoadData(datestring, logfilename)

	if True:  # Create HX711 Group and process raw value
		Group_Copy(Data, SIGNAL_HX711_RAW, GROUP_HX711)
		Trace_Rename(Data, GROUP_HX711, SIGNAL_HX711_RAW, TRACE_RAW)

		Trace_ApplyFunc(Data, GROUP_HX711, TRACE_RAW, func=lambda x: (x - offset) / offset_factor,
						TRACE_RES=TRACE_WEIGHT_GRAM)

		Trace_Scale(Data, GROUP_HX711, TRACE_WEIGHT_GRAM, ScaleFactor=9.81 / 1000.0, TRACE_RES=TRACE_FORCE)
		Trace_Scale(Data, GROUP_HX711, TRACE_FORCE, ScaleFactor=leverarm, TRACE_RES=TRACE_TORQUE)

	if True:  # Create Test Group to merge all data together
		Group_Create_dt(Data, GROUP_TEST, dt=0.1)
		Trace_Resample(Data, GROUP_HX711, TRACE_TORQUE, GROUP_TEST)
		Trace_Resample(Data, SIGNAL_ESC_APP, SIGNAL_ESC_APP, GROUP_TEST, TRACE_THROTTLE)
		Trace_Resample(Data, SIGNAL_INA219_CURR, SIGNAL_INA219_CURR, GROUP_TEST, TRACE_DC_CURRENT)
		Trace_Resample(Data, SIGNAL_INA219_VOLT, SIGNAL_INA219_VOLT, GROUP_TEST, TRACE_DC_VOLT)
		Trace_Resample(Data, SIGNAL_GPIO_FRQ_IN0_RPM, SIGNAL_GPIO_FRQ_IN0_RPM, GROUP_TEST, TRACE_MOTOR_SPEED)

		#Trace_Smooth(Data, GROUP_TEST, TRACE_DC_CURRENT, t_range=2)
		#Trace_Smooth(Data, GROUP_TEST, TRACE_DC_VOLT, t_range=2)
		#Trace_Smooth(Data, GROUP_TEST, TRACE_TORQUE, t_range=2)
		#Trace_Smooth(Data, GROUP_TEST, TRACE_MOTOR_SPEED, t_range=2)

	#OpenDiadem_Data(Data, PATH.PATH_TDV_OVERVIEW, block=False)

	#### Werte auslesen

	# TODO auto detect start and end time of motor spinning/steady state and replace "time" variable and torque offset "time - 5"
	range = 2.0 #[s]

	t_start = time - range / 2
	t_end = time + range / 2

	# Get Zero Offset of motor torque (5s before sample point)
	torque_offset = Trace_getValue_atTime(Data, GROUP_TEST, TRACE_TORQUE, time - 5)
	# remove offset from torque trace
	Trace_Scale(Data, GROUP_TEST, TRACE_TORQUE, Offset=-torque_offset)

	# get all sample values between t_start and t_end
	dc_current = Trace_getValues_TimeSegement(Data, GROUP_TEST, TRACE_DC_CURRENT, t_start, t_end)
	dc_voltage = Trace_getValues_TimeSegement(Data, GROUP_TEST, TRACE_DC_VOLT, t_start, t_end)
	motor_torque = Trace_getValues_TimeSegement(Data, GROUP_TEST, TRACE_TORQUE, t_start, t_end)
	motor_speed = Trace_getValues_TimeSegement(Data, GROUP_TEST, TRACE_MOTOR_SPEED, t_start, t_end)

	#dc_current = Trace_getValue_atTime(Data, GROUP_TEST, TRACE_DC_CURRENT, time)
	#dc_voltage = Trace_getValue_atTime(Data, GROUP_TEST, TRACE_DC_VOLT, time)
	#motor_torque = Trace_getValue_atTime(Data, GROUP_TEST, TRACE_TORQUE, time)
	#motor_speed = Trace_getValue_atTime(Data, GROUP_TEST, TRACE_MOTOR_SPEED, time)

	res = {
		FEATURE_DC_CURRENT : list(dc_current),
		FEATURE_DC_VOLTAGE : list(dc_voltage),
		FEATURE_MOTOR_TORQUE : list(motor_torque),
		FEATURE_MOTOR_SPEED : list(motor_speed),
	}

	return res

