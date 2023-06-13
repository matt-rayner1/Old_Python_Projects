# gamekiller.pyw: monitors current processes and terminates certain (game-focused) processes.

import psutil
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

#!use dict or wordlist for this instead?
#checks if executable is in process list. Terminates if found.
def Terminate_procs():
    for proc in psutil.process_iter(['pid', 'name']):
        if "discord.exe" in (proc.info['name']).lower():
            proc.terminate()
        if "steam.exe" in (proc.info['name']).lower():
            proc.terminate()
        if "battle.net.exe" in (proc.info['name']).lower():
            proc.terminate()
        if "upc.exe" in (proc.info['name']).lower():
            proc.terminate()

#main loop.
while(1==1):
    timestamp = Time_in_sec()
    
    #61200 = 5pm
    if timestamp <= 61200:
        Terminate_procs()
    else:
        exit()

    time.sleep(45)
