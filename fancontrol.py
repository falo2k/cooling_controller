# -*- coding: utf-8 -*-
from gpiozero import PWMLED, CPUTemperature, Button
import logging
import time

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

FAN_PIN='GPIO13'
FAN_FREQ=25
TACH_PIN='GPIO6'

rpm = 0
t = time.time()

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
        logging.info("CPU: {0}°C Fan Speed: {1}% RPM: {2}".format(round(cpu.temperature, 1), fan.value * 100., round(rpm, 1)))

        time.sleep(5)

except KeyboardInterrupt: # trap a CTRL+C keyboard interrupt
    print('Fan Control Sent SIGINT')
