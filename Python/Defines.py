from paths import PATH

FILEFORMAT_EVENTLOG_RAW = "EventLog{:02}.TXT"
FILEFORMAT_EVENTLOG = "EventLog{:02}.mat"
FOLDERFORMAT_LOGFILE = "LOG{:02}"
FILEFORMAT_LOGFILE_RAW = "LOG{:02}.TXT"
FILEFORMAT_LOGFILE = "LOG{:02}.mat"
FILEFORMAT_LOGFILE_OUT = "LOG{:02}_out.mat"
FILEFORMAT_LOGFILE_POSTFIX = "LOG{:02}_{}.mat"
FILEFORMAT_VBO_LOGFILE = "LOG{:02}.vbo"
FILEFORMAT_DATA_LAPDATA = "LapData{}_{:02}_{:02}.mat" #1:Datestring|2:LogNum|3:Lapnum
FILEFORMAT_DATA_LAPDATA_POSTFIX = "LapData{}_Log{:02}_Lap{:02}{}.mat" #1:Datestring|2:LogNum|3:Lapnum|4:postfix
FILEFORMAT_DATA_COURSE_POSTFIX = "LapData{}_Log{:02}_{:02}{}.mat" #1:Datestring|2:LogNum|3:coursenum|4:postfix
FILENAME_CONFIG = "config.txt"
FILENAME_TMP_JSON = "tmp.json"
FILENAME_TMP_JSON_TAG = "tmp_{}.json"
FILENAME_TMP_DATA = "tmp.mat"
FILENAME_TMP_DATA_TAG = "tmp_{}.mat"


FILENAME_CMPLaps = "CompareLab.mat"

#Signal Names
SIGNAL_GPIO_AI0_PERCENT = "GPIO.AI0.percent"
SIGNAL_GPIO_AI0_RAW = "GPIO.AI0.raw"
SIGNAL_GPIO_AI0_VOLT = "GPIO.AI0.volt"
SIGNAL_HX711_DT_READ = "HX711.dt.read"
SIGNAL_HX711_DT_UPDATE = "HX711.dt.update"
SIGNAL_HX711_RAW = "HX711.raw"
SIGNAL_INA219_CURR = "INA219.curr"
SIGNAL_INA219_PWR = "INA219.pwr"
SIGNAL_INA219_VOLT = "INA219.volt"
SIGNAL_CFG_APP = "cfg.app"
SIGNAL_ESC_ANGLE = "esc.angle"
SIGNAL_ESC_APP = "esc.app"
SIGNAL_GPIO_FRQ_IN0_DUR = "gpio.frq_in0.dur"
SIGNAL_GPIO_FRQ_IN0_FRQ = "gpio.frq_in0.frq"
SIGNAL_GPIO_FRQ_IN0_RPM = "gpio.frq_in0.rpm"


# Group Names
GROUP_HX711 = "HX711"
GROUP_INA219 = "INA219"
GROUP_FRQ_IN0 = "Frq_in0"
GROUP_AI0 = "AI0"

# Trace Names
TRACE_RAW = "raw" #[1]
TRACE_WEIGHT_GRAM = "weight_g" #[g]
TRACE_FORCE = "force" #[N]
TRACE_TORQUE = "torque" #[NM]
TRACE_DC_CURRENT = "dc_current" #[A]
TRACE_DC_VOLT = "dc_volt" #[V]
TRACE_DC_POWER = "dc_power" #[W]

TRACE_CHANNEL1_V = "Channel1_v" #[V]
TRACE_CHANNEL2_V = "Channel2_v" #[V]

TRACE_THROTTLE = "throttle"
TRACE_PHASE_CURRENT = "phase_current"
TRACE_MOTOR_SPEED = "motor_speed_rpm" #[rpm]
TRACE_MOTOR_POWER = "motor_power"

TRACE_IS_STEADY_STATE = "is_steady_state"


GROUP_OSCI = "Osci"
GROUP_PHASE_CURRENT_ANALYSIS = "phase_curr_analysis"

