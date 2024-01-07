from pymodbus.client.serial import ModbusSerialClient as ModbusClient

# Configure the client
client = ModbusClient(method='rtu', port='COM5', baudrate=9600, timeout=3)

# Connect to the client
connection = client.connect()
if connection:
    try:
        # Write to register 299 the value for 100 degrees
        # Assuming the temperature is written as an integer (100.0 degrees -> 1000)
        response = client.write_register(300, 1000, unit=1, signed=True)
        print(response)
    finally:
        # Close the client connection
        client.close()
else:
    print("Failed to connect to the Modbus device.")
