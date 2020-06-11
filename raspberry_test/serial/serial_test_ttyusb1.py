import serial
import time

ser = serial.Serial('/dev/ttyUSB1',115200)
if ser.isOpen  ==False:
    ser.open()

try:
    while  True:
        size = ser.inWaiting()
        if size !=0:
            response = ser.read(size)
            print (response)
            print ('\n\n')
            ser.flushInput()
            time.sleep(5)
except KeyboardInterrupt:
    ser.close()

