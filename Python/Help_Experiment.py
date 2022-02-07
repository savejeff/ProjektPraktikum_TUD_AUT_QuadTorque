from Defines import *
from FileHelp import *
from PlotHelp import *

FILENAME_EXP_DATA_STATS = "Data_Stats.json"
FILENAME_EXP_DATA_LOOKUP = "Data_Lookup.pkl"
FILENAME_EXP_RESULTS = "Results.json"
FILENAME_EXP_RESULTS_TXT = "Results.txt"


def correct_filename(txt):
	return txt.replace("ä", "ae") \
		.replace("ö", "oe") \
		.replace("ü", "ue") \
		.replace("-", "_") \
		.replace("#", "_") \
		.replace(" ", "_")


def Exp_getPath(exp_name):
	path = path_join(PATH.DIR_EXPERIMENTS, exp_name)
	mkdir(path)
	return path

def Exp_plot_to_file(exp_name, plot_file_name):
	plot_file_name = correct_filename(plot_file_name)
	plot_tofile(path_join(Exp_getPath(exp_name), plot_file_name + ".png"))


	ax = plot_get_current_axis()
	title = ax.get_title()
	plot_setup_title("", "")
	plot_tofile(path_join(Exp_getPath(exp_name), plot_file_name + "_notitle.png"))
	plot_tofile(path_join(Exp_getPath(exp_name), plot_file_name + "_notitle_svg.svg"))
	plot_tofile(path_join(Exp_getPath(exp_name), plot_file_name + "_notitle.pdf"))
	plot_setup_title(title)


#plot_tofile(path_join(Exp_getPath(exp_name), plot_file_name + ".svg"))

def Exp_clear_plots(exp_name):
	for filename in get_files_in_Folder(Exp_getPath(exp_name), ".png", withpath=True):
		file_delete(filename)
	for filename in get_files_in_Folder(Exp_getPath(exp_name), ".svg", withpath=True):
		file_delete(filename)