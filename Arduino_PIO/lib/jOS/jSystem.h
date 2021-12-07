#include "jDefines.h"

extern void LogD(const String msg);
extern void LogD(const char* format, ...) __attribute__((format(printf, 1, 2)));

//Log to EventLog not monitor
extern void LogR(const String msg);
extern void LogR(const char* format, ...) __attribute__((format(printf, 1, 2)));

//Log to EventLog and Debug out
extern void Log(const String msg);
extern void Log(const char* format, ...) __attribute__((format(printf, 1, 2)));

//Log to Monitor, Eventlog and Debug out
extern void LogM(const String msg);
extern void LogM(const char* format, ...) __attribute__((format(printf, 1, 2)));




//returns system voltage in [V] like 3.3V or 5V
float getSysVoltage();


uint32_t getCPU_Freq();

void jSystemRestart();

/******************************************
 *          LOW LEVEL FUNCTIONS           *
 * ***************************************/

#include <stdarg.h>

String s_vsnprintf(const char* format, va_list arg);

String s_printf(const char* format, ...)  __attribute__((format(printf, 1, 2)));
