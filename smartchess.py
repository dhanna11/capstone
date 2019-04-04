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

# White upper case, 1. Black lowercase, 0
# Blank negative -1
def convertFENToTernaryList(fen_str):
    l = []
    fen_str_board = fen_str.split(" ")[0]
    fen_rows = fen_str_board.split("/")
    for string_row in fen_rows:
        for c in string_row:
            if (c.isnumeric()):                
                l.extend([-1] * int(c))
            elif (c.islower()):
                l.append(0)
            elif (c.isupper()):
                l.append(1)

    assert(len(l) == 64)
    return l

# white 1. Black 0
# Blank -1                
def BoardChangeToMove(newboardArray, oldboardArray):
    print(len(newboardArray))
    assert(len(newboardArray) == len(oldboardArray))
    for i in range(len(newboardArray)):
        # Castling handled as rook captures own piece
        if ((newboardArray[i] != -1) and (oldboardArray[i] == -1)):
            # white or black move
            dest_square = i       
        elif (newboardArray[i] == 0) and (oldboardArray[i] == 1):
            # black capture
            dest_square = i
        elif (newboardArray[i] == 1) and (oldboardArray[i] == 0):
            # white capture
            dest_square = i
        elif (newboardArray[i] == -1) and (oldboardArray[i] != -1):
            # new blank place implies source. May break en pasante
            source_square = i
        else:
            assert(newboardArray[i] == oldboardArray[i])
    
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
