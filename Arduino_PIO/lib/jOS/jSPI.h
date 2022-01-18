#pragma once

#include "jDefines.h"


#define SPI_FRQ_10MHz 10E6
#define SPI_FRQ_1MHz 1E6
#define SPI_FRQ_4MHz 4E6
#define SPI_FRQ_7MHz 7E6
#define SPI_FRQ_500kHz 500E3
#define SPI_FRQ_100kHz 100E3
#define SPI_FRQ_10kHz 10E3


#define SPI_FRQ_DEFAULT SPI_FRQ_1MHz


enum SPI_BitOrder {
	SPI_BitOrder_LSBFIRST = 0,
	SPI_BitOrder_MSBFIRST = 1
};


//Mode          Clock Polarity (CPOL)   Clock Phase (CPHA)
	//SPI_MODE0             0                     0
	//SPI_MODE1             0                     1
	//SPI_MODE2             1                     0
	//SPI_MODE3             1                     1
enum SPI_DATAMODE {
	SPI_DATAMODE0 = 0x00,
	SPI_DATAMODE1 = 0x01,
	SPI_DATAMODE2 = 0x02,
	SPI_DATAMODE3 = 0x03
};


class jSPI
{

public:
	jSPI() { }
	virtual void begin() = 0;
	virtual void end() = 0;

	
	virtual void setBitOrder(SPI_BitOrder bitOrder) = 0;
	virtual void setDataMode(SPI_DATAMODE dataMode) = 0;
	virtual void setFrequency(uint32_t freq) = 0;

	virtual void beginTransaction() = 0;
	virtual void endTransaction(void) = 0;
	virtual void transfer(uint8_t * data, uint32_t size) = 0;
	virtual uint8_t transfer(uint8_t data) = 0;

	virtual void setCS(bool state) = 0;
};



#ifdef PLATFORM_AVR

#include "SPI.h"

class jSPI_Hard : public jSPI
{
protected:

	SPIClass* _spi = &SPI;
	uint8_t _pin_cs = -1;

	uint32_t _freq = SPI_FRQ_DEFAULT;
	SPI_BitOrder _bitOrder = SPI_BitOrder_MSBFIRST;
	SPI_DATAMODE _dataMode = SPI_DATAMODE0;


public:

	jSPI_Hard(SPIClass* _SPI, uint8_t pin_cs)
	{
		_spi = _SPI;
		_pin_cs = pin_cs;
	}
	void begin()
	{
		_spi->begin();
		pinMode(_pin_cs, OUTPUT);
		digitalWrite(_pin_cs, HIGH);
	}
	void end()
	{
		_spi->end();
	}

	void setBitOrder(SPI_BitOrder bitOrder)
	{
		_bitOrder = bitOrder;
	}
	void setDataMode(SPI_DATAMODE dataMode)
	{
		_dataMode = dataMode;
	}
	void setFrequency(uint32_t freq)
	{
		_freq = freq;
	}
	
	void beginTransaction()
	{
		if(_pin_cs >= 0)
			digitalWrite(_pin_cs, LOW);

				
		//#define LSBFIRST 0
		//#define MSBFIRST 1

		//#define SPI_MODE0 0x00
		//#define SPI_MODE1 0x04
		//#define SPI_MODE2 0x08
		//#define SPI_MODE3 0x0C

		uint8_t dm = SPI_MODE0;
		switch(_dataMode)
		{
			case SPI_DATAMODE0: dm = SPI_MODE0; break;
			case SPI_DATAMODE1: dm = SPI_MODE1; break;
			case SPI_DATAMODE2: dm = SPI_MODE2; break;
			case SPI_DATAMODE3: dm = SPI_MODE3; break;
		}

		_spi->beginTransaction(
			SPISettings(
				_freq, 
				(uint8_t) _bitOrder, 
				dm
			)
		);

	}
	void endTransaction(void)
	{
		_spi->endTransaction();
		
		if(_pin_cs >= 0)
			digitalWrite(_pin_cs, HIGH);
	}
	
	uint8_t transfer(uint8_t data)
	{
		return _spi->transfer(data);
	}

	void transfer(uint8_t * data, uint32_t size)
	{
		_spi->transfer(data, size);
	}

	
	void setCS(bool state) {
		digitalWrite(_pin_cs, state);
	}
	
};

#endif // PLATFORM_AVR
