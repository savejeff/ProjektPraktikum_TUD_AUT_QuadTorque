from ImportsBase import *


if __name__ == '__main__':
	# Load Osci Logging
	if False:
		datestring = "2021-11-11"
		#logfilename = "bldc_throttle_10.csv"

		logfilefolder = getLogfilefolder(datestring)

		for logfilename in getAllOsciLogfiles(datestring):

			data = load_csv_wHeader(logfilename, logfilefolder, mode = 1, sample_func=lambda x : float(x))

			#print(data)

			logfilename_out = file_name_swap_extension(logfilename, ".mat")

			store_mat({"Osci" : data}, path_join(logfilefolder, logfilename_out))




	if True:
		offset = -244498 #[1]
		offset_factor = 1148.709 #[1/g]
		leverarm = 0.025 #[m]

		datestring = "2021-11-16"
		logfilename = "COM_ser_2021-11-16_12-57-48"

		path_out = getLogfilefolder(datestring)
		Data = LoadData(datestring, logfilename)

		for group in Data:
			name = group.upper().replace(".", "_")
			print(f"SIGNAL_{name} = \"{group}\"")


		def CreateGroup_FromSignals(Data, GROUP, SIGNALS, dt=None, LOOKUP_SIGNAL_TO_TRACE : dict = None , delete_signal=False):

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
			Trace_Smooth(Data, GROUP_TEST, TRACE_MOTOR_SPEED, t_range=0.25)

			Trace_Derivative(Data, GROUP_TEST, TRACE_MOTOR_SPEED, TRACE_ACCEL)

			Trace_ApplyFunc(Data, GROUP_TEST, TRACE_ACCEL, lambda a: int(-100 < a < 100), TRACE_IS_STEADY_STATE)

		if True: # Create Second Group that only contains values where steady state

			Group_Filter_byTrace(Data, GROUP_TEST, TRACE_IS_STEADY_STATE, GROUP_RES=GROUP_TEST2)


		# Some cleanup by merge signals to groups
		CreateGroup_FromSignals(Data, GROUP_INA219, [SIGNAL_INA219_CURR, SIGNAL_INA219_PWR, SIGNAL_INA219_VOLT], delete_signal=True)
		CreateGroup_FromSignals(Data, GROUP_FRQ_IN0, [SIGNAL_GPIO_FRQ_IN0_DUR, SIGNAL_GPIO_FRQ_IN0_FRQ, SIGNAL_GPIO_FRQ_IN0_RPM], delete_signal=True)
		CreateGroup_FromSignals(Data, GROUP_AI0, [SIGNAL_GPIO_AI0_VOLT, SIGNAL_GPIO_AI0_PERCENT, SIGNAL_GPIO_AI0_RAW], delete_signal=True)


		if True: # Plot Current over Torque
			plot_setup("Current over Torque", xlable="Torque [NM]", ylable="DC Current [A]", figsize=FIGSIZE_BIG)

			x, y = Data[GROUP_TEST2][TRACE_TORQUE], Data[GROUP_TEST2][TRACE_DC_CURRENT]
			points = list(zip(x, y))
			plot_point(points, markersize=2)

			m, b = regression_linear(x, y)

			x_min, x_max = min(x), max(x)
			p_min = x_min, m * x_min + b
			p_max = x_max, m * x_max + b

			plot_xy([p_min, p_max], color=COLOR_RED)

			plot_tofile(path_join(path_out, "plot_current_over_torque.png"))
			plot_show(False)


		if True: # Plot Current over Torque
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

			plot_tofile(path_join(path_out, "plot_current_over_speed.png"))
			plot_show(False)



		if True: # Plot Speed over Throttle
			plot_setup("Current over Speed", xlable="Throttle [%]", ylable="Motor Speed [rpm]", figsize=FIGSIZE_BIG)

			x, y = Data[GROUP_TEST2][TRACE_THROTTLE], Data[GROUP_TEST2][TRACE_MOTOR_SPEED]
			points = list(zip(x, y))
			plot_point(points, markersize=2)

			plot_tofile(path_join(path_out, "plot_speed_over_throttle.png"))
			plot_show(False)




		OpenDiadem_Data(Data, PATH.PATH_TDV_OVERVIEW, block=False)


		plot_show()
