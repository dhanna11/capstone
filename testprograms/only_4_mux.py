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
    print("inside interpret")
    print(voltage)
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
def control_mux(x):
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

current_state = [nothing, nothing, nothing, nothing]


def print_value(y):
    if y == nothing:
        print("nothing ", end ='')
    elif y == black:
        print("black ", end ='')
    elif y == white:
        print("white ", end ='')

while True:
    #sweep through inputs on mux
    for i in range(2):
        #mux inputs
        print ("currently checking :", i)
        if i==0:
            control_mux(i)
            time.sleep(0.05)
            t_end = time.time() + 0.01
            avg_value = 0
            count = 0
            while time.time() < t_end:
                avg_value += chan_1.value
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
        #print_value(current_state[i])
        print("\n")
        time.sleep(0.5)

    print ("current state of board:")
    for i in range(4):
        print_value(current_state[i])
        if i == 1 or i == 3:
            print("\n")
    time.sleep(0.5)
            
    
            
