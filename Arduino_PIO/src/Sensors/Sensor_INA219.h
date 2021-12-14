#pragma once 

#include <jOS.h>


/** default I2C address **/
#define INA219_ADDRESS (0x40) // 1000000 (A0+A1=GND)


class Sensor_INA219_Class {
public:
	Sensor_INA219_Class(jI2C *theWire, uint8_t addr = INA219_ADDRESS);
	
	void begin();
	void end(); //shuts down sensor to save power

	//possible values: 1 (0.5ms), 2 (1ms), 4 (2ms), 8 (4ms), 16 (8ms), 32 (17ms), 64 (34ms), 128 (68ms)
	void setMultisampleMode(uint8_t sample_count);
	
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

	uint8_t multisample_mode;
	uint8_t ina219_i2caddr;
	uint32_t calVal;
	// The following multipliers are used to convert raw current and power
	// values to mA and mW, taking into account the current config settings
	float currentDivider_mA;
	float pwrMultiplier_mW;

	void wireWriteRegister(uint8_t reg, uint16_t value);
	void wireReadRegister(uint8_t reg, uint16_t *value);
	int16_t getBusVoltage_raw();
	int16_t getShuntVoltage_raw();
	int16_t getCurrent_raw();
	int16_t getPower_raw();
};

