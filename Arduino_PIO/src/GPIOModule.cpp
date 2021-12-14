#include "GPIOModule.h"

#include "Objects/GPIOButton.h"




#if defined(PIN_BUTTON1) && PIN_BUTTON1 != -1
#define ENABLE_BUTTON1
#endif 

#if defined(PIN_BUTTON2) && PIN_BUTTON2 != -1
#define ENABLE_BUTTON2
#endif 

#if defined(PIN_LED_BUILTIN) && PIN_LED_BUILTIN != -1
#define ENABLE_LED_BUILTIN
#endif // PIN_LED_BUILTIN




#if defined(PIN_ANALOG_IN_0) && PIN_ANALOG_IN_0 != -1
#define ENABLE_ANALOG_IN_0
#endif 

#if defined(PIN_ANALOG_IN_1) && PIN_ANALOG_IN_1 != -1
#define ENABLE_ANALOG_IN_1
#endif 


#if defined(PIN_ANALOG_OUT_0) && PIN_ANALOG_OUT_0 != -1
#define ENABLE_ANALOG_OUT_0
#endif 




#if defined(PIN_DIGITAL_OUT_0) && PIN_DIGITAL_OUT_0 != -1
#define ENABLE_DIGITAL_OUT_0
#ifndef PIN_DIGITAL_OUT_0_INIT
#define PIN_DIGITAL_OUT_0_INIT LOW
#endif 
#endif 

#if defined(PIN_FRQ_IN0) && PIN_FRQ_IN0 != -1
#define ENABLE_FRQ_IN0
#endif 



#ifdef ENABLE_FRQ_IN0



/*
static bool frq_in0_isr_pin_flag = false;
static long frq_in0_time_low = 0;
static long frq_in0_time_high = 0;
static uint32_t frq_in0_duration = 0;
static int frq_in0_last_state = 0;
*/

//#define FRQ_IN0_MODE_SINGLE
#define FRQ_IN0_MODE_LOWPASS


#ifdef FRQ_IN0_MODE_SINGLE
static uint16_t frq_in0_duration = 0; //duration of one period in [us]
static bool frq_in0_measured = false;
#endif // FRQ_IN0_MODE_SINGLE
#ifdef FRQ_IN0_MODE_LOWPASS
static ulong frq_in0_timestamp = 0;
static float frq_in0_duration = NAN; //duration of one period in [us]
#endif // FRQ_IN0_MODE_LOWPASS


void isr_frq_in0()
{
	static ulong frq_in0_last_time = 0; //[us] time of last trigger

	ulong t = micros(); //[us] time of this trigger
	
	/*
  	frq_in0_last_state = digitalRead(PIN_FRQ_IN0);
	frq_in0_isr_pin_flag = true;

	if (frq_in0_last_state)
	{
		frq_in0_duration = t - frq_in0_time_high;
		frq_in0_time_high = t;
	}
	else
		frq_in0_time_low = t;
	*/

#ifdef FRQ_IN0_MODE_SINGLE
	//Wait for flag to clear and not first time
	if(!frq_in0_measured && frq_in0_last_time > 0)
	{
		frq_in0_duration = t - frq_in0_last_time;
		frq_in0_measured = true;
	}
#endif // FRQ_IN0_MODE_SINGLE

#ifdef FRQ_IN0_MODE_LOWPASS

	if(frq_in0_last_time > 0)
	{
		static ulong frq_in0_last_time_set = t; //remember last sample
		float dt = ((float) (t - frq_in0_last_time_set)) * FACTOR_us_2_s; //calc sampele dt
		float new_duration = (float) (t - frq_in0_last_time); //calc new sample
		//frq_in0_duration = new_duration;
		lowpass(new_duration, dt, 10.0f, frq_in0_duration); //update smoothed value with lowpass
		frq_in0_timestamp = millis();

		frq_in0_last_time_set = t;
	}


#endif // FRQ_IN0_MODE_LOWPASS


	frq_in0_last_time = t; //update last trigger time

}


#endif // ENABLE_FRQ_IN0



#ifdef ENABLE_BUTTON1
static GPIOButton Button1;
#endif // ENABLE_BUTTON1

#ifdef ENABLE_BUTTON2
static GPIOButton Button2;
#endif // ENABLE_BUTTON2

static bool State_Transistor = false;

void Button1_onClick();
void Button1_onLongClick();

