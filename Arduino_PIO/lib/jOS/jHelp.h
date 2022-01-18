#include "jDefines.h"



/*******************************************
 *        DEBUG to String Functions        *
 * ****************************************/


String sprintBits(byte myByte);

void hexdump(const void *mem, uint32_t len, uint8_t cols);


//String toString(IPAddress ip);


/*******************************************
 *         Help Functions                  *
 * ****************************************/


bool isAlpha(char c);

bool isNumber(char c);

bool isSymbol(char c);

bool isPrintable(char c);

bool isNumber(const String& s);

bool isFloatNumber(const String& s);


/*******************************************
 *         Signal Processing               *
 * ****************************************/


bool is_valid(float v);
bool is_valid(double x);

#define deg2rad(a_deg) ((a_deg) * FACTOR_deg_2_rad)
#define rad2deg(a_rad) ((a_rad) * FACTOR_rad_2_deg)



float get_lowpass_coeff(float dt, float f_cutoff);

//Version 1: does update param y
float lowpass(float x, float dt, float f_cutoff, float& y);

//Version 2: does not update y but returns y_new
float lowpass2(float x, float dt, float f_cutoff, float y);

int32_t avg_filter(int32_t x, uint16_t& N, int64_t& sum);
void avg_filter2(int32_t x, uint16_t& N, int32_t& y);
float avg_filter(float x, uint16_t& N, float& sum);

