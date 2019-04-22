import time

import RPi.GPIO as GPIO

import board
import busio
from PyQt5.QtCore import QObject, pyqtSignal, QRunnable, pyqtSlot
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import neopixel

nothing = -1
white = 0
black = 1

class LEDWriter(QObject):
    def __init__(self):
        super(LEDWriter, self).__init__()
        self.pixel_pin = board.D18
        self.num_pixels = 64
        self.ORDER = neopixel.GRB
        self.pixels = neopixel.NeoPixel(self.pixel_pin, self.num_pixels, brightness=0.2, auto_write=False, pixel_order=self.ORDER)

    def led_index(self, raw_index):
        #only change for odd rows
        if(raw_index % 16 >= 8):
            row = raw_index//8
            add_index = 8 * (row+1) - 1 - raw_index
            led_index = 8*row + add_index
            return led_index
        else:
            return raw_index

    def write_leds(self, color, indices):
        for index in indices:
            print(self.led_index(index))
            self.pixels[self.led_index(index)] = color
        self.pixels.show()

    def clear_leds(self ):
        self.pixels.fill((0, 0, 0))
        self.pixels.show()
        
class SensorRead(QObject):

    new_physical_board_state = pyqtSignal(list)
    
    def __init__(self):
        super(SensorRead, self).__init__()
        
        # Create the I2C bus
        i2c = busio.I2C(board.SCL, board.SDA)

        # Create the ADC object using the I2C bus
        ads = ADS.ADS1015(i2c)

        # Create single-ended input on channel 1 and 2
        chan_0 = AnalogIn(ads, ADS.P0)     
        chan_1 = AnalogIn(ads, ADS.P1)

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

    def read_sensors_demo(self):
        for i in range(4):
            #mux inputs
            print ("currently checking :", i)
            if 0 <= i and i <= 2:
                control_mux(i)
                time.sleep(0.05)
                t_end = time.time() + 0.01
                avg_value = 0
                count = 0
                while time.time() < t_end:
                    avg_value += chan_0.value
                    count += 1
                    print(count)
                    current_value = avg_value/count
                    print(current_value) 
                    x = interpret(current_value)
                    print(x)
                    current_state[i] = x
                    print_value(x)
                    #adc input
            else:
                t_end = time.time() + 0.01
                avg_value = 0
                count = 0
                while time.time() < t_end:
                    avg_value += chan_1.value
                    count += 1
                    print(count)
                    current_value = avg_value/count
                    x = interpret(current_value)
                    current_state[i] = x
                    print(current_value)
                    print(x)
                    print_value(x)
                    print("\n")
                    time.sleep(0.5)

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

    new_physical_board_state = pyqtSignal(list)
    
    def __init__(self):
        super().__init__()
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
    
    @pyqtSlot()
    def read_sensors(self):
        if self.state_index < len(self.state):
            self.new_physical_board_state.emit(self.state[self.state_index])
            self.state_index += 1
