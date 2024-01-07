import csv, minimalmodbus


# main class for back end 
class PyClime:
    
    # class variables here used for 
        # constants
        # shared data
        # things that will be common amongst all instances
    slave_id = 1
    baud_rate = 9600
    
        
    def __init(self): # initialized with instance in GUI
        
        # Set up the instrument
        instrument = minimalmodbus.Instrument('COM10', 1)  # COM5: the port name, 63: the slave address
        instrument.serial.baudrate = 9600                  # Baud  F4 uses either 9600 or 19200
        instrument.serial.bytesize = 8                     # data bit size, refer to modbus manual chart, each pair of hex digits is 1 byte:8 bits 
        instrument.serial.stopbits = 1                     # 1 stop bit is default but we state it explicitly 
        instrument.serial.timeout  = 0.2                   # seconds.  increase if you are having problems
        print (instrument)                                 # prints out the settings for instrument
                
        
    def set_chamber_temp(self,desired_temp): # writes desired temp to the sp1 register 300
        
        instrument.write_register(300, desired_temp, functioncode=6, signed=True)
        
        
        



