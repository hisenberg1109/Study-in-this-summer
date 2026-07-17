import sys
import serial
import serial.tools.list_ports
from PySide6.QtCore import Qt, Signal, QTimer, QThread, QObject
from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                               QComboBox, QTextEdit, QVBoxLayout, QHBoxLayout, QMessageBox)
from queue import Queue
import pyqtgraph as pg


class serialWork(QObject):
    """串口扫描和操作后台工作类。

    这个类继承自 QObject，用于在 Qt 线程中执行串口扫描任务，
    并通过 Signal 将结果发送到主线程更新界面。
    """

    # 信号：扫描到的端口结果列表
    scanPortsResultSignal = Signal(list)
    # 信号：操作结果文本，用于显示状态信息
    operateResultSignal = Signal(str)

    def __init__(self, buffer: Queue):
        super().__init__()
        # 初始化一个队列对象，用于后续数据通信或任务缓存
        self.buffer = Queue()

    def scan_ports(self):
        """扫描系统中可用串口，并发送结果信号。"""
        # 获取当前可用串口列表
        ports = serial.tools.list_ports.comports()
        if ports:
            # 将扫描到的端口列表发送给界面
            self.scanPortsResultSignal.emit(ports)
            # 同时发送一条状态信息，显示端口设备名
            self.operateResultSignal.emit(f"浏览端口为：{[port.device for port in ports]}")
        else:
            # 没有找到串口时发送提示信息
            self.operateResultSignal.emit("未找到可用串口。")