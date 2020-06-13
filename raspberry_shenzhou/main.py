import json
import time
import smbus
import RPi.GPIO as GPIO
import requests
import re
import traceback
import serial
import calendar
from decimal import Decimal
import math

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
        print('read_raw_temp')
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
        raw = ((MSB * self.power(16)) + (LSB * self.power(8)) + XLSB) / self.power((8 - self._mode))
        return raw

    def read_temperature(self):
        # print('read_temperature')
        """Gets the compensated temperature in degrees celsius."""
        UT = self.read_raw_temp()

        X1 = ((UT - self.cal_AC6) * self.cal_AC5) / self.power(15)
        X2 = (self.cal_MC * self.power(11)) / (X1 + self.cal_MD)
        B5 = X1 + X2
        # temp = ((B5 + 8) >> 4) / 10
        temp = ((B5 + 8) / self.power(4)) / 10
        return temp

    def read_pressure(self):
        # print('read_pressure')
        """Gets the compensated pressure in Pascals."""
        UT = self.read_raw_temp()
        UP = self.read_raw_pressure()

        X1 = ((UT - self.cal_AC6) * self.cal_AC5) / self.power(15)
        X2 = (self.cal_MC * self.power(11)) / (X1 + self.cal_MD)
        B5 = X1 + X2

        # Pressure Calculations
        B6 = B5 - 4000
        X1 = (self.cal_B2 * (B6 * B6) / self.power(12)) / self.power(11)
        X2 = (self.cal_AC2 * B6) / self.power(11)
        X3 = X1 + X2
        B3 = (((self.cal_AC1 * 4 + X3) * self.power(self._mode)) + 2) / 4

        X1 = (self.cal_AC3 * B6) / self.power(13)
        X2 = (self.cal_B1 * ((B6 * B6) / self.power(12))) / self.power(16)
        X3 = ((X1 + X2) + 2) / self.power(2)
        B4 = (self.cal_AC4 * (X3 + 32768)) / self.power(15)
        B7 = (UP - B3) * (50000 / self.power(self._mode))

        if B7 < 0x80000000:
            p = (B7 * 2) / B4
        else:
            p = (B7 / B4) * 2
        X1 = (p / self.power(8)) * (p / self.power(8))
        X1 = (X1 * 3038) / self.power(16)
        X2 = (-7357 * p) / self.power(16)

        p = p + ((X1 + X2 + 3791) / self.power(4))
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


def get_bmp180():
    """
    大气压
    :return:
    """
    data = {'error': ''}
    try:
        bmp = BMP180()
        temp_bmp = bmp.read_temperature()
        pressure_air = bmp.read_pressure()
        altitude = bmp.read_altitude()
        data['timestamp'] = calendar.timegm(time.gmtime())
        data['temp_bmp'] = "{:.2f} C".format(temp_bmp)
        data['pressure_air'] = "{:.2f} hPa".format(pressure_air / 100.0)
        data['altitude'] = "{:.2f}".format(altitude)
        print('读取大气压')
        return data
        # res = requests.post(url_bpm, json=data)
        # print(res.json())
    except Exception as e:
        data['msg'] = '大气压信息失败'
        data['error'] = str(e)
        print('读取大气压', str(e))
        return data


"""
温湿度计
"""
GPIO.setmode(GPIO.BCM)
MAX_UNCHANGE_COUNT = 100
STATE_INIT_PULL_DOWN = 1
STATE_INIT_PULL_UP = 2
STATE_DATA_FIRST_PULL_DOWN = 3
STATE_DATA_PULL_UP = 4
STATE_DATA_PULL_DOWN = 5
DHTPIN = 17


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
            print("lengths --- Data not good, skip")
            return False
        print("lengths --- is  good")
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
        print("bits: %s, length: %d" % (bits, len(bits)))
        for i in range(0, len(bits)):
            byte = byte << 1
            if (bits[i]):
                byte = byte | 1
            else:
                byte = byte | 0
            if ((i + 1) % 8 == 0):
                the_bytes.append(byte)
                byte = 0
        print('the_bytes', the_bytes)
        checksum = (the_bytes[0] + the_bytes[1] + the_bytes[2] + the_bytes[3]) & 0xFF
        if the_bytes[4] != checksum:
            print("checksum ---- Data not good, skip")
            return False
        print("checksum ----  good")
        return the_bytes[0], the_bytes[2]

    def destory(self):
        print('终止 GPIO')
        GPIO.cleanup()


