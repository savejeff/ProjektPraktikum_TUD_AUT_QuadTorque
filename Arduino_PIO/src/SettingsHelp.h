#pragma once

#include "Defines.h"


ulong str2ulong(const String& s);
long str2long(const String& s);
float str2float(const String& s);



//splits up settings line into tag and value as String
//like "test=12" -> tag="test", value="12"
void ProcessSettingsLine(const String& line, String& tag, String& value);

//extract value from value string like "1234" -> 1234
bool ProcessContent_Float(const String& line_content, float& value);
bool ProcessContent_Long(const String& line_content, long& value);
bool ProcessContent_String(const String& line_content, String& value);
bool ProcessContent_Bool(const String& line_content, bool& value);

//converts value to value string like 1234 -> "1234"
String getSettingContent_String(const String& value);
String getSettingContent_Float(float& value);
String getSettingContent_Long(long& value);
String getSettingContent_Bool(bool& value);
