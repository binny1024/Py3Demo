import time
import traceback

import serial

def open_gps():
    ser = serial.Serial('/dev/ttyUSB2', 115200)
    if ser.isOpen == False:
        ser.open()
    try:
        print('开启 GPS  信息')
        send_data = 'at+qgps=1' + '\r\n'
        at = bytes(send_data, encoding = "utf8")
        ser.write(at)
        data = ser.read(1)  # 阻塞读直到读出第一个数据，然后用serial.inWaiting()计算出接收缓冲区还有多少个数据，使用read读出来
        time.sleep(1)  # 有些AT指令的回复太长，延迟一段时间，希望开发板的串口已经将AT指令的回复已经全部接收到缓冲区
        data = (data + ser.read(ser.inWaiting())).decode()
        print(str(data))
    except Exception as e:
        traceback.print_exc()
    except KeyboardInterrupt:
        ser.close()


if __name__ == '__main__':
    open_gps()
