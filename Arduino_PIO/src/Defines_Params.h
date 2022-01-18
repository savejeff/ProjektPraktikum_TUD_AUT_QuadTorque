#pragma once




#define ENABLE_WATCHDOGTIMER


//5 seconds WDT
#define WDT_TIMEOUT (5 * 1000)


#ifndef BOARD_DEFINED
	
	// Sensors
	#define ENABLE_SENSOR_INA219 //Voltage Current Sensor 26V
	//#define ENABLE_SENSOR_INA190 //Shunt Voltage Sensor
	#define ENABLE_SENSOR_HX711 //Load Cell Amplifier
	//#define ENABLE_SENSOR_HX711_2 //Load Cell Amplifier

	// Actors
	#define ENABLE_ACTOR_ESC //PWM ESC/Brushless Motor
	

	//System ENABLES
	#define ENABLE_SENSOR
	#define ENABLE_CONFIGURE


#else
	//if Board is Defined extern:
#endif



#ifndef RELEASE_DEFINED

	// - - SENSOR ENABLES - - 
	#define ENABLE_SERIAL_OUT   //Enable Log msg to SerialOut

	#define ENABLE_PRINT_STATUS

	#define ENABLE_MONITOR_TIMESTAMP

	#define ENABLE_DEBUG
	

#else
	
	#define ENABLE_SERIAL_OUT

	#define ENABLE_PRINT_STATUS

#endif


#ifdef ENABLE_DEBUG
	//#define WAIT_4_SERIAL
	
	//#define DEBUG_SERCOM
	//#define DEBUG_MODE
	//#define DEBUG_CONFIGURE
	//#define DEBUG_SETTINGS

	#define DEBUG_ESC

#endif //ENABLE_DEBUG



#ifdef ENABLE_PRINT_STATUS
	#define ENABLE_PRINT_STATUS_SYSTEM
	#define ENABLE_PRINT_STATUS_GPIO
	#define ENABLE_PRINT_STATUS_SENSOR
#endif


#ifdef ENABLE_SERIAL_OUT

	#define ENABLE_SERIAL_OUT_TIMESTAMP //print Timestamp with Log

#endif // ENABLE_SERIAL_OUT



//Looptime [ms] -> Time between Loop excecutions
#define LOOPTIME_PRINTSTATS 1000
#define SAMPLETIME_SENSOR 10