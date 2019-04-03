#!/usr/bin/python3

import chess
import chess.svg

import sys

from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtSvg import QSvgWidget, QSvgRenderer

class EventApi():
    PIECED_MOVE = 'EVT_PIECE_MOVED'
    

def startChessGame():
    board = chess.Board()
    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    svgWidget = QSvgWidget()
    svgWidget.renderer().load("temp.svg")
    svgWidget.show()
    app.exec_()
    sys.exit( app.exec_() )

