import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (QApplication,QWidget,QLabel,QVBoxLayout,QHBoxLayout,QPushButton,QLineEdit,QTextEdit,QComboBox,QTableWidget,QTableWidgetItem,QHeaderView,QFileDialog)
import pyqtgraph as pg
import numpy as np
import numpy as pd

from queue import Queue


class mainGui(QWidget):
    def __init__(self):
        super().__init()
        self.setWindowTitle('串口')
        self.resize(400,300)
    
    def portesan(self):
        self.pushbutton_scan = QPushButton("扫描串口")
        self.comboBox_ports = QComboBox()

        self.pushbutton_scan.clicked.connect()
    