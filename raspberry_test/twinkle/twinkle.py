import RPi.GPIO as GPIO
import time
pin = 11
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.OUT)
 
while True:
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(2)

