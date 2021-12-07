#include "GPIOButton.h"


GPIOButton::GPIOButton(uint8_t pin, bool trigger_level)
{
	//set_interval(DEBOUNCE_INTERVAL);
	if(pin < 0)
		return;
	
    this->pin = pin;
	this->trigger_level = trigger_level;
#ifdef INPUT_PULLDOWN
	pinMode(pin, (trigger_level) ? INPUT_PULLDOWN : INPUT_PULLUP);
#else
	pinMode(pin, (trigger_level) ? INPUT : INPUT_PULLUP);
#endif

	previous_millis = millis();
	state = 0; //state is not equal to pin reading
}



void GPIOButton::set_interval(unsigned long DEBOUNCE_INTERVAL)
{
  this->DEBOUNCE_INTERVAL = DEBOUNCE_INTERVAL;
  this->rebounce_millis = 0;
}

void GPIOButton::rebounce(unsigned long interval)
{
	 this->rebounce_millis = interval;
}



int GPIOButton::update()
{
	if(pin < 0)
		return 0;

	stateChanged = 0;

	if ( debounce() ) {
        rebounce(0);
        stateChanged = 1;
    }

     // We need to rebounce, so simulate a state change
     
	if ( rebounce_millis && (millis() - previous_millis >= rebounce_millis) ) {
        previous_millis = millis();
		rebounce(0);
		stateChanged = 1;
	}


	if(fallingEdge())
		lasttime_falling = millis();

	if(risingEdge())
		lasttime_rising = millis();

	_is_click = fallingEdge() && !longclick_active;
		
	//Long Click logic
	ulong duration_clicked = millis() - lasttime_rising;
	//alternative Version 
	/*
	if(isClicked() && duration_clicked > LONGCLICK_DURATION)
	{
		//only set is_longclick once
		if(!longclick_active)
		{
			longclick_active = true;
			_is_longclick = true;
		}
	}
	else
		longclick_active = false;
	*/
	
	//only set is_longclick once
	_is_longclick = false;
	if(!longclick_active && isClicked() && duration_clicked > LONGCLICK_DURATION)
	{
		longclick_active = true;
		_is_longclick = true;
	}
	if(!isClicked())
		longclick_active = false;


	return stateChanged;
}


unsigned long GPIOButton::duration()
{
  return millis() - previous_millis;
}


bool GPIOButton::isClicked()
{
	return state;
}

bool GPIOButton::isLongClick() {
	//alternative Version 
	/*
	if(_is_longclick)
	{
		_is_longclick = false;
		return true;
	}
	
	return false;
	*/
	return _is_longclick;
}

bool GPIOButton::isClick()
{
	return _is_click;
}

// Protected: debounces the pin
int GPIOButton::debounce() {
	
	uint8_t newState = _read();
	if (state != newState) {
  		if (millis() - previous_millis >= DEBOUNCE_INTERVAL) {
  			previous_millis = millis();
  			state = newState;
  			return 1;
	}
  }
  
  return 0;
	
}

// The risingEdge method is true for one scan after the de-bounced input goes from off-to-on.
bool  GPIOButton::risingEdge() { 
	return stateChanged && state; 
	}
// The fallingEdge  method it true for one scan after the de-bounced input goes from on-to-off. 
bool  GPIOButton::fallingEdge() { 
	return stateChanged && !state; 
	}

