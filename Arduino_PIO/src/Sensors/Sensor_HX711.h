#pragma once

/**************************
 *  Load Cell Amplifier   * 
 * ************************/

#include <jOS.h>

#include <jSensor.h>

#include <HX711.h>

//#define DEBUG_HX711

class Sensor_HX711_Class : public jSensor {
public:
  	Sensor_HX711_Class(int pin_clock, int pin_data)
		: jSensor("HX711")
	{ 
		_pin_clock = pin_clock;
		_pin_data = pin_data;
	}
  
	bool begin() override;

	void end() override {
		hx711.power_down();
	}

	void update() override;


	void print(const String& title) override { 
		Log("%s: raw=%ld", title.c_str(), value);
	}
	
	void print() { this->print(this->name);	}

	uint32_t getValue() {
		return value;
	}

	void Calib_Zero()
	{
		calib_zero += value;
	}

protected:

	byte _pin_data;
	byte _pin_clock;
	byte _gain = 128;
	
	HX711 hx711;

    uint32_t read();

	uint16_t sampletime = 100;

	float cutofffrq_lowpass = 1.0f;


	uint32_t calib_zero = 0;


	ulong lasttime_update = 0;
	uint32_t value = 0;

};
