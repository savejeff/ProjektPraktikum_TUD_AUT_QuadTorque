#pragma once

//#include <jOS.h>
#include <jCommon.h>
#include <jSystem.h>

#define I2C_SPEED_FAST 400000L
#define I2C_SPEED_NORMAL 100000L
#define I2C_SPEED_HALF (I2C_SPEED_NORMAL / 2)
#define I2C_SPEED_FORTH (I2C_SPEED_NORMAL / 4)


#define I2C_FRQ_DEFAULT I2C_SPEED_NORMAL


class jI2C
{

public:
	jI2C() { }
	virtual void begin() = 0;
	virtual void end() = 0;

	
	virtual void setFrequency(uint32_t freq) = 0;

	virtual void beginTransmission(uint8_t addr) = 0;
	virtual uint8_t endTransmission(bool stopBit) = 0;
    virtual uint8_t endTransmission(void) = 0;

    virtual uint8_t requestFrom(uint8_t address, size_t quantity, bool stopBit) = 0;
    virtual uint8_t requestFrom(uint8_t address, size_t quantity) = 0;

    virtual size_t write(uint8_t data) = 0;
    virtual size_t write(const uint8_t * data, size_t quantity) = 0;

	virtual byte read(void) = 0;

	virtual bool available() {
		return true;
	}
};



#if defined(PLATFORM_AVR) || defined(PLATFORM_SAMD) || defined(PLATFORM_STM32) || defined(PLATFORM_RP2040)

#include "Wire.h"


class jI2C_Hard : public jI2C
{
protected:

	TwoWire* _i2c = &Wire;
	uint32_t _freq = I2C_FRQ_DEFAULT;

public:

	jI2C_Hard(TwoWire* I2C)
	{
		_i2c = I2C;
	}
	
	jI2C_Hard(TwoWire* I2C, int8_t pin_sda, int8_t pin_scl)
	{
		_i2c = I2C;
	}

	void begin()
	{
		_i2c->begin();
	}
	void end()
	{
		_i2c->end();
	}

	
	void setFrequency(uint32_t freq)
	{
		_freq = freq;
		_i2c->setClock(freq);
	}

	void beginTransmission(uint8_t addr)
	{
		_i2c->beginTransmission(addr);
	}
	uint8_t endTransmission(bool stopBit)
	{
		return _i2c->endTransmission(stopBit);
	}
    uint8_t endTransmission(void)
	{
				
		// Errors:
		//  0 : Success
		//  1 : Data too long
		//  2 : NACK on transmit of address
		//  3 : NACK on transmit of data
		//  4 : Other error
		return _i2c->endTransmission();
	}

    uint8_t requestFrom(uint8_t address, size_t quantity, bool stopBit)
	{
		//return _i2c->requestFrom(address, quantity, stopBit);
		return _i2c->requestFrom(address, (uint8_t) quantity, (uint8_t) stopBit);
	}
    uint8_t requestFrom(uint8_t address, size_t quantity)
	{
		return _i2c->requestFrom(address, quantity);
	}

    size_t write(uint8_t data)
	{
		return _i2c->write(data);
	}
    size_t write(const uint8_t * data, size_t quantity)
	{
		return _i2c->write(data, quantity);
	}

	byte read(void)
	{
		return _i2c->read();
	}
	
};

#endif 