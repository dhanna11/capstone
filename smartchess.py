#!/usr/bin/python3

import chess
import chess.svg
import queue
import sys

from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtSvg import QSvgWidget, QSvgRenderer
from PyQt5.QtCore import QXmlStreamReader

# Use event-driven API
class BaseClass(object):

    def __init__(self, classtype):
        self._type = classtype

    def __repr__(self):
        return self._type

    def __hash__(self):
        return hash(str(self.__class__) + ": " + str(self.__dict__))

def ClassFactory(name, argnames,BaseClass=BaseClass):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key not in argnames:
                raise TypeError("argument {} not valid for {}".format(key, self.__class__.__name__))
            setattr(self, key, value)
        BaseClass.__init__(self, name)

    newclass = type(name, (BaseClass,), {"__init__": __init__})
    return newclass

def convertFENToTernaryList(fen_str):
    # TODO: Fix me
    l = []
    for c in fen_board_str:
        # white is lowercase
        if (c.islower()):
            l.append(-1)
        # black is uppercase
        elif (c.isupper()):
            l.append(1)
        else:
            l.append(0)
    return l

# -1 is white. 1 is black
def BoardChangeToMove(newboardArray, oldboardArray):
    print(newboardArray)
    for i in range(len(newboardArray)):
        # Castling handled as rook captures own piece
        if ((newboardArray[i] != 0) and (oldboardArray[i] == 0)):
            # move
            dest_square = i       
        elif (newboardArray[i] == -1) and (oldboardArray[i] == 1):
            # black capture
            dest_square = i
        elif (newboardArray[i] == 1) and (oldboardArray[i] == -1):
            # white capture
            dest_square = i
        elif (newboardArray[i] == 0) and (oldboardArray[i] != 0):
            # new blank place implies source. May break en pasante
            source_square = i
        else:
            print("Unhandled board change")
    
    return chess.Move(source_square, dest_square)
    
class EventApi():
    PIECE_MOVED = 'EVT_PIECE_MOVED'

class Event():
    PIECE_MOVED = ClassFactory(EventApi.PIECE_MOVED, ['newboardArray'])

event_q = queue.Queue()
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
            move = BoardChangeToMove(newboardArray, oldboardArray)
            if move in board.legal_moves:
                board.push(move)
            else:
                print("Illegal move detected")

            xml = QXmlStreamReader()
            xml.addData(chess.svg.board(board=board))
            
def main():
    app = QApplication(sys.argv)
    svgWidget = QSvgWidget()
    svgWidget.renderer().load("temp.svg")
    svgWidget.show()
    tempboardArray = [-1,-1,-1,-1,-1,-1,-1,-1
                      -1,-1,-1,-1,-1,-1,-1,-1,
                       0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0,
                       1, 1, 1, 1, 1, 1, 1, 1,
                       1, 1, 1, 1, 1, 1, 1, 1]
    
    tempEvent = Event.PIECE_MOVED(newboardArray=tempboardArray)
    event_q.put(tempEvent)
    gameLoop()
    sys.exit( app.exec_() )

if __name__ == "__main__":
    main()
