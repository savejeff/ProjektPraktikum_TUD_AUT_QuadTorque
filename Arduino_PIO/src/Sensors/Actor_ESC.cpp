#include "Actor_ESC.h"

#if defined(PLATFORM_AVR) || defined(PLATFORM_SAMD)

/*

static bool isr_pin_flag = false;
static int isr_pin = 0;
static long time_low = 0;
static long time_high = 0;
static int last_state = 0;

void isr_hcsr04_echo()
{
	ulong t = micros();
  	last_state = digitalRead(isr_pin);
	isr_pin_flag = true;

	if (last_state)
		time_high = t;
	else
		time_low = t;
}

*/





bool Actor_ESC_Class::begin() {
	pinMode(_pin_ctrl_pwm, OUTPUT); // Sets the trigPin as an Output
	//digitalWrite(_pin_ctrl_pwm, LOW);
	if(_pin_esc_pwr != -1)
		pinMode(_pin_esc_pwr, INPUT); // Sets the echoPin as an Input

	servo.attach(_pin_ctrl_pwm, 1000, 2000);  // (pin, min, max)
	servo.write(0);


	//isr_pin = _pin_echo;
	//attachInterrupt(digitalPinToInterrupt(_pin_echo), isr_hcsr04_echo, CHANGE);

	time_startup = millis();

	return jDevice::begin();
}


void Actor_ESC_Class::update() 
{
	//check if esc is off -> reset time_startup
	if(_pin_esc_pwr != -1 && digitalRead(_pin_esc_pwr) == LOW)
	{
		time_startup = millis();
	}

	//startup period -> trottle 0%
	if(millis() - time_startup < ACTOR_ESC_PARAM_STARTUP_DURATION)
	{
		servo.write(0);
		Log("esc: startup=1, app=0, angle=0");
	}
	else
	{
		
		uint8_t appi = app * 100;
		uint8_t angle;
		if(_has_reverse)
		{
			if(appi == 0)
				angle = 90; 
			else
				angle = MAP(appi, 0, 100, 103, 180); //TODO replace low angle (currently 100) to parameter
		}
		else
			angle = MAP(appi, 0, 100, 0, 180);
		servo.write(angle);
		
		//Log("esc: app=%.2f, v=%d", app, angle);
		Log("esc: app=%.2f, angle=%d", app, angle);
	}
}

#endif 