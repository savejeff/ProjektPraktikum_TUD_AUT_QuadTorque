#include "ModeModule.h"

#include "global.h"



void ModeModule_Init()
{
	
}


void ModeModule_Update() {
/*
	//Display every Xs
	static ulong last_time_display = 0;
	if (enabled_PrintStatus && millis() - last_time_display > LOOPTIME_PRINTSTATS)
	{
		last_time_display = millis();
		
		ModeModule_PrintStatus();
	}
	*/
}


void ModeModule_PrintStatus()
{
#ifdef ENABLE_PRINT_STATUS_MODE

#endif // ENABLE_PRINT_STATUS_MODE
}



//Changes Current Mode. Returns true if mode was changed
bool ChangeMode(int8_t mode)
{
	
	switch (mode)
	{

		//functions:
		case MODE_HALT: terminate = true; return true;
		case MODE_FUNC_HELP: FUNC_printHelp(); return true;
		
		case MODE_FUNC_DEBUG_CMD1: DEBUG_Func_1(); return true;
		case MODE_FUNC_DEBUG_CMD2: DEBUG_Func_2(); return true;
		case MODE_FUNC_DEBUG_CMD3: DEBUG_Func_3(); return true;
		
		case MODE_FUNC_CHANGE_CONFIG: FUNC_ConfigChange(); return true;
		case MODE_FUNC_RESET_MEMORY: FUNC_ResetMemory(); return true;
		
		case MODE_FUNC_ZERO: Func_Zero(); return true;
	}

	return false;
}


/********************************************
 *                 Function Modes           *
 * *****************************************/

#include "SERCOM_Module.h"

//Mode 7
void DEBUG_Func_1()
{
	LogD(F(">>> DEBUG #1"));

}



//Mode 8
void DEBUG_Func_2()
{
	LogD(F(">>> DEBUG #2"));

	UpdateConfig_fromLine("app=0.69");
	
}



//Mode 9
void DEBUG_Func_3()
{
	LogD(F(">>> DEBUG #3"));
	
}

//Mode c - Change Config 
void FUNC_ConfigChange()
{
	ulong time_start = millis();
	String s = "";
	bool contains_equal = false;
	bool permanent = false;
	while(millis() - time_start < 100)
	{
		if(!SerialInput_available()) //wait for input
			continue;
			
		char c = read_SerialInput();
		
		if(c == '\n') //end with new line to not make permanent
			break;

		if(c == '#') //end line with # to make change permanent
		{
			permanent = true;
			break;
		}
		
		
		s += c;
		
		if(c == '=')
			contains_equal = true;
	}

	
	if(s.length() == 0)
	{
		/*
		LogD("");
		LogD(F("    \"#cEXAMPLE_SETTING=12\" to change Setting EXAMPLE_SETTING to 12 temporarily (end with '#' for permanent)"));
		//LogD("    \"#cEXAMPLE_SETTING=12#\" to change Setting EXAMPLE_SETTING to 12 permanently");
		LogD(F("    \"#cEXAMPLE_SETTING\" to read current value of Setting"));
		*/
		return;
	}
	
	if(contains_equal)
	{
		//LogD("Config Update");
		UpdateConfig_fromLine(s, permanent);
		/*
		if(UpdateConfig_fromLine(s, permanent))
			LogD("Config Update successful");
		else
			LogD("Config Update failed with '%s'", s.c_str());
		*/
	}
	else
	{
		//LogD("Config Read");
		LogConfig_byTag(s);
	}
}

//Mode r
void FUNC_ResetMemory() 
{
#ifdef ENABLE_MEMORY
    Memory_Reset();

	jSystemRestart();
#endif //ENABLE_MEMORY
}


#ifdef ENABLE_SENSOR_HX711
#include <Sensors/Sensor_HX711.h>
extern Sensor_HX711_Class Sensor_HX711;
#endif // ENABLE_SENSOR_HX711

//Mode z
void Func_Zero()
{
	
#ifdef ENABLE_SENSOR_HX711
	Sensor_HX711.Calib_Zero();
#endif // ENABLE_SENSOR_HX711
}


void FUNC_printHelp()
{
	
	//LogD(F("______________________________"));
#ifdef PROJECT
	LogD("Config: %s", PROJECT);
#endif 
	LogD("Compile Time: " __DATE__ " " __TIME__ );
	LogD("");
	

#ifdef ENABLE_CONFIGURE
	LogD(F("c  FUNC_CHANGE_CONFIG like '#ctest=5' for write and '#ctest' for read"));
#endif // ENABLE_CONFIGURE
	
	//LogD(F("______________________________"));
}
