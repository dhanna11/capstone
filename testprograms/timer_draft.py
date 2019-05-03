import time
import datetime

from Adafruit_LED_Backpack import SevenSegment

#segment display intialization
segment = SevenSegment.SevenSegment(address=0x70)
segment.begin()

raw_start = datetime.datetime.now()
raw_start_str = str(raw_start)
#print(raw_start_str)
start_str = raw_start_str.split(":")
second_str = start_str[-1]
#print(second_str)


while(True):
    now = datetime.datetime.now()
    now_str = str(now)
    #print(now_str)
    now_second_str = now_str.split(":")
    now_second = now_second_str[-1]
    #print(now_second)
    
    diff = float(now_second) - float(second_str)
    print(diff)
    
    if diff < 0:
        print("ERROR")
        print("current time: " + str(now))
        print("start time: " + str(raw_start))
        print("current second" + now_second)
        print("start second: " + second_str)
        break
    
    if diff < 10:
        #print(diff)
        diff_str = str(diff)
        list_diff = list(diff_str)
        d_two = list_diff[0]
        d_three = list_diff[2]
        d_four = list_diff[3]
    else:
        diff_str = str(diff)
        list_diff = list(diff_str)
        d_one = list_diff[0]
        d_two = list_diff[1]
        d_three = list_diff[3]
        d_four = list_diff[4]
        
    

    segment.clear()
    if diff >= 10:
        segment.set_digit(0, d_one)        # Tens
    segment.set_digit(1, d_two)     # Ones

    segment.set_digit(2, d_three)   
    segment.set_digit(3, d_four)        
    # Toggle colon
    segment.set_colon(now.second % 2)             

    # Write the display buffer to the hardware.  This must be called to
    # update the actual display LEDs.
    segment.write_display()

    # Wait a quarter second (less than 1 second to prevent colon blinking getting$
    #time.sleep(0.25)