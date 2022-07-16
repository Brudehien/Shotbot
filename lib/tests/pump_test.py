#! /usr/bin/python2

import RPi.GPIO as GPIO            # import RPi.GPIO module  
from time import sleep             # lets us have a delay  
GPIO.setmode(GPIO.BCM)             # choose BCM or BOARD  
GPIO.setup(12, GPIO.OUT)           # set GPIO12 as an output   
  
try:  
    while True:  
        GPIO.output(12, 1)         # set GPIO12 to 1/GPIO.HIGH/True
        print("Pump On")  
        sleep(1.5)                 # wait half a second  
        GPIO.output(12, 0)         # set GPIO12 to 0/GPIO.LOW/False
        print("Pump Off")  
        sleep(1.5)                 # wait half a second  
  
except KeyboardInterrupt:          # trap a CTRL+C keyboard interrupt  
    GPIO.cleanup()                 # resets all GPIO ports used by this program  
