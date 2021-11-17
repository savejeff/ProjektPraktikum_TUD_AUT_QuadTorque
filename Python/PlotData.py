from PlotHelp import *
from StatisticHelp import *
from TraceHelp import *


def plot_getLabel_fromTag(TAG, add_unit=True, split_if_long=False):

	if not isinstance(TAG, str):
		return str(TAG)

	unit = get_Unit(TAG)
	LOOKUP_TAG_TO_TEXT = {
		# Example:
		#"Velx Support" : "$v_{x}$ Supp.",
	}

	if TAG in LOOKUP_TAG_TO_TEXT:
		tag = LOOKUP_TAG_TO_TEXT[TAG]
	else:
		tag = TAG.replace("_", " ")
	if add_unit and unit:
		if len(tag) > 10 and split_if_long:
			return "{}\n in {}".format(tag, unit)
		else:
			return "{} in {}".format(tag, unit)
	else:
		return tag

def plot_TraceXY(Data, GROUP, TRACE_X, TRACE_Y, marker="", t_start=None, t_end=None, color=None, label=None, linestyle=None, TIME_TRACE=TRACE_TIME):
	if t_start != None and t_end != None:
		from TraceHelp import Group_SplitStartEnd
		Data1 = {
			GROUP : Group_SplitStartEnd(Data, GROUP, t_start, t_end, TIME_TRACE)
		}

	else:
		Data1 = Data

	plot_x_y(
		Data1[GROUP][TRACE_X],
		Data1[GROUP][TRACE_Y],
		label, marker, color, linestyle
	)
	#plot_Trace(Data, GROUP, TRACE_Y, TRACE_X, marker, t_start, t_end, color, label)

def plot3d_TraceXYZ(Data, GROUP, TRACE_X, TRACE_Y, TRACE_Z, marker="", t_start=None, t_end=None, color=None, label=None, TIME_TRACE=TRACE_TIME):
	if t_start != None and t_end != None:
		from TraceHelp import Group_SplitStartEnd
		Data1 = {
			GROUP : Group_SplitStartEnd(Data, GROUP, t_start, t_end, TIME_TRACE)
		}

	else:
		Data1 = Data

	plot3D_x_y_z(
		Data1[GROUP][TRACE_X],
		Data1[GROUP][TRACE_Y],
		Data1[GROUP][TRACE_Z],
		label, marker, color
	)

def plot_Trace(Data, GROUP, TRACE, TIME_TRACE=TRACE_TIME, marker="", t_start=None, t_end=None, color=None, label=None):
	"""
	Plots a Given Trace over Time (or Optional over Given X Axis)
	"""

	"""
	plot_setup(
		title="Trace: {}->{}".format(GROUP, TRACE),
		xlable=get_Unit(TIME_TRACE),
		ylable=get_Unit(TRACE),
	)
	"""

	i_start = 0
	i_end = -1
	if t_start != None:
		from TraceHelp import time2index
		i_start = time2index(Data[GROUP], t_start, TIME_TRACE)
	if t_end != None:
		from TraceHelp import time2index
		i_end = time2index(Data[GROUP], t_end, TIME_TRACE)

	#print("i_start={}".format(i_start))
	#print("i_end={}".format(i_end))

	plot_x_y(
		Data[GROUP][TIME_TRACE][i_start: i_end],
		Data[GROUP][TRACE][i_start: i_end],
		label if label else TRACE, marker, color
	)
	"""
	plt.plot(
		Data[GROUP][TIME_TRACE][i_start: i_end],
		Data[GROUP][TRACE][i_start: i_end],
		marker=marker,
		#label=plot_getLable_byTrace(TRACE) if not label else label,
		label=label,
		color=_get_color(color)
	)
	"""


