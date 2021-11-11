from math import pi, atan2, tan, atan, cos, sin, acos, asin, nan, sqrt, isnan
import numpy as np


FACTOR_Min_2_Sec = 60
FACTOR_Hour_2_Sec = 3600
FACTOR_Day_2_Sec = 3600 * 24
FACTOR_Sec_2_Min = 1 / FACTOR_Min_2_Sec
FACTOR_Sec_2_Hour = 1 / FACTOR_Hour_2_Sec
FACTOR_S_2_Day = 1 / FACTOR_Day_2_Sec
FACTOR_MPS_2_KMH = 3.6
FACTOR_KMH_2_MPS = 1/FACTOR_MPS_2_KMH
FACTOR_G_2_MPSS = 9.81
FACTOR_MPSS_2_G = 1/FACTOR_G_2_MPSS
FACTOR_MS_2_S = (1/1000)
FACTOR_mAh_2_As = 3.6
FACTOR_M_2_KM = 1/1000
FACTOR_As_2_mAh = 1 / FACTOR_mAh_2_As
FACTOR_WEEK_TO_SECONDS = 7 * 24 * 60 * 60
FACTOR_deg_2_rad  = 0.017453292519943295769236907684886 #[rad/deg] pi / 180
FACTOR_rad_2_deg = 57.295779513082320876798154814105 #[deg/rad] 180 / pi



def Vec2d(x, y=0):
	if(isinstance(x, list) and len(x) == 2):
		return (x[0], x[1])
	return (x, y)

def Vec2d_sub(v1, v2):
	return np.subtract(v1, v2)

def Vec2d_add(v1, v2):
	return np.add(v1, v2)

def Vec2d_scale(v1, a):
	return (v1[0] * a, v1[1] * a)

def Vec2d_dist(v1, v2):
	return np.linalg.norm(Vec2d_sub(v1, v2))

def Vec2d_len(v1):
	return np.linalg.norm(v1)

def Vec2d_normalize(v1):
	""" Returns the unit vector of the vector.  """
	if(np.linalg.norm(v1) == 0):
		return v1

	return v1 / np.linalg.norm(v1)

def Vec2d_avg(list_v):
	""" Takes a list of 2d Vectors (as 2-tuple) and avg's them"""
	from Help import switchArrayDim
	x, y = switchArrayDim(list_v)
	return (mean(x), mean(y))

def Vec2_rotate(v, a, is_degree=False):
	"""
	Rotates vector (x, y) around z axis by angle a
	:param v: (x, y) Vector to rotate
	:param a: angle in [rad]
	:return: vector rotated
	"""
	x, y = v

	if is_degree:
		a = deg2rad(a)

	return (
		cos(a) * x - sin(a) * y,
		sin(a) * x + cos(a) * y
	)

def Vec2d_dir_deg(v1):
	"""
	Returns direction of Vector in [deg]
	example:
	(1, 1) = 45°
	(-1, 1) = 135°
	(0, 1) = 90°
	(1, 0) = 0°
	:param v1: (x, y)
	:return: Angle in [deg]
	"""
	x, y = v1
	if x == 0: #special cases
		return 90 if (y > 0) else (0 if (y == 0) else 270)

	elif (y == 0): # special cases
		return 0 if (x >= 0) else 180

	ret = rad2deg(atan(y / x))

	if (x < 0 and y < 0): # quadrant 3
		ret = 180 + ret
	elif (x < 0): # quadrant 2
		ret = 180 + ret # it actually substracts
	elif (y < 0): # quadrant 4
		ret = 270 + (90 + ret) # it actually substracts

	return ret


def mean(arr):
	if(len(arr) == 0):
		return 0
	#return sum(arr) / len(arr)
	return np.mean(arr)


def angle_between(v1, v2):
	""" Returns the angle in radians between vectors 'v1' and 'v2'::

			>>> angle_between((1, 0, 0), (0, 1, 0))
			1.5707963267948966
			>>> angle_between((1, 0, 0), (1, 0, 0))
			0.0
			>>> angle_between((1, 0, 0), (-1, 0, 0))
			3.141592653589793
	"""
	v1_u = Vec2d_normalize(v1)
	v2_u = Vec2d_normalize(v2)
	angle = np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

	if(isNaN(angle)):
		return 0
	if (np.cross(v1_u, v2_u) < 0):
		angle = -angle
	return angle




