/*!
 * @file Adafruit_INA219.cpp
 *
 * @mainpage Adafruit INA219 current/power monitor IC
 *
 * @section intro_sec Introduction
 *
 *  Driver for the INA219 current sensor
 *
 *  This is a library for the Adafruit INA219 breakout
 *  ----> https://www.adafruit.com/products/904
 *
 *  Adafruit invests time and resources providing this open source code,
 *  please support Adafruit and open-source hardware by purchasing
 *  products from Adafruit!
 *
 * @section author Author
 *
 * Written by Kevin "KTOWN" Townsend for Adafruit Industries.
 *
 * @section license License
 *
 * BSD license, all text here must be included in any redistribution.
 *
 */

#include "Adafruit_INA219.h"



/** read **/
#define INA219_READ (0x01)

/*=========================================================================
		CONFIG REGISTER (R/W)
**************************************************************************/

/** config register address **/
#define INA219_REG_CONFIG (0x00)

/** reset bit **/
#define INA219_CONFIG_RESET (0x8000) // Reset Bit

/** mask for bus voltage range **/
#define INA219_CONFIG_BVOLTAGERANGE_MASK (0x2000) // Bus Voltage Range Mask

/** bus voltage range values **/
enum {
	INA219_CONFIG_BVOLTAGERANGE_16V = (0x0000), // 0-16V Range
	INA219_CONFIG_BVOLTAGERANGE_32V = (0x2000), // 0-32V Range
};

/** mask for gain bits **/
#define INA219_CONFIG_GAIN_MASK (0x1800) // Gain Mask

/** values for gain bits **/
enum {
	INA219_CONFIG_GAIN_1_40MV = (0x0000),  // Gain 1, 40mV Range
	INA219_CONFIG_GAIN_2_80MV = (0x0800),  // Gain 2, 80mV Range
	INA219_CONFIG_GAIN_4_160MV = (0x1000), // Gain 4, 160mV Range
	INA219_CONFIG_GAIN_8_320MV = (0x1800), // Gain 8, 320mV Range
};

/** mask for bus ADC resolution bits **/
#define INA219_CONFIG_BADCRES_MASK (0x0780)

/** values for bus ADC resolution **/
enum {
	INA219_CONFIG_BADCRES_9BIT = (0x0000),  // 9-bit bus res = 0..511
	INA219_CONFIG_BADCRES_10BIT = (0x0080), // 10-bit bus res = 0..1023
	INA219_CONFIG_BADCRES_11BIT = (0x0100), // 11-bit bus res = 0..2047
	INA219_CONFIG_BADCRES_12BIT = (0x0180), // 12-bit bus res = 0..4097
};

/** mask for shunt ADC resolution bits **/
#define INA219_CONFIG_SADCRES_MASK                                             \
	(0x0078) // Shunt ADC Resolution and Averaging Mask

/** values for shunt ADC resolution **/
enum {
	INA219_CONFIG_SADCRES_9BIT_1S_84US = (0x0000),   // 1 x 9-bit shunt sample
	INA219_CONFIG_SADCRES_10BIT_1S_148US = (0x0008), // 1 x 10-bit shunt sample
	INA219_CONFIG_SADCRES_11BIT_1S_276US = (0x0010), // 1 x 11-bit shunt sample
	INA219_CONFIG_SADCRES_12BIT_1S_532US = (0x0018), // 1 x 12-bit shunt sample
	INA219_CONFIG_SADCRES_12BIT_2S_1060US =
			(0x0048), // 2 x 12-bit shunt samples averaged together
	INA219_CONFIG_SADCRES_12BIT_4S_2130US =
			(0x0050), // 4 x 12-bit shunt samples averaged together
	INA219_CONFIG_SADCRES_12BIT_8S_4260US =
			(0x0058), // 8 x 12-bit shunt samples averaged together
	INA219_CONFIG_SADCRES_12BIT_16S_8510US =
			(0x0060), // 16 x 12-bit shunt samples averaged together
	INA219_CONFIG_SADCRES_12BIT_32S_17MS =
			(0x0068), // 32 x 12-bit shunt samples averaged together
	INA219_CONFIG_SADCRES_12BIT_64S_34MS =
			(0x0070), // 64 x 12-bit shunt samples averaged together
	INA219_CONFIG_SADCRES_12BIT_128S_69MS =
			(0x0078), // 128 x 12-bit shunt samples averaged together
};

