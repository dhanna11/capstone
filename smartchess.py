#!/usr/bin/python3

import chess
import chess.svg
import queue
import sys

from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtSvg import QSvgWidget, QSvgRenderer

# https://github.com/jromang/picochess/blob/master/dgt/api.py
# Use event-driven API
class BaseClass(object):

    def __init__(self, classtype):
        self._type = classtype

    def __repr__(self):
        return self._type

    def __hash__(self):
        return hash(str(self.__class__) + ": " + str(self.__dict__))

def ClassFactory(name, argnames,BaseClass=BaseClass):
    """Class factory for generating."""
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            # here, the argnames variable is the one passed to the ClassFactory call
            if key not in argnames:
                raise TypeError("argument {} not valid for {}".format(key, self.__class__.__name__))
            setattr(self, key, value)
        BaseClass.__init__(self, name)

    newclass = type(name, (BaseClass,), {"__init__": __init__})
    return newclass

class EventApi():
    PIECE_MOVED = 'EVT_PIECE_MOVED'

class Event():
    PIECE_MOVED = ClassFactory(EventApi.PIECE_MOVED, ['move'])

event_q = queue.Queue()
board = chess.Board()

def gameLoop():
    try:
        event = event_q.get()
    except queue.Empty: 
        pass
    else:
        if isinstance(event, Event.PIECE_MOVED):
            
        
    
def main():
    app = QApplication(sys.argv)
    svgWidget = QSvgWidget()
    svgWidget.renderer().load("temp.svg")
    svgWidget.show()
    sys.exit( app.exec_() )

if __name__ == "__main__":
    main()
