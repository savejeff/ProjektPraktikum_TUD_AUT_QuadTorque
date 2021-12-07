#pragma once

#include "Defines.h"


#include "global.h"

#ifdef ENABLE_SPI0
#endif // ENABLE_SPI0

#ifdef ENABLE_I2C0
extern jI2C_Hard I2C0;
#endif // ENABLE_I2C0


extern jSerialHard jSerial0;

#ifdef ENABLE_SERIAL1
extern jSerialHard jSerial1;
#endif // ENABLE_SERIAL1

#ifndef SerialOut
#define SerialOut jSerial0
#endif // SerialOut


void SERCOM_Module_Init();

void SERCOM_Module_Update();

void SERCOM_Module_End();

void SERCOM_Module_Flush();



char read_SerialInput();
bool SerialInput_available();
