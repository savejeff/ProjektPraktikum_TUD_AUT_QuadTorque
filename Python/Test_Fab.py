from ImportsBase import *


if __name__ == '__main__':

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




