#pragma once 

#include "Defines.h"


class GPIOButton
{

public:
	// Initialize
	GPIOButton() {}
	GPIOButton(uint8_t pin, bool trigger_level); 
	// Sets the debounce interval
	void set_interval(unsigned long DEBOUNCE_INTERVAL); 
	// Updates the pin
	// Returns 1 if the state changed
	// Returns 0 if the state did not change
	int update(); 
	// Forces the pin to signal a change (through update()) in X milliseconds 
	// even if the state does not actually change
	// Example: press and hold a button and have it repeat every X milliseconds
	void rebounce(unsigned long interval); 
	// Returns the updated pin state
	bool isClicked();

	bool isLongClick(); //on Long Button click - only once true and resets until button released
	bool isClick(); //on Button release
	
	// Returns the number of milliseconds the pin has been in the current state
	unsigned long duration();
	// The risingEdge method is true for one scan after the de-bounced input goes from off-to-on.
	bool risingEdge();
	// The fallingEdge  method it true for one scan after the de-bounced input goes from on-to-off. 
	bool fallingEdge();
	
protected:

	bool _read() {
		return digitalRead(pin) == trigger_level;
	}

	int debounce();

	ulong DEBOUNCE_INTERVAL = 100;
	ulong LONGCLICK_DURATION = 1000;

	uint8_t pin = -1;

	bool state = 0;
	ulong previous_millis = 0; 
	ulong rebounce_millis = 0;

	ulong lasttime_falling = 0;
	ulong lasttime_rising = 0;

	bool longclick_active = false;
	bool _is_longclick = false;
	bool _is_click = false;


	bool stateChanged = false;
	bool trigger_level = LOW;
};