/** mask for operating mode bits **/
#define INA219_CONFIG_MODE_MASK (0x0007) // Operating Mode Mask

/** values for operating mode **/
enum {
	INA219_CONFIG_MODE_POWERDOWN,
	INA219_CONFIG_MODE_SVOLT_TRIGGERED,
	INA219_CONFIG_MODE_BVOLT_TRIGGERED,
	INA219_CONFIG_MODE_SANDBVOLT_TRIGGERED,
	INA219_CONFIG_MODE_ADCOFF,
	INA219_CONFIG_MODE_SVOLT_CONTINUOUS,
	INA219_CONFIG_MODE_BVOLT_CONTINUOUS,
	INA219_CONFIG_MODE_SANDBVOLT_CONTINUOUS
};

/** shunt voltage register **/
#define INA219_REG_SHUNTVOLTAGE (0x01)

/** bus voltage register **/
#define INA219_REG_BUSVOLTAGE (0x02)

/** power register **/
#define INA219_REG_POWER (0x03)

/** current register **/
#define INA219_REG_CURRENT (0x04)

/** calibration register **/
#define INA219_REG_CALIBRATION (0x05)


/*!
 *  @brief  Sends a single command byte over I2C
 *  @param  reg
 *          register address
 *  @param  value
 *          value to write
 */
void Adafruit_INA219::wireWriteRegister(uint8_t reg, uint16_t value) {
	_i2c->beginTransmission(ina219_i2caddr);
	_i2c->write(reg);                 // Register
	_i2c->write((value >> 8) & 0xFF); // Upper 8-bits
	_i2c->write(value & 0xFF);        // Lower 8-bits
	_i2c->endTransmission();
}

/*!
 *  @brief  Reads a 16 bit values over I2C
 *  @param  reg
 *          register address
 *  @param  *value
 *          read value
 */
void Adafruit_INA219::wireReadRegister(uint8_t reg, uint16_t *value) {

	_i2c->beginTransmission(ina219_i2caddr);
	_i2c->write(reg); // Register
	_i2c->endTransmission();

	delay(1); // Max 12-bit conversion time is 586us per sample

	_i2c->requestFrom(ina219_i2caddr, (uint8_t)2);
	// Shift values to create properly formed integer
	*value = ((_i2c->read() << 8) | _i2c->read());
}

/*!
 *  @brief  Configures to INA219 to be able to measure up to 32V and 2A
 *          of current.  Each unit of current corresponds to 100uA, and
 *          each unit of power corresponds to 2mW. Counter overflow
 *          occurs at 3.2A.
 *  @note   These calculations assume a 0.1 ohm resistor is present
 */
