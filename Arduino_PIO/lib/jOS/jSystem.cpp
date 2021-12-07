#include "jSystem.h"


#ifdef PLATFORM_AVR
#include <avr/wdt.h>
#endif // PLATFORM_AVR

float getSysVoltage()
{
#ifdef PLATFORM_AVR
	return 5.0f;
#else 
	return 3.3f;
#endif
}


uint32_t getCPU_Freq()
{
#ifdef PLATFORM_ESP32
	return getCpuFrequencyMhz(); //Get CPU clock
#endif // PLATFORM_ESP32
#ifdef PLATFORM_STM32
	return F_CPU;
#endif // PLATFORM_STM32
#ifdef PLATFORM_SAMD
	return F_CPU;
#endif // PLATFORM_SAMD
#ifdef PLATFORM_AVR
	return F_CPU;
#endif // PLATFORM_AVR
	
	return 0;
}

void jSystemRestart()
{
#ifdef PLATFORM_ESP32
	ESP.restart();
#endif // PLATFORM_ESP32
#ifdef PLATFORM_AVR
	// https://arduino.stackexchange.com/questions/61180/avr-software-reset-without-watchdog
	wdt_enable(WDTO_15MS);for(;;);// (this way enters recovery mode)
    //or
    //  asm ("jmp 0x0");// (this way function registers not being resetted)
#endif // PLATFORM_AVR
#if defined(PLATFORM_SAMD) || defined(PLATFORM_RP2040)
	NVIC_SystemReset();
#endif // ARM BASED
}


/******************************************
 *          LOW LEVEL FUNCTIONS           *
 * ***************************************/


String s_vsnprintf(const char* format, va_list arg)
{
	char loc_buf[64];
	char* temp = loc_buf;
	
	va_list copy;
	va_copy(copy, arg);
	int len = vsnprintf(temp, sizeof(loc_buf), format, copy);
	va_end(copy);
	if (len < 0) {
		return "";
	};
	if (len >= sizeof(loc_buf)) {
		temp = (char*)malloc(len + 1);
		if (temp == NULL) {
			return "";
		}
		len = vsnprintf(temp, len + 1, format, arg);
	}
	
	String s = String(temp);

	if (temp != loc_buf) {
		free(temp);
	}
	return s;
}




String s_printf(const char* format, ...)
{
	va_list arg;
	va_start(arg, format);
	String s = s_vsnprintf(format, arg);
	va_end(arg);
	
	return s;
}