#Group Names
GROUP_ACCEL = "Accelerometer"
GROUP_ACCEL_RAW = "Accelerometer_RAW"
GROUP_GYRO = "Gyroskop"
GROUP_GYRO_RAW = "Gyroskop_RAW"
GROUP_MAG = "Magnetometer"
GROUP_MAG_RAW = "Magnetometer_RAW"
GROUP_DISTANCE = "Distance"
GROUP_DIST = "RelDist"
GROUP_POSI = "Position"
GROUP_VELOCITY = "Velocity"
GROUP_ORIENTATION = "Orientation"
GROUP_STRING_LOG = "StringLog"
GROUP_BYTES_LOG = "BytesLog"
GROUP_MISC = "Misc"
GROUP_DEBUG_S = "DEBUG_S" #float
GROUP_DEBUG_T = "DEBUG_T" #float
GROUP_DEBUG_U = "DEBUG_U" #float
GROUP_DEBUG_V = "DEBUG_V" #id, float
GROUP_DEBUG_W = "DEBUG_W0" #5x int
GROUP_DEBUG_w = "DEBUG_W1" #5x int
GROUP_DEBUG_X = "DEBUG_X" #int32
GROUP_DEBUG_Y = "DEBUG_Y" #int32
GROUP_DEBUG_Z = "DEBUG_Z" #int32
GROUP_TEMPERATURE = "Temperature"
GROUP_BATTERY = "Battery"
GROUP_BATTERY_DATA = "Battery_Data"
GROUP_TIME = "Time"
GROUP_TIMESTAMP = "TimeStamp"
GROUP_TEMP_TIRE = "Temp_Tire"
GROUP_HV_BAT = "HV_Battery"
GROUP_DMC_STATUS = "DMC_Status"
GROUP_DMC_MOTOR = "DMC_Motor"
GROUP_MOTOR_SUPPLY = "Motor_Supply"
GROUP_MOTOR_DYNAMICS = "Motor_Dynamics"
GROUP_CAN_MSG = "CAN_MSGs"


GROUP_TMP = "tmp"
GROUP_TEST = "Test"
GROUP_TEST2 = "Test2"
GROUP_TEST3 = "Test3"


TRACE_POSTFIX_CORRECTED = "_corrected"
TRACE_POSTFIX_ROTATED = "_rot"
TRACE_POSTFIX_PREDICTED = "_predicted"
TRACE_POSTFIX_RAW = "_raw"
TRACE_POSTFIX_SMOOTH = "_smooth"
TRACE_POSTFIX_NORMALIZED = "_normalized"
TRACE_POSTFIX_TOTAL = "_total"
TRACE_POSTFIX_REMAIN = "_remain"
TRACE_POSTFIX_ERROR = "_Error"
TRACE_POSTFIX_ERROR_RATE = "_ErrorRate"

#Trace Names
TRACE_TIME = "Time"
TRACE_INDEX = "Index"
TRACE_VALUE = "Value"
TRACE_VALUE_X = "ValueX"
TRACE_VALUE_Y = "ValueY"
TRACE_VALUE_Z = "ValueZ"
TRACE_DELTA = "delta" #Delta between traces
TRACE_DELTA_ABS = "delta_abs" #absolute Delta between traces
TRACE_DELTA_TIME = "delta_Time" #dT Trace of TimeTrace
TRACE_TIME_DIFF = "Time_Diff" #Difference of to Time Traces
TRACE_TRIGGER = "Trigger" #[1]

TRACE_ACCEL_X = "AccelX" #[m/s²]
TRACE_ACCEL_Y = "AccelY" #[m/s²]
TRACE_ACCEL_Z = "AccelZ" #[m/s²]
TRACE_ACCEL_X_RAW = TRACE_ACCEL_X + TRACE_POSTFIX_RAW #[m/s²]
TRACE_ACCEL_Y_RAW = TRACE_ACCEL_Y + TRACE_POSTFIX_RAW #[m/s²]
TRACE_ACCEL_Z_RAW = TRACE_ACCEL_Z + TRACE_POSTFIX_RAW #[m/s²]
TRACE_GYRO_X = "GyroX" #[rad/s]
TRACE_GYRO_Y = "GyroY" #[rad/s]
TRACE_GYRO_Z = "GyroZ" #[rad/s]
TRACE_GYRO_X_RAW = TRACE_GYRO_X + TRACE_POSTFIX_RAW #[rad/s]
TRACE_GYRO_Y_RAW = TRACE_GYRO_Y + TRACE_POSTFIX_RAW #[rad/s]
TRACE_GYRO_Z_RAW = TRACE_GYRO_Z + TRACE_POSTFIX_RAW #[rad/s]
TRACE_MAG_X = "MagX"
TRACE_MAG_Y = "MagY"
TRACE_MAG_Z = "MagZ"
TRACE_MAG_X_NORM = TRACE_MAG_X + TRACE_POSTFIX_NORMALIZED
TRACE_MAG_Y_NORM = TRACE_MAG_Y + TRACE_POSTFIX_NORMALIZED
TRACE_MAG_Z_NORM = TRACE_MAG_Z + TRACE_POSTFIX_NORMALIZED

TRACE_LAT = "Lat" #[deg]
TRACE_LON = "Lon" #[deg]
TRACE_POSI_LAT = "Posi_lat" #[deg] Latitude
TRACE_POSI_LON = "Posi_lon" #[deg] Longitude
TRACE_POSI_ALT = "Posi_alt" #[deg] Altitude
TRACE_VELOCITY = "Velocity" #[m/s]
TRACE_VELOCITY_KMH = "Velocity_kmh" #[km/h]
TRACE_DISTANCE = "Distance" #[m]
TRACE_DISTANCE_TRAVEL = "Distance_Travel" #[m]
TRACE_DISTANCE_KM = "Distance_km" #[m]
TRACE_SATCOUNT = "NumSat"
TRACE_SENTENCE_COUNT = "Sentence_Count"
TRACE_CS_FAIL = "CS_Fail"
TRACE_GPS_FIX = "Fix"

