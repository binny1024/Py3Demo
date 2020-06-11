import RPi.GPIO as GPIO
import time

pin = 25
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)

if __name__ == '__main__':
    try:
        while True:
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(pin, GPIO.LOW)
            time.sleep(0.5)
    except KeyboardInterrupt:
        GPIO.cleanup()