def Vec3_rotX(v, a, is_degree=False):
	x, y, z = v

	if is_degree:
		a = deg2rad(a)

	return (
		x,
		cos(a) * y - sin(a) * z,
		sin(a) * y + cos(a) * z
	)

def Vec3_rotY(v, a, is_degree=False):
	x, y, z = v

	if is_degree:
		a = deg2rad(a)

	return (
		cos(a) * x + sin(a) * z,
		y,
		-sin(a) * x + cos(a) * z
	)

def Vec3_rotZ(v, a, is_degree=False):
	x, y, z = v

	if is_degree:
		a = deg2rad(a)

	return (
		cos(a) * x - sin(a) * y,
		sin(a) * x + cos(a) * y,
		z,
	)




def deg2rad(a_deg):
	return a_deg * FACTOR_deg_2_rad

def rad2deg(a_rad):
	return a_rad * FACTOR_rad_2_deg


def g2mpss(a_g):
	return a_g * FACTOR_G_2_MPSS

def mpss2g(a_mpss):
	return a_mpss * FACTOR_MPSS_2_G

def isValidNum(x):
	if x == None:
		return False
	if isNaN(x):
		return False
	return True

def isNaN(x):
	import math
	if x == None:
		return False
	try:
		return math.isnan(x) or math.isinf(x)
	except:
		return False
		#raise

def between(minv, val , maxv):
	return minv if val < minv else maxv if val > maxv else val


def Line_2_Line_Intersect(Line1, Line2, considerCollinearOverlapAsIntersect = False):
	"""
	Calculates Intersection Point of Two sets of Points connected by a straight line
	:param Line1: [(x1, y1), (x2, y2)]
	:param Line2: [(x1, y1), (x2, y2)]
	:param considerCollinearOverlapAsIntersect: ???
	:return: None if no intersection else (x, y) point of intersection
	"""
	# https://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect/565282#565282
	# http://www.codeproject.com/Tips/862988/Find-the-intersection-point-of-two-line-segments

	def np_perp( a ) :
		b = np.empty_like(a)
		b[0] = a[1]
		b[1] = -a[0]
		return b

	def np_cross_product(a, b):
		return np.dot(a, np_perp(b))

	Line1 = np.array(Line1)
	Line2 = np.array(Line2)
	r = Line1[1] - Line1[0]
	s = Line2[1] - Line2[0]
	v = Line2[0] - Line1[0]
	num = np_cross_product(v, r)
	denom = np_cross_product(r, s)
	# If r x s = 0 and (q - p) x r = 0, then the two lines are collinear.
	if np.isclose(denom, 0) and np.isclose(num, 0):
		# 1. If either  0 <= (q - p) * r <= r * r or 0 <= (p - q) * s <= * s
		# then the two lines are overlapping,
		if(considerCollinearOverlapAsIntersect):
			vDotR = np.dot(v, r)
			aDotS = np.dot(-v, s)
			if (0 <= vDotR  and vDotR <= np.dot(r,r)) or (0 <= aDotS  and aDotS <= np.dot(s,s)):
				return True
		# 2. If neither 0 <= (q - p) * r = r * r nor 0 <= (p - q) * s <= s * s
		# then the two lines are collinear but disjoint.
		# No need to implement this expression, as it follows from the expression above.
		return None
	if np.isclose(denom, 0) and not np.isclose(num, 0):
		# Parallel and non intersecting
		return None
	u = num / denom
	t = np_cross_product(v, s) / denom
	if u >= 0 and u <= 1 and t >= 0 and t <= 1:
		res = Line2[0] + (s * u)
		return (float(res[0]), float(res[1]))
	# Otherwise, the two line segments are not parallel but do not intersect.
	return None


def getRotMat(angleX=0, angleY=0, angleZ=0, isdegrees=False):
	from scipy.spatial.transform import Rotation
	#return Rotation.from_euler('zyx', [angleZ, angleY, angleX], degrees=isdegrees)

	#extrisic Rotation in order: Roll, Pitch, Yaw
	return Rotation.from_euler('xyz', [angleX, angleY, angleZ], degrees=isdegrees)
	#return Rotation.from_euler('ZYX', [angleZ, angleY, angleX], degrees=isdegrees)

