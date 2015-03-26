#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import glob
import time
import sqlite3 as lite
import re

# Import settings.
try:
    from settings import settings
except ImportError:
    from default_settings import settings

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

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

            # Round all measurements to the precision defined in settings.
            temp_c = round(temp_c, settings['precision'])
            temp_f = round(temp_f, settings['precision'])

            # Get the unique name of the device.
            device = file
            device = re.sub('/sys/bus/w1/devices/', '', device)
            device = re.sub('/w1_slave', '', device)

            # Add the measurement to the temps array.
            temps[device] = {'C': temp_c, 'F': temp_f}
    return temps

try:
    con = lite.connect(settings['db'])
    db = con.cursor()

    # Get the current timestamp as an integer.
    timestamp = int(time.time())

    # Gather the temperature readings from all devices.
    temps = read_temps()

    # Iterate through the devices.
    for device, data in temps.items():

        # Retrieve the device ID from the Devices table.
        db.execute("SELECT DeviceID FROM Devices WHERE Type = 'ds18b20' AND SerialID = '" + device + "'")
        id = db.fetchone()[0]

        # If the ID wasn't found, add it automatically.
        if not id:
          db.execute("INSERT INTO Devices (DeviceID, Type, SerialID, Label) VALUES (NULL, 'ds18b20', " + device + ", " + device + ")")
          id = db.lastrowid

        # Record the temperatures to the database.
        db.execute("INSERT INTO Temperature (DeviceID, Timestamp, C, F) VALUES(" + str(id) + ", " + str(timestamp) + ", " + str(data['C']) + ", " + str(data['F']) + ")")

    # Commit the changes to the database.
    con.commit()

except lite.Error, e:
    if con:
        con.rollback()
    print "Error %s:" % e.args[0]
    sys.exit(1)

finally:
    if con:
        con.close()
