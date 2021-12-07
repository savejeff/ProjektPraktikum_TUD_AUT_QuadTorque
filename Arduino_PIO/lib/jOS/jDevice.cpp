#include "jDevice.h"





/************************************************
 *                   jDeviceBus                 *
 * **********************************************/



bool jDeviceBus::read_bytes(uint8_t reg, uint8_t* data, uint8_t count)
{
	uint8_t read_count = Bus_readBytes(reg, data, count);
	return read_count == count;
}


bool jDeviceBus::write_bytes(uint8_t reg, uint8_t* data, uint8_t count)
{
	return Bus_writeBytes(reg, data, count);
}


uint16_t  jDeviceBus::read16(uint8_t reg) { 
	uint8_t data[2];
	Bus_readBytes(reg, data, 2);
	return ((uint16_t)data[1] << 8) | data[0];
};


bool jDeviceBus::read16(uint8_t reg, uint16_t& res) { 
	
	uint8_t data[2];
	if(2 == Bus_readBytes(reg, data, 2))
	{
		res = ((uint16_t)data[1] << 8) | data[0];
		return true;
	} else {
		return false;
	}
}


bool jDeviceBus::write16(uint8_t reg, uint16_t val) { 
	Bus_writeBytes(reg, (uint8_t*)&val, 2);
	return true;
};


uint8_t  jDeviceBus::read_reg(uint8_t reg) { 
	//uint8_t data[1];
	//Bus_readBytes(reg, data, 1);
	//return data[0];
	return Bus_readByte(reg);
};


//read register with mask and return result like read_reg_mask(REGXY, (1 << 2) | (1 << 7))
uint8_t  jDeviceBus::read_reg_mask(uint8_t reg, uint8_t mask) { 
	uint8_t data[1];
	Bus_readBytes(reg, data, 1);
	return data[0] & mask;
};

//read bit of register like read_reg_bit(REGXY, 2) to read 2th bit and check if is set
bool  jDeviceBus::read_reg_bit(uint8_t reg, uint8_t bit_index) { 

	uint8_t data[1];
	Bus_readBytes(reg, data, 1);
	return (data[0] & (1 << bit_index)) != 0;
};


bool jDeviceBus::write_reg(uint8_t reg, uint8_t val) { 
	//Bus_writeBytes(reg, (uint8_t*)&val, 1);
	//return true;

	return Bus_writeByte(reg, val);
};


//write register with mask and value like write_reg_mask(REGXY, 0x0F, 0x3) to overrite lower 4 bits with value 0011
uint8_t  jDeviceBus::write_reg_mask(uint8_t reg, uint8_t mask, uint8_t value) { 
	value = (read_reg(reg) & ~mask) | (mask & value);
	write_reg(reg, value);
	return value;
};

//set bits in reg like write_reg_bit(X, (1 << 4)) to set 4th bit in reg X without clearing rest of reg
void jDeviceBus::write_reg_set_bit(uint8_t reg, uint8_t val)
{
	val |= read_reg(reg);
	write_reg(reg, val);
}

//set bits in reg like write_reg_bit(X, (1 << 4)) to clear 4th bit in reg X without clearing rest of reg
void jDeviceBus::write_reg_reset_bit(uint8_t reg, uint8_t val)
{
	val = ~val;
	val &= read_reg(reg);
	write_reg(reg, val);
}




/************************************************
 *                   jDeviceI2C                 *
 * **********************************************/




bool jDeviceI2C::I2C_writeByte(uint8_t address, uint8_t subAddress, uint8_t data)
{
	_i2c->beginTransmission(address);  // Initialize the Tx buffer
	_i2c->write(subAddress);           // Put slave register address in Tx buffer
	_i2c->write(data);                 // Put data in Tx buffer
	_i2c->endTransmission();           // Send the Tx buffer
	return true;
}


bool jDeviceI2C::I2C_writeBytes(uint8_t address, uint8_t subAddress, uint8_t* data, uint8_t count)
{

	_i2c->beginTransmission(address);  // Initialize the Tx buffer
	_i2c->write(subAddress);           // Put slave register address in Tx buffer
	for(int i = 0; i < count; i++)
		_i2c->write(data[i]);
	_i2c->endTransmission();           // Send the Tx buffer
	return true;

}

uint8_t jDeviceI2C::I2C_readByte(uint8_t address, uint8_t subAddress)
{
	uint8_t data = 0; // 'data' will store the register data	
	_i2c->beginTransmission(address);         // Initialize the Tx buffer
	_i2c->write(subAddress);	                 // Put slave register address in Tx buffer
	_i2c->endTransmission(false);             // Send the Tx buffer, but send a restart to keep connection alive
	_i2c->requestFrom(address, (uint8_t) 1);  // Read one byte from slave register address 

	data = _i2c->read();                      // Fill Rx buffer with result

	_i2c->endTransmission();
	
	return data;                             // Return data read from slave register
}