def RotVec(vec, rotangles, isdegrees=False):
	anglex, angley, anglez = rotangles
	return tuple(getRotMat(anglex, angley, anglez, isdegrees).apply(vec))




def Sample_Kernel(arr, i, kernel):
	"""
	Samples an array at the position i with kernel for downsampling
	:param kernel: must be an array of numbers and length must be uneven
	"""
	glen = len(arr)
	k_center = int(len(kernel) / 2)
	k_sum = sum(kernel)

	return sum([kernel[r] * arr[between(0, i - k_center + r, glen - 1)] for r in range(len(kernel))]) / k_sum


def Scale_Down(arr, kernel):
	return [Sample_Kernel(arr, i, kernel) for i in range(len(arr)) if i % 2 == 0]


def Scale_UP(arr, kernel):

	k_center = int(len(kernel) / 2)
	k_sum = sum(kernel)

	arr2 = []
	for v in arr:
		arr2 += [0, v]
	for i in range(k_center):
		arr2 = [0] + arr2 + [0]
	#print(arr2)
	arr3 = [0 for i in range(len(arr2))]
	for k in kernel:
		arr3 = np.add(np.multiply(arr2 , k), arr3)
		arr3 = list(arr3)[1:] + [0]
		#print(arr3)
	arr3 = arr3[0:-(2*k_center + 1)]
	arr3 = np.divide(arr3, k_sum / 2)
	return arr3


def interpolate(x, y, x_new, order=1):
	"""
	Interpolates/Resamples given trace (x, y) to new x_new sample points

	:param x:
	:param y:
	:param x_new:
	:param order: 0=nearest value | 1:linear | 2:quadratic | 3:cubic
	:return: y_new
	"""


	if(order > 3):
		print("Error max order = 3")
		return None

	#nearest
	if(order == 0):
		i_new = np.interp(x_new, x, list(range(len(y))))
		i_new_round = [int(round(j)) for j in i_new]

		y_new = [y[j] for j in i_new_round]
		return y_new

	#linear but Nan Null possible
	if(order == 0.5):

		def isvalid(v):
			return not (v == None or isNaN(v))

		y_new_order0 = interpolate(x, y, x_new, order=0)
		y_no_None = [v if isvalid(v) else 0 for v in y]
		y_new_order1 = interpolate(x, y_no_None, x_new, order=1)

		y_new = [v if isvalid(y_new_order0[i]) else y_new_order0[i] for i, v in enumerate(y_new_order1)]
		#use nearest value if next value is invalid
		for i in range(1, len(y_new) - 1):
			if not isvalid(y_new[i]):
				y_new[i - 1] = y_new_order0[i - 1]
				y_new[i + 1] = y_new_order0[i + 1]

		return y_new

	if(order == 1):
		return np.interp(x_new, x, y)

	if(order >= 1):
		from scipy.interpolate import interp1d, splrep, splev
		kind = ['linear', 'quadratic', 'cubic'][order - 1]

		y_new = interp1d(x, y, kind=kind, bounds_error=False, fill_value="extrapolate")(x_new)
		#y_new = splev(new_x, splrep(x, y, k=order))

		return y_new

	return None

if __name__ == '__main__':

	R = getRotMat(angleX=0, angleY=90, angleZ=0, isdegrees=True)
	print(R.apply((1, 0, 0)))

	"""
	from PlotHelp import *
	from FileModule import LoadGroup
	from Defines import *

	group = LoadGroup("2019-12-17", 104, GROUP_ACCEL_RAW, 190, 200)
	arr = group[TRACE_ACCELX]
	res = arr[:]
	print(res)
	print(len(res))
	reses = []
	for j in range(7):
		res = group[TRACE_ACCELX][:]
		print(len(res), end="->")
		for i in range(j):
			res = Scale_Down(res, [1, 2, 1])
			#print(res)
		print(len(res), end="->")
		for i in range(j):
			res = Scale_UP(res, [1, 2, 1])
			#print(res)
		print(len(res))

		#reses.append(res[:])
		reses.append(np.subtract(arr[0: len(res)], res))

	plotY(reses)
	
	"""