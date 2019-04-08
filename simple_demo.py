import time
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

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
    if 500 <= voltage and voltage <= 530:
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
        GPIO.output(0, True)
    elif x & 1 == 0:
        GPIO.output(0, False)
    elif x & 2 == 1:
        GPIO.output(1, True)
    elif x & 2 == 0:
        GPIO.output(1, False)
    elif x & 4 == 1:
        GPIO.output(2, True)
    elif x & 4 == 0:
        GPIO.output(2, False)

current_state = [nothing, nothing, nothing, nothing]
for i in range(4):
    current_state[i] = read(i)

while True:
    #sweep through inputs
    for i in range(4):
        x = read(i)
        print ("currently checking :", i)
        time.sleep(0.5)
        if x != current_state[i]:
            print ("change detected in, ", i)
            current_state[i] = x
            exit()
            

        
    

# Create differential input between channel 0 and 1
#chan = AnalogIn(ads, ADS.P0, ADS.P1)

#print("{:>5}\t{:>5}".format('raw', 'v'))

#while True:
#    print("{:>5}\t{:>5.3f}".format(chan.value, chan.voltage))
#    time.sleep(0.5)
