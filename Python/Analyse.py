from ImportsBase import *

def mean_if_list(arr):
	if isinstance(arr, list):
		return mean(arr)
	else:
		return arr

def PlotResults_XY_Box(data, FEATURE_X, FEATURE_Y):

	d = {mean(d[FEATURE_X]) : d[FEATURE_Y] for d in data}
	pprint(d)
	plot_box_xy(d)



	plot_xy(
		[(mean_if_list(f[FEATURE_X]), mean_if_list(f[FEATURE_Y])) for f in data],
		label="Mittelwert",
		linestyle=LINESTYLE_DASHED, color=COLOR_GREEN
	)

def AnalyseResults_PlotPhaseCurrent(exp_name, DATASET):

	path_exp = Exp_getPath(exp_name)

	results = load_json(FILENAME_EXP_RESULTS, path_exp)
	data = load_json(FILENAME_EXP_DATA_STATS, path_exp)

	if True:
		plot_setup("Phasenstrom über Drehmoment", xlable="Drehmoment [NM]", ylable="Phasenstrom [A]", figsize=FIGSIZE_SMALL)

		FEATURE_X = FEATURE_MOTOR_TORQUE
		FEATURE_Y = FEATURE_AC_CURRENT

		PlotResults_XY_Box(data, FEATURE_X, FEATURE_Y)

		x = [mean_if_list(f[FEATURE_X]) for f in data]
		y = [mean_if_list(f[FEATURE_Y]) for f in data]

		plot_regression_linear(x, y, COLOR_RED, label="Regression")


		plot_setup_legend('upper left')

		plot_setup_grid()

		Exp_plot_to_file(exp_name, "ac_currents_over_torque")

		plot_show(False)

	if True:
		plot_setup("DC Strom über Drehmoment", xlable="Drehmoment [NM]", ylable="DC Strom [A]", figsize=FIGSIZE_SMALL)

		FEATURE_X = FEATURE_MOTOR_TORQUE
		FEATURE_Y = FEATURE_DC_CURRENT

		PlotResults_XY_Box(data, FEATURE_X, FEATURE_Y)

		x = [mean_if_list(f[FEATURE_X]) for f in data]
		y = [mean_if_list(f[FEATURE_Y]) for f in data]

		plot_regression_linear(x, y, COLOR_RED, label="Regression")

		plot_setup_legend()

		plot_setup_grid()

		Exp_plot_to_file(exp_name, "dc_currents_over_torque")

		plot_show(False)

	if True:
		plot_setup("Ströme über Drehmoment", xlable="Drehmoment [NM]", ylable="Strom [A]", figsize=FIGSIZE_SMALL)

		FEATURE_X = FEATURE_MOTOR_TORQUE
		FEATURE_Y = FEATURE_AC_CURRENT
		FEATURE_Y2 = FEATURE_DC_CURRENT

		plot_xy(
			[(mean_if_list(f[FEATURE_X]), mean_if_list(f[FEATURE_Y])) for f in data],
			label="AC",
			linestyle=LINESTYLE_DASHED, color=COLOR_GREEN
		)
		plot_xy(
			[(mean_if_list(f[FEATURE_X]), mean_if_list(f[FEATURE_Y2])) for f in data],
			label="DC",
			linestyle=LINESTYLE_DASHED, color=COLOR_BLUE
		)


		x = [mean_if_list(f[FEATURE_X]) for f in data]
		y = [mean_if_list(f[FEATURE_Y]) for f in data]
		y2 = [mean_if_list(f[FEATURE_Y2]) for f in data]

		plot_regression_linear(x, y, COLOR_RED, label="AC Regression")
		plot_regression_linear(x, y2, COLOR_MAGENTA, label="DC Regression")

		plot_setup_legend()

		plot_setup_grid()

		Exp_plot_to_file(exp_name, "currents_ac_dc_over_torque")

		plot_show(False)

	if False:
		plot_setup("Motorspeed over Torque", xlable="Torque [NM]", ylable="Motorspeed [rpm]", figsize=FIGSIZE_BIG)

		FEATURE_X = FEATURE_MOTOR_TORQUE
		FEATURE_Y = FEATURE_MOTOR_SPEED

		PlotResults_XY_Box(data, FEATURE_X, FEATURE_Y)


		plot_setup_legend()

		plot_setup_grid()

		Exp_plot_to_file(exp_name, "motorspeed_over_torque")

		plot_show(False)

	if False:
		plot_setup("Motorspeed over Phase Current", xlable="Phase Current [A]", ylable="Motorspeed [rpm]", figsize=FIGSIZE_BIG)

		FEATURE_X = FEATURE_AC_CURRENT
		FEATURE_Y = FEATURE_MOTOR_SPEED

		PlotResults_XY_Box(data, FEATURE_X, FEATURE_Y)

		plot_setup_legend()

		plot_setup_grid()

		Exp_plot_to_file(exp_name, "motorspeed_over_ac_current")

		plot_show(False)

	if False:
		plot_setup("Phase Current over DC Current", xlable="DC Current [A]", ylable="AC Current [A]", figsize=FIGSIZE_BIG)

		FEATURE_X = FEATURE_DC_CURRENT
		FEATURE_Y = FEATURE_AC_CURRENT

		PlotResults_XY_Box(data, FEATURE_X, FEATURE_Y)

		x = [mean_if_list(f[FEATURE_X]) for f in data]
		y = [mean_if_list(f[FEATURE_Y]) for f in data]

		plot_regression_linear(x, y, COLOR_RED)

		plot_setup_legend()

		plot_setup_grid()

		Exp_plot_to_file(exp_name, "phase_vs_dc_current")

		plot_show(False)

	plot_show()