uint8_t jDeviceI2C::I2C_readBytes(uint8_t address, uint8_t subAddress, uint8_t* dest, uint8_t count)
{
	byte retVal;

	_i2c->beginTransmission(address);      // Initialize the Tx buffer
	_i2c->write(subAddress);        // Put slave register address in Tx buffer
	bus_error = _i2c->endTransmission(false); // Send Tx buffer, send a restart to keep connection alive
	if (bus_error != 0) // endTransmission should return 0 on success
		return 0;

	retVal = _i2c->requestFrom(address, count);  // Read bytes from slave register address 
	
	if (retVal != count)
	{
		LogD("!NACK!");
		bus_error = NACK_ON_DATA;
		return 0;
	}

	for (int i = 0; i < count; i++)
		dest[i] = _i2c->read();

	_i2c->endTransmission();

	return count;
}



bool jDeviceI2C::Bus_writeByte(uint8_t subAddress, uint8_t data) {
	return I2C_writeByte(DEVICE_ADDR, subAddress, data);
}
bool jDeviceI2C::Bus_writeBytes(uint8_t subAddress, uint8_t* data, uint8_t count) {
	return I2C_writeBytes(DEVICE_ADDR, subAddress, data, count);
}
uint8_t jDeviceI2C::Bus_readByte(uint8_t subAddress) {
	return I2C_readByte(DEVICE_ADDR, subAddress);
}
uint8_t jDeviceI2C::Bus_readBytes(uint8_t subAddress, uint8_t* dest, uint8_t count) {
	return I2C_readBytes(DEVICE_ADDR, subAddress, dest, count);
}




uint8_t jDeviceI2C::getBusError(void)
	// If any library command fails, you can retrieve an extended
	// error code using this command. Errors are from the wire library: 
	// 0 = Success
	// 1 = Data too long to fit in transmit buffer
	// 2 = Received NACK on transmit of address
	// 3 = Received NACK on transmit of data
	// 4 = Other error
{
	return bus_error;
}




/************************************************
 *                   jDeviceSPI                 *
 * **********************************************/




byte jDeviceSPI::Bus_writeByte(uint8_t data) {
	
	_jSPI->beginTransaction();

	byte val = _jSPI->transfer(data);
	
	_jSPI->endTransaction();    

	return val;

}

void jDeviceSPI::Bus_writeBytes(uint8_t* data, uint8_t count) {
	
	_jSPI->beginTransaction();

	//TODO replace with
	//_jSPI->transfer(data, count);

	for(int i = 0; i < count; i++)
		data[i] = _jSPI->transfer(data[i]);
	
	_jSPI->endTransaction();
	
}

void jDeviceSPI::Bus_WriteReadByte(uint8_t* dataTX, uint16_t len_TX, uint8_t* dataRX, uint16_t len_RX)
{
	
	_jSPI->beginTransaction();

	for(int i = 0; i < len_TX; i++)
		_jSPI->transfer(dataTX[i]);
	
	for(int i = 0; i < len_RX; i++)
		dataRX[i] = _jSPI->transfer(0);
	
	_jSPI->endTransaction();
	
}

bool jDeviceSPI::Bus_writeByte(uint8_t subAddress, uint8_t data) {
	
	_jSPI->beginTransaction();


	//Write Operation: (0)(Addr)
	_jSPI->transfer(((subAddress & 0x7F) | 0x00));
	_jSPI->transfer(data);
	
	_jSPI->endTransaction();
	

	return true;
}
bool jDeviceSPI::Bus_writeBytes(uint8_t subAddress, uint8_t* data, uint8_t count) {
	
	_jSPI->beginTransaction();


	//Write Operation: (0)(Addr)
	_jSPI->transfer(((subAddress & 0x7F) | 0x00));
	
	//TODO replace with
	//_jSPI->transfer(data, count);

	for(int i = 0; i < count; i++)
		_jSPI->transfer(data[i]);
	
	_jSPI->endTransaction();
	

	return true;
}
uint8_t jDeviceSPI::Bus_readByte(uint8_t subAddress) {
		
	_jSPI->beginTransaction();


	//Read Operation: (1)(Addr)
	_jSPI->transfer(((subAddress & 0x7F) | 0x80));
	uint8_t val = _jSPI->transfer(0x00);
	
	_jSPI->endTransaction();
	

	return val;
}
uint8_t jDeviceSPI::Bus_readBytes(uint8_t subAddress, uint8_t* dest, uint8_t count) {
	
	_jSPI->beginTransaction();


	//Read Operation: (1)(Addr)
	_jSPI->transfer(((subAddress & 0x7F) | 0x80));

	for(int i = 0; i < count; i++)
		dest[i] = _jSPI->transfer(0x00);
	
	_jSPI->endTransaction();
	

	return count;
}




void jDeviceSPI::printReg(String name, uint8_t reg)
{
	byte val = read_reg(reg);
	//byte val = Bus_readByte(reg);
	//LogD("%s: %02X", name, val);
	LogD("REG %45s: %02X - b%s", name.c_str(), val, sprintBits(val).c_str());
}