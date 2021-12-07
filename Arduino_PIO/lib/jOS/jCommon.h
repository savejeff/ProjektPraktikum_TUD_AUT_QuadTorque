
#if defined(PLATFORM_RP2040) && !defined(__cplusplus)


/* Standard C library includes */
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <math.h>

typedef enum {
  LOW     = 0,
  HIGH    = 1,
  CHANGE  = 2,
  FALLING = 3,
  RISING  = 4,
} PinStatus;

typedef enum {
  INPUT           = 0x0,
  OUTPUT          = 0x1,
  INPUT_PULLUP    = 0x2,
  INPUT_PULLDOWN  = 0x3,
} PinMode;

#include "pgmspace.h"

//#define PROGMEM

#else


#include "Arduino.h" // Arduino support

#ifdef PLATFORM_AVR
typedef uint32_t time_t;
#endif // PLATFORM_AVR

/*

typedef unsigned int word;
typedef unsigned char uint8_t;
typedef char int8_t;
typedef unsigned short uint16_t;
typedef short int16_t;
typedef unsigned int uint32_t;
typedef int int32_t;

typedef uint8_t byte;
*/

typedef uint8_t 	ubyte;
typedef	uint16_t	ushort;
typedef	unsigned int	uint;
typedef	unsigned long	ulong;



/*
#ifdef PLATFORM_ESP32
#include <pgmspace.h>
#endif 
#ifdef PLATFORM_STM32   // stm32duino support
#include <avr/pgmspace.h>
#endif 
*/

#endif