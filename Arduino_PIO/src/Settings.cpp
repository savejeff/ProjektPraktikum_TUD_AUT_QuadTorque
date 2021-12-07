#include "Settings.h"



/**************** Settings Tag for storage and loading ******************************/

//#ifdef PLATFORM_AVR
//#define DECLARE_CONST_CHAR(VARNAME, VALUE) const char VARNAME[] PROGMEM = {VALUE};
//#else
#define DECLARE_CONST_CHAR(VARNAME, VALUE) const char* VARNAME = {VALUE};
//#endif 

#pragma region AUTOGEN_SETTINGS_DEFINES

//ESC
#define SETT_TAG_USE_ANALOG_THROTTLE "use_analog_throttle"
#define SETT_TAG_APP "app"
#define SETT_TAG_SET_SPEED "setspeed"



#pragma endregion


/*************************SETTING VAR DEFINITION**********************************/

#pragma region AUTOGEN_SETTINGS_CPP

//ESC
boolean USE_ANALOG_THROTTLE = true; //[%] 0.0 bis 1.0 to control throttle Position
float APP = 0.0; //[%] 0.0 bis 1.0 to control throttle position
long TIME_UPDATE_APP = 0.0; //[ms] timestamp of last update of APP Setting to implement timeout stopping
long SET_SPEED = 0; //[rpm] target speed to Motor



#pragma endregion

#ifdef ENABLE_CONFIGURE

#include "global.h"
#include "Help.h"
#include "SettingsHelp.h"


void onSettingChanged(const String& tag);



/************************* SETTING VAR DEFINITION **********************************/

static const char* LOG_FORMAT_ERROR_SETTING_STRING = "Error with Setting Value '%s'";

bool updateSetting_String(const String& tag, const String& value, String& setting)
{
	if (ProcessContent_String(value, setting))
	{
		onSettingChanged(tag);
		return true;    
	}
	LogR(LOG_FORMAT_ERROR_SETTING_STRING, value.c_str());
	return false;
}

bool updateSetting_Long(const String& tag, const String& value, long& setting)
{
	if (ProcessContent_Long(value, setting))
	{
		onSettingChanged(tag);
		return true;    
	}
	LogR(LOG_FORMAT_ERROR_SETTING_STRING, value.c_str());
	return false;
}

bool updateSetting_Float(const String& tag, const String& value, float& setting)
{
	if (ProcessContent_Float(value, setting))
	{
		onSettingChanged(tag);
		return true;    
	}
	LogR(LOG_FORMAT_ERROR_SETTING_STRING, value.c_str());
	return false;
}

bool updateSetting_Boolean(const String& tag, const String& value, bool& setting)
{
	if (ProcessContent_Bool(value, setting))
	{
		onSettingChanged(tag);
		return true;    
	}
	LogR(LOG_FORMAT_ERROR_SETTING_STRING, value.c_str());
	return false;
}




static String get_setting_string_by_tag(String tag)
{
	#define SETT_MATCH(SETT_TAG) (tag.equals(SETT_TAG))
	#define SETT_GET_BOOL(SETT_TAG, SETTING) if SETT_MATCH(SETT_TAG) return s_printf("%d", SETTING);
	#define SETT_GET_LONG(SETT_TAG, SETTING) if SETT_MATCH(SETT_TAG) return s_printf("%d", SETTING);
	#define SETT_GET_FLOAT(SETT_TAG, SETTING) if SETT_MATCH(SETT_TAG) return s_printf("%.7f",SETTING);
	#define SETT_GET_STR(SETT_TAG, SETTING) if SETT_MATCH(SETT_TAG) return s_printf("'%s'", (SETTING).c_str());


	
#pragma region AUTOGEN_SETTINGS_GET

	//ESC
	SETT_GET_BOOL(SETT_TAG_USE_ANALOG_THROTTLE, USE_ANALOG_THROTTLE);
	SETT_GET_FLOAT(SETT_TAG_APP, APP);
	SETT_GET_LONG(SETT_TAG_SET_SPEED, SET_SPEED);



#pragma endregion

	return "";
}

static const char* FORMAT_STR_PRINT_CONFIG = "cfg.%s: %s"; //like "cfg.motor_ctrl_mode: 2"

static const char* PRINT_FORMAT_SETTING_STR = "Setting: %s='%s'";
static const char* PRINT_FORMAT_SETTING_LONG = "Setting: %s=%ld";
static const char* PRINT_FORMAT_SETTING_FLOAT = "Setting: %s=%f";
static const char* PRINT_FORMAT_SETTING_BOOL = "Setting: %s=%s";

