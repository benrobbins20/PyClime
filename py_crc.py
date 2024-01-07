def modbus_crc(data):
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            lsb = crc & 1
            crc >>= 1
            if lsb:
                crc ^= 0xA001
    return crc

# Example usage
data = [0x01, 0x06, 0x01, 0x2c, 0x03, 0xe8]  # Sample Modbus data
crc_result = modbus_crc(data)
print(f"CRC: {crc_result:04X}") # format in 4 hex digits
