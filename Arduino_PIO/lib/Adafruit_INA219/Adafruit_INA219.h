/*!
 * @file Adafruit_INA219.h
 *
 * This is a library for the Adafruit INA219 breakout board
 * ----> https://www.adafruit.com/products/904
 *
 * Adafruit invests time and resources providing this open source code,
 * please support Adafruit and open-source hardware by purchasing
 * products from Adafruit!
 *
 * Written by Kevin "KTOWN" Townsend for Adafruit Industries.
 *
 * BSD license, all text here must be included in any redistribution.
 *
 */

#pragma once 

#include <jOS.h>


/** default I2C address **/
#define INA219_ADDRESS (0x40) // 1000000 (A0+A1=GND)

/*!
 *   @brief  Class that stores state and functions for interacting with INA219
 *  current/power monitor IC
 */
class Adafruit_INA219 {
public:
	Adafruit_INA219(uint8_t addr = INA219_ADDRESS);
	void begin(jI2C *theWire);
	void setCalibration_32V_2A();
	void setCalibration_32V_1A();
	void setCalibration_16V_400mA();
	void setCalibration(float resistor, float current_range);
	float getBusVoltage_V();
	float getShuntVoltage_mV();
	float getCurrent_mA();
	float getCurrent_A();
	float getPower_W();
	void powerSave(bool on);

private:
	jI2C *_i2c;

	uint8_t ina219_i2caddr;
	uint32_t calVal;
	// The following multipliers are used to convert raw current and power
	// values to mA and mW, taking into account the current config settings
	float currentDivider_mA;
	float pwrMultiplier_mW;

	void init();
	void wireWriteRegister(uint8_t reg, uint16_t value);
	void wireReadRegister(uint8_t reg, uint16_t *value);
	int16_t getBusVoltage_raw();
	int16_t getShuntVoltage_raw();
	int16_t getCurrent_raw();
	int16_t getPower_raw();
};

