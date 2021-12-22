import matplotlib.pyplot as plt

from ImportsBase import *


def Analyse_PhaseCurrent(datestring, logfilename, enable_offset_correct=False):
	"""
	Take a logfile and creates a json file with extracted feature vector for every period
	:param datestring: 
	:param logfilename: 
	:return: 
	"""

	logfilefolder = getLogfilefolder(datestring)

	Data = LoadData(datestring, logfilename)

	if True: # Extract / Process Osci Logging

		results = {}

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


		# Go over all periods and extract values
		for GROUP in GROUPS_PERIOD:

			results[GROUP] = {}

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

			current_period = mean(Data[GROUP][TRACE_PHASE_CURRENT + TRACE_POSTFIX_CORRECTED])

			current_period *= 3.0 / 2.0

			#print(f"current_period: {current_period}")


			results[GROUP][TAG_T_START] = Data[GROUP][TRACE_TIME][0]
			results[GROUP][TAG_T_END] = Data[GROUP][TRACE_TIME][-1]
			results[GROUP][TAG_CURRENT_PERIOD] = current_period


		#OpenDiadem_Data(Data, PATH.PATH_TDV_ALANYSIS_PERIODS)

		#store_json(results, f"results_{datestring}_{logfilename}", PATH.DIR_TMP)
		return results

def Analyse_all_Data(name, datestring, logfilename, time):

	#### alle Traces fürs Auslesen vorbereiten

	offset = -244498  # [1]
	offset_factor = 1148.709  # [1/g]
	leverarm = 0.025  # [m]

	# Load Data from File
	path_out = getLogfilefolder(datestring)
	Data = LoadData(datestring, logfilename)

	def CreateGroup_FromSignals(Data, GROUP, SIGNALS, dt=None, LOOKUP_SIGNAL_TO_TRACE: dict = None,
								delete_signal=False):

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

			TRACE = SIGNAL
			if SIGNAL in LOOKUP_SIGNAL_TO_TRACE:
				TRACE = LOOKUP_SIGNAL_TO_TRACE[SIGNAL]

			Trace_Resample(Data, SIGNAL, SIGNAL, GROUP, TRACE_NEW=TRACE)

			if delete_signal:
				Group_Delete(Data, SIGNAL)

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

		Trace_Smooth(Data, GROUP_TEST, TRACE_DC_CURRENT, t_range=2)
		Trace_Smooth(Data, GROUP_TEST, TRACE_DC_VOLT, t_range=2)
		Trace_Smooth(Data, GROUP_TEST, TRACE_TORQUE, t_range=2)
		Trace_Smooth(Data, GROUP_TEST, TRACE_MOTOR_SPEED, t_range=2)

	#OpenDiadem_Data(Data, PATH.PATH_TDV_OVERVIEW, block=False)

	#### Werte auslesen



	all_results[name]["DC_Current"].append(
		Trace_getValue_atTime(Data, GROUP_TEST, TRACE_DC_CURRENT, time))
	all_results[name]["DC_Voltage"].append(
		Trace_getValue_atTime(Data, GROUP_TEST, TRACE_DC_VOLT, time))
	all_results[name]["Torque"].append(
		Trace_getValue_atTime(Data, GROUP_TEST, TRACE_TORQUE, time) - Trace_getValue_atTime(Data,
																									 GROUP_TEST,
																									 TRACE_TORQUE,
																									time - 5))
	all_results[name]["Motorspeed"].append(
		Trace_getValue_atTime(Data, GROUP_TEST, TRACE_MOTOR_SPEED, time))

	return all_results

