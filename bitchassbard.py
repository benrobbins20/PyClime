from pymodbus.client import ModbusSerialClient

# Define port and baudrate
port = "COM5"  # Replace with your actual serial port
baudrate = 9600

# Define desired data and register address
data = 500
register_address = 300

# Create Modbus client directly using `ModbusSerialClient` class
client = ModbusSerialClient(method='rtu',port=port, baudrate=baudrate)

# Write data to the register
test = client.write_register(register_address, data, unit=1)  # 1 specifies slave address
#temp = client.read_holding_registers(100,slave=1)
print(test)
# Close the client connection
client.close()

print("Successfully sent data to register!")

