from Help import *
from Defines import *

import matplotlib.pyplot as plt
import numpy as np
import matplotlib

if isLinux():
	import matplotlib
	matplotlib.use('tkagg')


KEY_UP = 'up'
KEY_DOWN = 'down'
KEY_LEFT = 'left'
KEY_RIGH = 'right'
KEY_ENTER = 'enter'
KEY_BACKSPACE = 'backspace'
KEY_SPACE = ' '
KEY_N = 'n'
KEY_B = 'b'
KEY_D = 'd'


FIGSIZE_HUGE = (13, 10)
FIGSIZE_BIG = (10, 8)
FIGSIZE_BIG_T = (9, 11)
FIGSIZE_BIG_W = (14, 8)
FIGSIZE_BIG_UW = (24, 8)
FIGSIZE_MED = (8, 6)
FIGSIZE_MED_W = (12, 6)
FIGSIZE_MED_T = (7, 10)
FIGSIZE_SMALL = (6, 5)
FIGSIZE_SMALL_T = (5, 6)
FIGSIZE_SMALL_W = (8, 5)

FIGSIZE = FIGSIZE_MED

LABLE_FONTSIZE = 14

# https://matplotlib.org/stable/gallery/color/named_colors.html
COLOR_BLACK = 'k'
COLOR_YELLOW = 'y'
COLOR_GREEN = 'tab:green'
COLOR_LIME = 'lime'
COLOR_BLUE = 'tab:blue'
COLOR_BLUE2 = 'blue'
COLOR_ORANGE = 'tab:orange'
COLOR_ORANGE2 = 'orangered'
COLOR_RED = 'tab:red'
COLOR_PURPLE = 'tab:purple'
COLOR_BROWN = 'tab:brown'
COLOR_GOLD = 'gold'
COLOR_PINK = 'tab:pink'
COLOR_GRAY = 'tab:gray'
COLOR_DARK_GRAY = 'dimgray'
COLOR_OLIVE = 'tab:olive'
COLOR_CYAN = 'tab:cyan'
COLOR_MAGENTA = 'fuchsia'
COLOR_WHITE = 'w'


COLOR_PALETTE_1 = [
	COLOR_BLUE,
	COLOR_GREEN,
	COLOR_PURPLE,
	COLOR_BROWN,
	COLOR_ORANGE,
	COLOR_RED,
	COLOR_CYAN,
	COLOR_PINK,
	COLOR_GRAY,
	COLOR_OLIVE,
]

COLOR_PALETTE_2 = [
	COLOR_CYAN,
	COLOR_ORANGE2,
	COLOR_LIME,
	COLOR_PINK,
	COLOR_GOLD,
	COLOR_MAGENTA,
	COLOR_PINK,
	COLOR_PURPLE,
	COLOR_GRAY,
	COLOR_OLIVE,
]

COLOR_PALETTE_3 = [
	COLOR_LIME,
	COLOR_CYAN,
	COLOR_ORANGE,
	COLOR_GOLD,
	COLOR_ORANGE2,
	COLOR_MAGENTA,
	COLOR_PURPLE,
	COLOR_GRAY,
	COLOR_OLIVE,
]
COLOR_PALETTE_DEFAULT = COLOR_PALETTE_1

LEGENT_LOC_BEST = 'best'
LEGEND_LOC_TOP_RIGHT = 'upper right'
LEGEND_LOC_TOP_LEFT = 'upper left'
LEGEND_LOC_BOTTOM_LEFT = 'lower left'
LEGEND_LOC_BOTTOM_RIGHT = 'lower right'
LEGEND_LOC_RIGHT = 'right'
LEGENT_LOC_CENTER_LEFT = 'center left'
LEGENT_LOC_CENTER_RIGHT ='center right'
LEGENT_LOC_BOTTOM_CENTER ='lower center'
LEGENT_LOC_TOP_CENTER = 'upper center'
LEGENT_LOC_CENTER = 'center'