TRACE_TIME_DAYSECONDS = "DaySeconds" #Seconds since begin of day
TRACE_TIMESTRING = "Timestring" #like "2021-05-17 14:47:04"
TRACE_UNIX_TIMESTAMP = "UNIX_Timestamp" #[s] number of seconds that have elapsed since January 1, 1970 (midnight UTC/GMT), not counting leap seconds https://www.epochconverter.com/
TRACE_TIME_HOUR = "Hour"
TRACE_TIME_MINUTES = "Minutes"
TRACE_TIME_SECONDS = "Seconds"
TRACE_TIME_MILLISECONDS = "Milliseconds"
TRACE_HHMMSS = "HHMMSS"
TRACE_DAY = "Day"
TRACE_MONTH = "Month"
TRACE_YEAR = "Year"
TRACE_DDMMYY = "DDMMYY"

TRACE_DRIVE_DISTANCE = "DriveDistance" # [m] Driven Distance since start
TRACE_DRIVE_TIME = "DriveTime" # [s] Time Driven since start
TRACE_DRIVE_RANGE = "Range" # [m] Drivable Distance
TRACE_DISTANCE_REL = "RelDistance" #[m]
TRACE_ACCEL = "Acceleration" #[m/s²]
TRACE_ACCEL_LONGITUDINAL = "Accel_longitudinal" #[m/s²]
TRACE_ACCEL_LATERAL = "Accel_lateral" #[m/s²]
TRACE_ACCEL_VERTICAL = "Accel_vertical" #[m/s²]

TRACE_LAPTIME = "LapTime"
TRACE_LAPTIME_SECONDS = "LapTime_Seconds"
TRACE_LAPSTART = "LapStart"
TRACE_LAPEND = "LapEnd"

