# Bluetooth BLE Scanner/Sniffer
Python code to sniff BLE packets from around using PC with Microchip PICTAIL BLE Module as Observer. 
Unlike low-cost BLE modules for arduino-ists/hobbyists, BLE modules from IC Cos like Microchip and SiLabs come with useful functions such as RSSI measurements and switching between BLE modes. They also have poor documentation and sparse code examples hence this upload. 
Python IDE used: Analconda Spyder
BLE Module: Microchip PICTAIL RN4020 Bluetooth Low Energy Module
ble_scanner.py - configures PICTAIL BLE module as observer via serial port, captures and stores received BLE data packets incl Mac addr and RSSI value in data frame and filters them based on a user-specified Mac address.  