# https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html
LINESTYLE_SOLID = 'solid' # Same as (0, ()) or '-'
LINESTYLE_DOTTED = 'dotted' # Same as (0, (1, 1)) or '.'
LINESTYLE_DASHED = 'dashed' # Same as '--'
LINESTYLE_DASHDOT = 'dashdot' # Same as '-.'
LINESTYLE_LOOSELY_DOTTED = (0, (1, 10))
#LINESTYLE_DOTTED = (0, (1, 1))
LINESTYLE_DENSELY_DOTTED = (0, (1, 1))
LINESTYLE_LOOSELY_DASHED = (0, (5, 10))
#LINESTYLE_DASHED = (0, (5, 5))
LINESTYLE_DENSELY_DASHED = (0, (5, 1))
LINESTYLE_LOOSELY_DASHDOTTED = (0, (3, 10, 1, 10))
LINESTYLE_DASHDOTTED = (0, (3, 5, 1, 5))
LINESTYLE_DENSELY_DASHDOTTED = (0, (3, 1, 1, 1))
LINESTYLE_DASHDOTDOTTED = (0, (3, 5, 1, 5, 1, 5))
LINESTYLE_LOOSELY_DASHDOTDOTTED = (0, (3, 10, 1, 10, 1, 10))
LINESTYLE_DENSELY_DASHDOTDOTTED = (0, (3, 1, 1, 1, 1, 1))

LINESTYLE_PALETTE = [
	LINESTYLE_SOLID,
	LINESTYLE_DASHED,
	LINESTYLE_DOTTED,
	LINESTYLE_DASHDOT,
	LINESTYLE_LOOSELY_DOTTED,
	LINESTYLE_DENSELY_DOTTED,
	LINESTYLE_LOOSELY_DASHED,
	LINESTYLE_DENSELY_DASHED,
	LINESTYLE_LOOSELY_DASHDOTTED,
	LINESTYLE_DASHDOTTED,
	LINESTYLE_DENSELY_DASHDOTTED,
	LINESTYLE_DASHDOTDOTTED,
	LINESTYLE_LOOSELY_DASHDOTDOTTED,
	LINESTYLE_DENSELY_DASHDOTDOTTED,
]


def _get_color(color):
	if isinstance(color, int):
		return COLOR_PALETTE_DEFAULT[color % len(COLOR_PALETTE_DEFAULT)]
	else:
		return color

def _get_linestyle(linestyle):
	if isinstance(linestyle, int):
		return LINESTYLE_PALETTE[linestyle % len(LINESTYLE_PALETTE)]
	else:
		return linestyle



def plot_get_current_figure():
	return plt.gcf()

def plot_get_current_axis():
	return plt.gca()


###########################
#      Plot Setup         #
###########################
FONT_TIME_NEW_ROMAN = "Times New Roman"
PLOT_FONT = FONT_TIME_NEW_ROMAN

def plot_setup(title="", ylable="", xlable="", scale="", figsize=FIGSIZE):
	if figsize != None:
		plt.figure(figsize=figsize)


	plt.rcParams["font.family"] = PLOT_FONT

	if (len(title) > 0):
		#matplotlib.rc('font', family='Arial')
		plt.title(title)

	plt.xlabel(xlable, fontsize=LABLE_FONTSIZE)#, fontname=PLOT_FONT)
	plt.ylabel(ylable, fontsize=LABLE_FONTSIZE)#, fontname=PLOT_FONT)

	if (len(scale) > 0):
		plt.yscale(scale)

def plot_setup_legend(location=LEGENT_LOC_BEST):
	plt.legend(loc=location, shadow=True, fontsize='medium')

def plot_setup_legend_list(itemlist, title=None):
	from matplotlib.lines import Line2D
	plt.legend(
		[Line2D([0], [0], color=COLOR_BLACK, lw=1) for i in itemlist],
		itemlist,
		title=title,
		markerfirst=False, handlelength=0.0,
	)

def plot_setup_hide_x_axis_lables():
	plt.tick_params(
		axis='x',          # changes apply to the x-axis
		which='both',      # both major and minor ticks are affected
		bottom=False,      # ticks along the bottom edge are off
		top=False,         # ticks along the top edge are off
		labelbottom=False) # labels along the bottom edge are off
	plot_get_current_figure().tight_layout()

def plot_setup_hide_y_axis_lables():
	plt.tick_params(
		axis='y',          # changes apply to the y-axis
		which='both',      # both major and minor ticks are affected
		bottom=False,      # ticks along the bottom edge are off
		top=False,         # ticks along the top edge are off
		labelbottom=False) # labels along the bottom edge are off
	plot_get_current_figure().tight_layout()

def plot_setup_legend_outside():
	# Shrink current axis by 20%
	ax = plot_get_current_axis()
	box = ax.get_position()
	ax.set_position([box.x0, box.y0, box.width * 0.70, box.height])

	ax.legend(bbox_to_anchor=(1, 0.4))


def plot_setup_position(pos):
	x, y = pos
	if isWindows():
		thismanager = plt.get_current_fig_manager()
		thismanager.window.wm_geometry("+{}+{}".format(x, y))

def plot_setup_axis_equal():
	plt.axis('equal')

