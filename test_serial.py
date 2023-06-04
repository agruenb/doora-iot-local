import serial
import time
from time import sleep

serial_connection = serial.Serial("/dev/ttyUSB0", 9600, timeout=0.1)
#serial_connection = serial.Serial("/dev/cu.usbserial-210", 9600, timeout=0.1)
sleep(4)
timeL = 0
print("Opened Serial Connection")
print(serial_connection.read(2048))
serial_connection.close()
print("Closed Serial Connection")
sleep(3)
print("Opened Serial Connection")
serial_connection.open()
sleep(4)
print(serial_connection.read(2048))
print("Closed Serial Connection")