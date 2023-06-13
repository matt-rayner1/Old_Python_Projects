#force shutdown  at 9pm
import os
import time
import re

#!find a more elegant solution for this
#get the total seconds that have passed today
def Time_in_sec():
    datetime_vals = re.search(r"(\w{3})\s(\w{3})\s(\d+)\s(\d\d:\d\d:\d\d)", time.ctime())
    time_str = datetime_vals[4] 
    
    time_hms = time_str.split(':')
    time_hms = [int(i) for i in time_hms]
    
    time_sec = (time_hms[0] * 3600) + (time_hms[1] * 60) + (time_hms[2])
    return time_sec

#shut down computer if timestamp > 75600 (9pm)
def Check_past_time():
    timestamp = Time_in_sec()

    #75600: 9pm
    if timestamp >= 75600:
        os.system("shutdown /s")
        exit()

while(1==1):
    Check_past_time()
    time.sleep(60)
