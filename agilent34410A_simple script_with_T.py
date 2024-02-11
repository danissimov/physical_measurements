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
import UT321

# list_resources()
# pymeasure.instruments.list_resources()

# Set the input parameters
# data_points = 50
# averages = 50
delay = 1 #in seconds 
duration = 0 #in minutes, 0 - eternity
data_filename = 'Agilent_Pyscript_' + strftime("%d.%m.%Y_%H-%M", time.localtime()) +'.csv' #+ str(datetime.now()) +  
data_backup = 'Agilent_Pyscript_BACKUP.csv' 
# time.strftime("%d.%m.%Y г. %H:%M", time.localtime())

data = pd.DataFrame({   
'DateTime': ['2022-08-26 13:56:54.660542'],
'Timestamp': ['Seconds'],
'Resistance': ['Agilent 34410A, Ohm'],
'Temperature': ['UT321, C'],
}) 


Agilent_connect = False
Thermpcouple_connect = False

while True:
    
    # Connect and configure the instrument
    if Agilent_connect != True:
        try:
            device=pymeasure.instruments.agilent.Agilent34410A("USB0::0x0957::0x0607::MY47002100::INSTR")
            device.reset()
            sleep(0.1) # wait here to give the instrument time to react
            Agilent_connect = True 
        except Exception as e: 
            print('Agilent conncetion error' + e)            
            Agilent_connect = False
    
    if Thermpcouple_connect != True:
        try:
            thermometer = UT321.UT321()
            Thermpcouple_connect = True 
        except Exception as e: 
            print('UT321 conncetion error' + e)
            Thermpcouple_connect= False

    try:    
        resistance = device.resistance,
        temp = thermometer.get_temp()[0]
        sleep(delay)    
        Datetime = datetime.now()
        Timestamp = round(Datetime.timestamp()*1000,0) #check this out
        # E720 script uses this form: time.time()
        # Save the data columns in a CSV file
        row = pd.DataFrame({   
            'DateTime': Datetime,
            'Timestamp': Timestamp,
            'Resistance': resistance,
            'Temperature':  temp })
        data = pd.concat([data, row], ignore_index=True)   
        print(Datetime, '\t', Timestamp, '\t', resistance, '\t', temp)
        try: #append DataFrame row by row
            row.to_csv(data_backup, mode='a', index = False, header=False, sep='\t', encoding='utf-8')
            # print("Data point saved to csv", data_filename)
        except Exception as e:
            print("Data point backup append error", e)
    except KeyboardInterrupt:
        break

# after eternal loop is broken save the whole DataFrame
try: 
    data.to_csv(data_filename, sep='\t', encoding='utf-8')   
    print("ALL data saved to csv", data_filename)
except Exception as e:
    print("csv error", e)
device.shutdown()