PLOT_SCALE_LINEAR = "linear"
PLOT_SCALE_LOG = "log"
PLOT_SCALE_SYMLOG = "symlog"
PLOT_SCALE_LOGIT = "logit"

def plot_setup_scale(xscale=PLOT_SCALE_LINEAR, yscale=PLOT_SCALE_LINEAR):
	plt.xscale(xscale)
	plt.yscale(yscale)

def plot_setup_view(xlim=None, ylim=None):
	"""
	Set Displayed area in plot
	:param xlim: (xlim_min, xlim_max)
	:param ylim: (ylim_min, ylim_max)
	"""
	if xlim != None:
		plt.xlim(xlim)

	if ylim != None:
		plt.ylim(ylim)

def plot_setup_grid(enable=True):
	#plt.rcParams['axes.facecolor'] = 'white'
	#plt.rcParams['axes.edgecolor'] = 'white'
	#plt.rcParams['axes.grid'] = True
	#plt.rcParams['grid.alpha'] = 1
	#plt.rcParams['grid.color'] = "#cccccc"
	#If grid is not showing even after changing these parameters then use
	plt.grid(enable, linestyle='dashed')
	#plt.grid(True, which="minor", color='gray', linestyle='dashed')
	#plt.grid(True, which="major", color='gray', linestyle='dashed')


def plot_setup_grid_lines():
	ax = plot_get_current_axis()

	#Grid Lines
	ax.yaxis.grid(color='gray', linestyle='dashed')
	ax.set_axisbelow(True)

def plot_setup_axis_ticks(steps_x = None, steps_y= None):
	ax = plt.gca()
	if (steps_x):
		start, end = ax.get_xlim()
		ax.xaxis.set_ticks(np.arange(int(start), int(end), steps_x))

	if (steps_y):
		start, end = ax.get_ylim()
		ax.yaxis.set_ticks(np.arange(int(start), int(end), steps_y))

def plot_setup_title(title, subtitle=None):
	if subtitle == None:
		plt.title(title)
	else:
		plt.suptitle(title)
		plt.title(subtitle)



def plot_setup_window_title(text, fig=None):
	if not fig:
		fig = plot_get_current_figure()
	fig.canvas.set_window_title(text)


def plot_setup_notoolbar():
	""" must be called before figure is created """
	plt.rcParams['toolbar'] = 'None'

def plot_setup_fullscreen():
	""" must be called after figure was created before plt.show """
	mng = plt.get_current_fig_manager()
	mng.window.state('zoomed')


###########################
#    Plot Show / Close    #
###########################


def plot_close(fig=None):
	if fig == None:
		fig = 'all'
	plt.close(fig)



def plot_show(block=True):
	#plot_get_current_figure().tight_layout()
	plt.show(block=block)


def plot_tofile(path):
	print("save plot to {}".format(path))
	plt.savefig(path,
				dpi=200,
				transparent=True
				)
	#plt.savefig(tofile + ".svg", format="svg")

	#plt.close()

def plot_show_onClick(fig=None):
	"""
	Shows the setup-ed plot and exits on a Mouse Click
	returns location clicked in figure
	:param fig:
	:return: (x, y) as float (if img = pixel, plot = coordinate/datapoint)
	"""

	#https://matplotlib.org/3.1.1/users/event_handling.html9

	if not fig:
		fig = plot_get_current_figure()

	global ix, iy
	ix, iy = None, None
	def onclick(event):


		global ix, iy
		ix, iy = event.xdata, event.ydata
		if ix == None or iy == None:
			pass
		else:
			print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
				  ('double' if event.dblclick else 'single', event.button,
				   event.x, event.y, event.xdata, event.ydata))

			#ix, iy = int(ix), int(iy)
		print('x, y = {}, {}'.format(ix, iy))

		fig.canvas.mpl_disconnect(cid)

		plt.close(fig)

	cid = fig.canvas.mpl_connect('button_press_event', onclick)
	plt.show()
	if ix != None and iy != None:
		return (ix, iy)
	return None


def plot_setup_close_onKeyPress(fig=None, keys_only=[KEY_ENTER]):
	if not fig:
		fig = plot_get_current_figure()
	def onKey(event):

		key_pressed = event.key
		#print("key_pressed = '{}'".format(key_pressed))
		if key_pressed in keys_only:
			plt.close(fig)

	fig.canvas.mpl_connect("key_press_event", onKey)