def plot_point_onTrace(Data, GROUP, TRACE, t=None, i=None, color=None, label=None, TIME_TRACE=TRACE_TIME):
	"""
	Plots one sample or a set of samples on a given Trace
	:param t: one time or list of time
	:param i: one index or list of index
	"""

	if t != None:
		if isinstance(t, list):
			for _t in t:
				plot_point_onTrace(Data, GROUP, TRACE, t=_t, color=color, label=label, TIME_TRACE=TIME_TRACE)
			return
		else:
			i = time2index(Data[GROUP], t, TIME_TRACE)


	if i != None:

		if isinstance(i, list):
			for _i in i:
				plot_point_onTrace(Data, GROUP, TRACE, i=_i, color=color, label=label, TIME_TRACE=TIME_TRACE)
				return
		else:

			value = Data[GROUP][TRACE][i]
			time = index2time(Data[GROUP], i, TIME_TRACE) if t != None else t
			plot_point((time, value), color=color, label=label)





##################################
#         Plot Bars              #
##################################
#https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.bar.html
#https://www.tutorialspoint.com/matplotlib/matplotlib_bar_plot.htm

PLOT_PARAM_BAR_WIDTH = 0.7

def get_yerr_MinMax(arr):
	return (mean(arr) - min(arr) , max(arr) - mean(arr))


def plot_featurevector_bar(data_dict):
	"""
	Plot a single Feature-Vector
	:param data_dict: like {tag1: value1, tag2: value2, ...}
	"""

	values = list(data_dict.values())
	lables = list(data_dict.keys())
	bars = plot_bar(lables, values)


def plot_featureset_bar_individually(data_dicts, func_lable_to_text=lambda x : x):
	"""
	Plots multiple Feature Vector to compare
	:param data_dicts: list of feature-vectors like [{tag1: value1, tag2: value2, ...}, {tag1: value1, tag2: value2, ...}]
	or dict of feature-vectors like  {name1: {tag1 : value1, ..}, name2: {tag1 : value1, ..}}
	:return:
	"""

	if isinstance(data_dicts, list):

		lables = ["Index: {}".format(i) for i in range(len(data_dicts))] #These are shown in legend
		lables_group = list(data_dicts[0].keys()) #these are shown below on X-Axis
		values = [list(d.values()) for d in data_dicts]


	elif isinstance(data_dicts, dict):

		lables = list(data_dicts.keys())
		lables_group = list(data_dicts[lables[0]].keys())


		values = [list(d.values()) for key, d in data_dicts.items()]

	else:
		print("Error plot_featurevector_list_bar_multi: wrong input")
		return

	bar_width = PLOT_PARAM_BAR_WIDTH / len(values)
	index = np.arange(len(values[0]))

	for i in range(len(data_dicts)):

		v = values[i]
		posis = [p + (bar_width*i) for p in range(len(v))]
		plot_bar(posis,
				 v,
				 bar_width,
				 color=i,
				 label=func_lable_to_text(lables[i])
				 )



	plot_setup_grid_lines()

	#Add Bar Lables below
	ax = plot_get_current_axis()
	ax.set_xticks(index + (bar_width*(len(values)-1)) / 2)
	ax.set_xticklabels([func_lable_to_text(l) for l in lables_group], rotation=90)

	#fix layout
	plot_get_current_figure().tight_layout()

	#plot_setup_legend_outside()


def plot_featureset_bar_avg(data_dicts):
	"""
	Plot avg of a Set of FeatureVector
	:param data_dicts: list of feature-vectors like [{tag1: value1, tag2: value2, ...}, {tag1: value1, tag2: value2, ...}, ...]
	"""

	dict_values = ArrayofDict_2_DictofArray(data_dicts)
	lables = list(dict_values.keys())
	values_mean = [mean(values) for key, values in dict_values.items()]

	x_pos = np.arange(len(lables))
	plot_bar(x_pos,
			 values_mean,
			 PLOT_PARAM_BAR_WIDTH,
			 )

	plot_setup_grid_lines()


	#Add Bar Lables below
	ax = plot_get_current_axis()
	ax.set_xticks(x_pos)
	ax.set_xticklabels([plot_getLabel_fromTag(l) for l in lables], rotation=90)

	#fix layout
	plot_get_current_figure().tight_layout()

