import time
import smbus
import RPi.GPIO as GPIO
import requests
import re
import traceback
import serial
import calendar
from decimal import Decimal


# BMP085 default address.
BMP180_I2CADDR = 0x77

# Operating Modes
BMP180_ULTRALOWPOWER = 0
BMP180_STANDARD = 1
BMP180_HIGHRES = 2
BMP180_ULTRAHIGHRES = 3

# BMP085 Registers
BMP180_CAL_AC1 = 0xAA  # R   Calibration data (16 bits)
BMP180_CAL_AC2 = 0xAC  # R   Calibration data (16 bits)
BMP180_CAL_AC3 = 0xAE  # R   Calibration data (16 bits)
BMP180_CAL_AC4 = 0xB0  # R   Calibration data (16 bits)
BMP180_CAL_AC5 = 0xB2  # R   Calibration data (16 bits)
BMP180_CAL_AC6 = 0xB4  # R   Calibration data (16 bits)
BMP180_CAL_B1 = 0xB6  # R   Calibration data (16 bits)
BMP180_CAL_B2 = 0xB8  # R   Calibration data (16 bits)
BMP180_CAL_MB = 0xBA  # R   Calibration data (16 bits)
BMP180_CAL_MC = 0xBC  # R   Calibration data (16 bits)
BMP180_CAL_MD = 0xBE  # R   Calibration data (16 bits)
BMP180_CONTROL = 0xF4
BMP180_TEMPDATA = 0xF6
BMP180_PRESSUREDATA = 0xF6

# Commands
BMP180_READTEMPCMD = 0x2E
BMP180_READPRESSURECMD = 0x34


class BMP180(object):
    def __init__(self, address=BMP180_I2CADDR, mode=BMP180_STANDARD):
        self._mode = mode
        self._address = address
        self._bus = smbus.SMBus(1)
        # Load calibration values.
        self._load_calibration()

    def _read_byte(self, cmd):
        return self._bus.read_byte_data(self._address, cmd)

    def _read_u16(self, cmd):
        MSB = self._bus.read_byte_data(self._address, cmd)
        LSB = self._bus.read_byte_data(self._address, cmd + 1)
        return (MSB * self.power(8)) + LSB

    def _read_s16(self, cmd):
        result = self._read_u16(cmd)
        if result > 32767: result -= 65536
        return result

    def _write_byte(self, cmd, val):
        self._bus.write_byte_data(self._address, cmd, val)

    def _load_calibration(self):
        "load calibration"
        self.cal_AC1 = self._read_s16(BMP180_CAL_AC1)  # INT16
        self.cal_AC2 = self._read_s16(BMP180_CAL_AC2)  # INT16
        self.cal_AC3 = self._read_s16(BMP180_CAL_AC3)  # INT16
        self.cal_AC4 = self._read_u16(BMP180_CAL_AC4)  # UINT16
        self.cal_AC5 = self._read_u16(BMP180_CAL_AC5)  # UINT16
        self.cal_AC6 = self._read_u16(BMP180_CAL_AC6)  # UINT16
        self.cal_B1 = self._read_s16(BMP180_CAL_B1)  # INT16
        self.cal_B2 = self._read_s16(BMP180_CAL_B2)  # INT16
        self.cal_MB = self._read_s16(BMP180_CAL_MB)  # INT16
        self.cal_MC = self._read_s16(BMP180_CAL_MC)  # INT16
        self.cal_MD = self._read_s16(BMP180_CAL_MD)  # INT16

    def read_raw_temp(self):
        """Reads the raw (uncompensated) temperature from the sensor."""
        self._write_byte(BMP180_CONTROL, BMP180_READTEMPCMD)
        time.sleep(0.005)  # Wait 5ms
        MSB = self._read_byte(BMP180_TEMPDATA)
        LSB = self._read_byte(BMP180_TEMPDATA + 1)
        raw = (MSB * self.power(8)) + LSB
        return raw

    def read_raw_pressure(self):
        """Reads the raw (uncompensated) pressure level from the sensor."""
        self._write_byte(BMP180_CONTROL, BMP180_READPRESSURECMD + (self._mode << 6))
        if self._mode == BMP180_ULTRALOWPOWER:
            time.sleep(0.005)
        elif self._mode == BMP180_HIGHRES:
            time.sleep(0.014)
        elif self._mode == BMP180_ULTRAHIGHRES:
            time.sleep(0.026)
        else:
            time.sleep(0.008)
        MSB = self._read_byte(BMP180_PRESSUREDATA)
        LSB = self._read_byte(BMP180_PRESSUREDATA + 1)
        XLSB = self._read_byte(BMP180_PRESSUREDATA + 2)
        raw = ((MSB *self.power(16)) + (LSB *self.power(8) ) + XLSB) /self.power((8 - self._mode))
        return raw

    def read_temperature(self):
        """Gets the compensated temperature in degrees celsius."""
        UT = self.read_raw_temp()

        X1 = ((UT - self.cal_AC6) * self.cal_AC5) / self.power(15)
        X2 = (self.cal_MC * self.power(11)) / (X1 + self.cal_MD)
        B5 = X1 + X2
        # temp = ((B5 + 8) >> 4) / 10
        temp = ((B5 + 8) / self.power(4)) / 10
        return temp

    def read_pressure(self):
        """Gets the compensated pressure in Pascals."""
        UT = self.read_raw_temp()
        UP = self.read_raw_pressure()

        X1 = ((UT - self.cal_AC6) * self.cal_AC5) / self.power(15)
        X2 = (self.cal_MC * self.power(11)) / (X1 + self.cal_MD)
        B5 = X1 + X2

        # Pressure Calculations
        B6 = B5 - 4000
        X1 = (self.cal_B2 * (B6 * B6) /self.power(12)) /self.power(11)
        X2 = (self.cal_AC2 * B6) /self.power(11)
        X3 = X1 + X2
        B3 = (((self.cal_AC1 * 4 + X3) * self.power(self._mode)) + 2) / 4

        X1 = (self.cal_AC3 * B6) /self.power(13)
        X2 = (self.cal_B1 * ((B6 * B6)  /self.power(12))) /self.power(16)
        X3 = ((X1 + X2) + 2)/self.power(2)
        B4 = (self.cal_AC4 * (X3 + 32768)) / self.power(15)
        B7 = (UP - B3) * (50000 /self.power(self._mode))

        if B7 < 0x80000000:
            p = (B7 * 2) / B4
        else:
            p = (B7 / B4) * 2
        X1 = (p / self.power(8)) * (p /self.power(8))
        X1 = (X1 * 3038) /self.power(16)
        X2 = (-7357 * p) /self.power(16)

        p = p + ((X1 + X2 + 3791) /self.power(4))
        return p

    def read_altitude(self, sealevel_pa=101325.0):
        """Calculates the altitude in meters."""
        # Calculation taken straight from section 3.6 of the datasheet.
        pressure = float(self.read_pressure())
        altitude = 44330.0 * (1.0 - pow(pressure / sealevel_pa, (1.0 / 5.255)))
        return altitude

    def read_sealevel_pressure(self, altitude_m=0.0):
        """Calculates the pressure at sealevel when given a known altitude in
        meters. Returns a value in Pascals."""
        pressure = float(self.read_pressure())
        p0 = pressure / pow(1.0 - altitude_m / 44330.0, 5.255)

        return p0

    def power(self, num):
        return 2 ** num



