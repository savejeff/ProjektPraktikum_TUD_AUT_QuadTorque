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

		if time == None: # Auto Detect time of steady state

			Trace_Smooth(Data, GROUP_TEST, TRACE_MOTOR_SPEED, t_range=1.2, TRACE_RES=TRACE_TMP)
			Trace_Derivative(Data, GROUP_TEST, TRACE_TMP, TRACE_ACCEL)

			#Trace_ApplyFunc(Data, GROUP_TEST, TRACE_ACCEL, lambda a: int(-400 < a < 400), TRACE_IS_STEADY_STATE)
			Trace_ApplyFunc2Trace(Data, GROUP_TEST, TRACE_ACCEL, TRACE_MOTOR_SPEED, lambda a, v: int((-750 < a < 750) and v > 2000), TRACE_IS_STEADY_STATE)

			i_start = Trace_FindFirst(Data, GROUP_TEST, TRACE_IS_STEADY_STATE, func=lambda x : x > 0.5)
			i_end = Trace_FindFirst(Data, GROUP_TEST, TRACE_IS_STEADY_STATE, func=lambda x : x < 0.5, i_start = i_start + 1)

			t_start = index2time(Data[GROUP_TEST], i_start)
			t_end = index2time(Data[GROUP_TEST], i_end)

		else:

			range = 2.0 #[s]

			t_start = time - range / 2
			t_end = time + range / 2

			#i_start = time2index(Data[GROUP_TEST], t_start)
			#i_end = time2index(Data[GROUP_TEST], t_end)

		if True: # Plot Steady State Start and End

			plot_setup("Steady State", xlable="Time", ylable="isSteadyState", figsize=FIGSIZE_BIG_W)

			plot_x_y(Data[GROUP_TEST][TRACE_TIME], Data[GROUP_TEST][TRACE_IS_STEADY_STATE])

			plot_point([(t_start, 1), (t_end, 1)], markersize=10, marker="*")

			max_speed = max(Data[GROUP_TEST][TRACE_MOTOR_SPEED])
			Trace_Scale(Data, GROUP_TEST, TRACE_MOTOR_SPEED, ScaleFactor=1.0 / max_speed, TRACE_RES=TRACE_TMP)
			plot_Trace(Data, GROUP_TEST, TRACE_TMP)

			t0 = Data[GROUP_TEST][TRACE_TIME][0]

			plot_point([(mean([t0, t_start]), 0)], markersize=10, marker="*", color=COLOR_RED, label="Samplepoint Torque Offset")


			plot_tofile(path_join(path_out, "plot_steady_state.png"))

			#plot_show(True)
			plot_close()


	#OpenDiadem_Data(Data, PATH.PATH_TDV_OVERVIEW, block=False)

	#### Werte auslesen

	t0 = Data[GROUP_TEST][TRACE_TIME][0]

	# Get Zero Offset of motor torque (5s before sample point)
	torque_offset = Trace_getValue_atTime(Data, GROUP_TEST, TRACE_TORQUE, mean([t0, t_end]))
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

