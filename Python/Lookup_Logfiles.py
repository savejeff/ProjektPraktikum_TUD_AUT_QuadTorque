from Defines import *

DATESTRING_PHASE_VOLTAGE = "2021-11-09"
DATESTRING_PHASE_CURRENT = "2021-11-11"


# EXAMPLE:
if False:
	LIST_LOGFILES = [
					("throttle 10", "bldc_2x_phase_to_ground_voltage_throttle_10"),
					("throttle 20", "bldc_2x_phase_to_ground_voltage_throttle_20"),
					("throttle 30", "bldc_2x_phase_to_ground_voltage_throttle_30"),
					("throttle 40", "bldc_2x_phase_to_ground_voltage_throttle_40"),
					("throttle 50", "bldc_2x_phase_to_ground_voltage_throttle_50"),
					("throttle 60", "bldc_2x_phase_to_ground_voltage_throttle_60"),
					("throttle 70", "bldc_2x_phase_to_ground_voltage_throttle_70"),
					("throttle 80", "bldc_2x_phase_to_ground_voltage_throttle_80"),
					("throttle 90", "bldc_2x_phase_to_ground_voltage_throttle_90"),
					("throttle 100", "bldc_2x_phase_to_ground_voltage_throttle_100")
	]

if True:
	LIST_LOGFILES = [
					("throttle 10", "bldc_phase_current_phase_to_phase_voltage_throttle_10"),
					("throttle 30", "bldc_phase_current_phase_to_phase_voltage_throttle_30"),
					("throttle 50", "bldc_phase_current_phase_to_phase_voltage_throttle_50"),
					("throttle 70", "bldc_phase_current_phase_to_phase_voltage_throttle_70"),
					("throttle 100", "bldc_phase_current_phase_to_phase_voltage_throttle_100")
	]


DATASET_2021_12_21 = (
	# Base Feature Vector
	{
		FEAUTRE_MOTOR_KV : 1000,
		FEAUTRE_MOTOR_ID : 0,
		FEAUTRE_PROPELLER_ID : 0,
		FEAUTRE_PROPELLER_DIAMETER : 6,
		FEAUTRE_PROPELLER_PITCH : 35
	},
	# List of Recording group
	[
		#(throttle, datestring, arduino log, timestamp_steadystate)
		(10, "2021-12-21_010", "COM_ser_2021-12-21_13-37-40", 3567),
		(20, "2021-12-21_020", "COM_ser_2021-12-21_13-39-13", 3660),
		(30, "2021-12-21_030", "COM_ser_2021-12-21_13-40-22", 3735),
		(40, "2021-12-21_040", "COM_ser_2021-12-21_13-41-45", 3814),
		(50, "2021-12-21_050", "COM_ser_2021-12-21_13-42-50", 3881),
		(60, "2021-12-21_060", "COM_ser_2021-12-21_13-44-13", 3958),
		(70, "2021-12-21_070", "COM_ser_2021-12-21_13-45-05", 4012.8),
		(80, "2021-12-21_080", "COM_ser_2021-12-21_13-46-30", 4096),
		(90, "2021-12-21_090", "COM_ser_2021-12-21_13-47-34", 4160),
		(100, "2021-12-21_100", "COM_ser_2021-12-21_13-49-00", 4248),
	]
)