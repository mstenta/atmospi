#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import glob
import time
import datetime
import sqlite3 as lite
import re
from RPi import GPIO

os.system('/sbin/modprobe w1-gpio')
os.system('/sbin/modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folders = glob.glob(base_dir + '28*')
device_files = []
i = 0
for folder in device_folders:
    device_files.append(device_folders[i] + '/w1_slave')
    i += 1


def read_temp_raw(file):
    f = open(file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temps():
    temps = {}
    for file in device_files:
        lines = read_temp_raw(file)
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.5)
            lines = read_temp_raw(file)
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0

            # Round all measurements to the nearest degree.
            temp_c = round(temp_c)
            temp_f = round(temp_f)

            # Get the unique name of the device.
            device = file
            device = re.sub('/sys/bus/w1/devices/', '', device)
            device = re.sub('/w1_slave', '', device)

            # Add the measurement to the temps array.
            temps[device] = {'C': temp_c, 'F': temp_f}
    return temps


def log(msg):
    print datetime.datetime.now(), msg


def pin_setup(pin):

    # Turn off warnings.
    GPIO.setwarnings(False)
    
    # Use BCM GPIO pin numbering.
    GPIO.setmode(GPIO.BCM)

    # Set the GPIO mode to "out" on the relay pin.
    GPIO.setup(pin, GPIO.OUT)


def pin_on(pin):

    # Turn on the pin.
    GPIO.output(pin, 1)


def pin_off(pin):
    
    # Turn off the pin.
    GPIO.output(pin, 0)


def thermostat(threshold, pin):

    # Set up the pin.
    pin_setup(pin)

    # Get all temperature readings.
    readings = read_temps()

    # Define the DS18B20 ID that we're looking for.
    deviceid = '28-00000a00532d' 

    # Turn the pin off if we don't have a reading.
    if deviceid not in readings or 'F' not in readings[deviceid]:
        log('Reading not found. Pin: OFF')
        pin_off(pin)
        return

    # Get the temperature from the device.
    temp = readings[deviceid]['F']

    # Log the temperature.
    log(temp)

    # If there is no temperature, bail.
    if not temp:
        log('Temperature was invalid (' + str(temp) + '). Pin: OFF')
        pin_off(pin)
        return

    # If the temperature is below the threshold, turn on the pin. 
    if temp < threshold:
        pin_on(pin)
        log('Temperature below threshold (' + str(threshold) + '). Pin: ON')
        
    # Otherwise, turn it off.
    else:
       pin_off(pin)
       log('Temperature above threshold (' + str(threshold) + '). Pin: OFF')


# Run the thermostat() function.
threshold = 62
relay_pin = 25
thermostat(threshold, relay_pin)

