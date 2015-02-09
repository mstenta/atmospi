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
sensor_types = {
    'dht11': 11,
    'dht22': 22,
    'am2302': 22
}

# Initialize the dhtreader.
dhtreader.init()

# Function definition for reading a sensor.
def read_sensor(type, pin):

    # Read the temperature and humidity from the device.
    tc, h = dhtreader.read(sensor_types[type], int(pin))

    # Convert celsius to fahrenheit.
    tf = tc * 9.0 / 5.0 + 32.0

    # Round all measurements to the precision defined in settings.
    tc = round(tc, settings['precision'])
    tf = round(tf, settings['precision'])
    h = round(h, settings['precision'])

    # Format the reading data.
    reading = {'H': h, 'C': tc, 'F': tf}

    # Return the reading.
    return reading

try:
    con = lite.connect(settings['db'])
    db = con.cursor()

    # Retrieve the list of DHT devices from the database.
    db.execute("SELECT DeviceID, Type, SerialID FROM Devices WHERE Type IN ('dht22', 'dht11', 'am2302')")
    devices = db.fetchall()
    for device in devices:

        # Get the current timestamp as an integer.
        timestamp = int(time.time())

        # Gather sensor data.
        data = read_sensor(device[1], device[2])

        # Record the humidity to the database.
        db.execute("INSERT INTO Humidity (DeviceID, Timestamp, H) VALUES(" + str(device[0]) + ", " + str(timestamp) + ", " + str(data['H']) + ")")

        # Record the temperature to the database.
        db.execute("INSERT INTO Temperature (DeviceID, Timestamp, C, F) VALUES(" + str(device[0]) + ", " + str(timestamp) + ", " + str(data['C']) + ", " + str(data['F']) + ")")

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