void Adafruit_INA219::setCalibration_32V_2A() {
	// By default we use a pretty huge range for the input voltage,
	// which probably isn't the most appropriate choice for system
	// that don't use a lot of power.  But all of the calculations
	// are shown below if you want to change the settings.  You will
	// also need to change any relevant register settings, such as
	// setting the VBUS_MAX to 16V instead of 32V, etc.

	// VBUS_MAX = 32V             (Assumes 32V, can also be set to 16V)
	// VSHUNT_MAX = 0.32          (Assumes Gain 8, 320mV, can also be 0.16, 0.08, 0.04)
	float RSHUNT = 0.1; //               (Resistor value in ohms)

	// 1. Determine max possible current
	// MaxPossible_I = VSHUNT_MAX / RSHUNT
	// MaxPossible_I = 3.2A

	// 2. Determine max expected current
	// MaxExpected_I = 2.0A

	// 3. Calculate possible range of LSBs (Min = 15-bit, Max = 12-bit)
	// MinimumLSB = MaxExpected_I/32767
	// MinimumLSB = 0.000061              (61uA per bit)
	// MaximumLSB = MaxExpected_I/4096
	// MaximumLSB = 0,000488              (488uA per bit)

	// 4. Choose an LSB between the min and max values
	//    (Preferrably a roundish number close to MinLSB)
	float current_LSB = 0.0001; // (100uA per bit)

	// 5. Compute the calibration register
	float calVal_float = truncf(0.04096f / (current_LSB * RSHUNT));
	// Cal = 4096 (0x1000)

	//calVal = 4096;
	calVal = (uint32_t) calVal_float;

	// 6. Calculate the power LSB
	// PowerLSB = 20 * CurrentLSB
	// PowerLSB = 0.002 (2mW per bit)

	// 7. Compute the maximum current and shunt voltage values before overflow
	//
	// Max_Current = Current_LSB * 32767
	// Max_Current = 3.2767A before overflow
	//
	// If Max_Current > Max_Possible_I then
	//    Max_Current_Before_Overflow = MaxPossible_I
	// Else
	//    Max_Current_Before_Overflow = Max_Current
	// End If
	//
	// Max_ShuntVoltage = Max_Current_Before_Overflow * RSHUNT
	// Max_ShuntVoltage = 0.32V
	//
	// If Max_ShuntVoltage >= VSHUNT_MAX
	//    Max_ShuntVoltage_Before_Overflow = VSHUNT_MAX
	// Else
	//    Max_ShuntVoltage_Before_Overflow = Max_ShuntVoltage
	// End If

	// 8. Compute the Maximum Power
	// MaximumPower = Max_Current_Before_Overflow * VBUS_MAX
	// MaximumPower = 3.2 * 32V
	// MaximumPower = 102.4W

	// Set multipliers to convert raw current/power values
	currentDivider_mA = 10; // Current LSB = 100uA per bit (1000/100 = 10)
	pwrMultiplier_mW = 2; // Power LSB = 1mW per bit (2/1)

	LogD("INA219: current_LSB=%f, calVal=%ld, calVal_float=%f, currentDivider_mA=%f, pwrMultiplier_mW=%f", 
				current_LSB,
				calVal, 
				calVal_float,
				currentDivider_mA, 
				pwrMultiplier_mW
		);

	// Set Calibration register to 'Cal' calculated above
	wireWriteRegister(INA219_REG_CALIBRATION, calVal);

	// Set Config register to take into account the settings above
	uint16_t config = INA219_CONFIG_BVOLTAGERANGE_32V |
										INA219_CONFIG_GAIN_8_320MV | INA219_CONFIG_BADCRES_12BIT |
										INA219_CONFIG_SADCRES_12BIT_1S_532US |
										INA219_CONFIG_MODE_SANDBVOLT_CONTINUOUS;
	wireWriteRegister(INA219_REG_CONFIG, config);
}

/*!
 *  @brief  Configures to INA219 to be able to measure up to 32V and 2A
 *          of current.  Each unit of current corresponds to 100uA, and
 *          each unit of power corresponds to 2mW. Counter overflow
 *          occurs at 3.2A.
 *  @note   These calculations assume a 0.1 ohm resistor is present
 */
