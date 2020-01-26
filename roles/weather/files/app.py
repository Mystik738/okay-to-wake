#!/usr/bin/python3
# coding: utf8
# "DATASHEET": http://cl.ly/ekot
# https://gist.github.com/kadamski/92653913a53baf9dd1a8
from flask import Flask
import time, json
from datetime import datetime
from sense_hat import SenseHat
import os
import math

app = Flask(__name__)

@app.route('/')
def index():
  sense = SenseHat()

  htemp = 0.0
  ptemp = 0.0
  cputemp = 0.0
  pressure = 0.0
  humidity = 0.0
  r = 4

  for i in range(0,r):
    t = os.popen('/opt/vc/bin/vcgencmd measure_temp')
    cpu = t.read()
    cpu = cpu.replace('temp=','')
    cpu = cpu.replace('\'C\n','')
    cputemp += float(cpu)
    htemp += sense.get_temperature_from_humidity()
    ptemp += sense.get_temperature_from_pressure()
    pressure += sense.get_pressure()
    humidity += sense.get_humidity()

  cputemp = cputemp / r
  pressure = pressure / r
  htemp = htemp / r
  ptemp = ptemp / r
  humidity = humidity / r

  calctemp = 2.027930542 * ptemp - 1.242659026*htemp - 0.1552841127 * cputemp + 7.593930654
  calchum = -4.33469*htemp + 2.67323 * ptemp + 1.61276 * cputemp + 1.93523 * humidity - 12.21333 

  htemp = htemp * 1.8 + 32
  ptemp = ptemp * 1.8 + 32
  cputemp = cputemp * 1.8 + 32
  calctemp = calctemp * 1.8 + 32

  output = """  # HELP temperature
# TYPE temperature gauge
temperature {calctemp}
# HELP pressure 
# TYPE pressure gauge
pressure {pressure}
# HELP humidity
# TYPE humidity gauge
humidity {calchum}"""

  return output.format(calctemp=calctemp, pressure=pressure, calchum=calchum)

@app.route('/metrics')
def metrics():
  sense = SenseHat()

  htemp = 0.0
  ptemp = 0.0
  cputemp = 0.0
  pressure = 0.0
  humidity = 0.0
  r = 4

  for i in range(0,r):
    t = os.popen('/opt/vc/bin/vcgencmd measure_temp')
    cpu = t.read()
    cpu = cpu.replace('temp=','')
    cpu = cpu.replace('\'C\n','')
    cputemp += float(cpu)
    htemp += sense.get_temperature_from_humidity()
    ptemp += sense.get_temperature_from_pressure()
    pressure += sense.get_pressure()
    humidity += sense.get_humidity()

  cputemp = cputemp / r
  pressure = pressure / r
  htemp = htemp / r
  ptemp = ptemp / r
  humidity = humidity / r

  calctemp = 2.027930542 * ptemp - 1.242659026*htemp - 0.1552841127 * cputemp + 7.593930654
  calchum = -4.33469*htemp + 2.67323 * ptemp + 1.61276 * cputemp + 1.93523 * humidity - 12.21333 

  htemp = htemp * 1.8 + 32
  ptemp = ptemp * 1.8 + 32
  cputemp = cputemp * 1.8 + 32
  calctemp = calctemp * 1.8 + 32

  output = """  # HELP temperature
# TYPE temperature gauge
temperature {calctemp}
# HELP pressure 
# TYPE pressure gauge
pressure {pressure}
# HELP humidity
# TYPE humidity gauge
humidity {calchum}"""

  return output.format(calctemp=calctemp, pressure=pressure, calchum=calchum)

if __name__ == '__main__':
  app.run( host='0.0.0.0', port=8000)
