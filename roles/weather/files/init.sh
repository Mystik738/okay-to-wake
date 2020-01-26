#!/bin/bash

lines=$(ps aux | grep "python3 /home/pi/app.py" | wc -l)

if [ $lines -lt 2 ]
then
    cd /home/pi 
    { nohup flask run --host=0.0.0.0 --port=8000 & } & 
fi