import time
import board
import neopixel

import time

import RPi.GPIO as GPIO

import board
import busio
import sys
print (sys.path)
sys.path.append("/home/pi/.local/lib/python3.5/site-packages/")
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


pixel_pin = board.D18
# The number of NeoPixels
num_pixels = 10
# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False,
                           pixel_order=ORDER)

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

def state_logic(i, prev_state, new_state):
    current_state[i] = new_state 
    if prev_state == nothing and (new_state == black or new_state == white):
        print("piece placed 1")
        pixels.fill((0, 0, 0))
        pixels.show()
        #onPiecePlaced(current_state)
    elif (prev_state == black or prev_state == white) and new_state == nothing:
        print("piece selected")
        pixels[i] = (255,0,0)
        pixels.show()
        #onPieceSelected(current_state)
    elif (prev_state == black and new_state == white) or (prev_state == white and new_state == black):
        print("piece placed 2")
        pixels.fill((0, 0, 0))
        pixels.show()

current_state = [nothing, nothing, nothing, nothing]

while True:
    #sweep through inputs on mux
    for i in range(4):
        #mux inputs
        print ("currently checking :", i)
        if 0 <= i and i <= 2:
            #time.sleep(0.002)
            control_row_mux(i)
            x = interpret(chan_0.value)
            print(chan_0.value)
            if(x != current_state[i]):
                pixels[i] = (255,0,0)
                pixels.show()
                time.sleep(1)
            else:
                pixels.fill((0, 0, 0))
                pixels.show()
            #state_logic(i, current_state[i], x)
        #adc input
        else:
            #time.sleep(1)
            x = interpret(chan_1.value)
            print(chan_1.value)
            if(x != current_state[i]):
                pixels[i] = (255,0,0)
                pixels.show()
                time.sleep(1)
            else:
                pixels.fill((0, 0, 0))
                pixels.show()
                
            #state_logic(i, current_state[i], x)
        print_value(current_state[i])
        print("\n")
        #time.sleep(0.5)

    print ("current state of board:")
    for i in range(4):
        print_value(current_state[i])
        if i == 1 or i == 3:
            print("\n")
    #time.sleep(0.5)
