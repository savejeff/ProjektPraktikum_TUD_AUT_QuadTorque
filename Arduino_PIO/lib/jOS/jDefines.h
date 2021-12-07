#pragma once

#include "jCommon.h"

//#include <vector>
//#include "IPAddress.h"
//#include "time.h"



/*

// TEENSYDUINO has a port of Dean Camera's ATOMIC_BLOCK macros for AVR to ARM Cortex M3.
#define HAS_ATOMIC_BLOCK (defined(ARDUINO_ARCH_AVR) || defined(TEENSYDUINO))

// Whether we are running on either the ESP8266 or the ESP32.
#define ARCH_ESPRESSIF (defined(ARDUINO_ARCH_ESP8266) || defined(ARDUINO_ARCH_ESP32))

// Whether we are actually running on FreeRTOS.
#define IS_FREE_RTOS defined(ARDUINO_ARCH_ESP32)

// Define macro designating whether we're running on a reasonable
// fast CPU and so should slow down sampling from GPIO.
#define FAST_CPU \
    ( \
    ARCH_ESPRESSIF || \
    defined(ARDUINO_ARCH_SAM)     || defined(ARDUINO_ARCH_SAMD) || \
    defined(ARDUINO_ARCH_STM32)   || defined(TEENSYDUINO) \
    )

// https://arduino.github.io/arduino-cli/0.19/platform-specification/#hardware-folders-structure

#define PLATFORM_ESP32 defined(ARDUINO_ARCH_ESP32)
#define PLATFORM_STM32 defined(ARDUINO_ARCH_STM32)
#define PLATFORM_SAMD defined(ARDUINO_ARCH_SAMD)
#define PLATFORM_AVR defined(ARDUINO_ARCH_AVR)
#define PLATFORM_PICO defined(ARDUINO_ARCH_RP2040)

*/


#ifndef MIN
#define MIN(a,b) ((a)<(b)?(a):(b))
#endif
#ifndef MAX
#define MAX(a,b) ((a)>(b)?(a):(b))
#endif

#define LIMIT(LOWER, X, UPPER) ((X)<(LOWER)?(LOWER):((X)>(UPPER)?(UPPER):(X)))
#define median3(a,b,c) (MAX(MIN(a,b), MIN(MAX(a,b),c)))
#define MAP(value, FROM_MIN, FROM_MAX, TO_LOW, TO_HIGH) (map(LIMIT(FROM_MIN, value, FROM_MAX), FROM_MIN, FROM_MAX, TO_LOW, TO_HIGH))

#ifndef ULONG_MAX
#define ULONG_MAX 0xFFFFFFFF
#endif


#define EXECUTE_EVERY(ms) { \
	static ulong _last_time = 0; \
	if (millis() - _last_time > (ms)) \
	{ \
		_last_time = millis();\

#define EXECUTE_EVERY2(ms) { \
	static ulong _last_time = 0; \
	if (millis() - _last_time > (ms)) { \
		if(millis() - _last_time > 2 * ms) _last_time = millis(); \
		else _last_time += (ms); \

#define EXECUTE_EVERY2_NAME(last_time_variable, ms) { \
	if (millis() - last_time_variable > (ms)) { \
		if(millis() - last_time_variable > 2 * ms) last_time_variable = millis(); \
		else last_time_variable += (ms); \

#define EXECUTE_EVERY_END }}
#define EXECUTE_EVERY_RESET _last_time = millis();

//tracks microseconds time between STARTX and ENDX. result in param dt
#define TRACK_DT_MICROS_START0 ulong _tm0s = micros();
#define TRACK_DT_MICROS_END0(dt) ulong _tm0e = micros(); int dt = (_tm0s > _tm0e) ? (0xFFFFFFFF - _tm0s) + _tm0e : _tm0e - _tm0s;

//tracks miliseconds time between STARTX and ENDX. result in param dt
#define TRACK_DT_MILLIS_START0 ulong _t0s = millis();
#define TRACK_DT_MILLIS_END0(dt) ulong _t0e = millis(); int dt = _t0e - _t0s;



#define const_g 9.81


#define mm_2_m 1e-3
#define cm_2_m 1e-2
#define ns_2_ms 1e-6
#define ms_2_s 1e-3
#define s_2_h 3600
#define s_2_ms 1000


#define PI		  3.1415926535897932384626433832795
//#define HALF_PI	 1.5707963267948966192313216916398
//#define TWO_PI	  6.283185307179586476925286766559
//#define DEG_TO_RAD  0.017453292519943295769236907684886
//#define RAD_TO_DEG  57.295779513082320876798154814105
//#define EULER	   2.718281828459045235360287471352
#define CONST_G 9.81f


//FACTOR TIME
#define FACTOR_s_2_us (1000 * 1000)
#define FACTOR_min_2_s (60)
#define FACTOR_hour_2_s (3600)
#define FACTOR_s_2_ms (1000)
#define FACTOR_s_2_min (1.0f / 60.0f)
#define FACTOR_s_2_hour (1.0f / 3600.0f)
#define FACTOR_min_2_ms (1000 * 60)
#define FACTOR_hour_2_ms (1000 * 3600)
#define FACTOR_ms_2_s 1e-3f
#define FACTOR_ms_2_us (1000)
#define FACTOR_ms_2_ns (1000*1000)
#define FACTOR_us_2_s (1.0 / (1e+6))

//FACTOR GEOMETRIC
#define FACTOR_MPS_2_KMH 3.6f
#define FACTOR_KMH_2_MPS (1.0f/FACTOR_MPS_2_KMH)
#define FACTOR_G_2_MPSS 9.81f
#define FACTOR_MPSS_2_G (1.0f/FACTOR_G_2_MPSS)
#define FACTOR_M_2_KM 1e-3
#define FACTOR_deg_2_rad 0.017453292519943295769236907684886
#define FACTOR_rad_2_deg 57.295779513082320876798154814105

//FACTOR Electric
#define FACTOR_Ah_2_mAh 1000.0f
#define FACTOR_A_2_mA 1000.0f
#define FACTOR_mA_2_A (1.0f/1000.0f)
#define FACTOR_mAh_2_As 3.6f
#define FACTOR_As_2_mAh (1.0f / FACTOR_mAh_2_As)
#define FACTOR_As_2_Ah (1.0f / (3.6f * 1000.0f))
#define FACTOR_mW_2_W (1.0f / 1000.0f)


