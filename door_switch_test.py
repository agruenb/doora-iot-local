import RPi.GPIO as GPIO
 
GPIO.setmode(GPIO.BCM) # GPIO Nummern statt Board Nummern
 
DOOR_GPIO = 23
GPIO.setup(DOOR_GPIO, GPIO.IN) # GPIO Modus zuweisen
print(GPIO.input(DOOR_GPIO))