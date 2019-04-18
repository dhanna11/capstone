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

nothing = 0
white = 1
black = 2

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

def read(channel):
    if channel == 0:
        return interpret(chan_0.value)
        #return x
    elif channel == 1:
        return interpret(chan_1.value)
        #return x
    elif channel == 2:
        return interpret(chan_2.value)
        #return x
    elif channel == 3:
        return interpret(chan_3.value)
        #return x
    else:
        print ("wrong channel value for read")

#current_state = [nothing, nothing, nothing, nothing]


#function to control based on number input (0-7)
def control_mux(x):
    if x & 1 == 1:
        GPIO.output(13, True)
    else:
        GPIO.output(13, False)
    print("got here")
    print(x)
    print(x&1)
    if x & 2 == 2:
        GPIO.output(19, True)
        print("setting 19 to true")
    else:
        GPIO.output(19, False)
        print("setting 19 to false")
    if x & 4 == 4:
        GPIO.output(26, True)
        print("setting 26 to true")
    else:
        GPIO.output(26, False)
        print("setting 26 to false")


def print_value(y):
    if y == nothing:
        print("nothing ", end ='')
    elif y == black:
        print("black ", end ='')
    elif y == white:
        print("white ", end ='')


while True:
    control_mux(0)
    print("{:>5}\t{:>5.3f}".format(chan_0.value, chan_0.voltage))
    time.sleep(0.5)