def get_humiture():
    """
    温湿度信息
    :param url:  上传接口地址
    :return:
    """
    data = {'error': ''}
    dht11 = DHT11()
    try:
        data['timestamp'] = calendar.timegm(time.gmtime())
        result = dht11.read_dht11_dat()
        print('humiture', result)
        if result:
            humi_dht11, temp_dht11 = result
            data['humi_dht11'] = "{}".format(humi_dht11)
            data['temp_dht11'] = "{}".format(temp_dht11)
            # res = requests.post(url_humiture, json=data)
            # print(res.json())
        else:
            data['msg'] = 'Sensor is anomaly'
            data['error'] = 'Possible cause: Loose humiture  sensors'
        return data
    except Exception as e:
        dht11.destory()
        data['error'] = str(e)
        traceback.print_exc()
        return data


"""
GSP
"""


def open_gps():
    """
        开启 GSP 定位
        :return:
        """
    ser = serial.Serial('/dev/ttyUSB2', 115200)
    if ser.isOpen == False:
        ser.open()
    try:
        print('开启 GPS  信息')
        send_data = 'at+qgps=1' + '\r\n'
        at = bytes(send_data, encoding="utf8")
        ser.write(at)
        data = ser.read(1)  # 阻塞读直到读出第一个数据，然后用serial.inWaiting()计算出接收缓冲区还有多少个数据，使用read读出来
        time.sleep(0.1)  # 有些AT指令的回复太长，延迟一段时间，希望开发板的串口已经将AT指令的回复已经全部接收到缓冲区
        data = (data + ser.read(ser.inWaiting())).decode()
        print(data)
    except Exception as e:
        traceback.print_exc()
    except KeyboardInterrupt:
        ser.close()


def get_gps():
    """
    获取 GSP信息

    :return:
    """
    ser = serial.Serial('/dev/ttyUSB1', 115200)
    if ser.isOpen == False:
        ser.open()
    result = {'error': ''}
    try:
        print('获取 GPS 信息')
        while True:
            size = ser.inWaiting()
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
                # print('UTC 时间', utc_time)
                location_status = ls[2]
                # print('定位状态', location_status)
                # print('维度信息', ls[3])
                result['latitude_0'] = ls[3]
                latitude = ''
                if ls[3] != "":
                    latitude = float(ls[3]) // 100
                    latitude = latitude + (float(ls[3]) - latitude * 100) / float(60)
                    latitude = Decimal(latitude).quantize(Decimal('0.00000'))

                latitude_position = ls[4]
                # print('维度半球', latitude_position)

                result['longitude_0'] = ls[5]
                longitude = ''
                if ls[5] != "":
                    longitude = float(ls[5]) // 100
                    longitude = longitude + (float(ls[5]) - longitude * 100) / float(60)
                    longitude = Decimal(longitude).quantize(Decimal('0.00000'))
                # print('经度信息', longitude)
                longitude_position = ls[6]
                # print('经度半球', longitude_position)
                # print('地面速率', ls[7])
                # print('地面航向', ls[8])
                # print('UTC 日期', ls[9])
                # print('磁偏角', ls[10])
                # print('磁偏角方向', ls[11])
                # print('模式指示', ls[12])

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


"""
加速计
"""

