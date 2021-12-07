#pragma once

#include "jDefines.h"
#include "jSystem.h"

#define jStream Stream

#define SERIAL_BAUD_9600 9600
#define SERIAL_BAUD_115200 115200
#define SERIAL_BAUD_230400 230400
#define SERIAL_BAUD_460800 460800
//#define SERIAL_BAUD_921600 9021600

enum jSerial_DataBits {
	jSERIAL_DATABITS_7,
	jSERIAL_DATABITS_8
};

enum jSerial_StopBits {
	jSERIAL_STOPBITS_1,
	jSERIAL_STOPBITS_2
};

enum jSerial_Parity {
	jSERIAL_PARITY_NONE,
	jSERIAL_PARITY_EVEN,
	jSERIAL_PARITY_ODD
};

/*

#define SERIAL_5N1 0x8000010
#define SERIAL_6N1 0x8000014
#define SERIAL_7N1 0x8000018
#define SERIAL_8N1 0x800001c
#define SERIAL_5N2 0x8000030
#define SERIAL_6N2 0x8000034
#define SERIAL_7N2 0x8000038
#define SERIAL_8N2 0x800003c
#define SERIAL_5E1 0x8000012
#define SERIAL_6E1 0x8000016
#define SERIAL_7E1 0x800001a
#define SERIAL_8E1 0x800001e
#define SERIAL_5E2 0x8000032
#define SERIAL_6E2 0x8000036
#define SERIAL_7E2 0x800003a
#define SERIAL_8E2 0x800003e
#define SERIAL_5O1 0x8000013
#define SERIAL_6O1 0x8000017
#define SERIAL_7O1 0x800001b
#define SERIAL_8O1 0x800001f
#define SERIAL_5O2 0x8000033
#define SERIAL_6O2 0x8000037
#define SERIAL_7O2 0x800003b
#define SERIAL_8O2 0x800003f
*/

class jSerial
	: public jStream
{
public:
	jSerial() { }

	//void begin(unsigned long baud, uint32_t config=SERIAL_8N1, int8_t rxPin=-1, int8_t txPin=-1, bool invert=false, unsigned long timeout_ms = 20000UL);
	virtual void begin() = 0;
	virtual void end() = 0;


	virtual void updateBaudRate(unsigned long baud) = 0;
	//uint32_t baudRate();
	//size_t setRxBufferSize(size_t);

	//operator bool() const;

	//virtual uint16_t available(void) = 0;
	virtual int available(void) = 0;
	//int availableForWrite(void);
	
	virtual int peek(void) {
		return 0;
	}

	//read single byte from serial input / rx buffer
	//virtual uint8_t read(void) = 0;
	virtual int read(void) = 0;
	
	//writes tx buffer out
	//virtual void flush(void) = 0;
	
	//writes to Serial. 
	//returns length of written. 0 if failed. 1 if success
	virtual size_t write(uint8_t c) = 0;
	
	//returns length of written. 0 if failed. len of data send to Serial
	virtual size_t write(const uint8_t *buffer, size_t size) {
		for(size_t i = 0; i < size; i++)
			if(!write(buffer[i]))
				return i;
		return size;
	}

	inline size_t write(const char * s)
	{
		return write((uint8_t*) s, strlen(s));
	}
	inline size_t write(const char *buffer, size_t size)
	{
		return write((const uint8_t *) buffer, size);
	}


	virtual size_t printf(const char * format, ...)	__attribute__ ((format (printf, 2, 3)));
	//size_t print(const __FlashStringHelper *);
	virtual size_t print(const String &s)
	{
		return write(s.c_str(), s.length());
	}

	//size_t print(const char[]);
	virtual size_t print(char c)
	{
		return write(c);
	}

	using Print::print;

	//size_t print(unsigned char, int = DEC);
	//size_t print(int, int = DEC);
	//size_t print(unsigned int, int = DEC);
	//size_t print(long, int = DEC);
	//size_t print(unsigned long, int = DEC);
	//size_t print(double, int = 2);
	//size_t print(const Printable&);
	//size_t print(struct tm * timeinfo, const char * format = NULL);

	//size_t println(const __FlashStringHelper *);
	//virtual size_t println(const String &s);
	//virtual size_t println(const char[]);
	//size_t println(char);
	//size_t println(unsigned char, int = DEC);
	//size_t println(int, int = DEC);
	//size_t println(unsigned int, int = DEC);
	//size_t println(long, int = DEC);
	//size_t println(unsigned long, int = DEC);
	//size_t println(double, int = 2);
	//size_t println(const Printable&);
	//size_t println(struct tm * timeinfo, const char * format = NULL);
	//size_t println(void);
	
};



#ifdef PLATFORM_AVR

#ifdef USBCON
#define HAS_SERIAL_USB
#endif

class jSerialHard : public jSerial
{
protected:
	Stream* stream = nullptr;
	HardwareSerial* ser = nullptr;
#ifdef HAS_SERIAL_USB
	Serial_* serUSB = nullptr;
	bool is_USB = false;
#endif // HAS_SERIAL_USB

public:
	jSerialHard(HardwareSerial& serial) 
	: ser(&serial)
	{ 
		stream = ser;
	}
	
	jSerialHard(HardwareSerial& serial, int8_t txPin, int8_t rxPin) 
	: ser(&serial)
	{ 
		stream = ser;
		//_pin_tx = txPin;
		//_pin_rx = rxPin;
	}
	
#ifdef HAS_SERIAL_USB
	jSerialHard(Serial_& serial) 
	: serUSB(&serial)
	{ 
		stream = serUSB;
		is_USB = true;
	}
#endif // HAS_SERIAL_USB

	//void begin(unsigned long baud, uint32_t config=SERIAL_8N1, int8_t rxPin=-1, int8_t txPin=-1, bool invert=false, unsigned long timeout_ms = 20000UL);
	void begin() {
		begin(SERIAL_BAUD_115200);
	}
	
	void begin(ulong baud) {
#ifdef HAS_SERIAL_USB
		if(is_USB)
			serUSB->begin(baud);
		else
#endif // HAS_SERIAL_USB
			ser->begin(baud);
	}

	void end() {
#ifdef HAS_SERIAL_USB
		if(is_USB)
			serUSB->end();
		else
#endif // HAS_SERIAL_USB
			ser->end();
	}

	void updateBaudRate(unsigned long baud)
	{
		begin(baud);
	}
	//uint32_t baudRate();
	//size_t setRxBufferSize(size_t);

	//operator bool() const;

	//uint16_t available(void) {
	int available(void) {
		return stream->available();
	}
	//int availableForWrite(void);
	
	int peek(void) override {
		return stream->peek();
	}

	//read single byte from serial input / rx buffer
	//uint8_t read(void) {
	int read(void) {
		return stream->read();
	}
	
	//writes tx buffer out
	void flush(void) {
		stream->flush();
	}
	
	//writes to Serial. 
	//returns length of written. 0 if failed. 1 if success
	size_t write(uint8_t c) {
		return stream->write(c);
	}
	
	//returns length of written. 0 if failed. len of data send to Serial
	size_t write(const uint8_t *buffer, size_t size) override {
		return stream->write(buffer, size);
	}

};


#endif // PLATFORM_AVR
