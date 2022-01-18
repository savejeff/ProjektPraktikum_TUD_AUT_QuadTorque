#pragma once

#include "jDefines.h"
#include "jSystem.h"
#include "jHelp.h"


class jDevice
{
protected: 

	String name = "";
	bool initialized = false;

public :

    jDevice() {
		
	}

	jDevice(const String& name)
    {
        this->name = name;
    }

	virtual bool begin()
	{
		initialized = true;
		return true;
	}

	virtual void end() { }

	virtual void update() { }

	virtual void reset() { }

    void print()
	{
		print(this->name);
	}

	virtual void print(const String& title) { }

};


//Bus based sensor connected over I2C and SPI communcation based on register read and writes
class jDeviceBus : public jDevice {
	
protected:
	
	//TODO fix virtual definitions
	virtual bool Bus_writeByte(uint8_t subAddress, uint8_t data) = 0;
	virtual bool Bus_writeBytes(uint8_t subAddress, uint8_t* data, uint8_t count) = 0;
	virtual uint8_t Bus_readByte(uint8_t subAddress) = 0;
	virtual uint8_t Bus_readBytes(uint8_t subAddress, uint8_t* dest, uint8_t count)  = 0;

	virtual bool read_bytes(uint8_t reg, uint8_t* data, uint8_t count);
	virtual bool write_bytes(uint8_t reg, uint8_t* data, uint8_t count);

	virtual uint16_t  read16(uint8_t reg);
	virtual bool read16(uint8_t reg, uint16_t& res);
	virtual bool write16(uint8_t reg, uint16_t val);

	virtual uint8_t read_reg(uint8_t reg);
	virtual bool write_reg(uint8_t reg, uint8_t val);

	virtual uint8_t read_reg_mask(uint8_t reg, uint8_t mask);
	virtual bool read_reg_bit(uint8_t reg, uint8_t bit_index);

	virtual uint8_t write_reg_mask(uint8_t reg, uint8_t mask, uint8_t value);
	virtual void write_reg_set_bit(uint8_t reg, uint8_t val);
	virtual void write_reg_reset_bit(uint8_t reg, uint8_t val);
		
	void printReg(String name, uint8_t reg)
	{
		byte val = read_reg(reg);

		//LogD("%s %s", name, sprintBits(val).c_str());
		LogD("REG %45s: %02X - b%s", name.c_str(), val, sprintBits(val).c_str());
	}

	void printRegBit(String name, uint8_t reg, uint8_t bit)
	{
		uint8_t val = read_reg(reg);
		bool bit_val = (val & (1 << bit)) != 0;
		
		LogD("REG %45s: b%s -> %d", 
			name.c_str(), 
			sprintBits(val).c_str(), 
			bit_val
		);
	}

public:
	jDeviceBus(String name)
		:jDevice(name)
	{

	};
/*	
	jDeviceBus()
		:jDevice()
	{
		
	};
*/
};

#include "jI2C.h"

class jDeviceI2C : public jDeviceBus {

protected:

	
	jI2C* _i2c;


	byte DEVICE_ADDR;

	bool I2C_writeByte(uint8_t address, uint8_t subAddress, uint8_t data);
	bool I2C_writeBytes(uint8_t address, uint8_t subAddress, uint8_t* data, uint8_t count);
	uint8_t I2C_readByte(uint8_t address, uint8_t subAddress);
	uint8_t I2C_readBytes(uint8_t address, uint8_t subAddress, uint8_t* dest, uint8_t count);
	
	bool Bus_writeByte(uint8_t subAddress, uint8_t data) override;
	bool Bus_writeBytes(uint8_t subAddress, uint8_t* data, uint8_t count) override;
	uint8_t Bus_readByte(uint8_t subAddress) override;
	uint8_t Bus_readBytes(uint8_t subAddress, uint8_t* dest, uint8_t count) override;
	

	uint8_t bus_error;

	volatile bool initialized;

public:

    jDeviceI2C(String name, jI2C* _ji2c, uint8_t addr)
	: jDeviceBus(name)
	{
		//this->name = name;
		_i2c = _ji2c;
		DEVICE_ADDR = addr;
	}


	bool begin() { return true; }

	void print(String title) {}


	enum BUS_ERROR_TYPES {
		BUS_NO_ERROR,
		DATA_TO_LONG,
		NACK_ON_ADDR,
		NACK_ON_DATA,
		OTHER
	};

	uint8_t getBusError(void);
		// If any library command fails, you can retrieve an extended
		// error code using this command. Errors are from the wire library: 
		// 0 = Success
		// 1 = Data too long to fit in transmit buffer
		// 2 = Received NACK on transmit of address
		// 3 = Received NACK on transmit of data
		// 4 = Other error

};





#include "jSPI.h"


class jDeviceSPI : public jDeviceBus {

protected:

	jSPI* _jSPI;

	void Bus_writeBytes(uint8_t* data, uint8_t count);
	byte Bus_writeByte(uint8_t data);
	
	//First sends TX data then reads RX data
	void Bus_WriteReadByte(uint8_t* dataTX, uint16_t len_TX, uint8_t* dataRX, uint16_t len_RX);
	
	bool Bus_writeByte(uint8_t subAddress, uint8_t data) override;
	bool Bus_writeBytes(uint8_t subAddress, uint8_t* data, uint8_t count) override;
	uint8_t Bus_readByte(uint8_t subAddress) override;
	uint8_t Bus_readBytes(uint8_t subAddress, uint8_t* dest, uint8_t count) override;
	
	

	uint8_t bus_error;

	volatile bool initialized;

public:

    jDeviceSPI(String name, jSPI* _jspi)
		: jDeviceBus(name)
	{
		//this->name = name;
		this->_jSPI = _jspi;
	}

	bool begin() { return true; }

	void print(String title) {}

	void printReg(String name, uint8_t reg);

};