Gyro = [0, 0, 0]
Accel = [0, 0, 0]
Mag = [0, 0, 0]
pitch = 0.0
roll = 0.0
yaw = 0.0
pu8data = [0, 0, 0, 0, 0, 0, 0, 0]
U8tempX = [0, 0, 0, 0, 0, 0, 0, 0, 0]
U8tempY = [0, 0, 0, 0, 0, 0, 0, 0, 0]
U8tempZ = [0, 0, 0, 0, 0, 0, 0, 0, 0]
GyroOffset = [0, 0, 0]
Ki = 1.0
Kp = 4.50
q0 = 1.0
q1 = q2 = q3 = 0.0
angles = [0.0, 0.0, 0.0]
true = 0x01
false = 0x00
# define ICM-20948 Device I2C address
I2C_ADD_ICM20948 = 0x68
I2C_ADD_ICM20948_AK09916 = 0x0C
I2C_ADD_ICM20948_AK09916_READ = 0x80
I2C_ADD_ICM20948_AK09916_WRITE = 0x00
# define ICM-20948 Register
# user bank 0 register
REG_ADD_WIA = 0x00
REG_VAL_WIA = 0xEA
REG_ADD_USER_CTRL = 0x03
REG_VAL_BIT_DMP_EN = 0x80
REG_VAL_BIT_FIFO_EN = 0x40
REG_VAL_BIT_I2C_MST_EN = 0x20
REG_VAL_BIT_I2C_IF_DIS = 0x10
REG_VAL_BIT_DMP_RST = 0x08
REG_VAL_BIT_DIAMOND_DMP_RST = 0x04
REG_ADD_PWR_MIGMT_1 = 0x06
REG_VAL_ALL_RGE_RESET = 0x80
REG_VAL_RUN_MODE = 0x01  # Non low-power mode
REG_ADD_LP_CONFIG = 0x05
REG_ADD_PWR_MGMT_1 = 0x06
REG_ADD_PWR_MGMT_2 = 0x07
REG_ADD_ACCEL_XOUT_H = 0x2D
REG_ADD_ACCEL_XOUT_L = 0x2E
REG_ADD_ACCEL_YOUT_H = 0x2F
REG_ADD_ACCEL_YOUT_L = 0x30
REG_ADD_ACCEL_ZOUT_H = 0x31
REG_ADD_ACCEL_ZOUT_L = 0x32
REG_ADD_GYRO_XOUT_H = 0x33
REG_ADD_GYRO_XOUT_L = 0x34
REG_ADD_GYRO_YOUT_H = 0x35
REG_ADD_GYRO_YOUT_L = 0x36
REG_ADD_GYRO_ZOUT_H = 0x37
REG_ADD_GYRO_ZOUT_L = 0x38
REG_ADD_EXT_SENS_DATA_00 = 0x3B
REG_ADD_REG_BANK_SEL = 0x7F
REG_VAL_REG_BANK_0 = 0x00
REG_VAL_REG_BANK_1 = 0x10
REG_VAL_REG_BANK_2 = 0x20
REG_VAL_REG_BANK_3 = 0x30

# user bank 1 register
# user bank 2 register
REG_ADD_GYRO_SMPLRT_DIV = 0x00
REG_ADD_GYRO_CONFIG_1 = 0x01
REG_VAL_BIT_GYRO_DLPCFG_2 = 0x10  # bit[5:3]
REG_VAL_BIT_GYRO_DLPCFG_4 = 0x20  # bit[5:3]
REG_VAL_BIT_GYRO_DLPCFG_6 = 0x30  # bit[5:3]
REG_VAL_BIT_GYRO_FS_250DPS = 0x00  # bit[2:1]
REG_VAL_BIT_GYRO_FS_500DPS = 0x02  # bit[2:1]
REG_VAL_BIT_GYRO_FS_1000DPS = 0x04  # bit[2:1]
REG_VAL_BIT_GYRO_FS_2000DPS = 0x06  # bit[2:1]
REG_VAL_BIT_GYRO_DLPF = 0x01  # bit[0]
REG_ADD_ACCEL_SMPLRT_DIV_2 = 0x11
REG_ADD_ACCEL_CONFIG = 0x14
REG_VAL_BIT_ACCEL_DLPCFG_2 = 0x10  # bit[5:3]
REG_VAL_BIT_ACCEL_DLPCFG_4 = 0x20  # bit[5:3]
REG_VAL_BIT_ACCEL_DLPCFG_6 = 0x30  # bit[5:3]
REG_VAL_BIT_ACCEL_FS_2g = 0x00  # bit[2:1]
REG_VAL_BIT_ACCEL_FS_4g = 0x02  # bit[2:1]
REG_VAL_BIT_ACCEL_FS_8g = 0x04  # bit[2:1]
REG_VAL_BIT_ACCEL_FS_16g = 0x06  # bit[2:1]
REG_VAL_BIT_ACCEL_DLPF = 0x01  # bit[0]

# user bank 3 register
REG_ADD_I2C_SLV0_ADDR = 0x03
REG_ADD_I2C_SLV0_REG = 0x04
REG_ADD_I2C_SLV0_CTRL = 0x05
REG_VAL_BIT_SLV0_EN = 0x80
REG_VAL_BIT_MASK_LEN = 0x07
REG_ADD_I2C_SLV0_DO = 0x06
REG_ADD_I2C_SLV1_ADDR = 0x07
REG_ADD_I2C_SLV1_REG = 0x08
REG_ADD_I2C_SLV1_CTRL = 0x09
REG_ADD_I2C_SLV1_DO = 0x0A

