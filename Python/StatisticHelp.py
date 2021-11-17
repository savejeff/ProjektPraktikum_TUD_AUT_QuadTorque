from Help import *
from HelpMath import *


#import numpy
#import statistics
#from scipy import array


from scipy import stats

import numpy as np
import statistics as st

from numpy import pi
from statistics import median, median_low


def arr_abs(arr):
	return [abs(i) for i in arr]

def arr_absmean(arr):
	"""
	Calculates avg absolute value (usefull as loss func)
	:param arr:
	:return:
	"""
	return sum(arr_abs(arr)) / len(arr)

def sqrmean(arr):
	"""
	Calculates avg quadratic value (usefull as loss func)
	:param arr:
	:return:
	"""
	arr = np.array(arr)
	return (arr**2).sum() / len(arr)

def getSpannweite(arr):
	return max(arr) - min(arr)

def getStandardDeviation(arr):
	#from scipy import array
	#return array(arr).std()

	#return st.pstdev(arr)
	return np.std(arr)

def getVarianz(arr):
	#from scipy import array
	#return array(arr).var()
	import statistics as st
	return st.variance(arr)


def derivative(time, values):
	""" derives (time, values) and returns array of same length """
	from numpy import diff
	from HelpMath import isNaN
	values = [v if v else 0 for v in values]
	return [0] + [(x if not isNaN(x) else 0) for x in (list(diff(values) / diff(time)))]

def diff(values):
	return [0] + [values[i + 1] - values[i] if (isValidNum(values[i]) and isValidNum(values[i + 1])) else nan for i in range(len(values) - 1)]

def sum_integrate(values, start_value=0):
	# import scipy.integrate as integrate
	# return integrate.trapz(values, time)
	result = np.array(values)
	acc = start_value
	for i in range(len(values)):
		acc += values[i]
		result[i] = acc

	return result


def sum_integrate_fuse(values, fuse, alpha, start_value=0):
	# import scipy.integrate as integrate
	# return integrate.trapz(values, time)
	result = np.array(values)
	acc = start_value
	for i in range(len(values)):
		acc += values[i]
		acc = fuse[i] * (alpha) + (1 - (alpha)) * acc
		result[i] = acc

	return result


def integrate(time, values, start_value=0):
	#import scipy.integrate as integrate
	#return integrate.trapz(values, time)
	result = np.array(values)
	acc = start_value
	for i in range(len(time)):
		if(i == 0):
			result[i] = 0
			continue

		dt = time[i] - time[i - 1]
		dy = (values[i] + values[i - 1]) / 2
		acc += dt * dy
		result[i] = acc

	return result

def integrate_fuse(time, values, fuse, alpha, start_value=0):
	"""
	Integrates (time, values) but uses fuse values and alpha as leading trace
	:param time: time graph
	:param values: graph to integrate
	:param fuse:  guiding function: can be constant or array of same length as values
	:param alpha: fuse alpha. higher alphas increase influence of fuse
	:return: array that was integrated
	"""
	def getFuseValue(i):
		return fuse[i] if (isinstance(fuse, list) or isinstance(fuse, np.ndarray)) else fuse
	from HelpMath import isNaN

	result = np.array(values)
	acc = start_value
	for i in range(len(time)):

		if i != 0:

			dt = time[i] - time[i - 1]
			dy = (values[i] + values[i - 1]) / 2
			acc += dt * dy
			if isNaN(acc):
				print()
			acc = getFuseValue(i) * (dt * alpha) + (1 - (dt * alpha)) * acc
			if isNaN(acc):
				print()


		result[i] = acc

	return result

def movingaverage2(values, window):
	weights = np.repeat(1.0, window) / window
	sma = np.convolve(values, weights, 'same')
	return sma

def smooth_median(values, i_range=3):
	range_sub = int(i_range / 2)
	range_add = int(i_range / 2)
	if (i_range % 2 == 1):
		range_sub += 1

	arr_len = len(values)
	res = []
	for i in range(len(values)):
		low = max(0, i - range_sub)
		high = min(arr_len, i + range_add)
		res.append(median_low(values[low:high]))

	return res

def smooth_box(values, i_range=3, func=mean):
	range_sub = int(i_range / 2)
	range_add = int(i_range / 2)
	if (i_range % 2 == 1):
		range_sub += 1

	arr_len = len(values)
	res = []
	for i in range(len(values)):
		low = max(0, i - range_sub)
		high = min(arr_len, i + range_add)
		res.append(func(values[low:high]))

	return res

def smooth_moving_avg(values, i_range=3):
	""" calculates moving avg smoothing over a given array """

	#TODO implement nan tolerant smoothing

	vlen = len(values)

	#[..., i - range_sub, ...., i , ...., i + range_add, ... ]
	range_sub = int(i_range / 2)
	range_add = int(i_range / 2)
	if(i_range % 2 == 1):
		range_sub += 1

	#init acc
	v0 = values[0]
	acc = (range_sub * v0 if isValidNum(v0) else 0) + sum([v for v in values[1:range_add+1] if isValidNum(v)])
	if not isValidNum(acc):
		acc = 0
	res = []
	invalid_count = len([v for v in values[1:range_add+1] if not isValidNum(v)]) + (range_sub if not isValidNum(v0) else 0)

	if (i_range - invalid_count) == 0:
		res.append(nan)
	else:
		res.append(acc / (i_range - invalid_count))

	for i in range(1, len(values)):
		i_sub = max(0, i - range_sub)
		sub = values[i_sub]

		if isValidNum(sub):
			acc -= sub
		else:
			invalid_count -= 1

		i_add = min(vlen - 1, i + range_add)
		add = values[i_add]
		if isValidNum(add):
			acc += add
		else:
			invalid_count += 1

		arr_range = values[i_sub+1:i_add+1] #TODO remove

		#assert 0 <= invalid_count <= i_range
		if not (0 <= invalid_count <= i_range):
			print()

		if (i_range - invalid_count) == 0:
			res.append(nan)
		else:
			res.append(acc / (i_range - invalid_count))
	return res

	"""
	vlen = len(values)
	#[..., i - range_sub, ...., i , ...., i + range_add, ... ]
	range_sub = int(i_range / 2)
	range_add = int(i_range / 2)
	if(i_range % 2 == 1):
		range_sub += 1
	acc = range_sub * values[0] + sum(values[:range_add])
	res = []
	for i in range(len(values)):
		sub = values[max(0, i - range_sub)]
		add = values[min(vlen - 1, i + range_add)]
		acc -= sub
		acc += add
		res.append(acc / i_range)
	return res
	"""

def arr_divide(arr1, arr2):
	return list(np.divide(arr1, arr2))



def regression_linear(x, y):
	"""
	Calculates a linear regression m * x + b to fit given trace of x,y
	:param x: array/list of x values
	:param y: array/list of y values
	:return: m, b
	"""
	import numpy as np
	from sklearn.linear_model import LinearRegression
	X = np.array(x).reshape((-1, 1))
	Y = np.array(y)
	model = LinearRegression().fit(X, Y)
	print(model.score(X, Y))
	#print(model.predict(np.array([[3, 5]])))

	m = model.coef_[0]
	b = model.intercept_

	print(f"{m} * x + {b}")

	return m, b