TRACE_POSI_X = "Posi_X" #[m]
TRACE_POSI_Y = "Posi_Y" #[m]
TRACE_POSI_Z = "Posi_Z" #[m]
TRACE_VEL_X = "Vel_X" #[m/s]
TRACE_VEL_Y = "Vel_Y" #[m/s]
TRACE_VEL_Z = "Vel_Z" #[m/s]
TRACE_VEL_2D = "Vel_2D" #[m/s]
TRACE_VEL_3D = "Vel_3D" #[m/s]
TRACE_ACCEL_N = "Accel_North" #[m/s²]
TRACE_ACCEL_W = "Accel_West" #[m/s²]
TRACE_VEL_N = "Velocity_North" #[m/s]
TRACE_VEL_W = "Velocity_West" #[m/s]
TRACE_VEL_E = "Velocity_East" #[m/s]
TRACE_VEL_U = "Velocity_Up" #[m/s]
TRACE_POSI_N = "Posi_North" #[m]
TRACE_POSI_W = "Posi_West" #[m]
TRACE_POSI_U = "Posi_Up" #[m]
TRACE_ORIENTATION_X = "Orientation_X" #[rad]
TRACE_ORIENTATION_Y = "Orientation_Y" #[rad]
TRACE_ORIENTATION_Z = "Orientation_Z" #[rad]
TRACE_ORIENTATION_X_DEG = "Orientation_X_deg" #[deg]
TRACE_ORIENTATION_Y_DEG = "Orientation_Y_deg" #[deg]
TRACE_ORIENTATION_Z_DEG = "Orientation_Z_deg" #[deg]
TRACE_POSI_DIR = "Direction"
TRACE_POSI_ANGLE = "Angle"
TRACE_POSI_ANGLE_IGR = "Angle_integrat"
TRACE_POSI_ANGLE_DIFF = "Angle_diff"
TRACE_POSI_ANGLE_DIFF2 = "Angle_diff2"
TRACE_POSI_ANGLE_SIGN = "Angle Sign"
TRACE_SIDE_SLIP_ANGLE = "SideSlipAngle" #[rad]
TRACE_SIDE_SLIP_ANGLE_DEG = "SideSlipAngle_Deg" #[rad]
TRACE_COURSE_CURVATURE = "Course_Curvature" #[1/m]
TRACE_COURSE_RADIUS = "Course_Radius" #[m]
TRACE_ACCEL_CENTRIFUGAL = "Accel_Centrifugal" #[m/s²]
TRACE_ROLL_ANGLE = "Roll_Angle" #[rad]
TRACE_ROLL_ANGLE_VALID = "Roll_Angle_Valid" #[1]
TRACE_ROLL_ANGLE_DEG = "Roll_Angle_Deg" #[deg]
TRACE_ROLL_RATE = "Roll_Rate" #[rad/s]
TRACE_PITCH_ANGLE = "Pitch_Angle" #[rad]
TRACE_PITCH_ANGLE_DEG = "Pitch_Angle_Deg" #[deg]
TRACE_PITCH_RATE = "Pitch_Rate" #[rad/s]
TRACE_YAW_ANGLE = "Yaw_Angle" #[rad]
TRACE_YAW_ANGLE_CONTINUOUS = "Yaw_Angle_Continuous" #[rad]
TRACE_YAW_ANGLE_DEG = "Yaw_Angle_Deg" #[deg]
TRACE_YAW_RATE = "Yaw_Rate" #[rad/s]
TRACE_QUATERNION_X = "Quaternion_X"
TRACE_QUATERNION_Y = "Quaternion_Y"
TRACE_QUATERNION_Z = "Quaternion_Z"
TRACE_QUATERNION_W = "Quaternion_W"
TRACE_LEANANGLE_GPS = "LeanAngle_GPS" #Leanangle derived from GPS Posi and Speed
TRACE_LEANANGLE_GYRO = "LeanAngle_Gyro" #Leanangle derived from GyroX
TRACE_PROGRESS = "Progress"
TRACE_DEBUG_VALUE = "Value"
TRACE_HEADING = "Heading" #[rad]
TRACE_HEADING_DEG = "Heading_Deg" #[deg]
TRACE_HEADING_CONTINUOUS = "Heading_Continuous" #[rad]
TRACE_HEADING_CONTINUOUS_DEG = "Heading_Continuous_Deg" #[deg]
TRACE_ALTITUDE = "Altitude" #[m]
TRACE_ALTITUDE_GPS = TRACE_ALTITUDE + "_GPS" #[m]
TRACE_ALTITUDE_BARO = TRACE_ALTITUDE + "_BARO" #[m]
TRACE_ALTITUDE_DIFF = TRACE_ALTITUDE + "_diff" #[m] - Difference in Altitude
TRACE_VELOCITY_ALTITUDE = "Velocity_Altitude" #[m/s] - Altitude Rate of change
TRACE_ROAD_SLOPE = "Road_Slope" #[rad] road slope
TRACE_SLOPE_DEG = "Road_Slope_deg" #[deg] road slope
TRACE_PRESSURE = "Pressure"
TRACE_TEMPERATURE = "Temperature"
TRACE_HUMIDITY = "Humidity"
TRACE_SENSOR_ID = "SensorID"
TRACE_ID = "ID"
TRACE_LEN = "Length"
TRACE_DATA = "Data"
TRACE_TEMP_OBJ = "Temp_Obj"
TRACE_TEMP_AMB = "Temp_Amb"
TRACE_TEMP_TIRE_REAR_LEFT = "Temp_Rear_Left"
TRACE_TEMP_TIRE_REAR_CENTER = "Temp_Rear_Center"
TRACE_TEMP_TIRE_REAR_RIGHT = "Temp_Rear_Right"
TRACE_SOC = "SoC" #[1] (0 - 1)
TRACE_SOC_PERCENT = "SoC_Percent" #[%] (0% - 100%)
TRACE_VOLTAGE = "Voltage" #[V]
TRACE_CURRENT = "Current" #[A]
TRACE_CAPACITY = "Capacity" #[As]
TRACE_CAPACITY_mAh = "Capacity_mAh" #[mAh]
TRACE_DT_GPS = "DT_GPS"
TRACE_DT_AGM = "DT_AGM"
TRACE_DT_MONITOR = "DT_Monitor"
TRACE_DT_MISC = "DT_Misc"
TRACE_DT_STORAGE = "DT_Storage"
TRACE_DT_LOOP = "DT_Loop"
TRACE_TMP = "tmp"
TRACE_TEST = "test"
TRACE_TEST1 = "test1"
TRACE_TEST2 = "test2"
TRACE_TEST3 = "test3"
TRACE_1 = "Trace1"
TRACE_2 = "Trace2"
TRACE_3 = "Trace3"
TRACE_4 = "Trace4"
TRACE_5 = "Trace5"

TRACE_DMC_APP = "DMC_APP"
TRACE_DMC_MAP = "DMC_MAP"
TRACE_DMC_STAT = "DMC_STAT"
TRACE_DMC_LIMIT = "DMC_LIMIT"
TRACE_DMC_ERROR = "DMC_ERROR"

TRACE_BMS_PACKVOLTAGE = "PackVoltage" #[V]
TRACE_BMS_TEMP_DIE = "DieTemp" #[°C]
TRACE_BMS_STATUS_BITS = "StatusBits"
TRACE_BMS_CELL_VOLTAGE_MIN = "CellVoltage_Min"
TRACE_BMS_CELL_VOLTAGE_MAX = "CellVoltage_Max"
TRACE_BMS_CELL_VOLTAGE_MIN_ID = "CellID_Min"
TRACE_BMS_CELL_VOLTAGE_MAX_ID = "CellID_Max"


