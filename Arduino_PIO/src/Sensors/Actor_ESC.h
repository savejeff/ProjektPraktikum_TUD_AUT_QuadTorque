#pragma once

#include <jOS.h>
#include "jDevice.h"

//Servo Library only supports AVR, SAMD and STM32F4
#if defined(PLATFORM_AVR) || defined(PLATFORM_SAMD)

#include <Servo.h>

#define ACTOR_ESC_PARAM_STARTUP_DURATION (5 * 1000)

class Actor_ESC_Class : jDevice {
public:
  Actor_ESC_Class(int pin_ctrl_pwm, int pin_esc_pwr, bool has_reverse=false)
			: jDevice("ESC")
	{ 
		_has_reverse = has_reverse;
		_pin_ctrl_pwm = pin_ctrl_pwm;
		_pin_esc_pwr = pin_esc_pwr;
	}

	bool begin() override;

	void update() override;

	//Throttle between 0 and 1
	void setThrottle(float app)
	{
		this->app = LIMIT(0.0f, app, 1.0f);
	}

protected:

	bool _has_reverse = false; //if has reverse -> start with 0 Throttle at 90° servo angle else start with 0°
	int _pin_ctrl_pwm = - 1;
	int _pin_esc_pwr = -1;

	ulong time_startup = 0;
	float app;

	Servo servo;

};

#endif 