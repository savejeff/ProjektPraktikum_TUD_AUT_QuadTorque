#pragma once

#include "global.h"

#ifdef PLATFORM_AVR
#define GPIO_ANALOG_RESOLUTION 10
#else
#define GPIO_ANALOG_RESOLUTION 12
#endif // 


#define GPIO_ANALOG_MAX_VALUE (1<<GPIO_ANALOG_RESOLUTION)
//#define GPIO_ANALOG_MAX_VALUE 0xFFFF


void GPIOModule_Init();

void GPIOModule_Update();

void GPIOModule_PrintStatus();

void GPIOModule_End();


bool Button1_isDown();
bool Button2_isDown();

void setDigitalOut0(bool state);

float getAnalogIn0(); //factor [0 - 1] of Analog input level between 0V and Sys Volt/Analog Ref Voltage
float getAnalogIn0_Volt(); //Analog Voltage at Analog Input 0

float getAnalogIn1(); //factor [0 - 1] of Analog input level between 0V and Sys Volt/Analog Ref Voltage
float getAnalogIn1_Volt(); //Analog Voltage at Analog Input 1

void setAnalogOut0(float v);