#not basic special traces
TRACE_ACCEL_X_ROT = TRACE_ACCEL_X + TRACE_POSTFIX_ROTATED
TRACE_ACCEL_Y_ROT = TRACE_ACCEL_Y + TRACE_POSTFIX_ROTATED
TRACE_ACCEL_Z_ROT = TRACE_ACCEL_Z + TRACE_POSTFIX_ROTATED
TRACE_GYRO_X_ROT = TRACE_GYRO_X + TRACE_POSTFIX_ROTATED
TRACE_GYRO_Y_ROT = TRACE_GYRO_Y + TRACE_POSTFIX_ROTATED
TRACE_GYRO_Z_ROT = TRACE_GYRO_Z + TRACE_POSTFIX_ROTATED

TRACE_ACCEL_X_CORRECTED = TRACE_ACCEL_X + TRACE_POSTFIX_CORRECTED
TRACE_ACCEL_Y_CORRECTED = TRACE_ACCEL_Y + TRACE_POSTFIX_CORRECTED
TRACE_ACCEL_Z_CORRECTED = TRACE_ACCEL_Z + TRACE_POSTFIX_CORRECTED
TRACE_ACCEL_X_CORRECTED_SLOPE = TRACE_ACCEL_X + TRACE_POSTFIX_CORRECTED + "_slope"
TRACE_ACCEL_Y_CORRECTED_SLOPE = TRACE_ACCEL_Y + TRACE_POSTFIX_CORRECTED + "_slope"
TRACE_ACCEL_Z_CORRECTED_SLOPE = TRACE_ACCEL_Z + TRACE_POSTFIX_CORRECTED + "_slope"
TRACE_ANGLE_OFFSET_PITCH = "AngleOffset_Pitch"

TRACE_POSTFIX_X = "_x"
TRACE_POSTFIX_Y = "_y"
TRACE_POSTFIX_Z = "_z"
TRACE_POSTFIX_COD_SENSOR = "_sen" #Sensor Frame
TRACE_POSTFIX_COD_BODY = "_bod" #Body Frame
TRACE_POSTFIX_COD_HOR = "_hor" #horizontiert/leveled Frame
TRACE_POSTFIX_COD_NAV = "_nav" #Navigation Frame
TRACE_POSTFIX_COD_GEO = "_geo" #Eath fixed Frame
TRACE_POSTFIX_REF = "_ref" #Referenc Trace
TRACE_POSTFIX_ESTIMATED = "_estimated" #Estimated Trace

TRACE_ENABLE_REF = "Enable_Ref"
TRACE_ENABLE_REF_VEL = "Enable_Ref_Velocity"
TRACE_ENABLE_REF_ROLL = "Enable_Ref_Roll"
TRACE_ENABLE_REF_PITCH = "Enable_Ref_Pitch"
TRACE_ENABLE_REF_YAW = "Enable_Ref_Yaw"
TRACE_ENABLE_REF_POSI = "Enable_Ref_Posi"
TRACE_ENABLE_REF_ALT = "Enable_Ref_Alt"

TRACE_ACCEL_X_SEN = TRACE_ACCEL_X + TRACE_POSTFIX_COD_SENSOR
TRACE_ACCEL_Y_SEN = TRACE_ACCEL_Y + TRACE_POSTFIX_COD_SENSOR
TRACE_ACCEL_Z_SEN = TRACE_ACCEL_Z + TRACE_POSTFIX_COD_SENSOR
TRACE_GYRO_X_SEN = TRACE_GYRO_X + TRACE_POSTFIX_COD_SENSOR
TRACE_GYRO_Y_SEN = TRACE_GYRO_Y + TRACE_POSTFIX_COD_SENSOR
TRACE_GYRO_Z_SEN = TRACE_GYRO_Z + TRACE_POSTFIX_COD_SENSOR

TRACE_ACCEL_X_BOD = TRACE_ACCEL_X + TRACE_POSTFIX_COD_BODY
TRACE_ACCEL_Y_BOD = TRACE_ACCEL_Y + TRACE_POSTFIX_COD_BODY
TRACE_ACCEL_Z_BOD = TRACE_ACCEL_Z + TRACE_POSTFIX_COD_BODY
TRACE_ACCEL_X_BOD_REF = TRACE_ACCEL_X + TRACE_POSTFIX_COD_BODY + TRACE_POSTFIX_REF
TRACE_ACCEL_Y_BOD_REF = TRACE_ACCEL_Y + TRACE_POSTFIX_COD_BODY + TRACE_POSTFIX_REF
TRACE_ACCEL_Z_BOD_REF = TRACE_ACCEL_Z + TRACE_POSTFIX_COD_BODY + TRACE_POSTFIX_REF
TRACE_GYRO_X_BOD = TRACE_GYRO_X + TRACE_POSTFIX_COD_BODY
TRACE_GYRO_Y_BOD = TRACE_GYRO_Y + TRACE_POSTFIX_COD_BODY
TRACE_GYRO_Z_BOD = TRACE_GYRO_Z + TRACE_POSTFIX_COD_BODY
TRACE_GYRO_X_BOD_REF = TRACE_GYRO_X + TRACE_POSTFIX_COD_BODY + TRACE_POSTFIX_REF
TRACE_GYRO_Y_BOD_REF = TRACE_GYRO_Y + TRACE_POSTFIX_COD_BODY + TRACE_POSTFIX_REF
TRACE_GYRO_Z_BOD_REF = TRACE_GYRO_Z + TRACE_POSTFIX_COD_BODY + TRACE_POSTFIX_REF

