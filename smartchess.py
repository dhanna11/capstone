#!/usr/bin/python3
import sys
# Need when run as sudo
sys.path.append("/home/pi/.local/lib/python3.5/site-packages/")
import chess
import chess.engine
import chess.svg
import queue
import time
from PyQt5.QtWidgets import QApplication, QLineEdit
from PyQt5.QtSvg import QSvgWidget, QSvgRenderer
from PyQt5.QtCore import QXmlStreamReader, pyqtSignal, QObject, pyqtSlot, QThread, QTimer
from sensor_read import SensorReadMock, LEDWriter


nothing = -1
white = 0
black = 1

def BoardChangeToSourceSquare(newboardArray, oldboardArray):
    assert (len(newboardArray) == len(oldboardArray))
    assert (len(newboardArray) == 64)

    for i in range(64):
        if (newboardArray[i] == nothing) and (oldboardArray[i] != nothing):
            return i
        # should find a difference. Error out if not
    assert (false)

def interpreteBoardChange(newboardArray, oldboardArray):
    assert (len(newboardArray) == len(oldboardArray))
    dest_square = None
    source_square = None
    for i in range(len(newboardArray)):
        # Castling handled as rook captures own piece
        if ((newboardArray[i] != nothing) and (oldboardArray[i] == nothing)):
            # white or black move
            dest_square = i
        elif (newboardArray[i] == white) and (oldboardArray[i] == black):
            # black capture
            dest_square = i
        elif (newboardArray[i] == black) and (oldboardArray[i] == white):
            # white capture
            dest_square = i
        elif (newboardArray[i] == nothing) and (oldboardArray[i] != nothing):
            # new blank place implies source.
            # TODO: May break en_pasante captures?
            source_square = i
        else:
            assert (newboardArray[i] == oldboardArray[i])

    return (source_square, dest_square)

# White upper case, 1. Black lowercase, 0
# Blank negative -1
# Order matters
# FEN record starts from rank 8 and ends with rank 1
# and from file "a" to file "h"
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
    
    def __init__(self, gui: QSvgWidget, isMultiplayer: bool = False, stockfishTime: float = 0.100):
        super().__init__()
        self.gui = gui
        self.ledWriter = LEDWriter()
        self.isMultiplayer = isMultiplayer
        self.board = chess.Board()
        self.catchUpRequired = False
        self.stockfishTime = stockfishTime
        xml = QXmlStreamReader()
        xml.addData(chess.svg.board(board=self.board))
        self.gui.renderer().load(xml)
        
    def on_new_physical_board_state(self, newboardArray):
        oldboardArray = convertFENToTernaryList(self.board.fen())
        (source_square, dest_square) = interpreteBoardChange(newboardArray, oldboardArray)
        # If stockfish or remote player makes a move, the local player needs to manipulate the
        # board to match the current state
        if self.catchUpRequired:
            if (source_square is not None and dest_square is None):
                self.on_piece_selected_catchup(source_square)
            elif (source_square is not None and dest_square is not None):
                self.on_piece_placed_catchup(chess.Move(source_square, dest_square))
        else:
            if (source_square is not None and dest_square is None):
                self.on_piece_selected(source_square)
            elif (source_square is not None and dest_square is not None):
                self.on_piece_placed(chess.Move(source_square, dest_square))

    def on_piece_selected_catchup(self, source_square):
        if (source_square == self.board.peek().from_square):
            # TODO: Light up LED of to_square
            pass
        else:
            print("Error! Picked up wrong piece")

    def on_piece_placed_catchup(self, move):
        if (move.from_square == self.board.peek().from_square) and (move.to_square == self.board.peek().to_square):
            self.catchUpRequired = False
            # TODO: Smart clock manipulation?
        else:
            print("Error! Picked up wrong piece")
            
    def on_piece_selected(self, source_square):
        squares = chess.SquareSet()
        for move in self.board.legal_moves:
            if move.from_square == source_square:
                squares.add(move.to_square)
        # draw a circle by drawing an arrow
        arrows = [
            chess.svg.Arrow(
                source_square, source_square, color="black")
        ]
        xml = QXmlStreamReader()                
        xml.addData(chess.svg.board(board=self.board, squares=squares,
            arrows=arrows))
        self.gui.renderer().load(xml)
        self.ledWriter.write_leds((255,255,0), list(squares))
        
    def on_piece_placed(self, move):
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
            result = engine.play(self.board, chess.engine.Limit(time=self.stockfishTime))
            engine.quit()
            self.board.push(result.move)
            self.ledWriter.clear_leds()
            self.catchUpRequired = True
            xml = QXmlStreamReader()
            xml.addData(chess.svg.board(board=self.board))
            self.gui.renderer().load(xml)
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
        self.show()

class SmartChess():
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.coreGame = CoreGame(SmartChessGui())
        self.sensorRead = SensorReadMock()
        self.sensorRead.add_new_physical_board_state_slot(self.coreGame.on_new_physical_board_state)
        self.timer = QTimer()
        self.timer.timeout.connect(self.sensorRead.read_sensors)
        self.timer.start(1000)        
        sys.exit(self.app.exec_())

def main():
    smartChess = SmartChess()

if __name__ == "__main__":
    main()
