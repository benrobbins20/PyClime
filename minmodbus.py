import minimalmodbus

# Set up the instrument
instrument = minimalmodbus.Instrument('COM16', 1)  # COM5: the port name, 63: the slave address
instrument.serial.baudrate = 9600                  # Baud  F4 uses either 9600 or 19200
instrument.serial.bytesize = 8                     # data bit size, refer to modbus manual chart, each pair of hex digits is 1 byte:8 bits 
instrument.serial.stopbits = 1                     # 1 stop bit is default but we state it explicitly 
instrument.serial.timeout  = 0.2                   # seconds.  increase if you are having problems
print(instrument)                                  # prints out the settings for instrument



# Function to write to a register
def write_to_register(register_address, value):
    # Write a value to the given Modbus register address
    instrument.write_register(register_address, value, functioncode=6, signed=True)

# Example: Set temperature to 100 degrees on register 299
# The value might need to be scaled depending on how the register interprets the value.
# For example, if the register expects tenths of degrees, you would send 1000 for 100.0 degrees.
temperature_in_tenths = 1000  # Represents 100.0 degrees

#write_to_register(300, temperature_in_tenths)

print(instrument.read_register(100))

