import sys
import RPi.GPIO as GPIO            # import RPi.GPIO module  
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)             # choose BCM or BOARD  
GPIO.setup(12, GPIO.OUT)           # set GPIO12 as an output

def cleanAndExit():
    print("Clearing...")

    GPIO.cleanup()
        
    print("Bye!")
    sys.exit()

def togglePump(state='undefined'):
    if state != 'undefined':
        pump_state = state
    else:
        pump_state = not GPIO.input(12)
    pump_state_text = ("off", "on")[pump_state]
    print("Pump is", pump_state_text)
    GPIO.output(12, pump_state)
            
    
def pumpOn():
    print("Pump is on")
    GPIO.output(12, 1)

def pumpOff():
    print("Pump is off")
    GPIO.output(12, 0)
  
