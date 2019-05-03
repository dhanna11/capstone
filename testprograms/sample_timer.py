import time
import datetime


start = datetime.datetime.now()
start_sec = start.second

while(True):
        now = datetime.datetime.now()
        now_sec = now.second
        
        raw_diff = start - now
        print(raw_diff)
        
        seconds_passed = now_sec - start_sec
        print(seconds_passed)
        
        decsecond = raw_diff%0.1
        print(decsecond)
        
        centisecond = raw_diff%0.01
        
        milisecond = raw_diff%
