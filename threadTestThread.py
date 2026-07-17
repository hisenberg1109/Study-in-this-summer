import serial
import serial.tools.list_ports
from PySide6.QtCore import Qt, QThread, QTimer, QObject, Signal, Slot
from queue import Queue, Empty
import struct

class SerialOperate(QObject):
    scanPortsResultSignal = Signal(list)
    operateResultSignal = Signal(str)

    def __init__(self,buffer:Queue):
        super().__init__()
        self.buffer = buffer

    def scan_ports(self):
        ports = serial.tools.list_ports.comports()
        if ports:
            self.scanPortsResultSignal.emit(ports)
            self.operateResultSignal.emit(f"浏览端口为：{[port.device for port in ports]}")
        else:
            self.operateResultSignal.emit("未找到可用串口。")

    def open_port(self, port_name):
        try:
            self.ser = serial.Serial(port=port_name, baudrate=115200, timeout=0.01, write_timeout=1)
            self.operateResultSignal.emit(f"已打开串口：{port_name}")
        except Exception as e:
            self.operateResultSignal.emit(f"打开串口失败：{str(e)}")

    def close_port(self):
        if hasattr(self, 'ser') and self.ser.is_open:
            self.ser.close()
            self.operateResultSignal.emit("已关闭串口。")
        else:
            self.operateResultSignal.emit("串口未打开，无需关闭。")

    def start_acquisition(self):
        if hasattr(self, 'ser') and self.ser.is_open:
            frame = bytes([0xAA,0x55,0x02,0x00])
            # frame = bytes([0xD3,0x91,0xC7,0x01,0x31,0x00,0x01,0x00,0x02,0x00,0x14])
            # csv = self.crc16_ccitt_false(bytes([0x01,0x31,0x00,0x01,0x00,0x02,0x00,0x14]))
            # 计算校验和并追加到帧尾，形成完整命令帧
            csv = sum(frame)&0xFF
            frame += bytes([csv])
            # frame += csv.to_bytes(2, byteorder='big')
            self.ser.write(frame)
            self.operateResultSignal.emit(f"发送开始采集命令:{frame.hex()}。")
        else:
            self.operateResultSignal.emit("串口未打开，无法开始采集。")

    def stop_acquisition(self):
        if hasattr(self, 'ser') and self.ser.is_open:
            frame = bytes([0xAA,0x55,0x03,0x00])
            csv = sum(frame)&0xFF
            frame += bytes([csv])
            self.ser.write(frame)
            self.operateResultSignal.emit("发送停  止采集命令。")
        else:
            self.operateResultSignal.emit("串口未打开，无法停止采集。")

    def start_worker(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.read_serial)
        self.timer.start(20)

    def read_serial(self):
        if hasattr(self, 'ser') and self.ser.is_open:
            data = self.ser.read_all()
            if data:
                self.buffer.put(data)
                self.operateResultSignal.emit(f"接收到数据：{data.hex(' ')}")

    def crc16_ccitt_false(self,data: bytes) -> int:
        """
        CRC-16/CCITT-FALSE

        poly   = 0x1021
        init   = 0xFFFF
        refin  = False
        refout = False
        xorout = 0x0000
        """
        crc = 0xFFFF

        for byte in data:
            crc ^= byte << 8

            for _ in range(8):
                if crc & 0x8000:
                    crc = ((crc << 1) ^ 0x1021) & 0xFFFF
                else:
                    crc = (crc << 1) & 0xFFFF

        return crc

class ParsedWorker(QObject):
    # 用于向界面发送解析后的文本信息
    parsedResultSignal = Signal(str)
    parsedDataToPlotSignal = Signal(int,float,float)

    def __init__(self, buffer: Queue):
        super().__init__()
        self.buffer = buffer

    def start_worker(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.parse_data)
        self.timer.start(20)

    def parse_data(self):
        try:
            while True:
                data = self.buffer.get_nowait()
                if data:
                    #解析
                    if len(data) < 5:
                        continue
                    index = data.find(b'\xAA\x55')
                    if index == -1:
                        continue
                    data = data[index:]
                    if len(data) < 5:
                        continue
                    cmd = data[2]
                    length = data[3]
                    frame_len = 2 + 1 + 1 + length + 1
                    if len(data) < frame_len:
                        continue
                    frame = data[:frame_len]
                    if sum(frame[:-1]) & 0xFF != frame[-1]:
                        continue
                    if length == 0:
                        payload = b''
                        if cmd == 0x82:
                            parsed_text = "开始采集命令握手：开始采集握"
                        if cmd == 0x83:
                            parsed_text = "停止采集命令握手：停止采集握手"
                    else:
                        payload = frame[4:-1]
                        seq,temp,press = struct.unpack("<Hff", payload)
                        parsed_text = f"数据帧：No={seq}, Temp={temp:.2f} ℃, Press={press:.2f} kPa"
                        self.parsedResultSignal.emit(parsed_text)
                        self.parsedDataToPlotSignal.emit(seq,temp,press)
                else:
                    break
        except Empty:
            pass

    def stop_worker(self):
        if hasattr(self, 'timer'):
            self.timer.stop()

