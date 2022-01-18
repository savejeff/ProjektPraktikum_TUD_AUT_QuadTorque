from ImportsBase import *

from Analyse import *


if __name__ == '__main__':

	if False: # Convert Raw Osci Snapshots

		#datestring = "2021-11-09"
		#datestring = "2021-11-11"
		#datestring = "2021-11-16"
		#datestring = "2021-11-18"
		#datestring = "2021-11-22"
		#datestring = "2021-11-22_2"
		#datestring = "2021-11-22_S"
		#datestring = "2021-12-16"
		#datestring = "2021-12-21_T"
		#datestring = "2022-01-18_T"

		#datestrings = [datestring]

		#datestrings = ["2021-12-21_" + n for n in ["010", "020", "030", "040", "050", "060", "070", "080", "090", "100"]]
		datestrings = ["2022-01-18_" + n for n in ["010", "015", "020", "025", "030", "035", "040", "045", "050", "055", "060", "065", "070", "075", "080", "085", "090", "095", "100"]]

		for datestring in datestrings:

			ConvertOsciLoggingAll(datestring)

			Execute_ForAllOsci(datestring)

	if True: # Do Complete Processing of a Dataset

		FORMAT_OSCI_SNAPSHOT = "acq{:04d}"

		#exp_name, DATASET = "Complete_2021-12-21", DATASET_2021_12_21
		exp_name, DATASET = "Complete_2022-01-18", DATASET_2022_01_18

		if False: # Process Dataset - Extract List of Feature Vectors

			path_exp = Exp_getPath(exp_name)


			# Go over all Recording Groups in Dataset
			all_data = []
			base_res, rec_groups = DATASET
			for throttle, datestring, logfilename, timestamp in rec_groups:
				print(f"Start with Throttle {throttle}")

				res = {
					FEATURE_THROTTLE : throttle,
					FEATURE_DC_CURRENT : [],
					FEATURE_DC_VOLTAGE : [],
					FEATURE_MOTOR_TORQUE : [],
					FEATURE_MOTOR_SPEED : [],
					FEATURE_AC_CURRENT : [],
					FEATURE_AC_PERIOD : [],
				}

				res.update(deepcopy(base_res))

				res.update(ExtractFeatureVector_ArduinoLog(datestring, logfilename, timestamp))

				# Go over all Osci Recordings and extract AC Current and Period
				for snapshot_id in range(10, 35):
					logfilename = FORMAT_OSCI_SNAPSHOT.format(snapshot_id)

					results = ExtractFeatureVector_OsciSnapshot(datestring, logfilename)

					res[FEATURE_AC_CURRENT] += [r[FEATURE_AC_CURRENT] for r in results]
					res[FEATURE_AC_PERIOD]  += [r[FEATURE_AC_PERIOD]  for r in results]


				all_data.append(res)

			# store all sample vales
			store_json(all_data, FILENAME_EXP_DATA_STATS, path_exp)

			#all_data = load_json(FILENAME_EXP_DATA_STATS, path_exp)

			# avarage sample values to get veature vector
			results = []
			all_results = []
			for res in all_data:
				res_new = {}
				for f, v in res.items():
					if isinstance(v, list): # avg if multiple values
						v = mean(v)
					res_new[f] = v

				all_results.append(res_new)

			store_json(all_results, FILENAME_EXP_RESULTS, path_exp)


		if True: # Plot Dataset Results
			AnalyseResults_PlotPhaseCurrent(exp_name, DATASET)



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


