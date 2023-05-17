import serial
import serial.tools.list_ports
import time


def available_ports():
    ports = serial.tools.list_ports.comports()
    for port, desc, hwid in sorted(ports):
        print(f"{port}: {desc} [{hwid}]")

def drain(serial_connection):
    while serial_connection.in_waiting:
        serial_connection.read(serial_connection.in_waiting)
    
def scan_RFID_tags(serial_connection, duration):
    drain(serial_connection)
    start_time = time.time()
    finish_time = start_time + duration
    tags = list()
    while time.time() < finish_time:
        data = b""
        data += serial_connection.readline()
        num_in_list = tags.count(data)
        if num_in_list == 0:
            tags.append(data)
    #clean up tags
    clean_tags = list()
    for tag in tags:
        if tag == b"\x03": continue
        if tag == b"": continue
        clean_tags.append(tag.lstrip(b"\x02").rstrip(b"\r\n").decode('ascii'))
    return clean_tags