TRACE_ACCEL_X_HOR = TRACE_ACCEL_X + TRACE_POSTFIX_COD_HOR
TRACE_ACCEL_Y_HOR = TRACE_ACCEL_Y + TRACE_POSTFIX_COD_HOR
TRACE_ACCEL_Z_HOR = TRACE_ACCEL_Z + TRACE_POSTFIX_COD_HOR
TRACE_ACCEL_X_HOR_REF = TRACE_ACCEL_X + TRACE_POSTFIX_COD_HOR + TRACE_POSTFIX_REF
TRACE_ACCEL_Y_HOR_REF = TRACE_ACCEL_Y + TRACE_POSTFIX_COD_HOR + TRACE_POSTFIX_REF
TRACE_ACCEL_Z_HOR_REF = TRACE_ACCEL_Z + TRACE_POSTFIX_COD_HOR + TRACE_POSTFIX_REF
TRACE_GYRO_X_HOR = TRACE_GYRO_X + TRACE_POSTFIX_COD_HOR
TRACE_GYRO_Y_HOR = TRACE_GYRO_Y + TRACE_POSTFIX_COD_HOR
TRACE_GYRO_Z_HOR = TRACE_GYRO_Z + TRACE_POSTFIX_COD_HOR
TRACE_GYRO_X_HOR_REF = TRACE_GYRO_X + TRACE_POSTFIX_COD_HOR + TRACE_POSTFIX_REF
TRACE_GYRO_Y_HOR_REF = TRACE_GYRO_Y + TRACE_POSTFIX_COD_HOR + TRACE_POSTFIX_REF
TRACE_GYRO_Z_HOR_REF = TRACE_GYRO_Z + TRACE_POSTFIX_COD_HOR + TRACE_POSTFIX_REF
TRACE_VEL_X_HOR = TRACE_VEL_X + TRACE_POSTFIX_COD_HOR
TRACE_VEL_Y_HOR = TRACE_VEL_Y + TRACE_POSTFIX_COD_HOR
TRACE_VEL_Z_HOR = TRACE_VEL_Z + TRACE_POSTFIX_COD_HOR
TRACE_VEL_X_HOR_REF = TRACE_VEL_X + TRACE_POSTFIX_COD_HOR + TRACE_POSTFIX_REF
TRACE_VEL_Y_HOR_REF = TRACE_VEL_Y + TRACE_POSTFIX_COD_HOR + TRACE_POSTFIX_REF
TRACE_VEL_Z_HOR_REF = TRACE_VEL_Z + TRACE_POSTFIX_COD_HOR + TRACE_POSTFIX_REF
TRACE_ORIENTATION_X_HOR = TRACE_ORIENTATION_X + TRACE_POSTFIX_COD_HOR
TRACE_ORIENTATION_Y_HOR = TRACE_ORIENTATION_Y + TRACE_POSTFIX_COD_HOR
TRACE_ORIENTATION_Z_HOR = TRACE_ORIENTATION_Z + TRACE_POSTFIX_COD_HOR
TRACE_ORIENTATION_X_HOR_REF = TRACE_ORIENTATION_X + TRACE_POSTFIX_COD_HOR + TRACE_POSTFIX_REF
TRACE_ORIENTATION_Y_HOR_REF = TRACE_ORIENTATION_Y + TRACE_POSTFIX_COD_HOR + TRACE_POSTFIX_REF
TRACE_ORIENTATION_Z_HOR_REF = TRACE_ORIENTATION_Z + TRACE_POSTFIX_COD_HOR + TRACE_POSTFIX_REF

TRACE_ROLL_ANGLE_REF = TRACE_ROLL_ANGLE + TRACE_POSTFIX_REF
TRACE_PITCH_ANGLE_REF = TRACE_PITCH_ANGLE + TRACE_POSTFIX_REF
TRACE_YAW_ANGLE_REF = TRACE_YAW_ANGLE + TRACE_POSTFIX_REF