def plot_show_onKeyPressed(keys_only=[KEY_ENTER], fig=None):

	if fig == None:
		fig = plot_get_current_figure()

	global key_pressed
	key_pressed = None
	def onKey(event):
		global key_pressed
		key_pressed = event.key
		#print("key_pressed = '{}'".format(key_pressed))
		if not keys_only or key_pressed in keys_only:
			plt.close(fig)

	fig.canvas.mpl_connect("key_press_event", onKey)

	plt.show()
	return key_pressed


def plot_xy_errorbars(valuesXY, error_bars):
	"""
	https://problemsolvingwithpython.com/06-Plotting-with-Matplotlib/06.07-Error-Bars/
	https://matplotlib.org/1.2.1/examples/pylab_examples/errorbar_demo.html
	:param valuesXY:
	:param error_bars:
	:return:
	"""

	#TODO implement

####################################
#      plot Functions              #
####################################


def plot_text(text, posi=(0, 0)):

	plt.text(0, 0, s=text)



def plot_y(Y, label=None, marker=None, color=None, linestyle=None):
	"""
	Plots a single array of values or a list of values
	"""

	if isinstance(Y[0], list): # if list of traces given
		for i, y in enumerate(Y):
			plot_y(y, label[i] if label else None, marker)
		return


	plt.plot(Y, label=label, marker=marker, color=_get_color(color), linestyle=_get_linestyle(linestyle))

def plot_xy(XY, label="", marker="", color=None, linestyle=None):
	"""
	Plots a trace that is a points list (x, y)
	:param XY: points list like [(x1, y1), (x2, y2) ...]
	"""

	from Help import switchArrayDim
	X, Y = switchArrayDim(XY) #convert from [(x1, y1), (x2, y2) ...] -> [x1, x2, ...], [y1, y2, ...]
	plot_x_y(X, Y, label, marker, color, linestyle)

def plot_x_y(X, Y, label="", marker="", color=None, linestyle=None):
	"""
	Plots a trace with X and Y as array
	:param X: [x1, x2, ...]
	:param Y: [y1, y2, ...]
	"""
	plt.plot(X, Y, label=label, marker=marker, color=_get_color(color), linestyle=_get_linestyle(linestyle))



def PlotY_dict(Y, scale="", tofile="", title="", block=True, ylable="", xlable="", marker="", xtickssteps=None, exclude_tags=[]):
	Y_arr = [Y[t] for t in Y if t not in exclude_tags]
	labels = [t for t in Y]
	PlotY(Y_arr, scale, tofile, title, labels, block, ylable, xlable, marker, xtickssteps)


def plot_y_dict(data_dict, only_keys=[], marker=None):
	"""
	DataDict : dict of {tracename->Arrays}
	example Y = {'test':[1,2,3,4], 'val':[0, 1, 2, 3]}
	:param data_dict:
	:param only_keys:
	:param marker:
	:return:
	"""
	Y_arr = [data_dict[key] for key in data_dict if not only_keys or key in only_keys]
	labels = list(data_dict.keys())

	plot_y(Y_arr, label=labels, marker=marker)


def plot_xy_dict(data_dict, key_x, only_keys=[], marker=None):
	"""
	DataDict : dict of {tracename->Arrays}
	example:
	 data_dict = {'time':[1, 2, 3, 4], 'val':[1.0, 1.5, 2.0, 2.5]}
	 key_x = 'time'
	:param data_dict:
	:param key_x:
	:param only_keys:
	:param marker:
	:return:
	"""
	Y_arr = [data_dict[key] for key in data_dict if not key == key_x and (not only_keys or key in only_keys)]
	x = data_dict[key_x]
	labels = list(data_dict.keys())

	for i, y in enumerate(Y_arr):
		plot_x_y(x, y, label=labels[i] if labels else None, marker=marker)



#example: plot_point( (1,1) )
#example: plot_point( [ (1,1), (2,1), (1, 2), (2,2) ] )
#example: plot_point( [(1,2,3,4,5),(1,2,4,8,16) ] )
def plot_point(point, color=None, label=None, marker='o', markersize=None):
	"""
	Plots point on Plot.
	:param point: (x, y) or list of points
	"""

	from Help import switchArrayDim
	if isinstance(point, list):

		#[plot_point(p) for p in point]

		assert all([len(p) == 2 for p in point])

		pointX, pointY = switchArrayDim(point)
		plt.plot(pointX, pointY, marker, color=_get_color(color), label=label, markersize=markersize)

	else:
		x, y = point
		plt.plot(x, y, marker, color=_get_color(color), label=label, markersize=markersize)


def plot_circle(pos, radius, color=None):
	circle2 = plt.Circle(pos, radius, color=_get_color(color), fill=False)
	ax = plt.gca()
	ax.add_patch(circle2)