DHTPIN = 17

GPIO.setmode(GPIO.BCM)

MAX_UNCHANGE_COUNT = 100

STATE_INIT_PULL_DOWN = 1
STATE_INIT_PULL_UP = 2
STATE_DATA_FIRST_PULL_DOWN = 3
STATE_DATA_PULL_UP = 4
STATE_DATA_PULL_DOWN = 5


class DHT11(object):
    def read_dht11_dat(self):
        GPIO.setup(DHTPIN, GPIO.OUT)
        GPIO.output(DHTPIN, GPIO.HIGH)
        time.sleep(0.05)
        GPIO.output(DHTPIN, GPIO.LOW)
        time.sleep(0.02)
        GPIO.setup(DHTPIN, GPIO.IN, GPIO.PUD_UP)

        unchanged_count = 0
        last = -1
        data = []
        while True:
            current = GPIO.input(DHTPIN)
            data.append(current)
            if last != current:
                unchanged_count = 0
                last = current
            else:
                unchanged_count += 1
                if unchanged_count > MAX_UNCHANGE_COUNT:
                    break

        state = STATE_INIT_PULL_DOWN

        lengths = []
        current_length = 0

        for current in data:
            current_length += 1

            if state == STATE_INIT_PULL_DOWN:
                if current == GPIO.LOW:
                    state = STATE_INIT_PULL_UP
                else:
                    continue
            if state == STATE_INIT_PULL_UP:
                if current == GPIO.HIGH:
                    state = STATE_DATA_FIRST_PULL_DOWN
                else:
                    continue
            if state == STATE_DATA_FIRST_PULL_DOWN:
                if current == GPIO.LOW:
                    state = STATE_DATA_PULL_UP
                else:
                    continue
            if state == STATE_DATA_PULL_UP:
                if current == GPIO.HIGH:
                    current_length = 0
                    state = STATE_DATA_PULL_DOWN
                else:
                    continue
            if state == STATE_DATA_PULL_DOWN:
                if current == GPIO.LOW:
                    lengths.append(current_length)
                    state = STATE_DATA_PULL_UP
                else:
                    continue
        if len(lengths) != 40:
            print("Data not good, skip")
            return False

        shortest_pull_up = min(lengths)
        longest_pull_up = max(lengths)
        halfway = (longest_pull_up + shortest_pull_up) / 2
        bits = []
        the_bytes = []
        byte = 0

        for length in lengths:
            bit = 0
            if length > halfway:
                bit = 1
            bits.append(bit)
        # print("bits: %s, length: %d" % (bits, len(bits)))
        for i in range(0, len(bits)):
            byte = byte << 1
            if (bits[i]):
                byte = byte | 1
            else:
                byte = byte | 0
            if ((i + 1) % 8 == 0):
                the_bytes.append(byte)
                byte = 0
        # print(the_bytes)
        checksum = (the_bytes[0] + the_bytes[1] + the_bytes[2] + the_bytes[3]) & 0xFF
        if the_bytes[4] != checksum:
            print("Data not good, skip")
            return False

        return the_bytes[0], the_bytes[2]

    def destory(self):
        print('终止 GPIO')
        GPIO.cleanup()



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
    except:
        dht11.destory()
        traceback.print_exc()
    return data


if __name__ == '__main__':
    while True:
        data = {}
        data['device_id'] = '123456'
        humiture = get_humiture()
        print('mian-humiture',humiture)
        data['humiture'] = humiture
        bmp180 = get_bmp180()
        print('mian-bmp180', bmp180)
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

