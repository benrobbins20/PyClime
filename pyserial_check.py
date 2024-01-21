import serial
import struct

def calculate_crc(data):
    crc = 0xFFFF
    for pos in data:
        crc ^= pos
        for i in range(8):
            if ((crc & 1) != 0):
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return struct.pack('<H', crc)

# Assuming the port and baud rate are correct for your environment
serial_port = 'COM12'
baud_rate = 9600  # or the baud rate your device uses

# Create the message (update with actual data from the image)
# The example below is a Modbus RTU frame with a function code to read holding registers
slave_id = 0x01  # Example slave ID
function_code = 0x03  # Function code to read holding registers
start_address = 0x0000  # Starting address to read (update if needed)
quantity_of_registers = 0x0001  # Number of registers to read (update if needed)

# Construct the message with slave ID, function code, start address, and quantity of registers
message = struct.pack('>BBHH', slave_id, function_code, start_address, quantity_of_registers)

# Add the CRC to the message
message += calculate_crc(message)

# Send the message using pyserial
with serial.Serial(serial_port, baud_rate, timeout=1) as ser:
    ser.write(message)
    # Read response (modify the number of bytes to read as needed)
    response = ser.read(8)  # Change 7 to the expected number of bytes in the response
    print(response)
