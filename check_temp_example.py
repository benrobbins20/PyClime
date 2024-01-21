import minimalmodbus

# Set up the instrument
instrument = minimalmodbus.Instrument('COM12', 1)  # find the com device in device manager, 1: the slave address 
instrument.serial.baudrate = 9600                  # Baud F4 uses either 9600 or 19200
instrument.serial.bytesize = 8                     # data bit size, refer to modbus manual chart, each pair of hex digits is 1 byte:8 bits 
instrument.serial.stopbits = 1                     # 1 stop bit is default but we state it explicitly 
instrument.serial.timeout  = 0.2                   # seconds.  increase if you are having problems



print(instrument)                                 # prints out the settings for instrument
print(instrument.read_register(0))               # reads the current chamber temp

#print(instrument.write_register(int(addr), int(value), 0, 16, True))  # write 16-bit signed integer

#print(instrument.write_register(300, 1000, functioncode=6, signed=True))



