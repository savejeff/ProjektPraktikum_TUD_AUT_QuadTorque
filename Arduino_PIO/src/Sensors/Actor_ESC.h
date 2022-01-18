#pragma once

#include <jDefines.h>

#include "jDevice.h"

//Servo Library only supports AVR, SAMD and STM32F4
#if defined(PLATFORM_AVR) || defined(PLATFORM_SAMD)

#include <Servo.h>

#define ACTOR_ESC_PARAM_STARTUP_DURATION (5 * 1000)

class Actor_ESC_Class : jDevice {
public:
  Actor_ESC_Class(String name, int pin_ctrl_pwm, int pin_esc_pwr, bool has_reverse=false)
			: jDevice(name)

	{ 
		_has_reverse = has_reverse;
		_pin_ctrl_pwm = pin_ctrl_pwm;
		_pin_esc_pwr = pin_esc_pwr;
	}

	bool begin() override;
	void end() override;

	void update() override;

	//Throttle between 0.0 and 1.0
	void setThrottle(float app)
	{
		this->app_rqst = LIMIT(0.0f, app, 1.0f);
		last_time_throttle = millis();
	}

	float getThrottle() { return app_current; }


	void print(const String& title) override;
	using jDevice::print;

protected:

	// updates ctrl output to ESC with new throttle position 
	// app: throttle position between 0.0 and 1.0
	void apply_throttle(float app);

	bool _has_reverse = false; //if has reverse -> start with 0 Throttle at 90° servo angle else start with 0°
	int _pin_ctrl_pwm = - 1;
	int _pin_esc_pwr = -1;

	int timeout_throttle = 5 * FACTOR_s_2_ms; //[ms]

	ulong last_time_throttle = 0;
	ulong last_time_loop = 0;
	ulong time_startup = 0;
	float app_current; //[0.0 - 1.0]
	float app_rqst; //[0.0 - 1.0]

	float max_app_accel = 0.5f; //[%/s] maximum change in app per second

	// minimum and maximum duty cycle of pwm out
	uint16_t pwm_duty_min_us = 1000; //[us]
	uint16_t pwm_duty_max_us = 2000; //[us]

	Servo servo;

};

#endif 