def plot_bar(posis, values, bar_width=None, color=None, label=None, yerr=None):
	plt.bar(posis,
			values,
			bar_width,
			color=_get_color(color),
			label=label,
			yerr=yerr,
			align='center', ecolor='black', capsize=10
			)

def plot_errobar(posis, values, bar_width=None, color=None, label=None, yerr=None):
	# https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/errorbar_limits_simple.html#sphx-glr-gallery-lines-bars-and-markers-errorbar-limits-simple-py

	# TODO implement
	#plt.errorbar(x, y + 3, yerr=yerr, label='both limits (default)')
	pass


def plot_box(data_dict):
	"""

	:param data_dict: dict of value-list
	"""
	values = list(data_dict.values())
	lables = list(data_dict.keys())
	plt.boxplot(values, labels=lables)
	#ax.set_xticklabels(labels=labels, rotation=90)
	if len(lables) > 3:
		plot_get_current_axis().set_xticklabels(labels=lables, rotation=90)
	plot_setup_grid_lines()


def plot_box_xy(data_dict):
	"""
	:param data_dict: dict of {x -> sample-list}
	example:
	{
		0.1 : { 10.1, 9.0, 9.5, ... },
		0.2 : { 20.0, 21.4, 15.1, ... },
		...
	}
	"""

	values_y = list(data_dict.values())
	values_x = list(data_dict.keys())
	plt.boxplot(values_y, positions=values_x,
				widths=(0.5 * (max(values_x) - min(values_x)) / len(values_x)),
				manage_ticks = False
				)
	#ax.set_xticklabels(labels=labels, rotation=90)
	#if len(lables) > 3:
	#	plot_get_current_axis().set_xticklabels(labels=lables, rotation=90)
	#plot_setup_grid_lines()


def plot_regression_linear(x : list , y : list, color=COLOR_RED, label=None):
	"""
	Plot a Linear Regression line matching the given x and y values
	:param x: list of x values
	:param y: list of y values
	"""

	from StatisticHelp import regression_linear
	m, b = regression_linear(x, y)

	x_min, x_max = min(x), max(x)
	p_min = x_min, m * x_min + b
	p_max = x_max, m * x_max + b

	plot_xy([p_min, p_max], color=color, label=label)

###########################
#      Plot3D Functions   #
###########################


def plot3d_setup(title="", xlable="", ylable="", zlable="", figsize=FIGSIZE):
	fig = plt.figure(figsize=figsize)
	ax = fig.add_subplot(111, projection='3d')

	if (len(title) > 0):
		#matplotlib.rc('font', family='Arial')
		plt.title(title)

	plt.xlabel(xlable, fontsize=LABLE_FONTSIZE)
	plt.ylabel(ylable, fontsize=LABLE_FONTSIZE)
	ax.set_zlabel(zlable, fontsize=LABLE_FONTSIZE)


def plot3D_x_y_z(tracex, tracey, tracez, label="", marker=None, color=None):
	"""
	Plot a Trace in 3D space
	:param tracex: list of x values
	:param tracey: list of y values
	:param tracez: list of z values
	"""

	ax = plot_get_current_axis()
	ax.plot3D(tracex, tracey, tracez,
			  label=label,
			  marker=marker,
			  color=_get_color(color)
			  )

#####################################
#       Complete Plot Functions     #
#####################################


def Plot_X_Y(Values, scale="", tofile="", title="", ylable="", xlable="", labels=[], block=True, marker=".", color="k"):
	"""
	Displays an X over Y plot
	Values : array of traces
		trace: [array of X, array Y] -> [[X0, X1, ...], [Y0, Y1, ...]]
	"""

	plot_setup(title, ylable, xlable, scale)

	#plot values
	for i in range(len(Values)):

		#select color
		c = "k"
		if isinstance(color, str):
			c = color
		elif isinstance(color, list):
			if i in range(len(color)):
				color = color[i]

		plt.plot(
			Values[i][0],
			Values[i][1],
			c
		)

	for i in range(len(Values)):
		from Help import switchArrayDim
		values = switchArrayDim(Values[i])
		if(len(labels) == len(Values)):
			plt.plot(values[0], values[1], label=labels[i], marker=marker)
		else:
			plt.plot(values[0], values[1])#, "ro", marker=marker, markersize=15)

	if (len(labels) == len(Values)):
		plt.legend(loc='upper center', shadow=True, fontsize='medium')

	plot_show(block)


