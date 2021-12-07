#include "SystemModule.h"


#include "global.h"

#include "SERCOM_Module.h"


boolean enabled_PrintStatus = true;

#pragma region LOCAL FUNC

#pragma endregion


void SystemModule_Init() {
	Log("system.state: init");
	

#ifdef ENABLE_WATCHDOGTIMER
	jWatchdog_enable(WDT_TIMEOUT);
#else
	jWatchdog_disable();
#endif // ENABLE_WATCHDOGTIMER


	SystemModule_PrintStatus();
}

void SystemModule_End()
{
	
#ifdef ENABLE_WATCHDOGTIMER
	jWatchdog_disable();
#endif // ENABLE_WATCHDOGTIMER
}



void SystemModule_Update() 
{

	
#ifdef ENABLE_WATCHDOGTIMER
	jWatchdog_reset();
#endif // ENABLE_WATCHDOGTIMER		

	//Display every Xs
	static ulong last_time_display = millis();
	if (enabled_PrintStatus && millis() - last_time_display > LOOPTIME_PRINTSTATS * 2)
	{
		last_time_display = millis();
		
		SystemModule_PrintStatus();
	}
}


void SystemModule_PrintStatus()
{
#ifdef ENABLE_PRINT_STATUS_SYSTEM
	
#endif // ENABLE_PRINT_STATUS_SYSTEM
}


void System_restart()
{
	jSystemRestart();
}


#pragma region LOG




//Base function for Log. Only function that actually does the Logging.
//if blocking false lock print is not garanteed. if Print lock is locked printing is skipped
static void _Log(const String msg, bool log_to_file, bool log_to_monitor, bool blocking=true)
{
	String str_timestamp = s_printf("[%lu] ", millis());
	bool add_new_line = !msg.endsWith("\n");

#ifdef ENABLE_SERIAL_OUT
#ifdef ENABLE_SERIAL_OUT_TIMESTAMP
	SerialOut.print(str_timestamp);
	SerialOut.print(msg);
	if(add_new_line)
		SerialOut.print("\n");
#else
	SerialOut.print(msg);
	if(add_new_line)
		SerialOut.print("\n");
#endif
	
#endif // ENABLE_SERIAL_DEBUG

	if(log_to_file)
	{

	}

	if(log_to_monitor)
	{

	}
}

void Log(const String msg)
{
	_Log(msg, true, false, true);
}

void Log(const char* format, ...) {
	va_list arg;
	va_start(arg, format);
	String s = s_vsnprintf(format, arg);
	va_end(arg);

	_Log(s, true, false, true);
}

void LogM(const String msg)
{
	_Log(msg, true, true, true);
}

void LogM(const char* format, ...) {
	va_list arg;
	va_start(arg, format);
	String s = s_vsnprintf(format, arg);
	va_end(arg);

	_Log(s, true, true, true);
}


void LogD(const String msg)
{
	_Log(msg, false, false, false);
}

void LogD(const char* format, ...) {
	va_list arg;
	va_start(arg, format);
	String s = s_vsnprintf(format, arg);
	va_end(arg);

	_Log(s, false, false, false);
}

void LogR(const String msg)
{
	_Log(msg, true, false, true);
}

void LogR(const char* format, ...) {
	va_list arg;
	va_start(arg, format);
	String s = s_vsnprintf(format, arg);
	va_end(arg);

	_Log(s, true, false, true);
}
#pragma endregion