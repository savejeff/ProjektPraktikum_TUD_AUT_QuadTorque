#pragma once

#include <jOS.h>

#include "Defines.h"
#include "Help.h"
#include "SERCOM_Module.h"
#include "Settings.h"
#include "ModeModule.h"


extern bool enabled_PrintStatus;

extern bool terminate;

extern void switchBoardLED(bool ON);






//#include <stdarg.h>
//Only to SerialOut
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






extern void write_SerialInput(char c);
extern void write_SerialInput(String s);

