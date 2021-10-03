# -*- coding: utf-8 -*-
from gpiozero import PWMLED, CPUTemperature, Button
import logging
import math
import time

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

FAN_PIN='GPIO13'
FAN_FREQ=25
TACH_PIN='GPIO6'

FAN_OFF_THRESHOLD=43
FAN_MAX_THRESHOLD=55

FAN_LOW_LIMIT=0.05
FAN_POINT_COUNT=30

FAN_SET_POINTS=[FAN_LOW_LIMIT + ((1.-FAN_LOW_LIMIT)*(float(x)/FAN_POINT_COUNT)) for x in range(1,FAN_POINT_COUNT+1)]

rpm = 0
t = time.time()

def get_speed(temperature):
    if temperature <= FAN_OFF_THRESHOLD:
        return 0.
    elif temperature >= FAN_MAX_THRESHOLD:
        return 1.
    else:
        index = int(math.floor((FAN_POINT_COUNT-1) * ((temperature - FAN_OFF_THRESHOLD)/(FAN_MAX_THRESHOLD - FAN_OFF_THRESHOLD))))
        return FAN_SET_POINTS[index]

def tick():
    global rpm
    global t
    dt = time.time() - t
    if dt < 0.005: return
    freq = 1 / dt
    rpm = (freq / 2) * 60
    t = time.time()

fan = PWMLED(pin=FAN_PIN, frequency=FAN_FREQ, initial_value=1.)
cpu = CPUTemperature()
tach = Button(TACH_PIN)
tach.when_pressed = tick

try:
    while True:
        print(get_speed(cpu.temperature))
        logging.info("CPU: {0}°C Fan Speed: {1}% RPM: {2}".format(round(cpu.temperature, 1), fan.value * 100., round(rpm, 1)))
        time.sleep(5)

except KeyboardInterrupt: # trap a CTRL+C keyboard interrupt
    print('Fan Control Sent SIGINT')
