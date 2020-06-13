from decimal import Decimal

from humiture_dht11 import DHT11
import requests
import time
from bmp180 import BMP180
import traceback
import serial
import calendar
import re
import threading

host = 'http://192.168.22.121:3000'

url_sensor = host + '/api/logistics/sensor'


def get_gps():
    ser = serial.Serial('/dev/ttyUSB1', 115200)
    if ser.isOpen == False:
        ser.open()
    result = {}
    try:
        while True:
            # print('获取 GPS 信息')
            size = ser.inWaiting()
            # print('size', size)
            if size != 0:
                print('正在解析 GPS 信息')
                data = ser.read(size)
                p = '(?<=GPRMC).*\r\n'
                gps_data = data.decode('utf-8')
                print(gps_data)
                matchObj = re.search(p, gps_data)
                gprmc = matchObj.group()
                ls = gprmc.split(',')
                print(ls)
                utc_time = ls[1]
                print('UTC 时间', utc_time)
                location_status = ls[2]
                print('定位状态', location_status)
                print('维度信息', ls[3])
                result['latitude_0'] = ls[3]
                latitude = float(ls[3]) // 100
                latitude = latitude + (float(ls[3]) - latitude * 100) / float(60)
                latitude = Decimal(latitude).quantize(Decimal('0.00000'))

                latitude_position = ls[4]
                print('维度半球', latitude_position)

                result['longitude_0'] = ls[5]
                longitude = float(ls[5]) // 100
                longitude = longitude + (float(ls[5]) - longitude * 100) / float(60)
                longitude = Decimal(longitude).quantize(Decimal('0.00000'))
                print('经度信息', longitude)
                longitude_position = ls[6]
                print('经度半球', longitude_position)

                print('地面速率', ls[7])
                print('地面航向', ls[8])
                print('UTC 日期', ls[9])
                print('磁偏角', ls[10])
                print('磁偏角方向', ls[11])
                print('模式指示', ls[12])

                # result['gprmc'] = gprmc
                result['latitude'] = latitude
                result['longitude'] = longitude
                result['timestamp'] = calendar.timegm(time.gmtime())
                ser.flushInput()
                return result
                # res = requests.post(url_gps, json=data)
                # print(res.json())
    except Exception as e:
        traceback.print_exc()
        result['msg'] = '定位的失败'
        result['error'] = str(e)
        result['timestamp'] = calendar.timegm(time.gmtime())
        return result
    except KeyboardInterrupt:
        ser.close()
        return {}

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
            return data
    except:
        dht11.destory()
        traceback.print_exc()
        return data


if __name__ == '__main__':
    global gps_info
    while True:
        data = {}
        data['device_id'] = '123456'
        humiture = get_humiture()
        data['humiture'] = humiture
        bmp180 = get_bmp180()
        data['bmp180'] = bmp180
        gps = get_gps()
        if len(gps)==0 or 'error' in gps:
            print('未获取到 GPS 信息，即将重新获取')
            time.sleep(2)
            continue
        data['gps'] = gps
        res = requests.post(url_sensor, json=data)
        print(res.json())
        time.sleep(5)
