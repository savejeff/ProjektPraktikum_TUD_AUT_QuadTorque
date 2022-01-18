#include "SensorModule.h"

#ifdef ENABLE_SENSOR


#include "global.h"
#include "SERCOM_Module.h"
#include "GPIOModule.h"



#ifdef ENABLE_SENSOR_INA219
#ifndef I2C_INA219
#define I2C_INA219 I2C0
#endif

#include "Sensors/Sensor_INA219.h"
Sensor_INA219_Class Sensor_INA219(&I2C_INA219);
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
Actor_ESC_Class Actor_ESC("esc", PIN_ESC_PWM, PIN_ESC_PWR, true);
#endif // ENABLE_ACTOR_ESC




#endif // ENABLE_SENSOR


/******************************* Module Functions ***********************************************/


void SensorModule_Init()
{
#ifdef ENABLE_SENSOR
	Log(F("sen.state: init"));

#ifdef ENABLE_SENSOR_INA219

	Sensor_INA219.begin();
	
	//Sensor_INA219.setMultisampleMode(64);
	Sensor_INA219.setMultisampleMode(128);
	

	//Sensor_INA219.setCalibration_16V_400mA(); 	//100mOhm 400mA
	//Sensor_INA219.setCalibration_32V_2A(); 		//100mOhm 2A
	Sensor_INA219.setCalibration(0.01f, 32.0f); 	//10mOhm 32A
	//Sensor_INA219.setCalibration(0.001f, 320.0f); //5mOhm 32A
	
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

	Log(F("sen.state: init done"));

#endif // ENABLE_SENSOR
}

void SensorModule_Update() {
#ifdef ENABLE_SENSOR
	static ulong last_time_SimSensor = 0;
	if (millis() - last_time_SimSensor < SAMPLETIME_SENSOR)
		return;
	last_time_SimSensor = millis();
  

#ifdef ENABLE_SENSOR_INA219
	
	EXECUTE_EVERY(100)

		Log("INA219: volt=%.2f, curr=%.3f, pwr=%.1f",
			Sensor_INA219.getBusVoltage_V(),
			Sensor_INA219.getCurrent_A(),
			Sensor_INA219.getPower_W()
		);

	EXECUTE_EVERY_END

#endif // ENABLE_SENSOR_INA219

#ifdef ENABLE_SENSOR_HX711
	EXECUTE_EVERY(50)
		Sensor_HX711.update();
		Sensor_HX711.print("HX711");
	EXECUTE_EVERY_END
#endif // ENABLE_SENSOR_HX711

#ifdef ENABLE_SENSOR_HX711_2
	EXECUTE_EVERY(50)
		Sensor_HX711_2.update();
		Sensor_HX711_2.print("HX711#2");
	EXECUTE_EVERY_END
#endif // ENABLE_SENSOR_HX711_2

#ifdef ENABLE_ACTOR_ESC

	EXECUTE_EVERY(100)
		
		
		if(USE_ANALOG_THROTTLE)
		{
			float app = getAnalogIn0();
			if(app < 0.075)
				app = 0.0f;
			Actor_ESC.setThrottle(app);
		}
		else
		{
			if(is_valid(APP))
			{
				Actor_ESC.setThrottle(APP);
				APP = NAN;
			}
		}

		
		Actor_ESC.update();
		Actor_ESC.print();

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

#ifdef ENABLE_SENSOR_INA219
	Sensor_INA219.end();
#endif // ENABLE_SENSOR_INA219

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