void Adafruit_INA219::setCalibration(float resistor, float current_range) 
{
	// By default we use a pretty huge range for the input voltage,
	// which probably isn't the most appropriate choice for system
	// that don't use a lot of power.  But all of the calculations
	// are shown below if you want to change the settings.  You will
	// also need to change any relevant register settings, such as
	// setting the VBUS_MAX to 16V instead of 32V, etc.

	//float VBUS_MAX = 32; //V             (Assumes 32V, can also be set to 16V)
	//float VSHUNT_MAX = 0.32; //V          (Assumes Gain 8, 320mV, can also be 0.16, 0.08, 0.04)
	//float RSHUNT = resistor; //0.01               (Resistor value in ohms)

	// 1. Determine max possible current
	//float MaxPossible_I = VSHUNT_MAX / RSHUNT;
	// MaxPossible_I = 32.0A

	// 2. Determine max expected current
	//float MaxExpected_I = 10.0; //A

	// 3. Calculate possible range of LSBs (Min = 15-bit, Max = 12-bit)
	//float MinimumLSB = MaxExpected_I / 32767;
	// MinimumLSB = 0.000061              (61uA per bit)
	//float MaximumLSB = MaxExpected_I / 4096;
	// MaximumLSB = 0,000488              (488uA per bit)

	// 4. Choose an LSB between the min and max values
	//    (Preferrably a roundish number close to MinLSB)
	//float CurrentLSB = (MinimumLSB + MaximumLSB) / 2; // 0.0001 (100uA per bit)

	// 5. Compute the calibration register
	//float Cal = trunc (0.04096 / (CurrentLSB * RSHUNT))
	// Cal = 4096 (0x1000)

	//calVal = 4096;

	// 6. Calculate the power LSB
	// PowerLSB = 20 * CurrentLSB
	// PowerLSB = 0.002 (2mW per bit)

	// 7. Compute the maximum current and shunt voltage values before overflow
	//
	// Max_Current = Current_LSB * 32767
	// Max_Current = 3.2767A before overflow
	//
	// If Max_Current > Max_Possible_I then
	//    Max_Current_Before_Overflow = MaxPossible_I
	// Else
	//    Max_Current_Before_Overflow = Max_Current
	// End If
	//
	// Max_ShuntVoltage = Max_Current_Before_Overflow * RSHUNT
	// Max_ShuntVoltage = 0.32V
	//
	// If Max_ShuntVoltage >= VSHUNT_MAX
	//    Max_ShuntVoltage_Before_Overflow = VSHUNT_MAX
	// Else
	//    Max_ShuntVoltage_Before_Overflow = Max_ShuntVoltage
	// End If

	// 8. Compute the Maximum Power
	// MaximumPower = Max_Current_Before_Overflow * VBUS_MAX
	// MaximumPower = 3.2 * 32V
	// MaximumPower = 102.4W

	// Set multipliers to convert raw current/power values
	//currentDivider_mA = 10; // Current LSB = 100uA per bit (1000/100 = 10)
	//pwrMultiplier_mW = 2; // Power LSB = 1mW per bit (2/1)

	//__________________________________________________________________________________
	//Example: 
	//Rshunt = 0.002ohm 
	//Max Expected Current = 15A
	
	float current_LSB = abs(current_range / (1l << 15)); //457.7uA/bit

	//Cal=trunc[0.04096/(Current_LSB*R)]=44814
	float calVal_float = 0.04096 / (current_LSB * resistor);
	calVal = trunc(0.04096f / (current_LSB * resistor));
	
	currentDivider_mA = 0.001f / current_LSB;
	pwrMultiplier_mW = 1000.0 * (20.0 * current_LSB); // FACTOR_W_2_mW * PowerLSB

	LogD("INA219: current_LSB=%f, calVal=%ld, calVal_float=%f, currentDivider_mA=%f, pwrMultiplier_mW=%f", 
				current_LSB,
				calVal, 
				calVal_float,
				currentDivider_mA, 
				pwrMultiplier_mW
		);


	// Set Calibration register to 'Cal' calculated above
	wireWriteRegister(INA219_REG_CALIBRATION, calVal);

	// Set Config register to take into account the settings above
	uint16_t config = INA219_CONFIG_BVOLTAGERANGE_32V |
										INA219_CONFIG_GAIN_8_320MV | INA219_CONFIG_BADCRES_12BIT |
										INA219_CONFIG_SADCRES_12BIT_1S_532US |
										INA219_CONFIG_MODE_SANDBVOLT_CONTINUOUS;
	wireWriteRegister(INA219_REG_CONFIG, config);
}

/*!
 *  @brief  Set power save mode according to parameters
 *  @param  on
 *          boolean value
 */
void Adafruit_INA219::powerSave(bool on) {
	uint16_t current;
	wireReadRegister(INA219_REG_CONFIG, &current);
	uint8_t next;
	if (on) {
		next = current | INA219_CONFIG_MODE_POWERDOWN; 
	} else {
		next = current & ~INA219_CONFIG_MODE_POWERDOWN; 
	}
	wireWriteRegister(INA219_REG_CONFIG, next);
}


