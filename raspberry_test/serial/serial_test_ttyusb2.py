import serial
import time

ser = serial.Serial('/dev/ttyUSB2',115200)
if ser.isOpen  ==False:
    ser.open()

ser.write("at+qgps=1".encode("utf-8"))
ser.flushInput()
try:
    while  True:
        size = ser.inWaiting()
        if size !=0:
            response = ser.read(size)
            print (response)
            ser.flushInput()
            time.sleep(5)
except KeyboardInterrupt:
    ser.close()

