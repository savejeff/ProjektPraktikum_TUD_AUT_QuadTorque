#include "SERCOM_Module.h"

#include "global.h"


#ifdef ENABLE_I2C0
#if defined(PIN_I2C0_SDA) || defined(PIN_I2C0_SCL)
jI2C_Hard I2C0(&Wire, PIN_I2C0_SDA, PIN_I2C0_SCL);
#else
jI2C_Hard I2C0(&Wire);
#endif 

#endif // ENABLE_I2C0


jSerialHard jSerial0(Serial0);

#ifdef ENABLE_SERIAL1
#if defined(PIN_SERIAL1_TX) && defined(PIN_SERIAL1_TX)
jSerialHard jSerial1(Serial1, PIN_SERIAL1_TX, PIN_SERIAL1_RX);
#else
jSerialHard jSerial1(Serial1);
#endif 
#endif // ENABLE_SERIAL1

#ifdef ENABLE_SPI0

#endif // ENABLE_SPI0


void process_SerialInput();


void SERCOM_Module_Init()
{

#ifdef ENABLE_SERIAL0
	jSerial0.begin(SERIAL0_BAUD);
#elif defined(SERIAL0_RX) && defined(SERIAL0_TX)
	pinMode(SERIAL1_RX, OUTPUT);
	pinMode(SERIAL1_TX, OUTPUT);
	digitalWrite(SERIAL1_RX, LOW);
	digitalWrite(SERIAL1_TX, LOW);
#endif // ENABLE_SERIAL0

#ifdef ENABLE_SERIAL1
	jSerial1.begin(SERIAL1_BAUD);
#elif defined(SERIAL1_RX) && defined(SERIAL1_TX)
	pinMode(SERIAL1_RX, OUTPUT);
	pinMode(SERIAL1_TX, OUTPUT);
	digitalWrite(SERIAL1_RX, LOW);
	digitalWrite(SERIAL1_TX, LOW);
#endif // ENABLE_SERIAL1


#ifdef ENABLE_SERIAL_OUT
#ifdef WAIT_4_SERIAL
	while(!SerialOut.available())
	{
		delay(500);
		SerialOut.print(".");
	}
	while(SerialOut.available())
		SerialOut.read();
#endif //WAIT_4_SERIAL
#endif // ENABLE_SERIAL_OUT
	
	Log("ser.state: init");
	
	
#ifdef ENABLE_I2C0
	I2C0.begin();
	//I2C0.setFrequency(I2C_SPEED_NORMAL);
	I2C0.setFrequency(I2C_SPEED_FAST);
#endif // ENABLE_I2C0

#ifdef ENABLE_SPI0
	//SPI
	SPI.begin();
	//SPI.begin(PIN_SPI0_SCK, PIN_SPI0_MISO, PIN_SPI0_MOSI, -1);

#endif // ENABLE_SPI0

	//delay(1000);
	Log("ser.state: init done");
}


void SERCOM_Module_Update()
{
	static ulong last_time_ser_input = millis();
	
#ifdef ENABLE_SERIAL_OUT
	while(jSerial0.available())
	{
		write_SerialInput((char) jSerial0.read());
		last_time_ser_input = millis();
	}
#endif // ENABLE_SERIAL_OUT	

	//wait some before processing ser input if more is comming
	if(millis() - last_time_ser_input > 100)
	{
		process_SerialInput();
	}
}

void SERCOM_Module_End()
{
	Log("ser.state: end");

#ifdef ENABLE_SERIAL1
	jSerial1.flush();
	jSerial1.end();
#endif // ENABLE_SERIAL1

#ifdef ENABLE_SERIAL0
	jSerial0.end();
#endif // ENABLE_SERIAL0


#ifdef ENABLE_I2C0
	I2C0.end();
#endif // ENABLE_I2C0


}

void SERCOM_Module_Flush()
{
#ifdef ENABLE_SERIAL1
	jSerial1.flush();
#endif // ENABLE_SERIAL1

#ifdef ENABLE_SERIAL0
	jSerial0.flush();
#endif // ENABLE_SERIAL0

}



#pragma region SERIAL_INPUT

static String serialinput = "";

void write_SerialInput(String s)
{
	//for (int i = 0; i < s.length(); i++)
	//	write_SerialInput(s[i]);
	serialinput += s;
}

void write_SerialInput(char c)
{
	serialinput += c;
}


bool SerialInput_available() {
	return serialinput.length() > 0;
}

char read_SerialInput()
{
	char c = serialinput[0];
	serialinput = serialinput.substring(1);
	return c;
}

void process_SerialInput()
{
	static char c_prev = '\0';

#ifdef DEBUG_SERIAL_INPUT
	if(SerialInput_available())
	{
		LogD("__________________");
		LogD("SerInput: '%s'", serialinput.c_str());
		LogD("__________________");
		//delay(2000);
	}
#endif // DEBUG_SERIAL_INPUT

	while(SerialInput_available())
	{
		
		char c = read_SerialInput();
		
		if (c_prev == '#')
		{
			//Special Case '##'
			if (c == '#')
				ChangeMode(MODE_HALT);

			else if (isNumber(c))
			{
				char mode = c - '0';
				ChangeMode(mode);
			}
			else if (isAlpha(c))
			{
				ChangeMode(c);
			}
		}

		c_prev = c;
	}
}


#pragma endregion
