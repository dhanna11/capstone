#!/usr/bin/python3

import chess
import chess.svg
import queue
import sys

from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtSvg import QSvgWidget, QSvgRenderer
from PyQt5.QtCore import QXmlStreamReader



# white 1. Black 0
# Blank -1                

    
game_event_q = queue.Queue()
game_msg_event_q = queue.Queue()

board = chess.Board()

def gameLoop():
    try:
        event = event_q.get()
    except queue.Empty: 
        pass
    else:
        if isinstance(event, Event.PIECE_MOVED):
            oldboardArray = convertFENToTernaryList(board.fen())
            newboardArray = event.newboardArray
            print(oldboardArray)
            print(newboardArray)
            move = BoardChangeToMove(newboardArray, oldboardArray)
            print(move)
            if move in board.legal_moves:
                board.push(move)
            else:
                print("Illegal move detected")

            xml = QXmlStreamReader()
            xml.addData(chess.svg.board(board=board))
            
# white 1. Black 0
# Blank -1                
def main():
    app = QApplication(sys.argv)
    svgWidget = QSvgWidget()
    svgWidget.renderer().load("temp.svg")
    svgWidget.show()
    tempboardArray = [ 1, 1, 1, 1, 1, 1, 1, 1,
                       1, 1, 1, 1, 1, 1, 1,-1,
                      -1,-1,-1,-1,-1,-1,-1,-1,
                      -1,-1,-1,-1,-1,-1,-1, 1, 
                      -1,-1,-1,-1,-1,-1,-1,-1, 
                      -1,-1,-1,-1,-1,-1,-1,-1,
                       0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0]
    
    tempEvent = Event.PIECE_MOVED(newboardArray=tempboardArray)
    event_q.put(tempEvent)
    gameLoop()
    sys.exit( app.exec_() )

if __name__ == "__main__":
    main()