if __name__ == '__main__':

	if False: #automatisch alle Werte auslesen

		path_exp = path_join(PATH.DIR_EXPERIMENTS, "Auswertung")
		mkdir(path_exp)

		all_results = {}
		for count in range(10, 110, 10):
			all_results[f"throttle {count}"] = {}
			all_results[f"throttle {count}"]["DC_Current"] = []
			all_results[f"throttle {count}"]["DC_Voltage"] = []
			all_results[f"throttle {count}"]["Torque"] = []
			all_results[f"throttle {count}"]["Motorspeed"] = []
			all_results[f"throttle {count}"]["AC_Current"] = []

		for ii in range(len(LIST_ARDUINOFILES)):
			name, datestring, logfilename, time = LIST_ARDUINOFILES[ii]

			Analyse_all_Data(name, datestring, logfilename, time)


			for jj in range(10, 35):
				#logfilename = f"acq00{jj}"
				logfilename = "acq{:04d}".format(jj)

				results = Analyse_PhaseCurrent(datestring, logfilename)

				all_current = []
				for Period in results:
					all_current.append(results[Period][TAG_CURRENT_PERIOD])

				all_results[name]["AC_Current"].append(mean(all_current))

		store_json(all_results, f"test_2", path_exp)

	if False: #Daten graphisch darstellen

		path_exp = path_join(PATH.DIR_EXPERIMENTS, "Auswertung")
		mkdir(path_exp)

		results = load_json("test_2", path_exp)

		torque_vec = []
		ac_current_vec = []
		rpm_vec = []
		dc_current_vec = []

		for name in results:
			torque_vec.append(results[name]["Torque"])
			ac_current_vec.append(mean(results[name]["AC_Current"]))
			rpm_vec.append(results[name]["Motorspeed"])
			dc_current_vec.append(results[name]["DC_Current"])

		plot_setup("Currents over Torque", xlable="Torque [NM]", ylable="Current [A]", figsize=FIGSIZE_BIG)

		plt.plot(torque_vec, ac_current_vec, 'o')
		plt.plot(torque_vec, dc_current_vec, 'o')

		plt.legend(["AC Current", "DC Current"])

		plot_tofile(path_join(path_exp, "currents_over_torque.png"))

		plot_show(False)

		plot_setup("Motorspeed over Torque", xlable="Torque [NM]", ylable="Motorspeed [rpm]", figsize=FIGSIZE_BIG)
		plt.plot(torque_vec, rpm_vec, 'o')

		plot_tofile(path_join(path_exp, "motorspeed_over_torque.png"))

		plot_show(False)

		plot_setup("Motorspeed over Phase Current", xlable="Phase Current [A]", ylable="Motorspeed [rpm]", figsize=FIGSIZE_BIG)
		plt.plot(ac_current_vec, rpm_vec, 'o')

		plot_tofile(path_join(path_exp, "motorspeed_over_ac_current.png"))

		plot_show()




		

	if False: # Convert Osci Logging from .csv to .mat
		#datestring = "2021-11-09"
		#datestring = "2021-11-11"
		#datestring = "2021-11-16"
		#datestring = "2021-11-18"
		#datestring = "2021-11-22"
		#datestring = "2021-11-22_2"
		datestring = "2021-11-22_S"

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


	if True: # Example Process Osci Logging .mat and store to _mod.mat

		datestring, logfilename = "2021-12-21_020", "acq0020"

		logfilefolder = getLogfilefolder(datestring)

		Data = LoadData(datestring, logfilename)

		t0 = -0.0002054
		t1 = 0.0004064

		if True: # Test Example

			Trace_Rename(Data, GROUP_OSCI, TRACE_CHANNEL1_V, TRACE_PHASE_CURRENT)
			Trace_Rename(Data, GROUP_OSCI, TRACE_CHANNEL2_V, TRACE_VOLTAGE)

			i0 = time2index(Data[GROUP_OSCI], t0) # get index in array matching given time
			v0 = time2value(Data[GROUP_OSCI], t0, TRACE_PHASE_CURRENT) # get value of trace at given time

			# Create a Group by cropping another group
			Group_Crop(Data, GROUP_OSCI, t_start=t0, t_end=t1, GROUP_RES=GROUP_OSCI + "_TEST")

			Trace_Smooth(Data, GROUP_OSCI, TRACE_PHASE_CURRENT, TRACE_PHASE_CURRENT + "_smooth", t_range=0.0001)
			Trace_Smooth(Data, GROUP_OSCI, TRACE_PHASE_CURRENT + "_smooth", TRACE_PHASE_CURRENT + "_smooth", t_range=0.00012)
			Trace_Smooth(Data, GROUP_OSCI + "_TEST", TRACE_PHASE_CURRENT, TRACE_PHASE_CURRENT + "_smooth", t_range=0.0002)

			for i in range(Group_Length(Data, GROUP_OSCI)):
				t = Data[GROUP_OSCI][TRACE_TIME][i]
				v = Data[GROUP_OSCI][TRACE_PHASE_CURRENT][i]

			Trace_Diff(Data, GROUP_OSCI, TRACE_PHASE_CURRENT, TRACE_RES=TRACE_TEST)
			Trace_ApplyFunc(Data, GROUP_OSCI, TRACE_TEST, func=lambda x : x > 10, TRACE_RES=TRACE_TEST2)

			i_start = 0
			i_end = 100
			mean(Data[GROUP_OSCI][TRACE_TIME][i_start:i_end])

			#OpenDiadem_Data(Data, PATH.PATH_TDV_TMP)
			pass

		OpenDiadem_Data(Data, PATH.PATH_TDV_TMP)

		logfilename_out = logfilename + "_mod"
		#store_mat(Data, path_join(logfilefolder, logfilename_out))


	if False: # Example Process Osci Phase Detection


		datestring, logfilename = "2021-12-21_010", "acq0019"
		#datestring, logfilename = "2021-11-22", "bldc_phase_current_phase_to_phase_voltage_throttle_50"


		path_exp = path_join(PATH.DIR_EXPERIMENTS, "Test_Phase_Detection")
		mkdir(path_exp)

		results = Analyse_PhaseCurrent(datestring, logfilename, enable_offset_correct=False)

		store_json(results, f"results_{datestring}_{logfilename}", path_exp)

		#OpenDiadem_Data(Data, PATH.PATH_TDV_TMP)
		#OpenDiadem_Data(Data, PATH.PATH_TDV_ALANYSIS_PERIODS)

		#logfilename_out = logfilename + "_mod"
		#store_mat(Data, path_join(logfilefolder, logfilename_out))



	if False: # Process Results

		CURRENT_DATESTRING = "2021-11-22_S"
		logdata = True

		if True: #use several osci plots

			path_exp = path_join(PATH.DIR_EXPERIMENTS, "Test_Phase_Detection_VariableThrottle")
			mkdir(path_exp)

			LIST_LOGFILES_10 =(
				("throttle 10", CURRENT_DATESTRING, "bldc_phase_current_phase_to_phase_voltage_throttle_10"),
				("throttle 10", CURRENT_DATESTRING, "bldc_phase_current_phase_to_ground_voltage_throttle_10")
			)

			LIST_LOGFILES_30 = (
				("throttle 30", CURRENT_DATESTRING, "bldc_phase_current_phase_to_phase_voltage_throttle_30"),
				("throttle 30", CURRENT_DATESTRING, "bldc_phase_current_phase_to_ground_voltage_throttle_30")
			)

			LIST_LOGFILES_50 = (
				("throttle 50", CURRENT_DATESTRING, "bldc_phase_current_phase_to_phase_voltage_throttle_50"),
				("throttle 50", CURRENT_DATESTRING, "bldc_phase_current_phase_to_ground_voltage_throttle_50")
			)

			LIST_LOGFILES_70 = (
				("throttle 70", CURRENT_DATESTRING, "bldc_phase_current_phase_to_phase_voltage_throttle_70"),
				("throttle 70", CURRENT_DATESTRING, "bldc_phase_current_phase_to_ground_voltage_throttle_70")
			)

			LIST_LOGFILES_100 = (
				("throttle 100", CURRENT_DATESTRING, "bldc_phase_current_phase_to_phase_voltage_throttle_100"),
				("throttle 100", CURRENT_DATESTRING, "bldc_phase_current_phase_to_ground_voltage_throttle_100")
			)

			LIST_LOGFILES = (
				(LIST_LOGFILES_10),
				(LIST_LOGFILES_30),
				(LIST_LOGFILES_50),
				(LIST_LOGFILES_70),
				(LIST_LOGFILES_100)
			)

		if False: #just use one osci plot
			LIST_LOGFILES = (
				("throttle 10", CURRENT_DATESTRING, "bldc_phase_current_phase_to_phase_voltage_throttle_10"),
				("throttle 30", CURRENT_DATESTRING, "bldc_phase_current_phase_to_phase_voltage_throttle_30"),
				("throttle 50", CURRENT_DATESTRING, "bldc_phase_current_phase_to_phase_voltage_throttle_50"),
				("throttle 70", CURRENT_DATESTRING, "bldc_phase_current_phase_to_phase_voltage_throttle_70"),
				("throttle 100", CURRENT_DATESTRING, "bldc_phase_current_phase_to_phase_voltage_throttle_100")

			)

		plot_data = {}
		list_avg = []
		for ii in range(len(LIST_LOGFILES)):

			for name, datestring, logfilename in LIST_LOGFILES[ii]:

				path_exp = path_join(PATH.DIR_EXPERIMENTS, "Test_Phase_Detection")
				mkdir(path_exp)

				if True:
					results = Analyse_PhaseCurrent(datestring, logfilename)

					store_json(results, f" results_{datestring}_{logfilename}", path_exp)

					#results = load_json(f"results_{datestring}_{logfilename}", path_exp)

				all_current = []
				for Period in results:
					print(results[Period][TAG_CURRENT_PERIOD])
					all_current.append(results[Period][TAG_CURRENT_PERIOD])

				if name in plot_data:
					plot_data[name].extend(all_current)
				else:
					plot_data[name] = all_current


		for name in plot_data:

			list_avg.append(mean(plot_data[name]))
			print(f"{name}: avg={mean(plot_data[name])}")
