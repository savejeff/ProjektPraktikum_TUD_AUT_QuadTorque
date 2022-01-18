#include "Actor_ESC.h"

#include "global.h"

bool Actor_ESC_Class::begin() {
	
	
	if(_pin_esc_pwr != -1)
		pinMode(_pin_esc_pwr, INPUT); // Sets the echoPin as an Input

	// NEEDED??
	pinMode(_pin_ctrl_pwm, OUTPUT); // Sets the trigPin as an Output
	digitalWrite(_pin_ctrl_pwm, LOW);
	
	servo.attach(_pin_ctrl_pwm, pwm_duty_min_us, pwm_duty_max_us);  // (pin, min, max)
	servo.write(0);


	time_startup = millis();

	return jDevice::begin();
}


void Actor_ESC_Class::end() {

	jDevice::end();
}


void Actor_ESC_Class::apply_throttle(float app)
{
	// limit app to be between 0% and 100%
	//app = LIMIT(0.0f, app, 1.0f); //MAP also does LIMIT(0, app, 1)

	// new version that directly controlls duty length of pwm
	uint16_t value_us = (uint16_t) (MAP(app, 0.0f, 1.0f, pwm_duty_min_us, pwm_duty_max_us));
	servo.writeMicroseconds(value_us);

#ifdef DEBUG_ESC
	LogD("%s: micros=%d", name.c_str(), value_us);
#endif // DEBUG_ESC
	
	// old version using servo libs angle function
	//int angle = MAP((app * 100), 0, 100, 0, 180);
	//servo.write(angle);
	
}


void Actor_ESC_Class::update() 
{
	//check if esc is off -> reset time_startup
	if(_pin_esc_pwr != -1 && digitalRead(_pin_esc_pwr) == LOW)
	{
		time_startup = millis();
	}

	// if throttle command to old -> turn off 
	if(millis() - last_time_throttle > timeout_throttle)
	{
		app_current = 0;
		app_rqst = 0;
	}

	//startup period -> trottle 0%
	if(millis() - time_startup < ACTOR_ESC_PARAM_STARTUP_DURATION)
	{
		apply_throttle(0);

#ifdef DEBUG_ESC
		LogD("%s: startup=1", name.c_str());
#endif // DEBUG_ESC

	}
	else
	{
		float dt = (millis() - last_time_loop) * FACTOR_ms_2_s;
		float app_delta = dt * max_app_accel;

		// limit change of app_current by app_delta
		app_current = LIMIT(app_current - app_delta, app_rqst, app_current + app_delta);

		if(_has_reverse) // if ESC has reverse -> convert to 50% - 100%
			apply_throttle(MAP(app_current, 0.0f, 1.0f, 0.555f, 1.0f));
		else
			apply_throttle(app_current);
			
#ifdef DEBUG_ESC
		LogD("%s: startup=0", name.c_str());		
#endif // DEBUG_ESC
		
	}

	last_time_loop = millis();
}


void Actor_ESC_Class::print(const String& title) {
	Log("%s: app=%.3f", title.c_str(), 
		app_current
	);
}