void GPIOModule_Init()
{
	
	
#ifdef ENABLE_LED_BUILTIN
	//init LED
	pinMode(PIN_LED_BUILTIN, OUTPUT);
	//Start Blinking
	digitalWrite(PIN_LED_BUILTIN, LED_BUILTIN_ON_LEVEL);
	delay(500);
	digitalWrite(PIN_LED_BUILTIN, !LED_BUILTIN_ON_LEVEL);
	/*
	delay(500);
	digitalWrite(PIN_LED_BUILTIN, LED_BUILTIN_ON_LEVEL);
	delay(500);
	digitalWrite(PIN_LED_BUILTIN, !LED_BUILTIN_ON_LEVEL);
	*/
#endif // ENABLE_LED_BUILTIN
	

	

#ifdef ENABLE_BUTTON1
	//init Button
	//pinMode(PIN_BUTTON1, (BUTTON1_TRIGGER_LEVEL) ? INPUT_PULLDOWN : INPUT_PULLUP);
	Button1 = GPIOButton(PIN_BUTTON1, BUTTON1_TRIGGER_LEVEL);
#endif // ENABLE_BUTTON1

#ifdef ENABLE_BUTTON2
	//init Button
	//pinMode(PIN_BUTTON1, (BUTTON_TRIGGER_LEVEL) ? INPUT_PULLDOWN : INPUT_PULLUP);
	Button2 = GPIOButton(PIN_BUTTON2, BUTTON2_TRIGGER_LEVEL);
#endif // ENABLE_BUTTON2

	
#ifndef PLATFORM_AVR
	analogReadResolution(GPIO_ANALOG_RESOLUTION);
#endif



#ifdef ENABLE_ANALOG_IN_0
#ifdef INPUT_ANALOG
	pinMode(PIN_ANALOG_IN_0, INPUT_ANALOG);
#else
	pinMode(PIN_ANALOG_IN_0, INPUT);
#endif // 
#endif 



#ifdef ENABLE_ANALOG_IN_1
#ifdef INPUT_ANALOG
	pinMode(PIN_ANALOG_IN_1, INPUT_ANALOG);
#else
	pinMode(PIN_ANALOG_IN_1, INPUT);
#endif // 
#endif 


#ifdef ENABLE_ANALOG_OUT_0
	pinMode(PIN_ANALOG_OUT_0, OUTPUT);
#endif 


#ifdef ENABLE_DIGITAL_OUT_0
	pinMode(PIN_DIGITAL_OUT_0, OUTPUT);
	digitalWrite(PIN_DIGITAL_OUT_0, PIN_DIGITAL_OUT_0_INIT);
#endif 

#ifdef ENABLE_FRQ_IN0
	pinMode(PIN_FRQ_IN0, INPUT);

	//attachInterrupt(digitalPinToInterrupt(PIN_FRQ_IN0), isr_frq_in0, CHANGE);
	attachInterrupt(digitalPinToInterrupt(PIN_FRQ_IN0), isr_frq_in0, RISING);
#endif // ENABLE_FRQ_IN0



}


void GPIOModule_Update()
{
#ifdef ENABLE_BUTTON1
		
		Button1.update();


		if(Button1.isClick())
			Button1_onClick();
		
		if(Button1.isLongClick())
			Button1_onLongClick();
		

#endif // ENABLE_BUTTON1

#ifdef ENABLE_BUTTON2

	Button2.update();
	/*
	if(Button2.isClick())
		Button2_onClick();
	
	if(Button2.isLongClick())
		Button2_onLongClick();
	*/

#endif // ENABLE_BUTTON2


#ifdef ENABLE_LED_BUILTIN
	
	
#endif // ENABLE_LED_BUILTIN


#ifdef ENABLE_FRQ_IN0

#ifdef FRQ_IN0_MODE_SINGLE
	if(frq_in0_measured)
	{
		uint16_t duration = frq_in0_duration;
		frq_in0_measured = false;

		//float frq = 1.0f * FACTOR_s_2_us / ((float) duration);
		float frq = 1e6 / ((float) duration);
		uint16_t rpm = frq * 60;

		Log("gpio.frq_in0: dur=%d, frq=%.1f, rpm=%d", duration, frq, rpm);
	}
#endif // FRQ_IN0_MODE_SINGLE

#ifdef FRQ_IN0_MODE_LOWPASS
	EXECUTE_EVERY(100)
		float duration = frq_in0_duration;

		//float frq = 1.0f * FACTOR_s_2_us / ((float) duration);
		float frq = 1e6 / (duration);
		uint32_t rpm = frq * 60;

		if(millis() - frq_in0_timestamp > 100)
		{
			duration = 0;
			frq = 0;
			rpm = 0;
		}

		Log("gpio.frq_in0: dur=%.1f, frq=%.1f, rpm=%ld", duration, frq, rpm);
	
	EXECUTE_EVERY_END

#endif // FRQ_IN0_MODE_LOWPASS
	
#endif // ENABLE_FRQ_IN0


	//Display every Xs
	static ulong last_time_display = 0;
	if (enabled_PrintStatus && millis() - last_time_display > LOOPTIME_PRINTSTATS)
	{
		last_time_display = millis();

		GPIOModule_PrintStatus();
	}
}


