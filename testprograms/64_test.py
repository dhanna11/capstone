import time

import RPi.GPIO as GPIO

import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

#GPIO.setmode(GPIO.BOARD)
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
    #print("inside interpret")
    #print(voltage)
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

current_state = [nothing, nothing, nothing, nothing, nothing, nothing, nothing, nothing,
                 nothing, nothing, nothing, nothing, nothing, nothing, nothing, nothing,
                 nothing, nothing, nothing, nothing, nothing, nothing, nothing, nothing,
                 nothing, nothing, nothing, nothing, nothing, nothing, nothing, nothing,
                 nothing, nothing, nothing, nothing, nothing, nothing, nothing, nothing,
                 nothing, nothing, nothing, nothing, nothing, nothing, nothing, nothing,
                 nothing, nothing, nothing, nothing, nothing, nothing, nothing, nothing,
                 nothing, nothing, nothing, nothing, nothing, nothing, nothing, nothing]


def print_value(y):
    if y == nothing:
        print("nothing ", end ='')
    elif y == black:
        print("black ", end ='')
    elif y == white:
        print("white ", end ='')

while True:
    #sweep through inputs on mux
    time.sleep(1)
    for i in range(8):
        control_row_mux(i)
        for j in range(8):
            #mux inputs
            #print ("currently checking :", 8*i + j)
        
            control_col_mux(j)
            #time.sleep(0.05)
            t_end = time.time() + 0.01
            avg_value = 0
            count = 0
            while time.time() < t_end:
                avg_value += chan_0.value
                count += 1
                #print(count)
            current_value = avg_value/count
            #print(current_value) 
            x = interpret(current_value)
            #print(x)
            current_state[8*i + j] = x
            #print_value(x)
            #print("\n")
    print("\n")
    print ("current state of board:")
    for i in range(64):
        if i%8 == 0:
            print("\n")
        print_value(current_state[i])
    print("\n")
    #time.sleep(2)
            
    
            


