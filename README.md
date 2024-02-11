Agilent 34410A
Thermometer UT321

# Agilent + UT321 measurements 
# agilent_simple script_with_T
Scripts are a quick way to get up and running with a measurement in PyMeasure. For our IV characteristic measurement,
 we perform the following steps:
 1) Import the necessary packages
 2) Set the input parameters to define the measurement
 3) Connect to the Agilent 
 4) Set up the instrument for the IV characteristic
 5) Allocate arrays to store the resulting measurements
 6) Loop through the current points, measure property, and record
 7) Save the final data to a CSV file
 8) Shutdown the instrument
 These steps are expressed in code as follow
