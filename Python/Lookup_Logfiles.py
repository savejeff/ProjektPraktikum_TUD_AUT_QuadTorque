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
		FEAUTRE_PROPELLER_PITCH : 35,
		#TODO add paramter for motor like hight and width
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

DATASET_2022_01_18 = (
	# Base Feature Vector
	{
		FEAUTRE_MOTOR_KV : 2200,
		FEAUTRE_MOTOR_ID : 1,
		FEAUTRE_PROPELLER_ID : 0,
		FEAUTRE_PROPELLER_DIAMETER : 6,
		FEAUTRE_PROPELLER_PITCH : 35,
		#TODO add paramter for motor like hight and width
	},
	# List of Recording group
	[
		#(throttle, datestring, arduino log, timestamp_steadystate)
		(10, "2022-01-18_010", "COM_ser_2022-01-18_14-52-18", None),
		(15, "2022-01-18_015", "COM_ser_2022-01-18_14-53-57", None),
		(20, "2022-01-18_020", "COM_ser_2022-01-18_14-55-14", None),
		(25, "2022-01-18_025", "COM_ser_2022-01-18_14-56-01", None),
		(30, "2022-01-18_030", "COM_ser_2022-01-18_14-56-47", None),
		(35, "2022-01-18_035", "COM_ser_2022-01-18_14-57-43", None),
		(40, "2022-01-18_040", "COM_ser_2022-01-18_14-58-49", None),
		(45, "2022-01-18_045", "COM_ser_2022-01-18_15-00-04", None),
		(50, "2022-01-18_050", "COM_ser_2022-01-18_15-01-17", None),
		(55, "2022-01-18_055", "COM_ser_2022-01-18_15-02-24", None),
		(60, "2022-01-18_060", "COM_ser_2022-01-18_15-03-36", None),
		(65, "2022-01-18_065", "COM_ser_2022-01-18_15-04-42", None),
		(70, "2022-01-18_070", "COM_ser_2022-01-18_15-06-55", None),
		(75, "2022-01-18_075", "COM_ser_2022-01-18_15-08-00", None),
		(80, "2022-01-18_080", "COM_ser_2022-01-18_15-09-02", None),
		(85, "2022-01-18_085", "COM_ser_2022-01-18_15-10-12", None),
		(90, "2022-01-18_090", "COM_ser_2022-01-18_15-11-45", None),
		(95, "2022-01-18_095", "COM_ser_2022-01-18_15-12-48", None),
		(100, "2022-01-18_100", "COM_ser_2022-01-18_15-14-02", None),
	]
)