TRACE_ACCEL_X_NAV = TRACE_ACCEL_X + TRACE_POSTFIX_COD_NAV
TRACE_ACCEL_Y_NAV = TRACE_ACCEL_Y + TRACE_POSTFIX_COD_NAV
TRACE_ACCEL_Z_NAV = TRACE_ACCEL_Z + TRACE_POSTFIX_COD_NAV
TRACE_GYRO_X_NAV = TRACE_GYRO_X + TRACE_POSTFIX_COD_NAV
TRACE_GYRO_Y_NAV = TRACE_GYRO_Y + TRACE_POSTFIX_COD_NAV
TRACE_GYRO_Z_NAV = TRACE_GYRO_Z + TRACE_POSTFIX_COD_NAV
TRACE_VEL_X_NAV = TRACE_VEL_X + TRACE_POSTFIX_COD_NAV
TRACE_VEL_Y_NAV = TRACE_VEL_Y + TRACE_POSTFIX_COD_NAV
TRACE_VEL_Z_NAV = TRACE_VEL_Z + TRACE_POSTFIX_COD_NAV
TRACE_VEL_X_NAV_REF = TRACE_VEL_X + TRACE_POSTFIX_COD_NAV + TRACE_POSTFIX_REF
TRACE_VEL_Y_NAV_REF = TRACE_VEL_Y + TRACE_POSTFIX_COD_NAV + TRACE_POSTFIX_REF
TRACE_VEL_Z_NAV_REF = TRACE_VEL_Z + TRACE_POSTFIX_COD_NAV + TRACE_POSTFIX_REF
TRACE_ORIENTATION_X_NAV = TRACE_ORIENTATION_X + TRACE_POSTFIX_COD_NAV
TRACE_ORIENTATION_Y_NAV = TRACE_ORIENTATION_Y + TRACE_POSTFIX_COD_NAV
TRACE_ORIENTATION_Z_NAV = TRACE_ORIENTATION_Z + TRACE_POSTFIX_COD_NAV
TRACE_ORIENTATION_X_NAV_REF = TRACE_ORIENTATION_X + TRACE_POSTFIX_COD_NAV + TRACE_POSTFIX_REF
TRACE_ORIENTATION_Y_NAV_REF = TRACE_ORIENTATION_Y + TRACE_POSTFIX_COD_NAV + TRACE_POSTFIX_REF
TRACE_ORIENTATION_Z_NAV_REF = TRACE_ORIENTATION_Z + TRACE_POSTFIX_COD_NAV + TRACE_POSTFIX_REF
TRACE_POSI_X_HOR = TRACE_POSI_X + TRACE_POSTFIX_COD_HOR
TRACE_POSI_Y_HOR = TRACE_POSI_Y + TRACE_POSTFIX_COD_HOR
TRACE_POSI_Z_HOR = TRACE_POSI_Z + TRACE_POSTFIX_COD_HOR
TRACE_POSI_X_NAV = TRACE_POSI_X + TRACE_POSTFIX_COD_NAV
TRACE_POSI_Y_NAV = TRACE_POSI_Y + TRACE_POSTFIX_COD_NAV
TRACE_POSI_Z_NAV = TRACE_POSI_Z + TRACE_POSTFIX_COD_NAV
TRACE_POSI_X_NAV_REF = TRACE_POSI_X + TRACE_POSTFIX_COD_NAV + TRACE_POSTFIX_REF
TRACE_POSI_Y_NAV_REF = TRACE_POSI_Y + TRACE_POSTFIX_COD_NAV + TRACE_POSTFIX_REF
TRACE_POSI_Z_NAV_REF = TRACE_POSI_Z + TRACE_POSTFIX_COD_NAV + TRACE_POSTFIX_REF
TRACE_POSI_LAT_GEO = TRACE_POSI_LAT + TRACE_POSTFIX_COD_GEO
TRACE_POSI_LON_GEO = TRACE_POSI_LON + TRACE_POSTFIX_COD_GEO
TRACE_POSI_ALT_GEO = TRACE_POSI_ALT + TRACE_POSTFIX_COD_GEO
TRACE_POSI_LAT_GEO_REF = TRACE_POSI_LAT + TRACE_POSTFIX_COD_GEO + TRACE_POSTFIX_REF
TRACE_POSI_LON_GEO_REF = TRACE_POSI_LON + TRACE_POSTFIX_COD_GEO + TRACE_POSTFIX_REF
TRACE_POSI_ALT_GEO_REF = TRACE_POSI_ALT + TRACE_POSTFIX_COD_GEO + TRACE_POSTFIX_REF

TRACE_POSI_ERROR = "Posi_Error"
TRACE_LOSS = "Loss"



# Event Log Tags
TAG_IMU_TEMP = "imu.temp"
TAG_IMU_BIAS_TOTAL_X = "imu.g.bias.total.x"
TAG_IMU_BIAS_TOTAL_Y = "imu.g.bias.total.y"
TAG_IMU_BIAS_TOTAL_Z = "imu.g.bias.total.z"


