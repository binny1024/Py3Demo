import time
import traceback

import serial


def t_4g():
    ser = serial.Serial('/dev/ttyUSB2', 115200)
    if ser.isOpen == False:
        ser.open()
    try:
        print('检测 4G 模块')
        com_01 = 'at'
        send_data = com_01 + '\r\n'
        at = bytes(send_data, encoding="utf8")
        ser.write(at)
        data = ser.read(1)  # 阻塞读直到读出第一个数据，然后用serial.inWaiting()计算出接收缓冲区还有多少个数据，使用read读出来
        time.sleep(1)  # 有些AT指令的回复太长，延迟一段时间，希望开发板的串口已经将AT指令的回复已经全部接收到缓冲区
        data = (data + ser.read(ser.inWaiting())).decode()
        print(com_01, str(data))

        com_02 = 'ate1'
        send_data = com_02 + '\r\n'
        at = bytes(send_data, encoding="utf8")
        ser.write(at)
        data = ser.read(1)  # 阻塞读直到读出第一个数据，然后用serial.inWaiting()计算出接收缓冲区还有多少个数据，使用read读出来
        time.sleep(1)  # 有些AT指令的回复太长，延迟一段时间，希望开发板的串口已经将AT指令的回复已经全部接收到缓冲区
        data = (data + ser.read(ser.inWaiting())).decode()
        print(com_02, str(data))

        com_03 = 'at+cpin?'
        send_data = com_03 + '\r\n'
        at = bytes(send_data, encoding="utf8")
        ser.write(at)
        data = ser.read(1)  # 阻塞读直到读出第一个数据，然后用serial.inWaiting()计算出接收缓冲区还有多少个数据，使用read读出来
        time.sleep(1)  # 有些AT指令的回复太长，延迟一段时间，希望开发板的串口已经将AT指令的回复已经全部接收到缓冲区
        data = (data + ser.read(ser.inWaiting())).decode()
        print(com_03, str(data))

        com_04 = 'at+csq'
        send_data = com_04 + '\r\n'
        at = bytes(send_data, encoding="utf8")
        ser.write(at)
        data = ser.read(1)  # 阻塞读直到读出第一个数据，然后用serial.inWaiting()计算出接收缓冲区还有多少个数据，使用read读出来
        time.sleep(1)  # 有些AT指令的回复太长，延迟一段时间，希望开发板的串口已经将AT指令的回复已经全部接收到缓冲区
        data = (data + ser.read(ser.inWaiting())).decode()
        print(com_04, str(data))

        com_05 = "at+cops?"
        send_data = com_05 + '\r\n'
        at = bytes(send_data, encoding="utf8")
        ser.write(at)
        data = ser.read(1)  # 阻塞读直到读出第一个数据，然后用serial.inWaiting()计算出接收缓冲区还有多少个数据，使用read读出来
        time.sleep(1)  # 有些AT指令的回复太长，延迟一段时间，希望开发板的串口已经将AT指令的回复已经全部接收到缓冲区
        data = (data + ser.read(ser.inWaiting())).decode()
        print(com_05, str(data))

        com_06 = 'at+qnwinfo'
        send_data = com_06 + '\r\n'
        at = bytes(send_data, encoding="utf8")
        ser.write(at)
        data = ser.read(1)  # 阻塞读直到读出第一个数据，然后用serial.inWaiting()计算出接收缓冲区还有多少个数据，使用read读出来
        time.sleep(1)  # 有些AT指令的回复太长，延迟一段时间，希望开发板的串口已经将AT指令的回复已经全部接收到缓冲区
        data = (data + ser.read(ser.inWaiting())).decode()
        print(com_06, str(data))

        com_07 = 'at+creg?'
        send_data = com_07 + '\r\n'
        at = bytes(send_data, encoding="utf8")
        ser.write(at)
        data = ser.read(1)  # 阻塞读直到读出第一个数据，然后用serial.inWaiting()计算出接收缓冲区还有多少个数据，使用read读出来
        time.sleep(1)  # 有些AT指令的回复太长，延迟一段时间，希望开发板的串口已经将AT指令的回复已经全部接收到缓冲区
        data = (data + ser.read(ser.inWaiting())).decode()
        print(com_07, str(data))

        com_08 = 'AT+CGDCONT?'
        send_data = com_08 + '\r\n'
        at = bytes(send_data, encoding="utf8")
        ser.write(at)
        data = ser.read(1)  # 阻塞读直到读出第一个数据，然后用serial.inWaiting()计算出接收缓冲区还有多少个数据，使用read读出来
        time.sleep(1)  # 有些AT指令的回复太长，延迟一段时间，希望开发板的串口已经将AT指令的回复已经全部接收到缓冲区
        data = (data + ser.read(ser.inWaiting())).decode()
        print(com_08, str(data))
    except Exception as e:
        traceback.print_exc()
    except KeyboardInterrupt:
        ser.close()


if __name__ == '__main__':
    t_4g()
