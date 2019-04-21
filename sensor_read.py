import time

import RPi.GPIO as GPIO

import board
import busio
from PyQt5.QtCore import QObject, pyqtSignal, QRunnable, pyqtSlot
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

nothing = -1
white = 0
black = 1

class SensorRead(QObject):
        
    def __init__(self):
        super(SensorRead, self).__init__()
        self.new_physical_board_state = pyqtSignal(list)
        
        # Create the I2C bus
        i2c = busio.I2C(board.SCL, board.SDA)

        # Create the ADC object using the I2C bus
        ads = ADS.ADS1015(i2c)

        # Create single-ended input on channel 0
        chan_0 = AnalogIn(ads, ADS.P0)     

        #row pins
        GPIO.setup(13, GPIO.OUT)
        GPIO.setup(19, GPIO.OUT)
        GPIO.setup(26, GPIO.OUT)

        #column pins
        GPIO.setup(16, GPIO.OUT)
        GPIO.setup(20, GPIO.OUT)
        GPIO.setup(21, GPIO.OUT)
            
    def interpret(voltage):
        if 315 <= voltage and voltage <= 750:
            #print ("nothing")
            return nothing
        elif voltage < 315:
            #print("white")
            return white
        elif 750 < voltage:
            #print ("black")
            return black


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

    def print_value(y):
        if y == nothing:
            print("nothing ", end ='')
        elif y == black:
            print("black ", end ='')
        elif y == white:
            print("white ", end ='')

    def add_new_physical_board_state_slot(self, slot):
        self.new_physical_board_state.connect(slot)
        
    def read_sensors(self):
        new_physical_board_state = []
        #sweep through inputs on mux
        for i in range(8):
            control_row_mux(i)
            for j in range(8):
                control_col_mux(j)
                x = interpret(chan_0.value)
                new_physical_board_state.append(x)
                
        self.new_physical_board_state.emit(new_physical_board_state)
        
class SensorReadMock(QObject):
    
    def __init__(self):
        super().__init__()
        self.new_physical_board_state = pyqtSignal(list)
        self.state_index = 0;
        self.state = [
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
        
    def add_new_physical_board_state_slot(self, slot):
        self.new_physical_board_state.connect(slot)
    
    @pystSlot()
    def read_sensors(self):
        self.new_physical_board_state.emit(self.state[self.state_index])
        self.state_index += 1
