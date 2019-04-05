#!/usr/bin/python3

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow

class smartchessgui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Smart Chess 0.1"
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = smartchessgui()
    sys.exit(app.exec())
