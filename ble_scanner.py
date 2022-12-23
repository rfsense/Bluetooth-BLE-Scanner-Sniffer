# -*- coding: utf-8 -*-
"""
Created on Thu May 26 10:22:04 2022

@author: Rushi V
"""

import numpy as np
import pandas as pd
import serial
import math
import csv
import time

## FUNCTION TO SEND BLE UART COMMANDS TO SET UP PICTAIL BLE MODULE AS BLE OBSERVER

## Configure serial port
serialPort = serial.Serial(port='COM6', baudrate=115200, bytesize=8, stopbits=serial.STOPBITS_ONE)



#xmit rs232 commands to setup RN4020 PICTAIL BLE Module as Observer
serialPort.write('+'.encode('utf-8'))  # Turn on echo

serialPort.write('\r'.encode('utf-8'))  
time.sleep(0.2)

serialPort.write('SF,1'.encode('utf-8'))  # Set to factory defaults
serialPort.write('\r'.encode('utf-8'))
time.sleep(0.2)

serialPort.write('SS,C0000000'.encode('utf-8')) 
serialPort.write('\r'.encode('utf-8'))
time.sleep(0.2)

serialPort.write('SR,80000000'.encode('utf-8'))
serialPort.write('\r'.encode('utf-8'))
time.sleep(0.2)

serialPort.write('R,1'.encode('utf-8'))   
serialPort.write('\r'.encode('utf-8'))
serialPort.read(size=3)
time.sleep(5)

serialPort.write('F'.encode('utf-8'))
serialPort.write('\r'.encode('utf-8'))
serialPort.read(size=240)

time.sleep(0.5)

print('Serial Configurations Done')


serialPort.write('J,1'.encode('utf-8'))  #Enter observer mode and start broadcasts every 100 ms
serialPort.write('\r'.encode('utf-8'))
time.sleep(0.5)

## Start Timer
tStart = time.time() 
tPassed = 0

## Capture BLE data coming in PICTAIL Observer
rxBleDataList = [] #List to store all received BLE Broadcasts
rxBleDF = pd.DataFrame({}, columns = ['Mac Addr', 'Bit Flag', 'Rx Power', 'Data payload']) # Data frame to store all received BLE data observed
idx = 0 # index on DF for each BLE data line received

while tPassed <= 10:  #While tPassed<10 ms, caputre broadcasted BLE Data 
    rxData = serialPort.readline()
    if len(str(rxData.strip()).split(',')) == 4:  #To filter out a few AOK messages from PICTAIL 
        rxBleDataList.append(str(rxData.strip()).split(','))  #split each received line list by comma
        print(rxData)
        rxBleDF.loc[idx,:] = str(rxData.strip()).split(',') # move in Data Frame
        idx = idx+1
    tPassed = time.time() - tStart  #Measure passed time interval so far
    
## Close serial port
serialPort.write('J,0'.encode('utf-8'))  #Exit observer mode
serialPort.close()  # Close serial port



## Clean up Data Frame

rxBleDF.loc[:,'Mac Addr'] = rxBleDF.loc[:,'Mac Addr'].apply(lambda x: x.strip('b\''))
rxBleDF.loc[:,'Data payload'] = rxBleDF.loc[:,'Data payload'].apply(lambda x: x.strip('Brcst:'))
rxBleDF.loc[:,'Data payload'] = rxBleDF.loc[:,'Data payload'].apply(lambda x: x.strip('\''))
rxBleDF['Data payload in bytes'] = rxBleDF['Data payload'].apply(lambda x: bytes(x, 'utf-8')) 



## Filter in BLE Data from PIC BLE Tx Dongle based on Mac Address

rxBlePic = rxBleDF.loc[rxBleDF['Mac Addr'] == '64E7D832D60F' , :]
rxBlePic.loc[:,'Ble xmit counter'] = rxBlePic['Data payload in bytes'].apply(lambda x: (x[-1]))






















    