void GPIOModule_PrintStatus()
{
#ifdef ENABLE_PRINT_STATUS_GPIO

#ifdef ENABLE_ANALOG_IN_0
	
	uint32_t acc = 0;
	for(int i = 0; i < 10; i++)
		acc += analogRead(PIN_ANALOG_IN_0);
	int a0 = acc / 10;

	//int a0 = analogRead(PIN_ANALOG_IN_0); 
	
	
	LogD("GPIO.AI0: raw=%d, percent=%.2f, volt=%.2f", 
			a0,
			(((float) a0) / (1 << GPIO_ANALOG_RESOLUTION)),
			(((float) a0) / (1 << GPIO_ANALOG_RESOLUTION)) * getSysVoltage()
		);

// TODO move to one sensor class
#ifdef ENABLE_SENSOR_INA190
	float v = (((float) a0) / (1 << GPIO_ANALOG_RESOLUTION)) * getSysVoltage();
	v -= getSysVoltage() / 2.0f;

	float curr = v / (25.0 * 0.01);

	curr -= 0.077f;

	LogD("INA190: v=%.3f, curr=%.5f", v, curr);
#endif // ENABLE_SENSOR_INA190
	
#endif // ENABLE_ANALOG_IN_0

#ifdef ENABLE_ANALOG_IN_1
	
	int a0 = analogRead(PIN_ANALOG_IN_1); 
	LogD("GPIO.AI1: raw=%d, percent=%.2f, volt=%.2f", 
			a0,
			(((float) a0) / (1 << GPIO_ANALOG_RESOLUTION)),
			(((float) a0) / (1 << GPIO_ANALOG_RESOLUTION)) * getSysVoltage()
		);
	
#endif // ENABLE_ANALOG_IN_1

	//Display_PrintInfoSub2(s_printf("trigger: %d", (millis() - prev_last_time_trigger1) / 1000));

#endif // ENABLE_PRINT_STATUS_GPIO
}



void GPIOModule_End() 
{
	


	switchBoardLED(false);
}

bool Button1_isDown() {
#ifdef ENABLE_BUTTON1
	return Button1.isClicked();
#else
	return false;
#endif // ENABLE_BUTTON1
}

bool Button2_isDown() {
#ifdef ENABLE_BUTTON2
	return Button2.isClicked();
#else
	return false;
#endif
}


void switchBoardLED(bool ON)
{
#ifdef ENABLE_LED_BUILTIN
	digitalWrite(PIN_LED_BUILTIN, ON ? LED_BUILTIN_ON_LEVEL : !LED_BUILTIN_ON_LEVEL);
#endif // ENABLE_LED_BUILTIN
}


void setDigitalOut0(bool state)
{
#ifdef ENABLE_DIGITAL_OUT_0
	digitalWrite(PIN_DIGITAL_OUT_0, state);
#endif // ENABLE_DIGITAL_OUT_0
}

float getAnalogIn0()
{
#ifdef ENABLE_ANALOG_IN_0
	return (((float) analogRead(PIN_ANALOG_IN_0)) / (1 << GPIO_ANALOG_RESOLUTION));
#endif // ENABLE_ANALOG_IN_0

	return 0.0f;
}

float getAnalog0In_Volt()
{
#ifdef ENABLE_ANALOG_IN_0
	return (((float) analogRead(PIN_ANALOG_IN_0)) / (1 << GPIO_ANALOG_RESOLUTION)) * getSysVoltage();
#endif // ENABLE_ANALOG_IN_0

	return 0.0f;
}

float getAnalogIn1()
{
#ifdef ENABLE_ANALOG_IN_1
	return (((float) analogRead(PIN_ANALOG_IN_1)) / (1 << GPIO_ANALOG_RESOLUTION));
#endif // ENABLE_ANALOG_IN_1

	return 0.0f;
}

float getAnalog1In_Volt()
{
#ifdef ENABLE_ANALOG_IN_1
	return (((float) analogRead(PIN_ANALOG_IN_1)) / (1 << GPIO_ANALOG_RESOLUTION)) * getSysVoltage();
#endif // ENABLE_ANALOG_IN_1

	return 0.0f;
}

void setAnalogOut0(float v)
{
#ifdef ENABLE_ANALOG_OUT_0
	//TODO implement
#endif // ENABLE_ANALOG_OUT_0
}

#pragma region BUTTONS


extern void Mode_Button1_onClick();
extern void Mode_Button1_onLongClick();

void Button1_onClick()
{
	Log("Button1_onClick()");
	
	Mode_Button1_onClick();
}

void Button1_onLongClick()
{
	Log("Button1_onLongClick()");
	
	Mode_Button1_onLongClick();
}

#pragma endregion