def PlotXY(Values, scale="", tofile="", title="", labels=[], block=True, ylable="", xlable="", marker=None):
	"""
	Displays an X over Y plot
	:param Values : array of [X, Y] -> [[X0, Y0], [X1, Y1] ... ]
	:param marker: None for line, '.' for points, '*' for stars
	"""

	plot_setup(title, ylable, xlable, scale)

	if not isinstance(Values[0][0], list):
		Values = [Values]

	#plot values
	for i in range(len(Values)):
		from Help import switchArrayDim
		values = switchArrayDim(Values[i])
		if(len(labels) == len(Values)):
			plt.plot(values[0], values[1], label=labels[i], marker=marker)
		else:
			plt.plot(values[0], values[1], marker=marker)#, "ro", , markersize=15)

	if (len(labels) == len(Values)):
		plt.legend(loc='best', shadow=True, fontsize='medium')

	plot_show(block)


#Y : array of traces
def PlotY(Y, scale="", tofile="", title="", labels=[], block=True, ylable="", xlable="", marker="", xtickssteps=None):
	import matplotlib.pyplot as plt

	#plt.figure(figsize=(10, 8))
	#fig, ax = plt.subplots(figsize=(10, 8))
	fig, ax = plt.subplots(figsize=FIGSIZE)

	if(len(title) > 0):
		plt.title(title, fontsize=LABLE_FONTSIZE)

	plt.xlabel(xlable, fontsize=LABLE_FONTSIZE)
	plt.ylabel(ylable, fontsize=LABLE_FONTSIZE)

	if(len(scale) > 0):
		plt.yscale(scale)
	if not isinstance(Y[0], list):
		Y = [Y]
	for i in range(len(Y)):
		if(len(labels) == len(Y)):
			plt.plot(Y[i], label=labels[i], marker=marker)
		else:
			plt.plot(Y[i], marker=marker)

	# Grid Lines
	ax.yaxis.grid(color='gray', linestyle='dashed')
	ax.set_axisbelow(True)

	#integer steps
	#from matplotlib.ticker import MaxNLocator
	#ax.xaxis.set_major_locator(MaxNLocator(integer=True))

	if (xtickssteps):
		start, end = ax.get_xlim()
		ax.xaxis.set_ticks(np.arange(int(start), int(end), xtickssteps))

	if (len(labels) == len(Y)):
		plt.legend(loc='upper center', shadow=True, fontsize='medium')

	plot_show(block)

def Plot(traces):
	import matplotlib.pyplot as plt
	for trace in traces:
		plt.plot(trace[0], trace[1])
	plt.show()


#Y : dict of {tracename->Arrays}
#example Y = {'test':[1,2,3,4], 'val':[0, 1, 2, 3]}
def PlotY_dict(Y, scale="", tofile="", title="", block=True, ylable="", xlable="", marker="", xtickssteps=None, exclude_tags=[]):
	Y_arr = [Y[t] for t in Y if t not in exclude_tags]
	labels = [t for t in Y]
	PlotY(Y_arr, scale, tofile, title, labels, block, ylable, xlable, marker, xtickssteps)



def Plot_bar_dict(dic, title="", ylable="", sort=False, tofile="", block=True, ylim=None, key_to_text=None):
	lables = list(dic.keys())
	if(key_to_text):
		lables = [key_to_text(l) for l in lables]
	Plot_bar(list(dic.values()), lables,
			 title=title, y_lable=ylable, sort=sort, tofile=tofile, block=block, ylim=ylim)

def Plot_bar(values, labels=[], title="", y_lable="", sort=False, tofile="", block=True, ylim=None):
	"""
	:param values: like {tag1: value1, tag2: value2, ...}
	:param labels:
	:param title:
	:param y_lable:
	:param sort:
	:param tofile:
	:param block:
	:param ylim:
	:return:
	"""
	from Help import switchArrayDim

	#fig, ax = plt.subplots(figsize=(10, 8))
	fig, ax = plt.subplots(figsize=FIGSIZE)
	ind = np.arange(1, len(values) + 1)

	if(sort):
		lval = []
		if (len(values) == len(labels)):
			for i in range(len(values)):
				lval.append([values[i], labels[i]])
			lval = sorted(lval, key=lambda x: x[0])
			lval = switchArrayDim(lval)
			values = lval[0]
			labels = lval[1]
		else:
			values = sorted(values)


	#https://matplotlib.org/tutorials/colors/colormaps.html
	cmap = matplotlib.cm.get_cmap('winter')

	#Plot bars
	bars = plt.bar(ind, values)

	# Grid Lines
	ax.yaxis.grid(color='gray', linestyle='dashed')
	ax.set_axisbelow(True)

	ax.set_xticks(ind)
	if(ylim):
		ax.set_ylim([0, ylim])
	for i in range(len(bars)):
		#colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
		#bars[i].set_facecolor(colors[i % len(colors)])
		#bars[i].set_facecolor(cmap(float(i)/len(bars)))
		delta = max(values) - min(values)
		if(delta == 0):
			faktor = 0.5
		else:
			faktor = (values[i] - min(values)) / delta
		color = cmap(1 - faktor)
		bars[i].set_facecolor(color)

	#plt.legend((p1[0], p2[0]), ('Men', 'Women'))

	#x Lables
	if (len(labels) == len(values)):
		ax.set_xticklabels(labels=labels, rotation=90)

	#Set Y Limits
	#ax.set_ylim([0, 100])

	ax.set_ylabel(y_lable)
	ax.set_title(title)

	# show the figure, but do not block
	fig.tight_layout()

	plot_show(block)


