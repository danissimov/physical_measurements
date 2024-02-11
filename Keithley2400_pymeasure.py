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
from pymeasure.instruments.keithley import Keithley2400
import numpy as np
import pandas as pd
from time import sleep
import datetime 

# Set the input parameters
data_points = 50
averages = 50
max_current = 0.01
min_current = -max_current

# Connect and configure the instrument
sourcemeter = Keithley2400("GPIB::4")
sourcemeter.reset()
sourcemeter.use_front_terminals()
sourcemeter.measure_voltage()
sourcemeter.config_current_source()
sleep(0.1) # wait here to give the instrument time to react
sourcemeter.set_buffer(averages)

# Allocate arrays to store the measurement results
currents = np.linspace(min_current, max_current, num=data_points)
voltages = np.zeros_like(currents)
voltage_stds = np.zeros_like(currents)

# Loop through each current point, measure and record the voltage
for i in range(data_points):
    sourcemeter.current = currents[i]
    sourcemeter.reset_buffer()
    sleep(0.1)
    sourcemeter.start_buffer()
    sourcemeter.wait_for_buffer()
# Record the average and standard deviation
voltages[i] = sourcemeter.means
voltage_stds[i] = sourcemeter.standard_devs

# Save the data columns in a CSV file
data = pd.DataFrame({
'DateTime ()': datetime.now(),
'Current (A)': currents,
'Voltage (V)': voltages,
'Voltage Std (V)': voltage_stds,
})
data.to_csv('example.csv')
sourcemeter.shutdown()
