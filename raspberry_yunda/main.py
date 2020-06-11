from humiture_dht11 import DHT11
import requests
import time
from bmp180 import BMP180
import traceback
import serial
import calendar
import re

host = 'http://192.168.22.121:3000'
url_humiture = host + '/sensor/humiture'
url_bpm = host + '/sensor/bmp'
url_gps = host + '/sensor/gps'

url_all = host + '/sensor/all'


def get_gps():
    data = {}
    try:
        ser = serial.Serial('/dev/ttyUSB1', 115200)
        if ser.isOpen == False:
            ser.open()

        size = ser.inWaiting()
        if size != 0:
            data = ser.read(size)
            p = '(?<=GPRMC).*\r\n'
            matchObj = re.search(p, data)
            gprmc = matchObj.group()
            ls = gprmc.split(',')

            print('UTC 时间', ls[0])
            print('定位状态', ls[1])
            print('维度信息', ls[2])
            print('维度半球', ls[3])
            print('经度信息', ls[4])
            print('经度半球', ls[5])
            print('地面速率', ls[6])
            print('地面航向', ls[7])
            print('UTC 日期', ls[8])
            print('磁偏角', ls[9])
            print('磁偏角方向', ls[10])
            print('模式指示', ls[11])

            longitude = ls[2]
            latitude = ls[2]
            data['latitude'] = latitude
            data['longitude'] = longitude
            data['timestamp'] = calendar.timegm(time.gmtime())
            ser.flushInput()
            # res = requests.post(url_gps, json=data)
            # print(res.json())
    except Exception as e:
        data['msg'] = '定位的失败'
        data['error'] = str(e)
    return data


def get_bmp180():
    """
    大气压
    :return:
    """
    data = {}
    try:
        bmp = BMP180()
        temp_bmp = bmp.read_temperature()
        pressure_air = bmp.read_pressure()
        altitude = bmp.read_altitude()
        data['timestamp'] = calendar.timegm(time.gmtime())
        data['temp_bmp'] = "{:.2f} C".format(temp_bmp)
        data['pressure_air'] = "{:.2f} hPa".format(pressure_air / 100.0)
        data['altitude'] = "{:.2f}".format(altitude)

        # res = requests.post(url_bpm, json=data)
        # print(res.json())
    except Exception as e:
        data['msg'] = '大气压信息失败'
        data['error'] = str(e)
    return data


def get_humiture():
    """
    温湿度信息
    :param url:  上传接口地址
    :return:
    """
    data = {}
    dht11 = DHT11()
    try:
        data['timestamp'] = calendar.timegm(time.gmtime())
        result = dht11.read_dht11_dat()
        if result:
            humi_dht11, temp_dht11 = result
            data['humi_dht11'] = "{}".format(humi_dht11)
            data['temp_dht11'] = "{}".format(temp_dht11)
            # res = requests.post(url_humiture, json=data)
            # print(res.json())
    except:
        dht11.destory()
        traceback.print_exc()
    return data


if __name__ == '__main__':
    while True:
        data = {}
        data['sensor_id'] = "12342111"
        humiture = get_humiture()
        data['humiture'] = humiture
        bmp180 = get_bmp180()
        data['bmp180'] = bmp180
        gps = get_gps()
        data['gps'] = gps
        res = requests.post(url_humiture, json=data)
        print(res.json())
        time.sleep(60)
