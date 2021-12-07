#pragma once 

#include "Defines.h"


/*************************SETTING VAR DEFINITION**********************************/

#pragma region AUTOGEN_SETTINGS_H

//ESC
extern boolean USE_ANALOG_THROTTLE;
extern float APP;
extern long TIME_UPDATE_APP;
extern long SET_SPEED;



#pragma endregion

/*************************SETTING VAR DEFINITION**********************************/


bool UpdateConfig_fromLine(const String& setting_line, bool update_configtxt=false);

void LogConfig_byTag(String tag);
