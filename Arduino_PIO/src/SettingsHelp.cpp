#include "SettingsHelp.h"

#include "global.h"


ulong str2ulong(const String& s)
{
	return strtoul(s.c_str(), NULL, 0);
}

long str2long(const String& s)
{
	return strtol(s.c_str(), NULL, 0);
}

float str2float(const String& s)
{
	return atof(s.c_str());
}


String getSettingContent_String(const String& value) {
	return s_printf("'%s'", value.c_str());
}
String getSettingContent_Float(float& value) {
	return s_printf("%.7f", value);
}
String getSettingContent_Long(long& value) {
	return s_printf("%d", value);
}
String getSettingContent_Bool(bool& value) {
	return s_printf("%d", value);
}


#define SEPERATOR "="
#define SEPERATOR_LEN 1

void ProcessSettingsLine(const String& line, String& tag, String& value)
{
    int index_sep = line.indexOf(SEPERATOR);
    tag = line.substring(0, index_sep);

    value = "";
    value.concat(line.substring(index_sep + SEPERATOR_LEN));
}



#define STRING_STARTEND_CHAR0 '\''
#define STRING_STARTEND_CHAR1 '\"'

bool ProcessContent_String(const String& line_content, String& value)
{
    //value = "";

    //Check if starts with ' or "
    if ( 
        line_content.length() >= 3 &&
        (
            (line_content[0] == STRING_STARTEND_CHAR0 && line_content[line_content.length() - 1] == STRING_STARTEND_CHAR0)
            ||
            (line_content[0] == STRING_STARTEND_CHAR1 && line_content[line_content.length() - 1] == STRING_STARTEND_CHAR1)
        )
    )
    {
        value = line_content.substring(1, line_content.length() - 1);
        return true;
    }
    else
        return false;
}


bool ProcessContent_Long(const String& line_content, long& value)
{
    //value = 0;
    //check if string is a Number
    if (isNumber(line_content))
    {
        value = str2long(line_content);
        return true;
    }
    else
        return false;
}


bool ProcessContent_Float(const String& line_content, float& value)
{
    //value = 0;
    //check if string is a Number
    if (isFloatNumber(line_content))
    {
        value = str2float(line_content);
        return true;
    }
    else
        return false;
}

bool ProcessContent_Bool(const String& line_content, bool& value)
{
    //value = 0;
    //check if string is a Number
    if (isNumber(line_content))
    {
        value = 0 != str2long(line_content);
        return true;
    }
    else
        return false;
}

