import string
import threading
import RPi.GPIO as GPIO
import time
import math
import Data
from ADCDevice import *

class Thermometer:

    adc = ADCDevice() # Define an ADCDevice class object
    
    def __init__(self) -> None:
        self.setup()

    def setup(self):
        global adc
        if(self.adc.detectI2C(0x48)): # Detect the pcf8591.
            self.adc = PCF8591()
        elif(self.adc.detectI2C(0x4b)): # Detect the ads7830
            self.adc = ADS7830()
        else:
            print("No correct I2C address found, \n"
            "Please use command 'i2cdetect -y 1' to check the I2C address! \n"
            "Program Exit. \n");
            exit(-1)
            
    def run(self):
        self.thermometer_thread = threading.Thread(target=self.loop, daemon=True)
        self.thermometer_thread.start()
            
    def loop(self):
        while True:
            value = self.adc.analogRead(0)        # read ADC value A0 pin
            voltage = value / 255.0 * 3.3        # calculate voltage
            Rt = 10 * voltage / (3.3 - voltage)    # calculate resistance value of thermistor
            tempK = 1/(1/(273.15 + 25) + math.log(Rt/10)/3950.0) # calculate temperature (Kelvin)
            Data.current_temp = tempK -273.15        # calculate temperature (Celsius)
            # print ('ADC Value : %d, Voltage : %.2f, Temperature : %.2f'%(value,voltage,tempC))
            time.sleep(0.01)

    def destroy(self):
        self.adc.close()
        GPIO.cleanup()
