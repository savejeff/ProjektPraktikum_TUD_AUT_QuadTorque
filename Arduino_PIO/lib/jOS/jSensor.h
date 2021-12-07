#pragma once

#include <jDefines.h>


class jSensor
{
protected: 

	String name;
	bool initialized = false;

public :
	


    jSensor() {
		
	}

	jSensor(String name)
    {
        this->name = name;
    }

	virtual bool begin()
	{
		initialized = true;
		return true;
	}

	virtual void end()
	{

	}

	virtual void update() { }


	virtual void reset() { }


	virtual void print(const String& title) { }
	
	/*
	void print()
	{
		print(this->name);
	}
	*/
	

};


//Bus based sensor connected over I2C and SPI communcation based on register read and writes
class jSensorBus : public jSensor {
	
protected:
	virtual bool Bus_writeByte(uint8_t subAddress, uint8_t data);
	virtual bool Bus_writeBytes(uint8_t subAddress, uint8_t* data, uint8_t count);
	virtual uint8_t Bus_readByte(uint8_t subAddress);
	virtual uint8_t Bus_readBytes(uint8_t subAddress, uint8_t* dest, uint8_t count);

	bool read_bytes(uint8_t reg, uint8_t* data, uint8_t count);
	bool write_bytes(uint8_t reg, uint8_t* data, uint8_t count);

	uint16_t  read16(uint8_t reg);
	bool read16(uint8_t reg, uint16_t& res);
	bool write16(uint8_t reg, uint16_t val);

	uint8_t read_reg(uint8_t reg);
	bool write_reg(uint8_t reg, uint8_t val);

	uint8_t read_reg_mask(uint8_t reg, uint8_t mask);
	bool read_reg_bit(uint8_t reg, uint8_t bit_index);

	uint8_t write_reg_mask(uint8_t reg, uint8_t mask, uint8_t value);
	void write_reg_set_bit(uint8_t reg, uint8_t val);
	void write_reg_reset_bit(uint8_t reg, uint8_t val);

};

#include <jI2C.h>

class jSensorI2C : public jSensorBus {

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

    jSensorI2C(String name, jI2C* _ji2c, uint8_t addr)
	{
		this->name = name;
		_i2c = _ji2c;
		DEVICE_ADDR = addr;
	}


	bool begin() { 
		jSensor::begin();

		return true; 
	}

	void print(String title) {}

	void printReg(String name, uint8_t reg);

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





#include <jSPI.h>


class jSensorSPI : public jSensorBus {

protected:

	jSPI* _ThisSPI;

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

    jSensorSPI(String name, jSPI* _jspi)
	{
		this->name = name;
		_ThisSPI = _jspi;
	}

	bool begin() { 
		jSensor::begin();
		return true; 
	}

	void print(String title) {}

	void printReg(String name, uint8_t reg);

};
