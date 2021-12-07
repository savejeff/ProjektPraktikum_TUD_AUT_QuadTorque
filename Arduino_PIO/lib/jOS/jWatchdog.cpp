#include "jWatchdog.h"

#include "jSystem.h"



#if defined(PLATFORM_SAMD) || defined(PLATFORM_AVR)
// https://github.com/adafruit/Adafruit_SleepyDog
#include <Adafruit_SleepyDog.h>
#endif // PLATFORM_SAMD || PLATFORM_AVR


static uint16_t wdt_timeout = 0;
uint16_t jWatchdog_getTimeout()
{
	return wdt_timeout;
}


void jWatchdog_enable(uint16_t timeout_ms)
{
	wdt_timeout = timeout_ms;

#if defined(PLATFORM_SAMD) || defined(PLATFORM_AVR)
	Watchdog.enable(timeout_ms);
#endif // PLATFORM_SAMD || PLATFORM_AVR

}

void jWatchdog_disable()
{
	wdt_timeout = 0;
	

#if defined(PLATFORM_SAMD) || defined(PLATFORM_AVR)
	Watchdog.disable();
#endif // PLATFORM_SAMD || PLATFORM_AVR

}

void jWatchdog_reset()
{

#if defined(PLATFORM_SAMD) || defined(PLATFORM_AVR)
	Watchdog.reset();
#endif // PLATFORM_SAMD || PLATFORM_AVR

}