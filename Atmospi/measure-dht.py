#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import time
import dhtreader
import sqlite3 as lite

# Import settings.
try:
    from settings import settings
except ImportError:
    from default_settings import settings

# Define the sensor types (AM2302 is a DHT22 in an enclosure).
DHT11 = 11
DHT22 = 22
AM2302 = 22

# Initialize the dhtreader.
dhtreader.init()

# Function definition for reading the sensors.
def read_sensors():
    readings = {}

    # Iterate through the devices.
    for device in settings['dht_devices']:

        # Read the temperature and humidity from the device.
        #tc, h = dhtreader.read(device['type'], device['pin'])
        tc, h = dhtreader.read(22, 22)

        # Convert celsius to fahrenheit.
        tf = tc * 9.0 / 5.0 + 32.0

        # Add the measurements to the readings array.
        readings[device] = {'H': h, 'C': tc, 'F': tf}

    # Return the list of devices and their readings.
    return readings

try:
    con = lite.connect(settings['db'])
    db = con.cursor()

    # Get the current timestamp as an integer.
    timestamp = int(time.time())

    # Gather the temperature readings from all devices.
    readings = read_sensors()

    # Iterate through the devices.
    for device, data in readings.items():

        # Record the humidity to the database.
        db.execute("INSERT INTO Humidity VALUES('" + device + "', " + str(timestamp) + ", " + str(data['H']) + ")")

        # Record the temperature to the database.
        db.execute("INSERT INTO Temperature VALUES('" + device + "', " + str(timestamp) + ", " + str(data['C']) + ", " + str(data['F']) + ")")

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
