import keyboard
import serial
from association_manager import checkAssociations
from serial_connector import scan_RFID_tags
from pydub import AudioSegment
from pydub.playback import play
import os
import sys

def main():
    serial_connection = serial.Serial(os.environ.get("SERIAL_PORT_PATH"), 9600, timeout=0.01)
    success_audio = AudioSegment.from_file("./sound/ringtone-1-46486.mp3")
    error_audio = AudioSegment.from_file("./sound/melancholy-ui-chime.mp3")
    
    def on_init_scan(event):
        if event.scan_code == 12: #key "q"
            audio = AudioSegment.from_file("./sound/ringtone-1-46486.mp3")
            play(audio)
            print("\r\nq pressed, scanning...")
            tags = scan_RFID_tags(serial_connection, 5)
            print(tags)
            all_associations_correct = checkAssociations(tags)
            if all_associations_correct:
                play(success_audio)
            else:
                play(error_audio)
    
    keyboard.on_release(on_init_scan)
    keyboard.wait()

if __name__ == "__main__":
    # Set environment variables depending on target platform
    args = sys.argv[1:]
    if not len(args) >= 1:
        print("Insufficient arguments provided. Please specify the environment with --mac or --pi.")
        sys.exit(1)
    
    env_file_path = ""
    if args[0] == "--pi":
        env_file_path = "env.raspberryPi.txt"
    if args[0] == "--mac":
        env_file_path = "env.macintosh.txt"

    with open(env_file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()  # Remove leading/trailing whitespace
            if line:
                var_name, var_value = line.split('=')
                os.environ[var_name] = var_value
                print(var_name, var_value)

    main()
