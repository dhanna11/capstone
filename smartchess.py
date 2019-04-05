#!/usr/bin/python3

import chess
import chess.svg
import queue
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtSvg import QSvgWidget, QSvgRenderer
from PyQt5.QtCore import QXmlStreamReader
from utils import utils
from api import GameEvent
# white 1. Black 0
# Blank -1                

game_event_q = queue.Queue()
board = chess.Board()

def gameLoop(topWidget):
    try:
        event = game_event_q.get()
    except queue.Empty: 
        pass
    else:
        if isinstance(event, GameEvent.PIECE_SELECTED):
            oldboardArray = utils.convertFENToTernaryList(board.fen())
            newboardArray = event.newboardArray
            print(oldboardArray)
            print(newboardArray)
            source_square = utils.BoardChangeToSourceSquare(newboardArray, oldboardArray)
            print(source_square)
            squares = board.attacks(source_square)
            print(squares)
            xml = QXmlStreamReader()
            for move in board.legal_moves:
                if move.from_square == source_square:
                    squares.add(move.to_square)
            xml.addData(chess.svg.board(board=board, squares=squares))
            topWidget.renderer().load(xml)
            
# white 1. Black 0
# Blank -1                
def main():
    app = QApplication(sys.argv)
    svgWidget = QSvgWidget()
    svgWidget.setGeometry(10,10,640,480)
    svgWidget.show()

    tempboardArray = [ 1, 1, 1, 1, 1, 1, 1, 1,
                       1, 1, 1, 1, 1, 1, 1,-1,
                      -1,-1,-1,-1,-1,-1,-1,-1,
                      -1,-1,-1,-1,-1,-1,-1,-1, 
                      -1,-1,-1,-1,-1,-1,-1,-1, 
                      -1,-1,-1,-1,-1,-1,-1,-1,
                       0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0]
    
    tempEvent = GameEvent.PIECE_SELECTED(newboardArray=tempboardArray)
    game_event_q.put(tempEvent)
    gameLoop(svgWidget)
    sys.exit( app.exec_() )

if __name__ == "__main__":
    main()