#######

		path_exp = path_join(PATH.DIR_EXPERIMENTS, "Test_Phase_Detection_VariableThrottle")
		mkdir(path_exp)

		if CURRENT_DATESTRING == "2021-11-22":
			list_DCCurrent = [0.885, 3.17, 5.72, 9.57, 14.83]		#2021-11-22
			list_torque = [0.01, 0.026, 0.044, 0.066, 0.091]        #2021-11-22
		elif CURRENT_DATESTRING == "2021-11-22_S":
			list_torque = [0.003, 0.011, 0.013, 0.02, 0.025]        #2021-11-22_S
		elif CURRENT_DATESTRING == "2021-11-22_2":
			list_torque = [0.019, 0.032, 0.042, 0.049, 0.060]        #2021-11-22_2

		if logdata == True:
			store_json(plot_data, "plot_data_" + CURRENT_DATESTRING, path_exp)

		plot_setup("Phase Current over Throttle", ylable="Current in A")

		#plot_point(list(enumerate(all_current)))
		plot_box(plot_data)

		if logdata == True:
			plot_tofile(path_join(path_exp, "boxplot" + CURRENT_DATESTRING + ".png"))

		plot_show(False)

		plot_setup("Phase Current over Torque", xlable="Torque [NM]", ylable="Phase Current [A]", figsize=FIGSIZE_BIG)
		plt.plot(list_torque, list_avg)
		#plt.plot(list_torque, list_DCCurrent)

		m, b = regression_linear(list_torque, list_avg)

		x_min, x_max = min(list_torque), max(list_torque)
		p_min = x_min, m * x_min + b
		p_max = x_max, m * x_max + b

		plot_xy([p_min, p_max], color=COLOR_RED)

		if logdata == True:
			plot_tofile(path_join(path_exp, "PhaseCurrent_over_Torque_" + CURRENT_DATESTRING + "_regression.png"))

		print(f"Steigung= {m},Achsenabschnitt: {b}")

		plot_show()



	if False: # Convert Arduino Loggings
		offset = -244498 #[1]
		offset_factor = 1148.709 #[1/g]
		leverarm = 0.025 #[m]

		# Select a Logfile to work with
		#datestring, logfilename, name = "2021-11-16", "COM_ser_2021-11-16_12-57-48", "1000KV_4S_PropS_0"
		#datestring, logfilename, name = "2021-11-22", "COM_ser_2021-11-22_12-04-01", "LabMotor_3S_PropB_0"  # Motor Labor, 3S Bat, Big Prop #0
		#datestring, logfilename, name = "2021-11-22", "COM_ser_2021-11-22_12-27-57", "LabMotor_3S_PropB_1"  # Motor Labor, 3S Bat, Big Prop #1
		#datestring, logfilename, name = "2021-11-22", "COM_ser_2021-11-22_12-38-52", "LabMotor_3S_PropB_2"  # Motor Labor, 3S Bat, Big Prop #2
		#datestring, logfilename, name = "2021-11-22_S", "COM_ser_2021-11-22_12-50-35", "LabMotor_3S_PropS_1"  # Motor Labor, 3S Bat, Small Prop #1
		#datestring, logfilename, name = "2021-11-22_S", "COM_ser_2021-11-22_12-57-26", "LabMotor_3S_PropS_2" # Motor Labor, 3S Bat, Small Prop #2
		#datestring, logfilename, name = "2021-11-22_2", "COM_ser_2021-11-22_14-19-40", "LabMotor_3S_PropS_1" # Motor #2, 3S Bat, Small Prop #1
		#datestring, logfilename, name = "2021-11-22_2", "COM_ser_2021-11-22_14-28-17", "LabMotor_3S_PropS_2" # Motor #2, 3S Bat, Small Prop #2
		datestring, logfilename, name = "2021-12-21_100", "COM_ser_2021-12-21_13-49-00", "LabMotor_"


		# Load Data from File
		path_out = getLogfilefolder(datestring)
		Data = LoadData(datestring, logfilename)

		#for group in Data: # Generate Signal Defines for Defines.py
		#	sig_name = group.upper().replace(".", "_")
		#	print(f"SIGNAL_{sig_name} = \"{group}\"")


		def CreateGroup_FromSignals(Data, GROUP, SIGNALS, dt=None, LOOKUP_SIGNAL_TO_TRACE : dict = None, delete_signal=False):

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

				TRACE = SIGNAL
				if SIGNAL in LOOKUP_SIGNAL_TO_TRACE:
					TRACE = LOOKUP_SIGNAL_TO_TRACE[SIGNAL]

				Trace_Resample(Data, SIGNAL, SIGNAL, GROUP, TRACE_NEW=TRACE)

				if delete_signal:
					Group_Delete(Data, SIGNAL)




		if True: # Create HX711 Group and process raw value
			Group_Copy(Data, SIGNAL_HX711_RAW, GROUP_HX711)
			Trace_Rename(Data, GROUP_HX711, SIGNAL_HX711_RAW, TRACE_RAW)

			#OpenDiadem_Data(Data)

			Trace_ApplyFunc(Data, GROUP_HX711, TRACE_RAW, func= lambda x: (x - offset) / offset_factor, TRACE_RES=TRACE_WEIGHT_GRAM)

			Trace_Scale(Data, GROUP_HX711, TRACE_WEIGHT_GRAM, ScaleFactor=9.81 / 1000.0, TRACE_RES=TRACE_FORCE)
			Trace_Scale(Data, GROUP_HX711, TRACE_FORCE, ScaleFactor=leverarm, TRACE_RES=TRACE_TORQUE)


		if True: # Create Test Group to merge all data together
			Group_Create_dt(Data, GROUP_TEST, dt=0.1)
			Trace_Resample(Data, GROUP_HX711, TRACE_TORQUE, GROUP_TEST)
			Trace_Resample(Data, SIGNAL_ESC_APP, SIGNAL_ESC_APP, GROUP_TEST, TRACE_THROTTLE)
			Trace_Resample(Data, SIGNAL_INA219_CURR, SIGNAL_INA219_CURR, GROUP_TEST, TRACE_DC_CURRENT)
			Trace_Resample(Data, SIGNAL_INA219_VOLT, SIGNAL_INA219_VOLT, GROUP_TEST, TRACE_DC_VOLT)
			Trace_Resample(Data, SIGNAL_GPIO_FRQ_IN0_RPM, SIGNAL_GPIO_FRQ_IN0_RPM, GROUP_TEST, TRACE_MOTOR_SPEED)

			Trace_Smooth(Data, GROUP_TEST, TRACE_DC_CURRENT, t_range=0.25)
			Trace_Smooth(Data, GROUP_TEST, TRACE_TORQUE, t_range=0.25)
			Trace_Smooth(Data, GROUP_TEST, TRACE_MOTOR_SPEED, t_range=1, TRACE_RES=TRACE_TMP)

			Trace_Derivative(Data, GROUP_TEST, TRACE_TMP, TRACE_ACCEL)


			#Trace_ApplyFunc(Data, GROUP_TEST, TRACE_ACCEL, lambda a: int(-400 < a < 400), TRACE_IS_STEADY_STATE)
			Trace_ApplyFunc2Trace(Data, GROUP_TEST, TRACE_ACCEL, TRACE_MOTOR_SPEED, lambda a, v: int((-400 < a < 400) and v > 2000), TRACE_IS_STEADY_STATE)

		if True: # Create Second Group that only contains values where steady state

			Group_Filter_byTrace(Data, GROUP_TEST, TRACE_IS_STEADY_STATE, GROUP_RES=GROUP_TEST2)


		# Some cleanup by merge signals to groups
		CreateGroup_FromSignals(Data, GROUP_INA219, [SIGNAL_INA219_CURR, SIGNAL_INA219_PWR, SIGNAL_INA219_VOLT], delete_signal=True)
		CreateGroup_FromSignals(Data, GROUP_FRQ_IN0, [SIGNAL_GPIO_FRQ_IN0_DUR, SIGNAL_GPIO_FRQ_IN0_FRQ, SIGNAL_GPIO_FRQ_IN0_RPM], delete_signal=True)
		CreateGroup_FromSignals(Data, GROUP_AI0, [SIGNAL_GPIO_AI0_VOLT, SIGNAL_GPIO_AI0_PERCENT, SIGNAL_GPIO_AI0_RAW], delete_signal=True)





		if True: # EXAMPLE: Store processed data into _mod.mat

			logfilename_out = logfilename + "_mod"

			StoreData(Data, datestring, logfilename_out)

		# Show result in Diadem
		OpenDiadem_Data(Data, PATH.PATH_TDV_OVERVIEW, block=False)


		plot_show()
		#plot_close()
