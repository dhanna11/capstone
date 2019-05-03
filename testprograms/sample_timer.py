import time
import datetime


raw_start = datetime.datetime.now()
raw_start_str = str(raw_start)
print(raw_start_str)
start_str = raw_start_str.split(":")
second_str = start_str[-1]
print(second_str)


time.sleep(1)

while(True):
    now = datetime.datetime.now()
    now_str = str(now)
    print(now_str)
    now_second_str = now_str.split(":")
    now_second = now_second_str[-1]
    print(now_second)
    break
    

diff = float(now_second) - float(second_str)
print(diff)
diff_str = str(diff)
list_diff = list(diff_str)
d_one = list_diff[0]
d_two = list_diff[2]
d_three = list_diff[3]
d_four = list_diff[4]

print(d_one)
print(d_two)
print(d_three)
print(d_four)

    
    