TRACE_TO_UNITS = {
	TRACE_TIME : "s",
	TRACE_ACCEL_X : "g",
	TRACE_ACCEL_Y : "g",
	TRACE_ACCEL_Z : "g",
	TRACE_GYRO_X : "rad/s",
	TRACE_GYRO_Y : "rad/s",
	TRACE_GYRO_Z : "rad/s",
	TRACE_MAG_X : "mG",
	TRACE_MAG_Y : "mG",
	TRACE_MAG_Z : "mG",
	TRACE_SATCOUNT : "Count",
	TRACE_SENTENCE_COUNT : "Count",
	TRACE_CS_FAIL : "Count",
	TRACE_TIME_HOUR : "h",
	TRACE_TIME_MINUTES : "m",
	TRACE_TIME_SECONDS : "s",
	TRACE_HHMMSS : "",
	TRACE_DAY : "Day",
	TRACE_MONTH : "Month",
	TRACE_YEAR : "Year",
	TRACE_DDMMYY : "",
	TRACE_VELOCITY : "m/s",
	TRACE_VELOCITY_KMH : "kmh",
	TRACE_DISTANCE : "km",
	TRACE_LAT : "deg",
	TRACE_LON : "deg",
}


########## DATASET FEATURES ##########################

FEAUTRE_MOTOR_KV = "Motor_KV"
FEAUTRE_MOTOR_ID = "Motor_ID"
FEAUTRE_PROPELLER_ID = "Propeller_ID"
FEAUTRE_PROPELLER_DIAMETER = "Propeller_Diameter" #[in]
FEAUTRE_PROPELLER_PITCH = "Propeller_Diameter" #[deg]

FEATURE_THROTTLE = "Throttle" #[%]

FEATURE_MOTOR_TORQUE = "Motor_Torque" #[NM]
FEATURE_MOTOR_SPEED = "Motor_Speed" #[rpm]

FEATURE_DC_CURRENT = "DC_Current" #[A]
FEATURE_DC_VOLTAGE = "DC_Voltage" #[V]

FEATURE_AC_CURRENT = "AC_Current" #[A]
FEATURE_AC_PERIOD = "AC_Period" #[s] duration of period




CORNER_NUM = "num"
CORNER_T_START = "t_start"
CORNER_T_END = "t_end"
CORNER_T_CENTER = "t_center"
CORNER_POSITION_X = "position_x" #positon/location at t_center
CORNER_POSITION_Y = "position_y" #positon/location at t_center
CORNER_ISRIGHT = "isRight" #is Right corner
CORNER_LENGTH = "length" #length of corner
CORNER_ANGLE = "angle" #complete angle from entry to exit
CORNER_ANGLE_INTEGRATE = "angle_integrat" #angle trace integrated
CORNER_CENTER_ANGLE = "center_angle" #angle at corner center
CORNER_CENTER_SPEED = "center_speed" #speed at corner center
CORNER_BRAKE_DISTANCE = "brake_distance" #distance from center to brake point
CORNER_BRAKE_SPEED = "brake_speed" #speed at brake point
CORNER_CORRECT = "correct"
CORNER_CORRECT_DIST = "correct_dist" #distance from closest correct corner

TAG_TO_UNIT = {
	CORNER_NUM: "Num",
	CORNER_T_START : "s",
	CORNER_T_END : "s",
	CORNER_T_CENTER : "s",
	CORNER_POSITION_X : "m",
	CORNER_POSITION_Y : "m",
	CORNER_ISRIGHT : "",
	CORNER_LENGTH : "m",
	CORNER_ANGLE : "°",
	CORNER_ANGLE_INTEGRATE : "°",
	CORNER_CENTER_ANGLE : "°/m",
	CORNER_CENTER_SPEED : "°/m",
	CORNER_BRAKE_DISTANCE : "m",
	CORNER_BRAKE_SPEED : "km/h",
	CORNER_CORRECT : "",
	CORNER_CORRECT_DIST : "",
}

#Limits
TRACE_TO_LIMITS = {
	TRACE_VELOCITY : [0, 300],
	TRACE_LAT : [0, 360],
	TRACE_LON : [0, 360],
	TRACE_ACCEL_X : [-5, 5],
	TRACE_ACCEL_Y: [-5, 5],
	TRACE_ACCEL_Z: [-5, 5],
	TRACE_GYRO_X: [-600, 600],
	TRACE_GYRO_Y: [-600, 600],
	TRACE_GYRO_Z: [-600, 600],
	TRACE_MAG_X : [-2000, 2000],
	TRACE_MAG_Y: [-2000, 2000],
	TRACE_MAG_Z: [-2000, 2000],
}


def get_Unit(Tag):
	if(Tag in TRACE_TO_UNITS):
		return TRACE_TO_UNITS[Tag]
	if Tag in TAG_TO_UNIT:
		return TAG_TO_UNIT[Tag]
	else:
		return ""

def getText(Tag):

	return Tag

FEATURE_TO_TEXT = {}

def getFeature_Text(Tag, without_tag=False):
	braket_text = Tag
	if(Tag in TAG_TO_UNIT and without_tag):
		braket_text = get_Unit(Tag)
	if Tag in FEATURE_TO_TEXT:
		return "{}\n ({})".format(FEATURE_TO_TEXT[Tag], braket_text)
	else:
		return Tag







# Result Tags


TAG_T_START = "t_start"
TAG_T_END = "t_end"
TAG_CURRENT_PERIOD = "current_period"

