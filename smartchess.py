#!/usr/bin/python3

import chess
import chess.engine
import chess.svg
import queue
import sys
import time
from PyQt5.QtWidgets import QApplication, QLineEdit
from PyQt5.QtSvg import QSvgWidget, QSvgRenderer
from PyQt5.QtCore import QXmlStreamReader, pyqtSignal, QObject, pyqtSlot

#from sensor_read import sensorRead
from sensor_read_mock import SensorMock
class utils():
    @staticmethod
    def BoardChangeToSourceSquare(newboardArray, oldboardArray):
        assert (len(newboardArray) == len(oldboardArray))
        assert (len(newboardArray) == 64)

        for i in range(64):
            if (newboardArray[i] == -1) and (oldboardArray[i] != -1):
                return i
        # should find a difference. Error out if not
        assert (false)

    @staticmethod
    def BoardChangeToMove(newboardArray, oldboardArray):
        assert (len(newboardArray) == len(oldboardArray))
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
                # new blank place implies source.
                # TODO: May break en_pasante captures?
                source_square = i
            else:
                assert (newboardArray[i] == oldboardArray[i])

        return chess.Move(source_square, dest_square)

    # White upper case, 1. Black lowercase, 0
    # Blank negative -1
    # Order matters
    # FEN record starts from rank 8 and ends with rank 1
    # and from file "a" to file "h"
    @staticmethod
    def convertFENToTernaryList(fen_str):
        l = []
        fen_str_board = fen_str.split(" ")[0]
        fen_rows = fen_str_board.split("/")
        for string_row in fen_rows[::-1]:
            for c in string_row:
                if (c.isnumeric()):
                    l.extend([-1] * int(c))
                elif (c.islower()):
                    l.append(0)
                elif (c.isupper()):
                    l.append(1)

        assert (len(l) == 64)
        return l

class CoreGame(QObject):
    
    def __init__(self, gui: QSvgWidget, isMultiplayer: bool = False, time: float = 0.100):
        super().__init__()
        self.gui = gui
        self.isMultiplayer = isMultiplayer
        self.board = chess.Board()
        self.time = time
        
    @pyqtSlot()
    def on_piece_selected(self, newboardArray):
        oldboardArray = utils.convertFENToTernaryList(self.board.fen())
        source_square = utils.BoardChangeToSourceSquare(
            newboardArray, oldboardArray)
        squareSet = chess.SquareSet()
        for move in self.board.legal_moves:
            if move.from_square == source_square:
                squareSet.add(move.to_square)
        # draw a circle by drawing an arrow
        arrows = [
            chess.svg.Arrow(
                source_square, source_square, color="black")
        ]
        xml = QXmlStreamReader()                
        xml.addData(chess.svg.board(board=self.board, squares=squareSet,
            arrows=arrows))
        self.gui.load(xml)

    @pyqtSlot()
    def on_piece_placed(self, newboardArray):
        oldboardArray = utils.convertFENToTernaryList(self.board.fen())
        move = utils.BoardChangeToMove(newboardArray, oldboardArray)
        if move not in self.board.legal_moves:
            # TODO: Send illegal move Message
            print("illegal move detected")
            return                
        self.board.push(move)
        xml = QXmlStreamReader()
        xml.addData(chess.svg.board(board=self.board))
        # TODO: Refactor using Observer pattern
        self.gui.renderer().load(xml)
                
        if self.board.is_game_over():
            # TODO: Send game over message
            print("Game Over! Player wins")
        if not self.isMultiplayer:
            # Launch stockfish, ask for a move, then terminate. 
            engine = chess.engine.SimpleEngine.popen_uci("/usr/local/bin/stockfish")
            result = engine.play(self.board, chess.engine.Limit(time=self.time))
            engine.quit()
            self.board.push(result.move)
            xml = QXmlStreamReader()
            xml.addData(chess.svg.board(board=self.board))
            if self.board.is_game_over():
                print("Game Over! Stockfish Wins!")
                                
class SmartChessGui(QSvgWidget):
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
        self.textbox = QLineEdit(self)
        self.show()

    def renderXML(self, xml):
        self.gui.renderer().load(xml)
        
        
class SmartChess():
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.coreGame = CoreGame(SmartChessGui())
        self.sensorRead = SensorMock(self.coreGame)
        sys.exit(self.app.exec_())

def main():
    smartChess = SmartChess()

if __name__ == "__main__":
    main()
