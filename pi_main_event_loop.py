import os
import serial
from time import sleep
import RPi.GPIO as GPIO
from association_manager import checkAssociations, checkAlwaysRequired, extractInTimeTags
from serial_connector import scan_RFID_tags
import pygame
import time



def main_event_loop():
    GPIO.setmode(GPIO.BCM)
    DOOR_GPIO = 23
    GPIO.setup(DOOR_GPIO, GPIO.IN)
    print("Initial Door state: {}".format("Open" if (GPIO.input(DOOR_GPIO) == 0) else "Closed"))
    print("Ready")
    tag_list = {}
    #serial breaks the audio somehow
    serial_connection = serial.Serial(os.environ.get("SERIAL_PORT_PATH"), 9600, timeout=0.2)
    i = 0
    while True:
        i += 1
        if i%100 == 0:
            print("loop " + str(i))
        scan_RFID_tags(serial_connection, tag_list)
        door_open = (GPIO.input(DOOR_GPIO) == 0)
        if door_open:
            print(" - Door Open - ")
            tags = extractInTimeTags(tag_list, 2)
            print(tag_list)
            print(tags)
            print(time.time())
            all_associations_correct = checkAssociations(tags)
            all_required_items = checkAlwaysRequired(tags)
            if all_associations_correct and all_required_items:
                pygame.mixer.music.load("{}/sound/retro_game.mp3".format(os.environ.get("DOORA_PATH")))
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy() == True:
                    sleep(0.2)
                    continue
                print("Assiciations fullfilled")
            else:
                pygame.mixer.music.load("{}/sound/melancholy-ui-chime.mp3".format(os.environ.get("DOORA_PATH")))
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy() == True:
                    sleep(0.2)
                    continue
                print("Associations not fullfilled")
            