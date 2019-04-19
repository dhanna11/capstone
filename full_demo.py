import time

import RPi.GPIO as GPIO

import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

import smartchess

class sensorRead(QObject):
    
    piece_selected = pyqtSignal(list)
    piece_placed = pyqtSignal(list)
    
    def __init__(self, coreGame):
        self.coreGame = coreGame

    def add_piece_selected_slot(self, slot):
        self.piece_selected.connect(slot)

    def add_piece_placed_slot(self, slot):
        self.piece_placed.connect(slot)
    
    #GPIO.setmode(GPIO.BOARD)
    #row pins
    GPIO.setup(13, GPIO.OUT)
    GPIO.setup(19, GPIO.OUT)
    GPIO.setup(26, GPIO.OUT)

    #column pins
    GPIO.setup(16, GPIO.OUT)
    GPIO.setup(20, GPIO.OUT)
    GPIO.setup(21, GPIO.OUT)

    # Create the I2C bus
    i2c = busio.I2C(board.SCL, board.SDA)

    # Create the ADC object using the I2C bus
    ads = ADS.ADS1015(i2c)

    # Create single-ended input on channel 0
    chan_0 = AnalogIn(ads, ADS.P0) 
    chan_1 = AnalogIn(ads, ADS.P1)
    chan_2 = AnalogIn(ads, ADS.P2)
    chan_3 = AnalogIn(ads, ADS.P3)

    nothing = -1
    white = 0
    black = 1

    def interpret(voltage):
        if 315 <= voltage and voltage <= 730:
            #print ("nothing")
            return nothing
        elif voltage <= 310:
            #print("white")
            return white
        elif 750 < voltage:
            #print ("black")
            return black
        #else:
         #   print ("error")


    #function to control based on number input (0-7)
    def control_row_mux(x):
        if x & 1 == 1:
            GPIO.output(13, True)
        else:
            GPIO.output(13, False)
        if x & 2 == 2:
            GPIO.output(19, True)
        else:
            GPIO.output(19, False)
        if x & 4 == 4:
            GPIO.output(26, True)
        else:
            GPIO.output(26, False)
            
    def control_col_mux(x):
        if x & 1 == 1:
            GPIO.output(16, True)
        else:
            GPIO.output(16, False)
        if x & 2 == 2:
            GPIO.output(20, True)
        else:
            GPIO.output(20, False)
        if x & 4 == 4:
            GPIO.output(21, True)
        else:
            GPIO.output(21, False)

    board_current_state = []

    for i in range(64):
        board_current_state.append(nothing)


    def print_value(y):
        if y == nothing:
            print("nothing ", end ='')
        elif y == black:
            print("black ", end ='')
        elif y == white:
            print("white ", end ='')
            
    def state_logic(i, j, piece_prev_state, piece_new_state):
        board_current_state[i*8 + j] = new_piece_state
        if (piece_prev_state == nothing
            and (piece_new_state == black or piece_new_state == white)):
            piece_placed.emit(board_current_state)
        elif ((piece_prev_state == black or piece_prev_state == white)
              and piece_new_state == nothing):
            piece_selected.emit(board_current_state)
        elif ((piece_prev_state == black and piece_new_state == white)
              or (piece_prev_state == white and piece_new_state == black)):
            piece_placed.emit(board_current_state)
            
    def read_sensors():
        while True:
            #sweep through inputs on mux
            for i in range(8):
                control_row_mux(i)
                for j in range(8):
                    control_col_mux(j)
                    x = interpret(chan_0.value)
                    self.state_logic(i, j, board_current_state[i*8 +j], x)

            print ("current state of board:")
            for i in range(64):
                print_value(board_current_state[i])
                if i % 8 == 7:
                    print("\n")
            time.sleep(0.5)
                
        
                

