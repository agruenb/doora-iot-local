import serial
import serial.tools.list_ports
import time
import serial


def available_ports():
    ports = serial.tools.list_ports.comports()
    for port, desc, hwid in sorted(ports):
        print(f"{port}: {desc} [{hwid}]")

def scan_RFID_tags(serial_connection, tag_dict):
    start_time = time.time()
    serial_buffer_contents = serial_connection.read(4096)
    codes = serial_buffer_contents.decode('ascii').split("\r\n")
    for code in codes:
        if code == "":
            continue
        code = code.lstrip("\x02").lstrip("\x03").lstrip("\x02")
        if code == "":
            continue
        print("Found " + code)
        tag_dict[code] = {
            "lastSeen":time.time()
        }

    end_time = time.time()
    if end_time - start_time > 0.5:
        print(f"Scan duration: {end_time - start_time}")



