#include "Sensor_HX711.h"

bool Sensor_HX711_Class::begin() {
	jSensor::begin();
	
	hx711.begin(_pin_data, _pin_clock, _gain);
	hx711.power_up();
	
	return true;
}

void Sensor_HX711_Class::update() {
	
	if(millis() - lasttime_update < sampletime)
		return;
	if(!hx711.is_ready())
		return;
	
#ifdef DEBUG_HX711
	LogD("%s.dt: update=%d", this->name.c_str(), millis() - lasttime_update);
#endif // DEBUG_HX711

	lasttime_update = millis();

	value = read();

	value -= calib_zero;
	
}




uint32_t Sensor_HX711_Class::read() {

#ifdef DEBUG_HX711
	TRACK_DT_MILLIS_START0
#endif // DEBUG_HX711

	uint32_t v = hx711.read();
	
#ifdef DEBUG_HX711
	TRACK_DT_MILLIS_END0(dt);
	LogD("%s.dt: read=%d", this->name.c_str(), dt);
#endif // DEBUG_HX711

	return v;
}

