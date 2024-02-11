# Scripts are a quick way to get up and running with a measurement in PyMeasure. For our IV characteristic measurement,
# we perform the following steps:
# 1) Import the necessary packages
# 2) Set the input parameters to define the measurement
# 3) Connect to the Keithley 2400
# 4) Set up the instrument for the IV characteristic
# 5) Allocate arrays to store the resulting measurements
# 6) Loop through the current points, measure the voltage, and record
# 7) Save the final data to a CSV file
# 8) Shutdown the instrument
# These steps are expressed in code as follow

# Import necessary packages
import pymeasure
from pymeasure.instruments.agilent import agilent34410A
from pymeasure.instruments import list_resources
#import numpy as np
import pandas as pd
from time import sleep, gmtime, strftime
from datetime import datetime 
import time

list_resources()
# pymeasure.instruments.list_resources()

# Set the input parameters
# data_points = 50
# averages = 50
delay = 1 #in seconds 
duration = 0 #in minutes, 0 - eternity
data_filename = 'Agilent_Pyscript_' + strftime("%d.%m.%Y_%H-%M", time.localtime()) +'.csv' #+ str(datetime.now()) +  
# time.strftime("%d.%m.%Y г. %H:%M", time.localtime())

# Connect and configure the instrument
device=pymeasure.instruments.agilent.Agilent34410A("USB0::0x0957::0x0607::MY47002100::INSTR")
# pymeasure.instruments.agilent.Agilent34410A("USB0::0x0957::0x0607::MY47002100::INSTR")    #address without USB-hub

device.reset()
sleep(0.1) # wait here to give the instrument time to react

data = pd.DataFrame({   
'DateTime ()': [datetime.now()],
'Timestamp ()': time.time(),
'Resistance (Ohm)': [device.resistance],
}) 

while True:
    try:
        resistance = device.resistance,
        sleep(delay)    
        Datetime = datetime.now()
        Timestamp = Datetime.timestamp()
        # Save the data columns in a CSV  file
        data = pd.concat([data, pd.DataFrame({   
            'DateTime ()': Datetime,
            'Timestamp ()': Timestamp,
            'Resistance (Ohm)': resistance,
        })], ignore_index=True)   
        print(Datetime, '\t', Timestamp, '\t', resistance)
    except KeyboardInterrupt:
        break
        
try: 
    data.to_csv(data_filename)
    print("Data saved to csv", data_filename)
except Exception as e:
    print("csv error", e)
device.shutdown()
