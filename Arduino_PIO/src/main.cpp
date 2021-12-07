#include "global.h"
#include "SystemModule.h"
#include "SERCOM_Module.h"
#include "GPIOModule.h"
#include "SensorModule.h"


bool terminate = false;


void Mode_Button1_onClick()
{
	LogD(">>> Button1 Click!");

}

void Mode_Button1_onLongClick()
{
	LogD(">>> Button1 LongClick!");
	terminate = true;
}


void setup() {

	/************ INIT MODULES *************/

	SERCOM_Module_Init();

	SystemModule_Init();

	GPIOModule_Init();

#ifdef ENABLE_SENSOR
	SensorModule_Init();
#endif // ENABLE_SENSOR

	
	for(int i = 0; i < 5; i++)
	{
		switchBoardLED(true);
		delay(100);
		switchBoardLED(false);
		delay(100);
		jWatchdog_reset();
	}	
	
	
	while(!terminate)
	{

		/************ LOOP MODULES *************/

		SERCOM_Module_Update();

		SystemModule_Update();

		GPIOModule_Update();

#ifdef ENABLE_SENSOR
		SensorModule_Update();
#endif // ENABLE_SENSOR	
		

		EXECUTE_EVERY(1000)
			
			//LogD("loop");

		EXECUTE_EVERY_END


		delay(1);
	}

	LogD("- - Terminating - -");

	/************ END MODULES *************/

	


#ifdef ENABLE_SENSOR
	SensorModule_End();
#endif // ENABLE_SENSOR


	SystemModule_End();

	//SERCOM_Module_End();

	//GPIOModule_End();


	LogD("- - terminate - -");

	while (true)
	{
		delay(1000);
	}
	
}


void loop() {

	
	
}