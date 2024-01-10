import csv, minimalmodbus, logging
import minimalmodbus


# main class for back end 
class PyClime:
    
    # class variables here used for 
        # constants
        # shared data
        # things that will be common amongst all instances
    slave_id = 1
    baud_rate = 9600
    
    # 
    
        
    def __init(self): # initialized with instance in GUI
        
        # Set up the instrument
        self.instrument = minimalmodbus.Instrument('COM10', self.slave_id)  # COM5: the port name, 63: the slave address
        self.instrument.serial.baudrate = self.baud_rate                  # Baud  F4 uses either 9600 or 19200
        self.instrument.serial.bytesize = 8                     # data bit size, refer to modbus manual chart, each pair of hex digits is 1 byte:8 bits 
        self.instrument.serial.stopbits = 1                     # 1 stop bit is default but we state it explicitly 
        self.instrument.serial.timeout  = 0.2                   # seconds.  increase if you are having problems
        print(self.instrument)                                 # prints out the settings for instrument
        
        # set up logging
        logging.basicConfig(filename='log/pyclime.log', level=logging.DEBUG)
        
        
        
    def set_chamber_temp(self,desired_temp): # writes desired temp to the sp1 register 300
        # this is important to get autocomplete on the instrument variable
        instrument = self.instrument
        instrument.write_register(300, desired_temp, functioncode=6, signed=True)
        logging.info('set_chamber_temp: desired_temp: %s', desired_temp)
        
        

        
        
        



