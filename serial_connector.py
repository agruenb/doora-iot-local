import serial
import serial.tools.list_ports
import time
import serial


def available_ports():
    ports = serial.tools.list_ports.comports()
    for port, desc, hwid in sorted(ports):
        print(f"{port}: {desc} [{hwid}]")
    
def scan_RFID_tags(serial_connection, tag_dict):
    max_rows = 10
    read_rows = 0
    while(read_rows < max_rows and serial_connection.in_waiting):
        read_rows += 1
        raw_line = serial_connection.readline()
        tag = raw_line.lstrip(b"\x02").rstrip(b"\r\n").decode('ascii')
        if tag == "":
            continue
        #remove line from queue
        serial_connection.read(len(raw_line))
        print("Found " + tag)
        if tag != b"\x03" and tag != b"":
            tag_dict[tag] = {
                "lastSeen":time.time()
            }



