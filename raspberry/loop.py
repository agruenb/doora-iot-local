import os
import serial
from time import sleep
import RPi.GPIO as GPIO
from association_manager import checkAssociations, extractInTimeTags
from connector_backend import getAssociations, getKnownTags
from connector_serial import scan_RFID_tags
import pygame
import time

def loop():
    pygame.mixer.init()
    GPIO.setmode(GPIO.BCM)
    DOOR_GPIO = 23
    GPIO.setup(DOOR_GPIO, GPIO.IN)
    tag_list = {}
    serial_connection = serial.Serial(os.environ.get("SERIAL_PORT_PATH"), 9600, timeout=0.2)
    i = 0
    print("Initial Door state: {}".format("Open" if (GPIO.input(DOOR_GPIO) == 0) else "Closed"))
    door_open_prev_loop = False
    while True:
        i += 1
        if i%32000 == 0:
            print("loop " + str(i))
            getKnownTags()
            getAssociations()
        scan_RFID_tags(serial_connection, tag_list)
        door_open = (GPIO.input(DOOR_GPIO) == 0)
        if door_open and not door_open_prev_loop:
            print(" - Door Open - ")
            tags = extractInTimeTags(tag_list, 2)
            print(tags)
            if checkAssociations(tags):
                print("Assiciations fullfilled")
            else:
                pygame.mixer.music.load("{}/sound/retro_game.mp3".format(os.environ.get("DOORA_PATH")))
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy() == True:
                    sleep(0.2)
                    continue
                print("Associations not fullfilled")
            door_open_prev_loop = True
        if not door_open:
            door_open_prev_loop = False