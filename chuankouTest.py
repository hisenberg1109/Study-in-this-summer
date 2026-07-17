import sys
from PySide6.QtCore import Qt, Signal, QTimer,QThread
from PySide6.QtWidgets import (QApplication,QWidget,QLabel,QPushButton,
                               QComboBox,QTextEdit,QVBoxLayout,QHBoxLayout,QMessageBox)
from queue import Queue
import pyqtgraph as pg
from chuankouSerial import serialWork

class mainGui(QWidget):

    scanPortSignal = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("串口数据采集")
        self.resize(800, 600)
        self.buffer = Queue()
        self.portsScan()
        self.operateDisplayText()
        self.threadInit()
        self.init_ui()

    def init_ui(self):
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.pushButton_scan)
        mainLayout.addWidget(self.comboBox_ports)
        mainLayout.addWidget(self.display_text)

        self.setLayout(mainLayout)

    def portsScan(self):
        self.pushButton_scan = QPushButton("扫描串口")
        self.comboBox_ports = QComboBox()

        self.pushButton_scan.clicked.connect(self.scan_ports)


    def operateDisplayText(self):
        self.display_text = QTextEdit()
        self.display_text.setReadOnly(True)


    def threadInit(self):
        self.serial_thread = QThread()
        self.serial_worker = serialWork(self.buffer)
        self.serial_worker.moveToThread(self.serial_thread)

        self.scanPortSignal.connect(self.serial_worker.scan_ports)
        self.serial_worker.scanPortsResultSignal.connect(self.update_ports)
        self.serial_worker.operateResultSignal.connect(self.update_display)
        self.serial_thread.start()

    #slot
    def scan_ports(self):
        # 扫描串口的逻辑
        self.scanPortSignal.emit()

    def update_ports(self, ports):
        self.comboBox_ports.clear()
        for port in ports:
            self.comboBox_ports.addItem(port.device)
    def update_display(self, message):
        self.display_text.append(message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = mainGui()
    window.show()
    sys.exit(app.exec())






