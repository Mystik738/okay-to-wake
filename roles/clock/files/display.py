#!/usr/bin/env python

# Needs to be set as a cron job:
# * * * * * python /var/www/html/display.py
from sense_hat import SenseHat
import time
import os
import json
from datetime import datetime

def add_time_to_today(time_param):
        result = datetime.now()
        result = result.replace(hour=time_param.hour,minute=time_param.minute,second=time_param.second)
        return result

#Get our times
dir_path = os.path.dirname(os.path.realpath(__file__))
now = datetime.now()

#see the difference in times, in seconds
elapsedTime = 0

#Get our times
dir_path = os.path.dirname(os.path.realpath(__file__))
with open(dir_path + '/time.txt') as json_file:
        intervals = json.load(json_file)
        in_interval = False
        now = datetime.now()
        otwtime = datetime.strptime(intervals['time'],'%Y-%m-%d %H:%M:%S')
        elapsedTime = otwtime - now
        for interv in intervals['schedule']:
                stime = add_time_to_today(datetime.strptime(interv[0], '%H:%M'))
                etime = add_time_to_today(datetime.strptime(interv[1], '%H:%M'))
                if now >= stime and now <= etime:
                        in_interval = True
                        break

sense = SenseHat()

#set the default color to green
c = [0,96,0]
#If we're before alarm time, turn red
if intervals['use_schedule']:
    #If we're in an interval, turn red
    if in_interval:
        c = [96,0,0]
else:
    if now <= otwtime:
        c = [96,0,0]
  
#Compare with our current pixels
pixel_list = sense.get_pixels()
p = pixel_list[0]
if p[0] != c[0] or p[1] != c[1] or p[2] != c[2]:
    
    #Clear the last image
    sense.clear()
    
    #Set the new image to our screen
    img = [
      c,c,c,c,c,c,c,c,
      c,c,c,c,c,c,c,c,
      c,c,c,c,c,c,c,c,
      c,c,c,c,c,c,c,c,
      c,c,c,c,c,c,c,c,
      c,c,c,c,c,c,c,c,
      c,c,c,c,c,c,c,c,
      c,c,c,c,c,c,c,c
      ]
    
    sense.set_pixels(img)
