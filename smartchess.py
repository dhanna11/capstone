#!/usr/bin/python3

import chess
import chess.svg
import queue
import sys

from PyQt5.QtWidgets import QApplication
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

class GameEventApi():
    PIECE_SELECTED = 'EVT_PIECE_MOVED'
    
class GameEvent():
    PIECE_SELECTED = ClassFactory(GameEventApi.PIECE_SELECTED, ['newboardArray'])

class GameMessageApi():
    SELECT_SQUARES = 'SELECT_SQUARES'

class GameMessage():
    SELECT_SQUARES = ClassFactory(GameMessageApi.SELECT_SQUARES, ["squareSet"])



game_event_q = queue.Queue()
board = chess.Board()

class utils():
    def BoardChangeToSourceSquare(newboardArray, oldboardArray):
        assert(len(newboardArray) == len(oldboardArray))
        assert(len(newboardArray) == 64)
    
        for i in range(64):
            if (newboardArray[i] == -1) and (oldboardArray[i] != -1):
                return i
        # should find a difference. Error out if now    
        assert(false)
    
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

    # White upper case, 1. Black lowercase, 0
    # Blank negative -1
    # Order matters
    # FEN record starts from rank 8 and ends with rank 1
    # and from file "a" to file "h"
    def convertFENToTernaryList(fen_str):
        l = []
        fen_str_board = fen_str.split(" ")[0]
        fen_rows = fen_str_board.split("/")
        print(fen_rows)
        for string_row in fen_rows[::-1]:
            for c in string_row:
                print(c)
                if (c.isnumeric()):                
                    l.extend([-1] * int(c))
                elif (c.islower()):
                    l.append(0)
                elif (c.isupper()):
                    l.append(1)

        assert(len(l) == 64)
        return l

class CoreGame():


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