#dict: {L:[L:V, L:V, L:V], L:[L:V, L:V, L:V]
def Plot_multi_bars_dict(dic, title="", tofile="", ylim=None, onlykeys=[], key_to_text=None, ylable=""):
	grouplables = list(dic.keys())
	lables = list(dic[grouplables[0]].keys())
	lables = [k for k in lables if (
			len(onlykeys) == 0 or k in onlykeys
	)]
	if(key_to_text):
		lables = [key_to_text(k) for k in lables]

	values = []
	for gl in grouplables:
		values.append([dic[gl][k] for k in dic[gl] if (
				len(onlykeys) == 0 or k in onlykeys
		)])
	Plot_multi_bars(values, lables, grouplables, title=title, tofile=tofile, ylim=ylim, ylable=ylable)
	Plot_bars_error(values, lables, grouplables, title=title, tofile=tofile + "_yerr", ylim=ylim, ylable=ylable)


#values: [[X, X, X], [X, X, X]]
#lables: [L, L, L]
#grouplables:[L, L]
def Plot_multi_bars(values, lables, grouplables, ylable="", title="", tofile="", block=True, ylim=None):

	n_groups = len(values[0])

	fig, ax = plt.subplots(figsize=FIGSIZE)

	index = np.arange(n_groups)
	bar_width = 0.70 / len(values)

	bars = []
	for i in range(len(values)):
		bars.append(ax.bar(index + (bar_width*i), values[i], bar_width,
						   #alpha=opacity,
						   # #color='b',
						   label=grouplables[i]))

	#Grid Lines
	ax.yaxis.grid(color='gray', linestyle='dashed')
	ax.set_axisbelow(True)

	#ax.set_xlabel('Group')
	ax.set_ylabel(ylable, fontsize=LABLE_FONTSIZE)
	ax.set_title(title, fontsize=LABLE_FONTSIZE)
	ax.set_xticks(index + (bar_width*(len(values)-1)) / 2)
	ax.set_xticklabels(lables, rotation=90)
	if (ylim):
		ax.set_ylim([0, ylim])

	fig.tight_layout()

	# Shrink current axis by 20%
	box = ax.get_position()
	ax.set_position([box.x0, box.y0, box.width * 0.70, box.height])
	ax.legend(bbox_to_anchor=(1, 0.4))

	plot_show(block)

#values: [[X, X, X], [X, X, X]]
#lables: [L, L, L]
#grouplables:[L, L]
def Plot_bars_error(values, lables, grouplables, ylable="", title="", tofile="", block=True, ylim=None):
	from StatisticHelp import mean, getStandardDeviation
	from Help import switchArrayDim
	n_groups = len(values[0])

	fig, ax = plt.subplots(figsize=FIGSIZE)

	index = np.arange(n_groups)
	bar_width = 0.70

	bar_values = switchArrayDim(values)
	yerr_values = [getStandardDeviation(values) for values in bar_values]
	bar_values = [mean(v) for v in bar_values]

	ax.bar(index, bar_values, bar_width, yerr=yerr_values)
	"""
	bars = []
	for i in range(len(values)):
		bars.append(ax.bar(index + (bar_width*i), values[i], bar_width,
					#alpha=opacity,
					# #color='b',
					label=grouplables[i]))
	"""
	#Grid Lines
	ax.yaxis.grid(color='gray', linestyle='dashed')
	ax.set_axisbelow(True)

	#ax.set_xlabel('Group')
	ax.set_ylabel(ylable)
	ax.set_title(title)
	ax.set_xticks(index)
	ax.set_xticklabels(lables, rotation=90)
	if (ylim):
		ax.set_ylim([0, ylim])
	fig.tight_layout()

	# Shrink current axis by 20%
	box = ax.get_position()
	ax.set_position([box.x0, box.y0, box.width * 0.75, box.height])
	ax.legend(bbox_to_anchor=(1, 0.5))

	plot_show(block)


