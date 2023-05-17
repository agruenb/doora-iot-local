import keyboard
import serial
from association_manager import checkAssociations
from serial_connector import scan_RFID_tags
from pydub import AudioSegment
from pydub.playback import play

def main():
    serial_connection = serial.Serial('/dev/cu.usbserial-210', 9600, timeout=0.01)
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
    main()
