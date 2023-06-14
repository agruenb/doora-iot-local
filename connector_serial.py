import serial
import serial.tools.list_ports
import time
import serial

from association_manager import getItem
from connector_backend import reportNewItem

#print all available serial ports
def available_ports():
    ports = serial.tools.list_ports.comports()
    for port, desc, hwid in sorted(ports):
        print(f"{port}: {desc} [{hwid}]")

#update tags last seen and report new tags
def scan_RFID_tags(serial_connection, tag_dict):
    serial_buffer_contents = serial_connection.read(4096)
    codes = serial_buffer_contents.decode('ascii').split("\r\n")
    new_tags = []
    for code in codes:
        if code == "":
            continue
        code = code.lstrip("\x02").lstrip("\x03").lstrip("\x02")
        if code == "":
            continue
        print("Found " + code)
        #if tag is not already in dict -> check if it is completely new
        if not code in tag_dict and getItem(code) == None:
            if code not in new_tags:
                new_tags.append(code)
        else:
            tag_dict[code] = {
                "lastSeen":time.time()
            }

    # report new tags
    for tag in new_tags:
        print("Unseen tag: " + tag)
        reportNewItem(tag)



