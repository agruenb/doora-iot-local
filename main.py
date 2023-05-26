import serial
from association_manager import checkAssociations
from serial_connector import scan_RFID_tags
import os
import sys
from pi_main_event_loop import main_event_loop

def main():
    serial_connection = serial.Serial(os.environ.get("SERIAL_PORT_PATH"), 9600, timeout=0.01)
    if os.environ.get("ENV") == "pi":
        print("Running pi")
        main_event_loop(serial_connection)

    if os.environ.get("ENV") == "macintosh":
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
        env_file_path = ".env.raspberry_pi.txt"
    if args[0] == "--mac":
        env_file_path = ".env.macintosh.txt"
        from pydub import AudioSegment
        from pydub.playback import play
        import keyboard

    with open(env_file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()  # Remove leading/trailing whitespace
            if line:
                var_name, var_value = line.split('=')
                os.environ[var_name] = var_value

    main()