static bool update_settings(String tag, String value)
{
	const char* STR_TRUE = "TRUE";
	const char* STR_FALSE = "FALSE";


#define SETT_MATCH(SETT_TAG) (tag.equals(SETT_TAG))
#define SETT_SET_STR(SETTING) bool b = updateSetting_String(tag, value, SETTING)
#define SETT_SET_LONG(SETTING) bool b = updateSetting_Long(tag, value, SETTING)
#define SETT_SET_FLOAT(SETTING) bool b = updateSetting_Float(tag, value, SETTING)
#define SETT_SET_BOOLEAN(SETTING) bool b = updateSetting_Boolean(tag, value, SETTING)
#define SETT_PRINT_STR(SETT_TAG, SETTING) 
#define SETT_PRINT_LONG(SETT_TAG, SETTING) 
#define SETT_PRINT_FLOAT(SETT_TAG, SETTING) 
#define SETT_PRINT_BOOLEAN(SETT_TAG, SETTING) 

//#define SETT_PRINT_STR(SETT_TAG, SETTING) LogR(PRINT_FORMAT_SETTING_STR, SETT_TAG, (SETTING).c_str())
//#define SETT_PRINT_LONG(SETT_TAG, SETTING) LogR(PRINT_FORMAT_SETTING_LONG, SETT_TAG, SETTING)
//#define SETT_PRINT_FLOAT(SETT_TAG, SETTING) LogR(PRINT_FORMAT_SETTING_FLOAT, SETT_TAG, SETTING)
//#define SETT_PRINT_BOOLEAN(SETT_TAG, SETTING) LogR(PRINT_FORMAT_SETTING_BOOL, SETT_TAG, SETTING ? STR_TRUE : STR_FALSE)

#define SETT_UPDATE_STR(SETT_TAG, SETTING) if SETT_MATCH(SETT_TAG) { SETT_SET_STR(SETTING); SETT_PRINT_STR(SETT_TAG, SETTING); return b; }
#define SETT_UPDATE_LONG(SETT_TAG, SETTING) if SETT_MATCH(SETT_TAG) { SETT_SET_LONG(SETTING); SETT_PRINT_LONG(SETT_TAG, SETTING); return b; }
#define SETT_UPDATE_FLOAT(SETT_TAG, SETTING) if SETT_MATCH(SETT_TAG) { SETT_SET_FLOAT(SETTING); SETT_PRINT_FLOAT(SETT_TAG, SETTING); return b; }
#define SETT_UPDATE_BOOLEAN(SETT_TAG, SETTING) if SETT_MATCH(SETT_TAG) { SETT_SET_BOOLEAN(SETTING); SETT_PRINT_BOOLEAN(SETT_TAG, SETTING); return b; }
	
		
	//only one that works with progmem
	//String s = "";
	//for(int i = 0; i < sizeof(SETT_TAG_APP); i++)
	//	s += SETT_TAG_APP[i];
	//Log("'%s'=app: %d", tag.c_str(), tag.equals(s.c_str()));
	
#pragma region AUTOGEN_SETTINGS_SET

	//ESC
	SETT_UPDATE_BOOLEAN(SETT_TAG_USE_ANALOG_THROTTLE, USE_ANALOG_THROTTLE);
	SETT_UPDATE_FLOAT(SETT_TAG_APP, APP);
	SETT_UPDATE_LONG(SETT_TAG_SET_SPEED, SET_SPEED);



#pragma endregion

	return false;
}



void onSettingChanged(const String& tag)
{
	#ifdef SETT_TAG_APP
	if(tag.equals(SETT_TAG_APP))
	{
		TIME_UPDATE_APP = millis();
	}
	#endif // SETT_TAG_APP
}

#endif // ENABLE_CONFIGURE

/************************* Generall Functions **********************************/


//Prints current value of Setting to Log output
void LogConfig_byTag(String tag)
{
#ifdef ENABLE_CONFIGURE
	
	
	String value_str = "";

	value_str = get_setting_string_by_tag(tag);
	if(value_str.length() > 0)
	{
		LogM(FORMAT_STR_PRINT_CONFIG, tag.c_str(), value_str.c_str());
	}


#endif // ENABLE_CONFIGURE
}


//Updates Setting from line like "app=69"
//if Starts with ; or # it is ignored
//if permanent is true the config file is updated or memory is commited and change is permanent
//returns true if setting was updated
bool UpdateConfig_fromLine(const String& setting_line, bool permanent)
{
#ifdef ENABLE_CONFIGURE
	//commented line
	if (setting_line[0] == '#' || setting_line[0] == ';')
		return false;

	//LogD(setting_line);

	String line_content, tag;
	ProcessSettingsLine(setting_line, tag, line_content);

#ifdef DEBUG_CONFIGURE

	LogD("tag='%s' value='%s'", tag.c_str(), line_content.c_str());

	String value_str = "";
	if (ProcessContent_String(line_content, value_str))
	{
		LogD("\tString value='%s'", value_str.c_str());
	}

	long value_long = 0;
	if (ProcessContent_Long(line_content, value_long))
	{
		LogD("\tLong value=%ld", value_long);
	}

	float value_float = 0;
	if (ProcessContent_Float(line_content, value_float))
	{
		LogD("\tFloat value=%f", str2float(line_content));
	}

#endif // DEBUG_CONFIGURE


	bool sett_up = update_settings(tag, line_content);

	if(sett_up)
	{
		LogConfig_byTag(tag); //Print/Log updated setting value


		if(permanent)
		{
			
		}
	}

	if(sett_up)
		return true;

#endif // ENABLE_CONFIGURE
	
	return false;
}
