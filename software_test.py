#!/usr/bin/python3
import time
import smartchess

nothing = -1
white = 0
black = 1

state = [
        [
        1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1,
       -1,-1,-1,-1,-1,-1,-1,-1,
       -1,-1,-1,-1,-1,-1,-1,-1,
       -1,-1,-1,-1,-1,-1,-1,-1,
       -1,-1,-1,-1,-1,-1,-1,-1,
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0
    ],
        [
        1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1,-1,
       -1,-1,-1,-1,-1,-1,-1,-1,
       -1,-1,-1,-1,-1,-1,-1,-1,
       -1,-1,-1,-1,-1,-1,-1,-1,
       -1,-1,-1,-1,-1,-1,-1,-1,
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0
    ],
        [
        1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1,-1,
       -1,-1,-1,-1,-1,-1,-1,-1,
       -1,-1,-1,-1,-1,-1,-1, 1,
       -1,-1,-1,-1,-1,-1,-1,-1,
       -1,-1,-1,-1,-1,-1,-1,-1,
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0
    ]
]

class SensorMock(QObject):
    
    piece_selected = pyqtSignal(list)
    piece_placed = pyqtSignal(list)
    
    def __init__(self, coreGame):
        self.coreGame = coreGame

    def add_piece_selected_slot(self, slot):
        self.piece_selected.connect(slot)

    def add_piece_placed_slot(self, slot):
        self.piece_placed.connect(slot)
    
    def state_logic(self, i, j, prev_state, new_state):
        if prev_state == nothing and (new_state == black or new_state == white):
            print("piece placed 1")
            piece_placed.emit(new_state)
        elif (prev_state == black or prev_state == white) and new_state == nothing:
            print("piece selected")
            piece_selected.emit(new_state)
        elif (prev_state == black and new_state == white) or (prev_state == white and new_state == black):
            print("piece placed 2")
            piece_placed.emit(new_state)

    def sensorLoop(self):
        for state_index in range(2):
            for i in range(8):
                for j in range(8):
                    self.state_logic(i, j, state[state_index][i*8 +j], state[state_index + 1][i*8 +j] )

            time.sleep(0.5)
