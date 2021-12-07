#include "jHelp.h"

#include "jSystem.h"




/*******************************************
 *        DEBUG to String Functions        *
 * ****************************************/



String sprintBits(byte myByte) {
	String s = "";
	for (byte mask = 0x80; mask; mask >>= 1) {
		if (mask & myByte)
			s += '1';
		else
			s += '0';

		if(mask == 0x10)
			s += " ";
	}
	return s;
}


void hexdump(const void *mem, uint32_t len, uint8_t cols) {
	const uint8_t* src = (const uint8_t*) mem;
	LogD("[HEXDUMP] Address: 0x%08X len: 0x%X (%d)", (ptrdiff_t)src, len, len);
	String out = "";
	for(uint32_t i = 0; i < len; i++) {
		if(i % cols == 0) {
			LogD(out);
			out = s_printf("[0x%08X] 0x%08X: ", (ptrdiff_t)src, i);
		}
		out += s_printf("%02X ", *src);
		src++;
	}
	LogD(out);
}

/*
String toString(IPAddress ip)
{
	return s_printf("%d.%d.%d.%d", ip[0], ip[1], ip[2], ip[3]);
}
*/



/*******************************************
 *         Help Functions                  *
 * ****************************************/




bool isAlpha(char c)
{
	return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z');
}

bool isAlpha(String s)
{
	for (int i = 0; i < s.length(); i++)
		if (!isAlpha(s[i]))
			return false;
	return true;
}

bool isNumber(char c)
{
	return (c >= '0' && c <= '9');
}

bool isSymbol(char c)
{
	return (c >= '!' && c <= '/') || (c >= ':' && c <= '@') || (c >= '[' && c < 'a') || (c >= '{' && c <= '~');
}

bool isPrintable(char c)
{
	return (c >= ' ' && c <= '~');
}


//returns true for all Numbers (also negative)
bool isNumber(const String& s)
{
	for (int i = 0; i < s.length(); i++)
		if (!(i == 0 && s[i] == '-' && s.length() > 1) && !isNumber(s[i]))
			return false;
	return true;
}


bool isFloatNumber(const String& s) {
	/*
	std::string string = std::string(s.c_str());
	std::string::const_iterator it = string.begin();
	bool decimalPoint = false;
	int minSize = 0;
	if (string.size() > 0 && (string[0] == '-' || string[0] == '+')) {
		it++;
		minSize++;
	}
	
	while (it != string.end()) {
		
		if (*it == '.') {
			if (!decimalPoint) 
				decimalPoint = true;
			else 
				break;
		}
		else if (!std::isdigit(*it) && ((*it != 'f') || it + 1 != string.end() || !decimalPoint))
			break;
		++it;
	}
	return string.size() > minSize && it == string.end();
	*/

	
	const char* it = s.c_str(); 
	bool decimalPoint = false;
	int minSize = 0;
	
	//check if start with '+' or '-'
	if (s.length() > 0 && (s[0] == '-' || s[0] == '+')) {
		it++;
		minSize++;
	}
	//itterate over string
	while (*it) {
		
		if (*it == '.') {
			if (!decimalPoint) 
				decimalPoint = true;
			else 
				break; //if two decimalPoint found -> not a float string
		}
		else if (!isNumber(*it) && ((*it != 'f') || *(it + 1) || !decimalPoint)) //if not a number or f at the end of the string or decimal point -> not a float string
			break;
		++it;
	}
	return s.length() > minSize && !*it; //check if end reached -> if yes is valid float
}


/*******************************************
 *         Signal Processing               *
 * ****************************************/




/*
calculates lowpass coefficient
:param dt: time delta between samples [s]
:param f_cutoff: cutoff frequency
:return: alpha for func: y_new = a * x + (1 - a) * y_old
*/
float get_lowpass_coeff(float dt, float f_cutoff)
{
	float RC = 1.0f / (TWO_PI * f_cutoff); // RC = Time constant of PT1 Glied
	return dt / (RC + dt);
}



// Return RC low-pass filter output samples, given input samples,
// time interval dt in [s], and time constant RC
// returns smoothed value
float lowpass(float x, float dt, float f_cutoff, float& y)
{
	//if f_cutoff = 0
	//or y is not valid
	// ->  override y with x
	if (f_cutoff == 0 || isnan(y))
	{
		y = x;
	}
	else if(isnan(x)) //if new value is invalid -> invalidate y
	{
		y = NAN;
	}
	else
	{
		float RC = 1.0f / (TWO_PI * f_cutoff);
		float a = dt / (RC + dt);
		y = a * x + (1.0f - a) * y;
	}

	/*
	if (isnan(y))
	{
		//SerialOut.println("!ISNAN!<-------------------");
		y = x;
	}
	*/

	return y;
}

// Return RC low-pass filter output samples, given input samples,
// time interval dt [s], and time constant RC
// returns smoothed value
float lowpass2(float x, float dt, float f_cutoff, float y)
{
	//if f_cutoff = 0
	//or y is not valid
	// ->  override y with x
	if (f_cutoff == 0 || isnan(y))
	{
		y = x;
	}
	else if(isnan(x)) //if new value is invalid -> invalidate y
	{
		y = NAN;
	}
	else
	{
		float RC = 1.0f / (TWO_PI * f_cutoff);
		float a = dt / (RC + dt);
		y = a * x + (1.0f - a) * y;
	}

	/*
	if (isnan(y))
	{
		//SerialOut.println("!ISNAN!<-------------------");
		y = x;
	}
	*/

	return y;
}

int32_t avg_filter(int32_t x, uint16_t& N, int64_t& sum)
{
	if (N == 0)
		sum = 0;

	sum += x;
	N++;

	return sum / N;
}

void avg_filter2(int32_t x, uint16_t& N, int32_t& y)
{
	if (N == 0)
		y = x;
	else
		y = (int32_t)(((float)y) + ((float)x / (N))) / ((float)(N + 1) / (float)(N));
	N++;
}


float avg_filter(float x, uint16_t& N, float& sum)
{
	if (N == 0)
		sum = 0;

	sum += x;
	N++;
	
	return sum / N;
}

