#include "SensorModule.h"

#ifdef ENABLE_SENSOR


#include "global.h"
#include "SERCOM_Module.h"
#include "GPIOModule.h"



#ifdef ENABLE_SENSOR_INA219
#include <Adafruit_INA219.h>
Adafruit_INA219 Sensor_INA219;
#endif // ENABLE_SENSOR_INA219


#ifdef ENABLE_SENSOR_HX711
#include <Sensors/Sensor_HX711.h>
Sensor_HX711_Class Sensor_HX711(PIN_HX711_CLOCK, PIN_HX711_DATA);
#endif // ENABLE_SENSOR_HX711

#ifdef ENABLE_SENSOR_HX711_2
#include <Sensors/Sensor_HX711.h>
Sensor_HX711_Class Sensor_HX711_2(PIN_HX711_2_CLOCK, PIN_HX711_2_DATA);
#endif // ENABLE_SENSOR_HX711_2

#ifdef ENABLE_ACTOR_ESC
#include "Sensors/Actor_ESC.h"
Actor_ESC_Class Actor_ESC(PIN_PWM_OUT_ESC, PIN_ESC_PWR, true);
#endif // ENABLE_ACTOR_ESC


#endif // ENABLE_SENSOR

void SensorModule_Init()
{
#ifdef ENABLE_SENSOR
	Log("sen.state: init");

#ifdef ENABLE_SENSOR_INA219
#ifndef I2C_INA219
#define I2C_INA219 I2C0
#endif 
	Sensor_INA219.begin(&I2C_INA219);
	//Sensor_INA219.setCalibration(0.001f, 10.0f);
	//Sensor_INA219.setCalibration_32V_2A();
	Sensor_INA219.setCalibration(0.01f, 20.0f);
	//Sensor_INA219.setCalibration(0.001f, 320.0f);
	
#endif // ENABLE_SENSOR_INA219

#ifdef ENABLE_SENSOR_HX711
	Sensor_HX711.begin();
#endif // ENABLE_SENSOR_HX711

#ifdef ENABLE_SENSOR_HX711_2
	Sensor_HX711_2.begin();
#endif // ENABLE_SENSOR_HX711_2

#ifdef ENABLE_ACTOR_ESC
	Actor_ESC.begin();
#endif // ENABLE_ACTOR_ESC

#endif // ENABLE_SENSOR
}

void SensorModule_Update() {
#ifdef ENABLE_SENSOR
	static ulong last_time_SimSensor = 0;
	if (millis() - last_time_SimSensor < SAMPLETIME_SENSOR)
		return;
	last_time_SimSensor = millis();
  

#ifdef ENABLE_SENSOR_INA219
	
	EXECUTE_EVERY(125)

		Log("INA219: volt=%.2f, curr=%.3f, pwr=%.1f",
			Sensor_INA219.getBusVoltage_V(),
			Sensor_INA219.getCurrent_A(),
			Sensor_INA219.getPower_W()
		);

	EXECUTE_EVERY_END

#endif // ENABLE_SENSOR_INA219

#ifdef ENABLE_SENSOR_HX711
	EXECUTE_EVERY(25)
		Sensor_HX711.update();
		Sensor_HX711.print("HX711");
	EXECUTE_EVERY_END
#endif // ENABLE_SENSOR_HX711

#ifdef ENABLE_SENSOR_HX711_2
	EXECUTE_EVERY(25)
		Sensor_HX711_2.update();
		Sensor_HX711_2.print("HX711#2");
	EXECUTE_EVERY_END
#endif // ENABLE_SENSOR_HX711_2

#ifdef ENABLE_ACTOR_ESC

	EXECUTE_EVERY(250)
		
		float app = 0.0f;
		if(USE_ANALOG_THROTTLE)
		{
			app = getAnalogIn0();
			if(app < 0.075)
				app = 0.0f;
		}
		else
		{
			if(millis() - TIME_UPDATE_APP > 4 * 1000) //check if timeout
				app = 0.0f;
			else
				app = APP;
		}

		Actor_ESC.setThrottle(app);
		Actor_ESC.update();

	EXECUTE_EVERY_END

#endif // ENABLE_ACTOR_ESC


	//Display every Xs
	static ulong last_time_display = 0;
	if (enabled_PrintStatus && millis() - last_time_display > LOOPTIME_PRINTSTATS)
	{
		last_time_display = millis();

		SensorModule_PrintStatus();
	}

#endif // ENABLE_SENSOR
}


void SensorModule_End()
{
#ifdef ENABLE_SENSOR

#endif // ENABLE_SENSOR
}

void SensorModule_PrintStatus()
{
#ifdef ENABLE_SENSOR
#ifdef ENABLE_PRINT_STATUS_SENSOR

#ifdef ENABLE_SENSOR_HX711
	//Sensor_HX711.print();
#endif // ENABLE_SENSOR_HX711

#ifdef ENABLE_SENSOR_HX711_2
	//Sensor_HX711_2.print();
#endif // ENABLE_SENSOR_HX711_2


#endif // ENABLE_PRINT_STATUS_SENSOR
#endif // ENABLE_SENSOR
}