/*!
 *  @brief  Configures to INA219 to be able to measure up to 32V and 1A
 *          of current.  Each unit of current corresponds to 40uA, and each
 *          unit of power corresponds to 800�W. Counter overflow occurs at
 *          1.3A.
 *  @note   These calculations assume a 0.1 ohm resistor is present
 */
void Adafruit_INA219::setCalibration_32V_1A() {
	// By default we use a pretty huge range for the input voltage,
	// which probably isn't the most appropriate choice for system
	// that don't use a lot of power.  But all of the calculations
	// are shown below if you want to change the settings.  You will
	// also need to change any relevant register settings, such as
	// setting the VBUS_MAX to 16V instead of 32V, etc.

	// VBUS_MAX = 32V		(Assumes 32V, can also be set to 16V)
	// VSHUNT_MAX = 0.32	(Assumes Gain 8, 320mV, can also be 0.16, 0.08, 0.04)
	// RSHUNT = 0.1			(Resistor value in ohms)

	// 1. Determine max possible current
	// MaxPossible_I = VSHUNT_MAX / RSHUNT
	// MaxPossible_I = 3.2A

	// 2. Determine max expected current
	// MaxExpected_I = 1.0A

	// 3. Calculate possible range of LSBs (Min = 15-bit, Max = 12-bit)
	// MinimumLSB = MaxExpected_I/32767
	// MinimumLSB = 0.0000305             (30.5�A per bit)
	// MaximumLSB = MaxExpected_I/4096
	// MaximumLSB = 0.000244              (244�A per bit)

	// 4. Choose an LSB between the min and max values
	//    (Preferrably a roundish number close to MinLSB)
	// CurrentLSB = 0.0000400 (40�A per bit)

	// 5. Compute the calibration register
	// Cal = trunc (0.04096 / (Current_LSB * RSHUNT))
	// Cal = 10240 (0x2800)

	calVal = 10240;

	// 6. Calculate the power LSB
	// PowerLSB = 20 * CurrentLSB
	// PowerLSB = 0.0008 (800�W per bit)

	// 7. Compute the maximum current and shunt voltage values before overflow
	//
	// Max_Current = Current_LSB * 32767
	// Max_Current = 1.31068A before overflow
	//
	// If Max_Current > Max_Possible_I then
	//    Max_Current_Before_Overflow = MaxPossible_I
	// Else
	//    Max_Current_Before_Overflow = Max_Current
	// End If
	//
	// ... In this case, we're good though since Max_Current is less than
	// MaxPossible_I
	//
	// Max_ShuntVoltage = Max_Current_Before_Overflow * RSHUNT
	// Max_ShuntVoltage = 0.131068V
	//
	// If Max_ShuntVoltage >= VSHUNT_MAX
	//    Max_ShuntVoltage_Before_Overflow = VSHUNT_MAX
	// Else
	//    Max_ShuntVoltage_Before_Overflow = Max_ShuntVoltage
	// End If

	// 8. Compute the Maximum Power
	// MaximumPower = Max_Current_Before_Overflow * VBUS_MAX
	// MaximumPower = 1.31068 * 32V
	// MaximumPower = 41.94176W

	// Set multipliers to convert raw current/power values
	currentDivider_mA = 25;    // Current LSB = 40uA per bit (1000/40 = 25)
	pwrMultiplier_mW = 0.8f; // Power LSB = 800uW per bit

	// Set Calibration register to 'Cal' calculated above
	wireWriteRegister(INA219_REG_CALIBRATION, calVal);

	// Set Config register to take into account the settings above
	uint16_t config = INA219_CONFIG_BVOLTAGERANGE_32V |
										INA219_CONFIG_GAIN_8_320MV | INA219_CONFIG_BADCRES_12BIT |
										INA219_CONFIG_SADCRES_12BIT_1S_532US |
										INA219_CONFIG_MODE_SANDBVOLT_CONTINUOUS;
	wireWriteRegister(INA219_REG_CONFIG, config);
}

