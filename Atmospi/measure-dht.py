#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import time
import Adafruit_DHT
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

# Function definition for reading a sensor.
def read_sensor(type, pin):

    # Read the temperature and humidity from the device.
    h, t = Adafruit_DHT.read_retry(sensor_types[type], int(pin))

    # Round all measurements to the precision defined in settings.
    t = round(t, settings['precision'])
    h = round(h, settings['precision'])

    # Format the reading data.
    reading = {'H': h, 'C': t}

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
        db.execute("INSERT INTO Temperature (DeviceID, Timestamp, C) VALUES(" + str(device[0]) + ", " + str(timestamp) + ", " + str(data['C']) + ")")

    # Commit the changes to the database.
    con.commit()

except lite.Error, e:
    if con:
        con.rollback()
    print('Error querying the database.')
    print(e)
    sys.exit(1)

finally:
    if con:
        con.close()
