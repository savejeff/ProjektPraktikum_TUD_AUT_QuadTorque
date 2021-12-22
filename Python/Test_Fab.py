from ImportsBase import *


if __name__ == '__main__':

	if False: # Convert Osci Logging from .csv to .mat
		#datestring = "2021-11-09"
		#datestring = "2021-11-11"
		#datestring = "2021-11-16"
		#datestring = "2021-11-18"
		datestring = "2021-11-22"
		#datestring = "2021-11-22_2"
		#datestring = "2021-11-22_S"

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

		datestring, logfilename = "2021-11-22", "bldc_phase_current_phase_to_ground_throttle_50"

		logfilefolder = getLogfilefolder(datestring)

		Data = LoadData(datestring, logfilename)
		if False: #Testwerte für 2021-11-22_S
			if False:  # Testwerte für 100%
				t_start = 0.000095
				t_end = 0.002535

				ta = 0.001621
				tb = 0.001723
				tc = 0.001926
				td = 0.002028
				te = 0.002231

			if False:  # Testwerte für 70%
				t_start = -0.001272
				t_end = 0.0021515

				ta = -0.000213
				tb = -0.000115
				tc = 0.000110
				td = 0.000222
				te = 0.000462

			if False:  # Testwerte für 50%
				t_start = -0.000174
				t_end = 0.002029

				ta = 0.000973
				tb = 0.001095
				tc = 0.001340
				td = 0.001462
				te = 0.001707

			if True:  # Testwerte für 30%
				t_start = -0.0018175
				t_end = 0.002584

				ta = 0.000409
				tb = 0.000566
				tc = 0.000879
				td = 0.001036
				te = 0.001350

		if True: #Testwerte für 2021-11-22

			if False:  # Testwerte für 100%
				t_start = -2.33e-3
				t_end = 2.58e-3

				ta = -2.61e-4
				tb = -1.26e-4
				tc = 1.45e-4
				td = 2.76e-4
				te = 5.54e-4

			if False:  # Testwerte für 70%
				t_start = -1.98e-3
				t_end = 8.28e-4

				ta = -1.47e-3
				tb = -1.31e-3
				tc = -9.93e-4
				td = -8.42e-4
				te = -5e-4

			if True:  # Testwerte für 50%
				t_start = -2.17e-3
				t_end = 2.47e-3

				ta = -1.49e-3
				tb = -1.29e-3
				tc = -9.10e-4
				td = -7.52e-4
				te = -3.81e-4

			if False:  # Testwerte für 30%
				t_start = -2.12e-3
				t_end = 2.16e-3

				ta = 7.33e-4
				tb = 9.71e-4
				tc = 1.44e-3
				td = 1.68e-3
				te = 2.16e-3

			if False:  # Testwerte für 10%
				t_start = -1.28e-3
				t_end = 1.26e-3

				ta = -1.28e-3
				tb = -7.38e-4
				tc = -3.3e-5
				td = 4.82e-4
				te = 1.26e-3

		if True: # Test Example

			Trace_Rename(Data, GROUP_OSCI, TRACE_CHANNEL1_V, TRACE_PHASE_CURRENT)
			Trace_Rename(Data, GROUP_OSCI, TRACE_CHANNEL2_V, TRACE_VOLTAGE)

			i0 = time2index(Data[GROUP_OSCI], t_start) # get index in array matching given time
			v0 = time2value(Data[GROUP_OSCI], t_start, TRACE_PHASE_CURRENT) # get value of trace at given time

			# Create a Group by cropping another group
			Group_Crop(Data, GROUP_OSCI, t_start=t_start, t_end=t_end, GROUP_RES=GROUP_OSCI + "_CROP")

			Trace_Smooth(Data, GROUP_OSCI, TRACE_PHASE_CURRENT, TRACE_PHASE_CURRENT + "_smooth", t_range=0.00001)
			Trace_Smooth(Data, GROUP_OSCI + "_CROP", TRACE_PHASE_CURRENT, TRACE_PHASE_CURRENT + "_smooth", t_range=0.00001)

			offset = mean(Data[GROUP_OSCI + "_CROP"][TRACE_PHASE_CURRENT + "_smooth"])

			Trace_ApplyFunc(Data, GROUP_OSCI + "_CROP", TRACE_PHASE_CURRENT + "_smooth", func= lambda x: (x - offset), TRACE_RES= TRACE_PHASE_CURRENT + "_REAL")
			Trace_ApplyFunc(Data, GROUP_OSCI, TRACE_PHASE_CURRENT + "_smooth", func= lambda x: (x - offset), TRACE_RES= TRACE_PHASE_CURRENT + "_REAL")

			Group_Crop(Data, GROUP_OSCI, t_start=ta, t_end=te, GROUP_RES=GROUP_OSCI + "_Period")
			Group_Crop(Data, GROUP_OSCI, t_start=tb, t_end=tc, GROUP_RES=GROUP_OSCI + "_ACTIVE_HIGH")
			Group_Crop(Data, GROUP_OSCI, t_start=td, t_end=te, GROUP_RES=GROUP_OSCI + "_ACTIVE_LOW")

			print("AVG_crop:" + str(mean(Data[GROUP_OSCI + "_CROP"][TRACE_PHASE_CURRENT + "_REAL"])))
			print("AVG_orig:" + str(mean(Data[GROUP_OSCI][TRACE_PHASE_CURRENT + "_REAL"])))
			print("AVG_period:" + str(mean(Data[GROUP_OSCI + "_Period"][TRACE_PHASE_CURRENT + "_REAL"])))
			print("Durchschnitt im Sektor b) - c):" + str(mean(Data[GROUP_OSCI + "_ACTIVE_HIGH"][TRACE_PHASE_CURRENT + "_REAL"])) )
			print("Durchschnitt im Sektor d) - e):" + str(mean(Data[GROUP_OSCI + "_ACTIVE_LOW"][TRACE_PHASE_CURRENT + "_REAL"])) )


			#OpenDiadem_Data(Data, PATH.PATH_TDV_TMP)
			pass

		OpenDiadem_Data(Data, PATH.PATH_TDV_TMP)

		logfilename_out = logfilename + "_mod"
		store_mat(Data, path_join(logfilefolder, logfilename_out))



	if False: # Convert Arduino Loggings
		offset = -244498 #[1]
		offset_factor = 1148.709 #[1/g]
		leverarm = 0.025 #[m]

		# Select a Logfile to work with
		#datestring, logfilename, name = "2021-11-16", "COM_ser_2021-11-16_12-57-48", "1000KV_4S_PropS_0"
		#datestring, logfilename, name = "2021-11-22", "COM_ser_2021-11-22_12-04-01", "LabMotor_3S_PropB_0"  # Motor Labor, 3S Bat, Big Prop #0
		datestring, logfilename, name = "2021-11-22", "COM_ser_2021-11-22_12-27-57", "LabMotor_3S_PropB_1"  # Motor Labor, 3S Bat, Big Prop #1
		#datestring, logfilename, name = "2021-11-22", "COM_ser_2021-11-22_12-38-52", "LabMotor_3S_PropB_2"  # Motor Labor, 3S Bat, Big Prop #2
		#datestring, logfilename, name = "2021-11-22_S", "COM_ser_2021-11-22_12-50-35", "LabMotor_3S_PropS_1"  # Motor Labor, 3S Bat, Small Prop #1
		#datestring, logfilename, name = "2021-11-22_S", "COM_ser_2021-11-22_12-57-26", "LabMotor_3S_PropS_2" # Motor Labor, 3S Bat, Small Prop #2
		#datestring, logfilename, name = "2021-11-22_2", "COM_ser_2021-11-22_14-19-40", "LabMotor_3S_PropS_1" # Motor #2, 3S Bat, Small Prop #1
		#datestring, logfilename, name = "2021-11-22_2", "COM_ser_2021-11-22_14-28-17", "LabMotor_3S_PropS_2" # Motor #2, 3S Bat, Small Prop #2


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


		if False: # Plot Current over Torque
			plot_setup("Current over Torque", xlable="Torque [NM]", ylable="DC Current [A]", figsize=FIGSIZE_BIG)

			x, y = Data[GROUP_TEST2][TRACE_TORQUE], Data[GROUP_TEST2][TRACE_DC_CURRENT]
			points = list(zip(x, y))
			points = [(x, y) for x, y in points if not (y < 0.2 and x > 0.025)]
			plot_point(points, markersize=2)

			m, b = regression_linear(x, y)

			x_min, x_max = min(x), max(x)
			p_min = x_min, m * x_min + b
			p_max = x_max, m * x_max + b

			plot_xy([p_min, p_max], color=COLOR_RED)

			plot_tofile(path_join(path_out, "plot_current_over_torque_{}.png".format(name)))
			plot_show(False)


		if False: # Plot Current over Torque
			plot_setup("Current over Speed", xlable="Motor Speed [rpm]", ylable="DC Current [A]", figsize=FIGSIZE_BIG)

			x, y = Data[GROUP_TEST2][TRACE_MOTOR_SPEED], Data[GROUP_TEST2][TRACE_DC_CURRENT]
			points = list(zip(x, y))
			plot_point(points, markersize=2)

			coefs = np.polyfit(x, y, 2)
			print(f"coefs: {coefs}")

			#coefs[0] *= 0.75
			#coefs[1] = 0
			#coefs[2] = 0

			x_min, x_max = min(x), max(x)

			x_seq = np.linspace(x_min, x_max, 100)
			y_seq = np.polyval(coefs, x_seq)
			points = list(zip(x_seq, y_seq))
			plot_xy(points, color=COLOR_RED)

			plot_tofile(path_join(path_out, "plot_current_over_speed_{}.png".format(name)))
			plot_show(False)



		if False: # Plot Speed over Throttle
			plot_setup("Current over Speed", xlable="Throttle [%]", ylable="Motor Speed [rpm]", figsize=FIGSIZE_BIG)

			x, y = Data[GROUP_TEST2][TRACE_THROTTLE], Data[GROUP_TEST2][TRACE_MOTOR_SPEED]
			points = list(zip(x, y))
			plot_point(points, markersize=2)

			plot_tofile(path_join(path_out, "plot_speed_over_throttle_{}.png".format(name)))
			plot_show(False)


		if True: # EXAMPLE: Store processed data into _mod.mat

			logfilename_out = logfilename + "_mod"

			StoreData(Data, datestring, logfilename_out)

		# Show result in Diadem
		OpenDiadem_Data(Data, PATH.PATH_TDV_OVERVIEW, block=False)


		plot_show()
		#plot_close()