# define ICM-20948 Register  end

# define ICM-20948 MAG Register
REG_ADD_MAG_WIA1 = 0x00
REG_VAL_MAG_WIA1 = 0x48
REG_ADD_MAG_WIA2 = 0x01
REG_VAL_MAG_WIA2 = 0x09
REG_ADD_MAG_ST2 = 0x10
REG_ADD_MAG_DATA = 0x11
REG_ADD_MAG_CNTL2 = 0x31
REG_VAL_MAG_MODE_PD = 0x00
REG_VAL_MAG_MODE_SM = 0x01
REG_VAL_MAG_MODE_10HZ = 0x02
REG_VAL_MAG_MODE_20HZ = 0x04
REG_VAL_MAG_MODE_50HZ = 0x05
REG_VAL_MAG_MODE_100HZ = 0x08
REG_VAL_MAG_MODE_ST = 0x10
# define ICM-20948 MAG Register  end
MAG_DATA_LEN = 6


class ICM20948(object):
    def __init__(self, address=I2C_ADD_ICM20948):
        self._address = address
        self._bus = smbus.SMBus(1)
        bRet = self.icm20948Check()  # Initialization of the device multiple times after power on will result in a return error
        # while true != bRet:
        #   print("ICM-20948 Error\n" )
        #   time.sleep(0.5)
        # print("ICM-20948 OK\n" )
        time.sleep(0.5)  # We can skip this detection by delaying it by 500 milliseconds
        # user bank 0 register
        self._write_byte(REG_ADD_REG_BANK_SEL, REG_VAL_REG_BANK_0)
        self._write_byte(REG_ADD_PWR_MIGMT_1, REG_VAL_ALL_RGE_RESET)
        time.sleep(0.1)
        self._write_byte(REG_ADD_PWR_MIGMT_1, REG_VAL_RUN_MODE)
        # user bank 2 register
        self._write_byte(REG_ADD_REG_BANK_SEL, REG_VAL_REG_BANK_2)
        self._write_byte(REG_ADD_GYRO_SMPLRT_DIV, 0x07)
        self._write_byte(REG_ADD_GYRO_CONFIG_1,
                         REG_VAL_BIT_GYRO_DLPCFG_6 | REG_VAL_BIT_GYRO_FS_1000DPS | REG_VAL_BIT_GYRO_DLPF)
        self._write_byte(REG_ADD_ACCEL_SMPLRT_DIV_2, 0x07)
        self._write_byte(REG_ADD_ACCEL_CONFIG,
                         REG_VAL_BIT_ACCEL_DLPCFG_6 | REG_VAL_BIT_ACCEL_FS_2g | REG_VAL_BIT_ACCEL_DLPF)
        # user bank 0 register
        self._write_byte(REG_ADD_REG_BANK_SEL, REG_VAL_REG_BANK_0)
        time.sleep(0.1)
        self.icm20948GyroOffset()
        self.icm20948MagCheck()
        self.icm20948WriteSecondary(I2C_ADD_ICM20948_AK09916 | I2C_ADD_ICM20948_AK09916_WRITE, REG_ADD_MAG_CNTL2,
                                    REG_VAL_MAG_MODE_20HZ)

    def icm20948_Gyro_Accel_Read(self):
        self._write_byte(REG_ADD_REG_BANK_SEL, REG_VAL_REG_BANK_0)
        data = self._read_block(REG_ADD_ACCEL_XOUT_H, 12)
        self._write_byte(REG_ADD_REG_BANK_SEL, REG_VAL_REG_BANK_2)
        Accel[0] = (data[0] << 8) | data[1]
        Accel[1] = (data[2] << 8) | data[3]
        Accel[2] = (data[4] << 8) | data[5]
        Gyro[0] = ((data[6] << 8) | data[7]) - GyroOffset[0]
        Gyro[1] = ((data[8] << 8) | data[9]) - GyroOffset[1]
        Gyro[2] = ((data[10] << 8) | data[11]) - GyroOffset[2]
        if Accel[0] >= 32767:  # Solve the problem that Python shift will not overflow
            Accel[0] = Accel[0] - 65535
        elif Accel[0] <= -32767:
            Accel[0] = Accel[0] + 65535
        if Accel[1] >= 32767:
            Accel[1] = Accel[1] - 65535
        elif Accel[1] <= -32767:
            Accel[1] = Accel[1] + 65535
        if Accel[2] >= 32767:
            Accel[2] = Accel[2] - 65535
        elif Accel[2] <= -32767:
            Accel[2] = Accel[2] + 65535
        if Gyro[0] >= 32767:
            Gyro[0] = Gyro[0] - 65535
        elif Gyro[0] <= -32767:
            Gyro[0] = Gyro[0] + 65535
        if Gyro[1] >= 32767:
            Gyro[1] = Gyro[1] - 65535
        elif Gyro[1] <= -32767:
            Gyro[1] = Gyro[1] + 65535
        if Gyro[2] >= 32767:
            Gyro[2] = Gyro[2] - 65535
        elif Gyro[2] <= -32767:
            Gyro[2] = Gyro[2] + 65535

    def icm20948MagRead(self):
        counter = 20
        while (counter > 0):
            time.sleep(0.01)
            self.icm20948ReadSecondary(I2C_ADD_ICM20948_AK09916 | I2C_ADD_ICM20948_AK09916_READ, REG_ADD_MAG_ST2, 1)
            if ((pu8data[0] & 0x01) != 0):
                break
            counter -= 1
        if counter != 0:
            for i in range(0, 8):
                self.icm20948ReadSecondary(I2C_ADD_ICM20948_AK09916 | I2C_ADD_ICM20948_AK09916_READ, REG_ADD_MAG_DATA,
                                           MAG_DATA_LEN)
                U8tempX[i] = (pu8data[1] << 8) | pu8data[0]
                U8tempY[i] = (pu8data[3] << 8) | pu8data[2]
                U8tempZ[i] = (pu8data[5] << 8) | pu8data[4]
            Mag[0] = (U8tempX[0] + U8tempX[1] + U8tempX[2] + U8tempX[3] + U8tempX[4] + U8tempX[5] + U8tempX[6] +
                      U8tempX[7]) / 8
            Mag[1] = -(U8tempY[0] + U8tempY[1] + U8tempY[2] + U8tempY[3] + U8tempY[4] + U8tempY[5] + U8tempY[6] +
                       U8tempY[7]) / 8
            Mag[2] = -(U8tempZ[0] + U8tempZ[1] + U8tempZ[2] + U8tempZ[3] + U8tempZ[4] + U8tempZ[5] + U8tempZ[6] +
                       U8tempZ[7]) / 8
        if Mag[0] >= 32767:  # Solve the problem that Python shift will not overflow
            Mag[0] = Mag[0] - 65535
        elif Mag[0] <= -32767:
            Mag[0] = Mag[0] + 65535
        if Mag[1] >= 32767:
            Mag[1] = Mag[1] - 65535
        elif Mag[1] <= -32767:
            Mag[1] = Mag[1] + 65535
        if Mag[2] >= 32767:
            Mag[2] = Mag[2] - 65535
        elif Mag[2] <= -32767:
            Mag[2] = Mag[2] + 65535

    def icm20948ReadSecondary(self, u8I2CAddr, u8RegAddr, u8Len):
        u8Temp = 0
        self._write_byte(REG_ADD_REG_BANK_SEL, REG_VAL_REG_BANK_3)  # swtich bank3
        self._write_byte(REG_ADD_I2C_SLV0_ADDR, u8I2CAddr)
        self._write_byte(REG_ADD_I2C_SLV0_REG, u8RegAddr)
        self._write_byte(REG_ADD_I2C_SLV0_CTRL, REG_VAL_BIT_SLV0_EN | u8Len)

        self._write_byte(REG_ADD_REG_BANK_SEL, REG_VAL_REG_BANK_0)  # swtich bank0

        u8Temp = self._read_byte(REG_ADD_USER_CTRL)
        u8Temp |= REG_VAL_BIT_I2C_MST_EN
        self._write_byte(REG_ADD_USER_CTRL, u8Temp)
        time.sleep(0.01)
        u8Temp &= ~REG_VAL_BIT_I2C_MST_EN
        self._write_byte(REG_ADD_USER_CTRL, u8Temp)

        for i in range(0, u8Len):
            pu8data[i] = self._read_byte(REG_ADD_EXT_SENS_DATA_00 + i)

        self._write_byte(REG_ADD_REG_BANK_SEL, REG_VAL_REG_BANK_3)  # swtich bank3

        u8Temp = self._read_byte(REG_ADD_I2C_SLV0_CTRL)
        u8Temp &= ~((REG_VAL_BIT_I2C_MST_EN) & (REG_VAL_BIT_MASK_LEN))
        self._write_byte(REG_ADD_I2C_SLV0_CTRL, u8Temp)

        self._write_byte(REG_ADD_REG_BANK_SEL, REG_VAL_REG_BANK_0)  # swtich bank0

    def icm20948WriteSecondary(self, u8I2CAddr, u8RegAddr, u8data):
        u8Temp = 0
        self._write_byte(REG_ADD_REG_BANK_SEL, REG_VAL_REG_BANK_3)  # swtich bank3
        self._write_byte(REG_ADD_I2C_SLV1_ADDR, u8I2CAddr)
        self._write_byte(REG_ADD_I2C_SLV1_REG, u8RegAddr)
        self._write_byte(REG_ADD_I2C_SLV1_DO, u8data)
        self._write_byte(REG_ADD_I2C_SLV1_CTRL, REG_VAL_BIT_SLV0_EN | 1)

        self._write_byte(REG_ADD_REG_BANK_SEL, REG_VAL_REG_BANK_0)  # swtich bank0

        u8Temp = self._read_byte(REG_ADD_USER_CTRL)
        u8Temp |= REG_VAL_BIT_I2C_MST_EN
        self._write_byte(REG_ADD_USER_CTRL, u8Temp)
        time.sleep(0.01)
        u8Temp &= ~REG_VAL_BIT_I2C_MST_EN
        self._write_byte(REG_ADD_USER_CTRL, u8Temp)

        self._write_byte(REG_ADD_REG_BANK_SEL, REG_VAL_REG_BANK_3)  # swtich bank3

        u8Temp = self._read_byte(REG_ADD_I2C_SLV0_CTRL)
        u8Temp &= ~((REG_VAL_BIT_I2C_MST_EN) & (REG_VAL_BIT_MASK_LEN))
        self._write_byte(REG_ADD_I2C_SLV0_CTRL, u8Temp)

        self._write_byte(REG_ADD_REG_BANK_SEL, REG_VAL_REG_BANK_0)  # swtich bank0

    def icm20948GyroOffset(self):
        s32TempGx = 0
        s32TempGy = 0
        s32TempGz = 0
        for i in range(0, 32):
            self.icm20948_Gyro_Accel_Read()
            s32TempGx += Gyro[0]
            s32TempGy += Gyro[1]
            s32TempGz += Gyro[2]
            time.sleep(0.01)
        GyroOffset[0] = s32TempGx >> 5
        GyroOffset[1] = s32TempGy >> 5
        GyroOffset[2] = s32TempGz >> 5

    def _read_byte(self, cmd):
        return self._bus.read_byte_data(self._address, cmd)

    def _read_block(self, reg, length=1):
        return self._bus.read_i2c_block_data(self._address, reg, length)

    def _read_u16(self, cmd):
        LSB = self._bus.read_byte_data(self._address, cmd)
        MSB = self._bus.read_byte_data(self._address, cmd + 1)
        return (MSB << 8) + LSB

    def _write_byte(self, cmd, val):
        self._bus.write_byte_data(self._address, cmd, val)
        time.sleep(0.0001)

    def imuAHRSupdate(self, gx, gy, gz, ax, ay, az, mx, my, mz):
        norm = 0.0
        hx = hy = hz = bx = bz = 0.0
        vx = vy = vz = wx = wy = wz = 0.0
        exInt = eyInt = ezInt = 0.0
        ex = ey = ez = 0.0
        halfT = 0.024
        global q0
        global q1
        global q2
        global q3
        q0q0 = q0 * q0
        q0q1 = q0 * q1
        q0q2 = q0 * q2
        q0q3 = q0 * q3
        q1q1 = q1 * q1
        q1q2 = q1 * q2
        q1q3 = q1 * q3
        q2q2 = q2 * q2
        q2q3 = q2 * q3
        q3q3 = q3 * q3

        norm = float(1 / math.sqrt(ax * ax + ay * ay + az * az))
        ax = ax * norm
        ay = ay * norm
        az = az * norm

        norm = float(1 / math.sqrt(mx * mx + my * my + mz * mz))
        mx = mx * norm
        my = my * norm
        mz = mz * norm

        # compute reference direction of flux
        hx = 2 * mx * (0.5 - q2q2 - q3q3) + 2 * my * (q1q2 - q0q3) + 2 * mz * (q1q3 + q0q2)
        hy = 2 * mx * (q1q2 + q0q3) + 2 * my * (0.5 - q1q1 - q3q3) + 2 * mz * (q2q3 - q0q1)
        hz = 2 * mx * (q1q3 - q0q2) + 2 * my * (q2q3 + q0q1) + 2 * mz * (0.5 - q1q1 - q2q2)
        bx = math.sqrt((hx * hx) + (hy * hy))
        bz = hz

        # estimated direction of gravity and flux (v and w)
        vx = 2 * (q1q3 - q0q2)
        vy = 2 * (q0q1 + q2q3)
        vz = q0q0 - q1q1 - q2q2 + q3q3
        wx = 2 * bx * (0.5 - q2q2 - q3q3) + 2 * bz * (q1q3 - q0q2)
        wy = 2 * bx * (q1q2 - q0q3) + 2 * bz * (q0q1 + q2q3)
        wz = 2 * bx * (q0q2 + q1q3) + 2 * bz * (0.5 - q1q1 - q2q2)

        # error is sum of cross product between reference direction of fields and direction measured by sensors
        ex = (ay * vz - az * vy) + (my * wz - mz * wy)
        ey = (az * vx - ax * vz) + (mz * wx - mx * wz)
        ez = (ax * vy - ay * vx) + (mx * wy - my * wx)

        if (ex != 0.0 and ey != 0.0 and ez != 0.0):
            exInt = exInt + ex * Ki * halfT
            eyInt = eyInt + ey * Ki * halfT
            ezInt = ezInt + ez * Ki * halfT

            gx = gx + Kp * ex + exInt
            gy = gy + Kp * ey + eyInt
            gz = gz + Kp * ez + ezInt

        q0 = q0 + (-q1 * gx - q2 * gy - q3 * gz) * halfT
        q1 = q1 + (q0 * gx + q2 * gz - q3 * gy) * halfT
        q2 = q2 + (q0 * gy - q1 * gz + q3 * gx) * halfT
        q3 = q3 + (q0 * gz + q1 * gy - q2 * gx) * halfT

        norm = float(1 / math.sqrt(q0 * q0 + q1 * q1 + q2 * q2 + q3 * q3))
        q0 = q0 * norm
        q1 = q1 * norm
        q2 = q2 * norm
        q3 = q3 * norm

    def icm20948Check(self):
        bRet = false
        if REG_VAL_WIA == self._read_byte(REG_ADD_WIA):
            bRet = true
        return bRet

    def icm20948MagCheck(self):
        self.icm20948ReadSecondary(I2C_ADD_ICM20948_AK09916 | I2C_ADD_ICM20948_AK09916_READ, REG_ADD_MAG_WIA1, 2)
        if (pu8data[0] == REG_VAL_MAG_WIA1) and (pu8data[1] == REG_VAL_MAG_WIA2):
            bRet = true
            return bRet

    def icm20948CalAvgValue(self):
        MotionVal[0] = Gyro[0] / 32.8
        MotionVal[1] = Gyro[1] / 32.8
        MotionVal[2] = Gyro[2] / 32.8
        MotionVal[3] = Accel[0]
        MotionVal[4] = Accel[1]
        MotionVal[5] = Accel[2]
        MotionVal[6] = Mag[0]
        MotionVal[7] = Mag[1]
        MotionVal[8] = Mag[2]


