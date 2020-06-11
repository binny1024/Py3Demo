import re
import serial
import time

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB1', 115200)
    if ser.isOpen == False:
        ser.open()
    try:
        while True:
            size = ser.inWaiting()
            if size != 0:
                data = ser.read(size)
                if (data == "quit"):
                    print("oppo seri has closen.\n>>", end="")
                    continue

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
                print('\n\n')
                ser.flushInput()
                time.sleep(5)
    except KeyboardInterrupt:
        ser.close()
