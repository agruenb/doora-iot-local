import os
import RPi.GPIO as GPIO
from association_manager import checkAssociations, checkAlwaysRequired
from serial_connector import scan_RFID_tags

def main_event_loop(serial_connection):
    GPIO.setmode(GPIO.BCM)
    DOOR_GPIO = 23
    GPIO.setup(DOOR_GPIO, GPIO.IN)
    searching_tags = False
    while True:
        door_open = (GPIO.input(DOOR_GPIO) == 0)
        if door_open and not searching_tags:
            print("Start Search...")
            searching_tags = True
            tags = scan_RFID_tags(serial_connection, 3)
            print(tags)
            all_associations_correct = checkAssociations(tags)
            all_required_items = checkAlwaysRequired(tags)
            if all_associations_correct and all_required_items:
                os.system("mpg123 {}/sound/retro_game.mp3".format(os.environ.get("DOORA_PATH")))
                print("Assiciations fullfilled")
            else:
                os.system("mpg123 {}/sound/melancholy-ui-chime.mp3".format(os.environ.get("DOORA_PATH")))
                print("Associations not fullfilled")
            searching_tags = False
            