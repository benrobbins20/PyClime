import csv, minimalmodbus, logging, os, subprocess, re, serial, traceback


# main class for back end 
class PyClime:
    
    def __init__(self, slave_id=1, baud_rate=9600,env_com=None, hv_com=None, lv_com=None): # initialized with instance in GUI, default to None because they will be updated and tested
        self.slave_id = slave_id
        self.env_com = env_com          # chamber serial
        self.hv_com = hv_com            # high voltage ps serial
        self.lv_com = lv_com            # low voltage ps serial
        self.baud_rate = baud_rate      # baud rate for all devices
        # set up logging
        self.logger = logging.getLogger(__name__)
        handler = logging.FileHandler('./logs/pyclime.log')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)
        
        
    def set_chamber_temp(self,desired_temp): # writes desired temp to the sp1 register 300
        # this is important to get autocomplete on the instrument variable
        instrument = self.instrument
        instrument.write_register(300, desired_temp, functioncode=6, signed=True)
        self.logger.info('set_chamber_temp: desired_temp: %s', desired_temp)
        
        
    def com_helper(self): # function to populate the com ports and check connectivity
        # list all com info 
        command = "Get-WmiObject Win32_PnPEntity | Where-Object { $_.Name -match 'COM\d+' } | Select-Object Caption, DeviceID, Manufacturer, SystemName"  # powershell command to poll the com devices
        # get only com ports
        process = subprocess.Popen(["powershell", "-Command", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE) # execute the command
        stdout, stderr = process.communicate() # BLOCKING process that needs to run and finish before the rest of the code can run, return standard error and standard out

        # Decode and print the output
        if process.returncode == 0: # if the process returns 0, it was successful
            # Decode the byte string
            output = stdout.decode('utf-8')
            com_pattern = r'\((COM\d+)\)' # regex pattern to match com ports, escape parens in (COM), put COM string in a (group) with 1 or more digits
            self.com_list = re.findall(com_pattern, output) # find all com ports in the output
            return self.com_list
            self.logger.debug('com_helper: output: %s', output)
            
        else:
            print("Error:", stderr.decode('utf-8'))
            logging.error('com_helper: error: %s', stderr.decode('utf-8'))
            
            
    def setup_instrument(self,com_port, slave_id=1, baud_rate=9600):  
        
        # Set up the instrument
        self.instrument = minimalmodbus.Instrument(com_port, self.slave_id)     # COM5: the port name, 1: the slave address
        self.instrument.serial.baudrate = self.baud_rate                        # Baud  F4 uses either 9600 or 19200
        self.instrument.serial.bytesize = 8                                     # data bit size, refer to modbus manual chart, each pair of hex digits is 1 byte:8 bits 
        self.instrument.serial.stopbits = 1                                     # 1 stop bit is default but we state it explicitly 
        self.instrument.serial.timeout  = 0.2                                   # seconds.  increase if you are having problems
        #print(self.instrument)  
        return self.instrument

        
    def set_env_com(self): # Function gets the list of com and serial ports and then sets up the modbus and serial instruments
        com_list = self.com_helper()
        for com in com_list:
            try:
                self.instrument = self.setup_instrument(com) # sets the shared instrument object within the class 
                self.logger.info('test_and_update_com(): testing com: %s with instrument: %s', com,self.instrument)
                reg_val = self.read_register(0) # register 0 holds the model number of the chamber == 5270 aka 4F (little endian f4)
                # print(f"Register 0 value: {reg_val} for COM port: {com}")
                if reg_val == 5270: 
                    self.env_com = com
                    self.logger.info('test_and_update_com(): env_com: %s, test success model num: %s', self.env_com,reg_val)
                    break # can break out of loop 
                    # TODO might be to check all of them because talking to a lot of chambers may be a project idea
                else:
                    self.logger.info('Unexpected register result: %s', reg_val)
                    self.instrument.serial.close() # VERY IMPORTANT, need to release the com port to use with other instruments
                    continue
            except Exception as e:
                self.instrument.serial.close() # VERY IMPORTANT, need to release the com port to use with other instruments
                self.logger.error("could not establish Thermal Chamber %s, error: %s", com,e)
        self.setup_instrument(self.env_com)
        
    def set_ps_com(self): # set up ps com ports by sending scpi command to each port
        # the small one is a XR 50-40 and the big one is a SQA375-54
        big_ps_model = 'SQA375-54'
        small_ps_model = 'XR 50-40'
        com_list = self.com_helper()
        for com in com_list:
            try:
                conn = serial.Serial(com, 19200, timeout=1)
                conn.write('*IDN?\n'.encode()) # return byte encoded ID b'Magna-Power Electronics, Inc., SQA375-54, S/N:106-1588\r\n'
                id = (conn.readline())
                id = id.decode('utf-8').strip('\r\n')
                self.logger.info('set_ps_com(): testing com: %s santized id: %s', com,id)
                
                if big_ps_model in id:
                    self.hv_com = com
                    self.logger.info('set_ps_com(): hv_com: %s, test success model num: %s', self.hv_com,id)
                    
                elif small_ps_model in id:
                    self.lv_com = com
                    self.logger.info('set_ps_com(): lv_com: %s, test success model num: %s', self.lv_com,id)
                       
                else:
                    # getting to this block means the ID returned over serial may be null
                    self.logger.error('set_ps_com(): could not establish PS %s, error: %s', com, id)
            except Exception as e:
  
                # exception_traceback = traceback.format_exc()
                # print(exception_traceback)
                self.logger.error("could not establish PS %s, error: %s", com, e)
        self.logger.debug('set_ps_com(): hv_com: %s, lv_com: %s', self.hv_com, self.lv_com) # at end of loop ensure that both are assigned
        if not self.hv_com or not self.lv_com:
            self.logger.error('set_ps_com(): could not set com port hv_com: %s, lv_com: %s', self.hv_com, self.lv_com) # error out if either are not set
        
    def read_register(self, register):
        return self.instrument.read_register(register)
        
    def print_instr(self):
        print(self.instrument)
        
    def send_scpi(self, com, scpi_cmd):
        conn = serial.Serial(com, 19200, timeout=1)
        message = scpi_cmd + '\n'
        conn.write(message.encode())
        return conn.readline()
    


test_instance = PyClime() # create an instance of the class

        
test_instance.set_env_com() # test the com ports
test_instance.set_ps_com() # test the com ports
test_instance.set_chamber_temp(220) # set the chamber temp to 100C

print(test_instance.send_scpi(test_instance.hv_com, 'OUTP:STOP')) # this worked!!! AND I DIDNT HAVE IT HOOKED UP TO ANYTHING!!!! 360 VOLTS JUST APPLIED AND IM SETTING NEXT TO LEADS. HA. well ill take it 
