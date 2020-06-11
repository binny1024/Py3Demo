#!/usr/bin/env python
#----------------------------------------------------------------
#	Note:
#		ds18b20's data pin must be connected to pin7.
#		replace the 28-XXXXXXXXX as yours.
#----------------------------------------------------------------
import os

ds18b20 = ''

def setup():
	global ds18b20
	for i in os.listdir('/sys/bus/w1/devices'):
		if i != 'w1_bus_master1':
			ds18b20 = i

def read():
#	global ds18b20
	location = '/sys/devices/platform/dht11@0/iio:device0/in_temp_input'
	tfile = open(location)
	text = tfile.read()
	tfile.close()
	# secondline = text.split("\n")[1]
	# temperaturedata = secondline.split(" ")[9]
	# temperature = float(temperaturedata[2:])
	# temperature = temperature / 1000
	# return temperature
	return text

def loop():
	while True:
		if read() != None:
			print ("Current temperature :  " % read())

def destroy():
	pass

if __name__ == '__main__':
	try:
		#setup()
		# loop()
		path = '/sys/devices/platform/dht11@0/iio:device0'
		for root, dirs, files in os.walk(path):
			print(files)
	except KeyboardInterrupt:
		destroy()
