
# Sample code to demonstrate Encoder class.  Prints the value every 5 seconds, and also whenever it changes.
# GPIO 26, GND, 19 looking on encoder from above with 3 pins at top
import time
import RPi.GPIO as GPIO
from encoder import Encoder

def valueChanged(value, direction):
    print("* New value: {}, Direction: {}".format(value, direction))

GPIO.setmode(GPIO.BCM)

e1 = Encoder(18, 17, valueChanged)

try:
    while True:
        time.sleep(5)
        print("Value is {}".format(e1.getValue()))
except Exception:
    pass

GPIO.cleanup()

