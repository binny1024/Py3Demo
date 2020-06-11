#!/usr/bin/python
import Adafruit_DHT
import json
import copy
from w1thermsensor import W1ThermSensor

sensor1 = Adafruit_DHT.DHT11
humidity_dht11, temperature_dht11 = Adafruit_DHT.read_retry(sensor1, 17)

sensor2 = Adafruit_DHT.DHT22
humidity_dht22, temperature_dht22 = Adafruit_DHT.read_retry(sensor2, 13)

sensor = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20)
temperature_ds18b20 = sensor.get_temperature()

env = []
if humidity_dht11 is not None and temperature_dht11 is not None:
        data = {"metric":"humidity","tag":"module=dht11","value":humidity_dht11}
        env.append(copy.copy(data))
        data = {"metric":"temperature","tag":"module=dht11","value":temperature_dht11}
        env.append(copy.copy(data))
if humidity_dht22 is not None and temperature_dht22 is not None:
        data = {"metric":"humidity","tag":"module=dht22","value":humidity_dht22}
        env.append(copy.copy(data))
        data = {"metric":"temperature","tag":"module=dht22","value":temperature_dht22}
        env.append(copy.copy(data))
if temperature_ds18b20 is not None:
        data = {"metric":"temperature","tag":"module=ds18b20","value":temperature_ds18b20}
        env.append(copy.copy(data))
if len(env) > 0:
        with open("/opt/falcon-scripts/env.json", 'w') as f:
                f.write(json.dumps(env))