def plot_featureset_bar_avg_yerr(data_dicts, func_error=get_yerr_MinMax, plot_values=False):
	"""
	Plot avg of a Set of FeatureVector
	:param data_dicts: list of feature-vectors like [{tag1: value1, tag2: value2, ...}, {tag1: value1, tag2: value2, ...}, ...]
	:param func_error: function to calculate error value from array like Variance etc
	"""

	dict_values = ArrayofDict_2_DictofArray(data_dicts)

	lables = list(dict_values.keys())

	values_list = [values for key, values in dict_values.items()]
	values_mean = [mean(values) for key, values in dict_values.items()]

	yerr_values = [func_error(values) for key, values in dict_values.items()]

	if isinstance(yerr_values[0], tuple) and len(yerr_values[0]) == 2:
		yerr_values = switchArrayDim(yerr_values)

	x_posis = np.arange(len(lables))
	plot_bar(x_posis,
			 values_mean,
			 PLOT_PARAM_BAR_WIDTH,
			 yerr=yerr_values
			 )
	if plot_values:
		for p, vs in zip(x_posis, values_list):
			plot_point([(p, sample_v) for sample_v in vs], color=COLOR_RED, marker="*")



	#Add Bar Lables below
	ax = plot_get_current_axis()
	ax.set_xticks(x_posis)
	ax.set_xticklabels([plot_getLabel_fromTag(l) for l in lables], rotation=90)

	#fix layout
	plot_get_current_figure().tight_layout()


def plot_grouped_featuresets_bar_avg(grouped_featuresets, func_lable_to_text=plot_getLabel_fromTag, yerr=None, plot_values=False):
	"""

	:param grouped_featuresets: dict of feature sets
	:return:
	"""

	groups = list(grouped_featuresets.keys())
	features = list(grouped_featuresets[groups[0]][0].keys())
	from FeatureSetsHelp import DictList_FuncAllValues
	all_values = []
	for group, featurelist in grouped_featuresets.items():
		v = []
		for feauture in features:
			v.append([f[feauture] for f in featurelist])
		all_values.append(v)
	values = [list(DictList_FuncAllValues(featurelist, func=arr_absmean).values()) for group, featurelist in grouped_featuresets.items()]
	if yerr != None:
		values_yerr = [list(DictList_FuncAllValues(featurelist, func=yerr).values()) for group, featurelist in grouped_featuresets.items()]

	bar_width = PLOT_PARAM_BAR_WIDTH / len(values)
	index = np.arange(len(values[0]))

	for i in range(len(grouped_featuresets)):

		v = values[i]
		allv = all_values[i]

		if yerr != None:
			yerr_values = values_yerr[i]
			if isinstance(yerr_values[0], tuple) and len(yerr_values[0]) == 2:
				yerr_values = switchArrayDim(yerr_values)
		else:
			yerr_values = None

		x_posis = [p + (bar_width*i) for p in range(len(v))]
		plot_bar(x_posis,
				 v,
				 bar_width,
				 #alpha=opacity,
				 color=i,
				 label=func_lable_to_text(groups[i]),
				 yerr=yerr_values
				 )

		if plot_values:
			for p, vs in zip(x_posis, allv):
				plot_point([(p, sample_v) for sample_v in vs], color=COLOR_RED, marker="*")



	plot_setup_grid_lines()

	#Add Bar Lables below
	ax = plot_get_current_axis()
	ax.set_xticks(index + (bar_width*(len(values)-1)) / 2)
	ax.set_xticklabels([func_lable_to_text(l) for l in features], rotation=90)

	#fix layout
	plot_get_current_figure().tight_layout()

	#plot_setup_legend_outside()