/*!
 *  @brief set device to alibration which uses the highest precision for
 *     current measurement (0.1mA), at the expense of
 *     only supporting 16V at 400mA max.
 */
void Adafruit_INA219::setCalibration_16V_400mA() {

	// Calibration which uses the highest precision for
	// current measurement (0.1mA), at the expense of
	// only supporting 16V at 400mA max.

	// VBUS_MAX = 16V
	// VSHUNT_MAX = 0.04          (Assumes Gain 1, 40mV)
	// RSHUNT = 0.1               (Resistor value in ohms)

	// 1. Determine max possible current
	// MaxPossible_I = VSHUNT_MAX / RSHUNT
	// MaxPossible_I = 0.4A

	// 2. Determine max expected current
	// MaxExpected_I = 0.4A

	// 3. Calculate possible range of LSBs (Min = 15-bit, Max = 12-bit)
	// MinimumLSB = MaxExpected_I/32767
	// MinimumLSB = 0.0000122              (12uA per bit)
	// MaximumLSB = MaxExpected_I/4096
	// MaximumLSB = 0.0000977              (98uA per bit)

	// 4. Choose an LSB between the min and max values
	//    (Preferrably a roundish number close to MinLSB)
	// CurrentLSB = 0.00005 (50uA per bit)

	// 5. Compute the calibration register
	// Cal = trunc (0.04096 / (Current_LSB * RSHUNT))
	// Cal = 8192 (0x2000)

	calVal = 8192;

	// 6. Calculate the power LSB
	// PowerLSB = 20 * CurrentLSB
	// PowerLSB = 0.001 (1mW per bit)

	// 7. Compute the maximum current and shunt voltage values before overflow
	//
	// Max_Current = Current_LSB * 32767
	// Max_Current = 1.63835A before overflow
	//
	// If Max_Current > Max_Possible_I then
	//    Max_Current_Before_Overflow = MaxPossible_I
	// Else
	//    Max_Current_Before_Overflow = Max_Current
	// End If
	//
	// Max_Current_Before_Overflow = MaxPossible_I
	// Max_Current_Before_Overflow = 0.4
	//
	// Max_ShuntVoltage = Max_Current_Before_Overflow * RSHUNT
	// Max_ShuntVoltage = 0.04V
	//
	// If Max_ShuntVoltage >= VSHUNT_MAX
	//    Max_ShuntVoltage_Before_Overflow = VSHUNT_MAX
	// Else
	//    Max_ShuntVoltage_Before_Overflow = Max_ShuntVoltage
	// End If
	//
	// Max_ShuntVoltage_Before_Overflow = VSHUNT_MAX
	// Max_ShuntVoltage_Before_Overflow = 0.04V

	// 8. Compute the Maximum Power
	// MaximumPower = Max_Current_Before_Overflow * VBUS_MAX
	// MaximumPower = 0.4 * 16V
	// MaximumPower = 6.4W

	// Set multipliers to convert raw current/power values
	currentDivider_mA = 20;    // Current LSB = 50uA per bit (1000/50 = 20)
	pwrMultiplier_mW = 1.0f; // Power LSB = 1mW per bit

	// Set Calibration register to 'Cal' calculated above
	wireWriteRegister(INA219_REG_CALIBRATION, calVal);

	// Set Config register to take into account the settings above
	uint16_t config = INA219_CONFIG_BVOLTAGERANGE_16V |
										INA219_CONFIG_GAIN_1_40MV | INA219_CONFIG_BADCRES_12BIT |
										INA219_CONFIG_SADCRES_12BIT_1S_532US |
										INA219_CONFIG_MODE_SANDBVOLT_CONTINUOUS;
	wireWriteRegister(INA219_REG_CONFIG, config);
}

/*!
 *  @brief  Instantiates a new INA219 class
 *  @param addr the I2C address the device can be found on. Default is 0x40
 */
