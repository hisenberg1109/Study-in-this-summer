import serial
import time

ser = serial.Serial(port=r"\\\\.\\COM10", baudrate=115200, timeout=1)
while True:
    # 正确发送单字节 0xA6
    send_buf = bytes([0xA6,0x88,0xA0,0x01])
    ser.write(send_buf)
    print("已发送字节:", send_buf)
    time.sleep(1)
