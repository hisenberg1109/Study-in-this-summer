import serial
import struct

ser = serial.Serial(port=r"\\\\.\\COM11", baudrate=115200, timeout=1)
# 字节缓存区
buf = b""
while True:
    raw = ser.read(100)
    if raw:
        buf += raw
        # 假设协议固定2字节一帧，循环解析
        while len(buf) >= 4:
            frame = buf[:4]
            buf = buf[4:]  # 切掉已解析的数据
            val1= struct.unpack("<f", frame)
            val2= struct.unpack(">f", frame)
            print(f"小端解析成功：字节1={val1}")
            print(f"大端解析成功：字节1={val2}")
