import time
import datetime

from Adafruit_LED_Backpack import SevenSegment

#segment display intialization
segment = SevenSegment.SevenSegment(address=0x70)
segment.begin()

raw_start = time.time()
#raw_start_str = str(raw_start)
#print(raw_start_str)
#start_str = raw_start_str.split(":")
#second_str = start_str[-1]
#print(second_str)


while(True):
    now = time.time()
    #now_str = str(now)
    #print(now_str)
    #now_second_str = now_str.split(":")
    #now_second = now_second_str[-1]
    #print(now_second)
    
    diff = now - raw_start
    print(diff)
    
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
    segment.set_colon(now % 2)             

    # Write the display buffer to the hardware.  This must be called to
    # update the actual display LEDs.
    segment.write_display()

    # Wait a quarter second (less than 1 second to prevent colon blinking getting$
    #time.sleep(0.25)