#example: plot_points([[1,1], [2,1], [1, 2], [2,2]], title="Random")
#example: plot_points([[1,2,3,4,5],[1,2,4,8,16]], title="Random")
def Plot_points(points, title=""):
	fig, ax = plt.subplots()
	from Help import switchArrayDim
	if len(points) > 0 and all([len(p) == 2 for p in points]):
		points =  switchArrayDim(points)
	ax.Plot(points[0], points[1], 'o')

	ax.set_title(title)
	plt.show()


def Plot_box(Values, tofile="", title="", block=True, ylable="", xlable=""):
	fig1, ax = plt.subplots()
	ax.set_title(title, fontsize=LABLE_FONTSIZE)
	dic = {}
	for v in Values:
		if(v[0] in dic):
			dic[v[0]].append(v[1])
		else:
			dic[v[0]] = [v[1]]

	maxkey = max(list(dic.keys()))
	Values = list(range(maxkey))

	for i in range(maxkey):
		if(i + 1 in dic):
			Values[i] = dic[i + 1]
		else:
			Values[i] = []


	ax.boxplot(Values)
	ax.set_ylabel(ylable, fontsize=LABLE_FONTSIZE)
	ax.set_xlabel(xlable, fontsize=LABLE_FONTSIZE)

	plot_show(block)


def PlotY_error(values, Yerr, title="", tofile="", block=True, ylable="", xlable=""):
	fig, ax = plt.subplots()
	ax.errorbar(list(range(len(values))), values, yerr=Yerr)
	ax.set_title(title, fontsize=LABLE_FONTSIZE)

	plt.xlabel(xlable, fontsize=LABLE_FONTSIZE)
	plt.ylabel(ylable, fontsize=LABLE_FONTSIZE)

	plot_show(block)

if __name__ == '__main__':
	#plotXY([[[1,1], [2,4], [3,9], [4,16], [5,25]]])


	"""
	plot_multi_bars([[1, 2, 3], [3, 2, 1], [2, 2, 2]], ["A", "B", "C"], ["G1", "G2", "G3"])
	#plot_multi_bars([[1, 2, 3], [3, 2, 1]], ["A", "B", "C"], ["G1", "G2"])
	exit()

	# Fixing random state for reproducibility
	np.random.seed(19680801)
	"""
	# fake up some data
	#spread = np.random.rand(50) * 100
	#center = np.ones(25) * 50
	#flier_high = np.random.rand(10) * 100 + 100
	#flier_low = np.random.rand(10) * -100
	#data = np.concatenate((spread, center, flier_high, flier_low), 0)
	#plot_box([[1,2,3,4,5,6]], tofile="test")

	"""
	DataDict = [i ** 2 for i in range(10)]
	labels = ["Test"]
	xlable = "time"
	ylable = "output"
	title = "Some Data"
	marker = "*"

	textstr = "Haasvsfgs\nasfgsdf\nasfdasdf"

	scale = []

	xtickssteps = None

	import matplotlib.pyplot as plt

	# plt.figure(figsize=(10, 8))
	# fig, ax = plt.subplots(figsize=(10, 8))
	fig, ax = plt.subplots(figsize=FIGSIZE)

	if (len(title) > 0):
		plt.title(title, fontsize=LABLE_FONTSIZE)

	plt.xlabel(xlable, fontsize=LABLE_FONTSIZE)
	plt.ylabel(ylable, fontsize=LABLE_FONTSIZE)

	if (len(scale) > 0):
		plt.yscale(scale)

	for i in range(len(DataDict)):
		if (len(labels) == len(DataDict)):
			plt.plot(i, DataDict[i], label=labels[i], marker=marker)
		else:
			plt.plot(i, DataDict[i], marker=marker)

	# Grid Lines
	ax.yaxis.grid(color='gray', linestyle='dashed')
	ax.set_axisbelow(True)

	# integer steps
	# from matplotlib.ticker import MaxNLocator
	# ax.xaxis.set_major_locator(MaxNLocator(integer=True))

	if (xtickssteps):
		start, end = ax.get_xlim()
		ax.xaxis.set_ticks(np.arange(int(start), int(end), xtickssteps))

	if (len(labels) == len(DataDict)):
		plt.legend(loc='upper center', shadow=True, fontsize='medium')

	props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

	ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
			verticalalignment='top', bbox=props)

	plot_show()
	"""
	pass



