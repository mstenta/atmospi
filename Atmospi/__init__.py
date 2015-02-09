#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import json
import db
import data
from flask import Flask
from flask import request
from flask import render_template

# Import settings.
try:
    from settings import settings
except ImportError:
    from default_settings import settings

# Create a new Flask app.
app = Flask(__name__)

# Define the index router item.
@app.route('/')
def index():

    # Return the rendered index.
    return render_template('index.html')

# Define the temperature devices router item.
@app.route('/data/devices/temperature')
def devices_temperature():

    # Select all available device ids.
    rows = db.select("SELECT DeviceID, Label FROM Devices WHERE Type IN ('ds18b20', 'dht22', 'dht11', 'am2302')")

    # Build a dictionary of devices.
    devices = {}
    for row in rows:
        devices[row[0]] = row[1]

    # Return as a string.
    return json.dumps(devices)

# Define the humidity devices router item.
@app.route('/data/devices/humidity')
def devices_humidity():

    # Select all available device ids.
    rows = db.select("SELECT DeviceID, Label FROM Devices WHERE Type IN ('dht22', 'dht11', 'am2302')")

    # Build a dictionary of devices.
    devices = {}
    for row in rows:
        devices[row[0]] = row[1]

    # Return as a string.
    return json.dumps(devices)

# Define the device temperature data router item.
@app.route('/data/device/<device_id>/<device_type>')
def device_data(device_id, device_type):

    # Set min and max range values, starting with the past X seconds (from settings) from right now.
    range_max = int(time.time())
    range_min = range_max - settings['range_seconds']

    # If min and max values are set in the GET parameters, convert them to
    # milliseconds.
    if ('range_min' in request.args and 'range_max' in request.args):

        # Convert milliseconds to seconds.
        range_min = int(request.args['range_min']) / 1000
        range_max = int(request.args['range_max']) / 1000

    # Query the data and return it as JSON.
    results = data.query(device_id, device_type, range_min, range_max)
    return json.dumps(results)

# Define the latest temperature data router item.
@app.route('/data/latest/temperature')
def latest_temperature():

    # Build a dictionary of data.
    data = {}

    # Select all temperature devices.
    devices = db.select("SELECT DeviceID, Label FROM Devices WHERE Type IN ('ds18b20', 'dht22', 'dht11', 'am2302')")

    # Iterate through the devices.
    for device in devices:

        # Get the latest temperature.
        args = (device[0],)
        rows = db.select("SELECT Timestamp, " + settings['t_unit'] + " FROM Temperature WHERE DeviceID = ? ORDER BY Timestamp DESC LIMIT 1", args)

        # Fill in the data.
        for row in rows:
            timestamp = int(str(row[0]) + '000')
            label = device[1]
            temperature = row[1]
            data[label] = [timestamp, temperature]

    # Return as a string.
    return json.dumps(data)

# Define the latest humidity data router item.
@app.route('/data/latest/humidity')
def latest_humidity():

    # Build a dictionary of data.
    data = {}

    # Select all humidity devices.
    devices = db.select("SELECT DeviceID, Label FROM Devices WHERE Type IN ('dht22', 'dht11', 'am2302')")

    # Iterate through the devices.
    for device in devices:

        # Get the latest humidity.
        args = (device[0],)
        rows = db.select("SELECT Timestamp, H FROM Humidity WHERE DeviceID = ? ORDER BY Timestamp DESC LIMIT 1", args)

        # Fill in the data.
        for row in rows:
            timestamp = int(str(row[0]) + '000')
            label = device[1]
            humidity = row[1]
            data[label] = [timestamp, humidity]

    # Return as a string.
    return json.dumps(data)

# Run it!
if __name__ == '__main__':
    app.run()