Adafruit_INA219::Adafruit_INA219(uint8_t addr) {
	ina219_i2caddr = addr;
	currentDivider_mA = 0;
	pwrMultiplier_mW = 0.0f;
}

/*!
 *  @brief  Setups the HW (defaults to 32V and 2A for calibration values)
 *  @param theWire the TwoWire object to use
 */
void Adafruit_INA219::begin(jI2C *theWire) {
	_i2c = theWire;
	init();
}

/*!
 *  @brief  begin I2C and set up the hardware
 */
void Adafruit_INA219::init() {
	//_i2c->begin();
	// Set chip to large range config values to start
	setCalibration_32V_2A();
}

/*!
 *  @brief  Gets the raw bus voltage (16-bit signed integer, so +-32767)
 *  @return the raw bus voltage reading
 */
int16_t Adafruit_INA219::getBusVoltage_raw() {
	uint16_t value;
	wireReadRegister(INA219_REG_BUSVOLTAGE, &value);

	// Shift to the right 3 to drop CNVR and OVF and multiply by LSB
	return (int16_t)((value >> 3) * 4);
}

/*!
 *  @brief  Gets the raw shunt voltage (16-bit signed integer, so +-32767)
 *  @return the raw shunt voltage reading
 */
int16_t Adafruit_INA219::getShuntVoltage_raw() {
	uint16_t value;
	wireReadRegister(INA219_REG_SHUNTVOLTAGE, &value);
	return (int16_t)value;
}

/*!
 *  @brief  Gets the raw current value (16-bit signed integer, so +-32767)
 *  @return the raw current reading
 */
int16_t Adafruit_INA219::getCurrent_raw() {
	uint16_t value;

	// Sometimes a sharp load will reset the INA219, which will
	// reset the cal register, meaning CURRENT and POWER will
	// not be available ... avoid this by always setting a cal
	// value even if it's an unfortunate extra step
	wireWriteRegister(INA219_REG_CALIBRATION, calVal);

	// Now we can safely read the CURRENT register!
	wireReadRegister(INA219_REG_CURRENT, &value);

	return (int16_t)value;
}

/*!
 *  @brief  Gets the raw power value (16-bit signed integer, so +-32767)
 *  @return raw power reading
 */
int16_t Adafruit_INA219::getPower_raw() {
	uint16_t value;

	// Sometimes a sharp load will reset the INA219, which will
	// reset the cal register, meaning CURRENT and POWER will
	// not be available ... avoid this by always setting a cal
	// value even if it's an unfortunate extra step
	wireWriteRegister(INA219_REG_CALIBRATION, calVal);

	// Now we can safely read the POWER register!
	wireReadRegister(INA219_REG_POWER, &value);

	return (int16_t)value;
}

/*!
 *  @brief  Gets the shunt voltage in mV (so +-327mV)
 *  @return the shunt voltage converted to millivolts
 */
float Adafruit_INA219::getShuntVoltage_mV() {
	int16_t value;
	value = getShuntVoltage_raw();
	return value * 0.01;
}

/*!
 *  @brief  Gets the shunt voltage in volts
 *  @return the bus voltage converted to volts
 */
float Adafruit_INA219::getBusVoltage_V() {
	int16_t value = getBusVoltage_raw();
	return value * 0.001;
}

/*!
 *  @brief  Gets the current value in mA, taking into account the
 *          config settings and current LSB
 *  @return the current reading convereted to milliamps
 */
float Adafruit_INA219::getCurrent_mA() {
	float valueDec = getCurrent_raw();
	valueDec /= currentDivider_mA;
	return valueDec;
}

float Adafruit_INA219::getCurrent_A() {
	float valueDec = getCurrent_raw();
	valueDec /= (currentDivider_mA * 1000.0f);
	return valueDec;
}

/*!
 *  @brief  Gets the power value in mW, taking into account the
 *          config settings and current LSB
 *  @return power reading converted to milliwatts
 */
float Adafruit_INA219::getPower_W() {
	float valueDec = getPower_raw();
	valueDec *= (pwrMultiplier_mW / 1000.0f);
	return valueDec;
}