if __name__ == '__main__':
    MotionVal = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    icm20948 = ICM20948()
    host = 'http://192.168.22.121:3001'
    # host = 'http://dangerapi.vonescan.com'
    url_sensor = host + '/api/poc/cc/sensor'
    open_gps()
    time.sleep(5)
    # 有个传感器数据没有拿到，就记录一次
    try_again_times = 0
    try_again_times_total = 3

    error = ''
    while True:
        no_data_humi = 0
        no_data_gps = 0
        no_data_acc = 0
        """
        记录传感器异常的个数，只要有一个就准备重新获取传感器信息
        """
        data = {'error': ''}
        data['device_id'] = 'ionc'
        """
        获取温湿度信息
        """
        try:
            humiture = get_humiture()
            if humiture['error'] != '':
                print('未获取到 GPS 信息，即将重新获取')
                no_data_humi = no_data_humi + 1
            # print('mian-humiture', humiture)
            data['humiture'] = humiture
        except Exception as e:
            traceback.print_exc()
            print('获取 温湿度 信息异常')

        """
        获取大气压信息
        """
        try:
            bmp180 = get_bmp180()
            if bmp180['error'] != '':
                print('未获取大气压信息信息，即将重新获取')
                no_data_gps = no_data_gps + 1
            # print('mian-bmp180', bmp180)
            data['bmp180'] = bmp180
        except Exception as e:
            traceback.print_exc()
            print('获取 气压 信息异常')

        """
        获取 GSP 信息
        """
        try:
            gps = get_gps()
            if gps['error'] != '':
                print('未获取到 GPS 信息，即将重新获取')
                no_data_acc = no_data_acc + 1
            data['gps'] = gps
        except:
            traceback.print_exc()
            print('获取 GSP 信息异常')

        """
        获取加速计信息
        """
        try:
            icm20948.icm20948_Gyro_Accel_Read()
            icm20948.icm20948MagRead()
            icm20948.icm20948CalAvgValue()
            time.sleep(0.1)
            icm20948.imuAHRSupdate(MotionVal[0] * 0.0175, MotionVal[1] * 0.0175, MotionVal[2] * 0.0175,
                                   MotionVal[3], MotionVal[4], MotionVal[5],
                                   MotionVal[6], MotionVal[7], MotionVal[8])
            pitch = math.asin(-2 * q1 * q3 + 2 * q0 * q2) * 57.3
            roll = math.atan2(2 * q2 * q3 + 2 * q0 * q1, -2 * q1 * q1 - 2 * q2 * q2 + 1) * 57.3
            yaw = math.atan2(-2 * q1 * q2 - 2 * q0 * q3, 2 * q2 * q2 + 2 * q3 * q3 - 1) * 57.3
            # print("\r\n /-------------------------------------------------------------/ \r\n")
            # print('\r\n Roll = %.2f , Pitch = %.2f , Yaw = %.2f\r\n' % (roll, pitch, yaw))
            # print('\r\nAcceleration:  X = %d , Y = %d , Z = %d\r\n' % (Accel[0], Accel[1], Accel[2]))
            # print('\r\nGyroscope:     X = %d , Y = %d , Z = %d\r\n' % (Gyro[0], Gyro[1], Gyro[2]))
            # print('\r\nMagnetic:      X = %d , Y = %d , Z = %d' % ((Mag[0]), Mag[1], Mag[2]))

            acceleration = {}
            acceleration['x'] = Accel[0]
            acceleration['y'] = Accel[1]
            acceleration['z'] = Accel[2]
            acceleration['error'] = ''

            gyroscope = {}
            gyroscope['x'] = Gyro[0]
            gyroscope['y'] = Gyro[1]
            gyroscope['z'] = Gyro[2]
            gyroscope['error'] = ''

            magnetic = {}
            magnetic['x'] = Mag[0]
            magnetic['y'] = Mag[1]
            magnetic['z'] = Mag[2]
            magnetic['error'] = ''

            data['acceleration'] = acceleration
            data['gyroscope'] = gyroscope
            data['magnetic'] = magnetic
        except Exception as e:
            traceback.print_exc()
            print('加速计信息')
            acceleration = {}
            acceleration['x'] = '0'
            acceleration['y'] = '0'
            acceleration['z'] = '0'
            acceleration['error'] = str(e)

            gyroscope = {}
            gyroscope['x'] = '0'
            gyroscope['y'] = '0'
            gyroscope['z'] = '0'
            gyroscope['error'] = str(e)

            magnetic = {}
            magnetic['x'] = '0'
            magnetic['y'] = '0'
            magnetic['z'] = '0'
            magnetic['error'] = str(e)

            data['acceleration'] = acceleration
            data['gyroscope'] = gyroscope
            data['magnetic'] = magnetic
            print('1', no_data_humi, no_data_gps, no_data_acc)
        if (no_data_acc != 0 or no_data_gps != 0 or no_data_humi != 0) and try_again_times < try_again_times_total:
            try_again_times = try_again_times + 1
            """
            如果有异常数据
            """
            error = 'After ' + str(
                try_again_times) + ' times attempts, all data is not obtained. Please check if the sensor is abnormal or contact the administrator'
            data['error'] = error
            print('failure', json.dumps(data))
            time.sleep(2)
            print('try_again_times = ', try_again_times)
            continue

        data['error'] = error
        try_again_times = 0

        print('result', json.dumps(data))
        """
        数据上链
        """
        # try:
        #     res = requests.post(url_sensor, json=data)
        #     print(res.json())
        # except:
        #     # traceback.print_exc()
        #     print('服务异常', url_sensor)
        #     continue

        time.sleep(5)
