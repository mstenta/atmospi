#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import json
import db
import data
from flask import Flask
from flask import request
from flask import render_template

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
    rows = db.select("SELECT DeviceID FROM Devices WHERE Type IN ('ds18b20', 'dht22', 'dht11', 'am2302')");

    # Build an array of device ids.
    devices = []
    for row in rows:
        devices.append(str(row[0]))

    # Return as a string.
    return json.dumps(devices)

# Define the humidity devices router item.
@app.route('/data/devices/humidity')
def devices_humidity():

    # Select all available device ids.
    rows = db.select("SELECT DeviceID FROM Devices WHERE Type IN ('dht22', 'dht11', 'am2302')");

    # Build an array of device ids.
    devices = []
    for row in rows:
        devices.append(str(row[0]))

    # Return as a string.
    return json.dumps(devices)

# Define the device temperature data router item.
@app.route('/data/device/<device_id>/<device_type>')
def device_data(device_id, device_type):

    # Set min and max range values, starting with a default of 0 (no range).
    range_min = 0
    range_max = 0

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

    # Select all available device ids.
    rows = db.select('SELECT MAX(Timestamp), Device, F FROM Temperature GROUP BY Device');

    # Build a dictionary of data
    data = {}
    for row in rows:
        timestamp = int(str(row[0]) + '000')
        device = row[1]
        temperature = row[2]
        data[device] = [timestamp, temperature]

    # Return as a string.
    return json.dumps(data)

# Define the latest humidity data router item.
@app.route('/data/latest/humidity')
def latest_humidity():

    # Select all available device ids.
    rows = db.select('SELECT MAX(Timestamp), Device, H FROM Humidity GROUP BY Device');

    # Build a dictionary of data
    data = {}
    for row in rows:
        timestamp = int(str(row[0]) + '000')
        device = row[1]
        humidity = row[2]
        data[device] = [timestamp, humidity]

    # Return as a string.
    return json.dumps(data)

# Run it!
if __name__ == '__main__':
    app.run()
