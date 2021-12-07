#pragma once

#include <jOS.h>

#include "Defines_Params.h"



#define SERIAL0_BAUD SERIAL_BAUD_115200

#define SERIAL1_BAUD SERIAL_BAUD_115200
//#define SERIAL1_BAUD SERIAL_BAUD_460800



#ifdef BOARD_LEONARDO

	//SPI
	//#define ENABLE_SPI0
	#define PIN_SPI0_SCK 15
	#define PIN_SPI0_MISO 14
	#define PIN_SPI0_MOSI 16

	//I2C
	#define ENABLE_I2C0
	#define PIN_I2C0_SCL 3
	#define PIN_I2C0_SDA 2


	//Serial
	//Serial0
	#define ENABLE_SERIAL0
	#define Serial0 Serial
	
	//Serial1
	#define ENABLE_SERIAL1
	#define PIN_SERIAL1_RX 0 
	#define PIN_SERIAL1_TX 1 
	
	#define SerialOut Serial0
	

	#define PIN_LED_BUILTIN 6
	#define LED_BUILTIN_ON_LEVEL LOW
	
	#define PIN_BUTTON1 4
	#define BUTTON1_TRIGGER_LEVEL LOW

	#define PIN_ANALOG_IN_0 A0
	//#define PIN_ANALOG_IN_1 A1

	//#define PIN_DIGITAL_OUT_0 10


#endif //BOARD_LEONARDO

#ifdef BOARD_LEONARDO_ESC


	//SPI
	//#define ENABLE_SPI0
	#define PIN_SPI0_SCK 15
	#define PIN_SPI0_MISO 14
	#define PIN_SPI0_MOSI 16

	//I2C
	#define ENABLE_I2C0
	#define PIN_I2C0_SCL 3
	#define PIN_I2C0_SDA 2
	

	//Serial
	//Serial0
	#define ENABLE_SERIAL0
	#define Serial0 Serial
	
	//Serial1
	#define ENABLE_SERIAL1
	#define PIN_SERIAL1_RX 0 
	#define PIN_SERIAL1_TX 1 
	
	//#define SerialOut Serial0

	#define PIN_LED_BUILTIN 6
	#define LED_BUILTIN_ON_LEVEL LOW

	#define PIN_HX711_CLOCK 5
	#define PIN_HX711_DATA A1

	#define PIN_BUTTON1 4
	#define BUTTON1_TRIGGER_LEVEL LOW

	#define PIN_ANALOG_IN_0 A0

	//#define PIN_DIGITAL_OUT_0 10

	#define PIN_FRQ_IN0 7
	#define PIN_PWM_OUT_ESC 9
	
	#define PIN_ESC_PWR 8



#endif //BOARD_LEONARDO

#ifdef BOARD_UNO_ESC


	//SPI
	//#define ENABLE_SPI0
	#define PIN_SPI0_SCK PIN_SPI_SCK
	#define PIN_SPI0_MISO PIN_SPI_MISO
	#define PIN_SPI0_MOSI PIN_SPI_MOSI

	//I2C
	#define ENABLE_I2C0
	#define PIN_I2C0_SCL PIN_WIRE_SCL
	#define PIN_I2C0_SDA PIN_WIRE_SDA


	//Serial
	//Serial0
	#define ENABLE_SERIAL0
	#define Serial0 Serial
	
	//#define SerialOut Serial0

	#define PIN_LED_BUILTIN 13
	#define LED_BUILTIN_ON_LEVEL LOW

	// Motor Torque
	#define PIN_HX711_CLOCK 10
	#define PIN_HX711_DATA 9

	// Thrust Force 
	#define PIN_HX711_2_CLOCK 7
	#define PIN_HX711_2_DATA 6

	#define PIN_BUTTON1 4
	#define BUTTON1_TRIGGER_LEVEL LOW

	//#define PIN_ANALOG_IN_0 A0
	#define PIN_ANALOG_IN_1 A3

	//#define PIN_DIGITAL_OUT_0 10


	#define PIN_FRQ_IN0 2
	#define PIN_PWM_OUT_ESC 5
	
	#define PIN_ESC_PWR -1 //11


#endif //BOARD_UNO_ESC

#ifdef BOARD_MEGA
	
	//SPI
	#define PIN_SPI0_SCK SCK
	#define PIN_SPI0_MISO MISO
	#define PIN_SPI0_MOSI MOSI

	//I2C
	#define ENABLE_I2C0
	//#define PIN_I2C0_SCL 21 (allready defined)
	//#define PIN_I2C0_SDA 20 (allready defined)


	//Serial
	//Serial0
	#define ENABLE_SERIAL0
	#define Serial0 Serial

	//Serial1
	#define ENABLE_SERIAL1
	#define PIN_SERIAL1_RX 0 
	#define PIN_SERIAL1_TX 1 
	

	#define PIN_LED_BUILTIN LED_BUILTIN
	#define LED_BUILTIN_ON_LEVEL HIGH

	#define PIN_BUTTON1 7
	#define BUTTON1_TRIGGER_LEVEL LOW

	
	#define PIN_DIGITAL_OUT_0 10



#endif //BOARD_MEGA

