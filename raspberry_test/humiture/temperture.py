from w1thermsensor import W1ThermSensor

sensor = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20)
temperature = sensor.get_temperature()
print (temperature)
