#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import json
import db
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
    rows = db.select('SELECT Device FROM Temperature GROUP BY Device');

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
    rows = db.select('SELECT Device FROM Humidity GROUP BY Device');

    # Build an array of device ids.
    devices = []
    for row in rows:
        devices.append(str(row[0]))

    # Return as a string.
    return json.dumps(devices)

# Define the device temperature data router item.
@app.route('/data/device/<id>/temperature')
def device_data_temperature(id):

    # If min and max values are set in the GET parameters, parse them.
    if ('min' in request.args and 'max' in request.args):

        # Convert milliseconds to seconds.
        min = int(request.args['min']) / 1000
        max = int(request.args['max']) / 1000

        # Build the query and arguments.
        query = 'SELECT * FROM Temperature WHERE Device = ? AND Timestamp BETWEEN ? AND ? ORDER BY Timestamp ASC'
        args = (id, min, max,)

    # Otherwise, get all data.
    else:
        query = 'SELECT * FROM Temperature WHERE Device = ? ORDER BY Timestamp ASC'
        args = (id,)

    # Execute the select query.
    rows = db.select(query, args)

    # Build a series of timestamps and Fahrenheit readings.
    data = []
    for row in rows:

        # Get the timestamp (in milliseconds).
        timestamp = int(str(row[1]) + '000')

        # Get the temperature.
        temperature = row[3]

        # Append the data point.
        data.append([timestamp, temperature])

    return json.dumps(data)

# Define the device humidity data router item.
@app.route('/data/device/<id>/humidity')
def device_data_humidity(id):

    # If min and max values are set in the GET parameters, parse them.
    if ('min' in request.args and 'max' in request.args):

        # Convert milliseconds to seconds.
        min = int(request.args['min']) / 1000
        max = int(request.args['max']) / 1000

        # Build the query and arguments.
        query = 'SELECT * FROM Humidity WHERE Device = ? AND Timestamp BETWEEN ? AND ? ORDER BY Timestamp ASC'
        args = (id, min, max,)

    # Otherwise, get all data.
    else:
        query = 'SELECT * FROM Humidity WHERE Device = ? ORDER BY Timestamp ASC'
        args = (id,)

    # Execute the select query.
    rows = db.select(query, args)

    # Build a series of timestamps and humidity readings.
    data = []
    for row in rows:

        # Get the timestamp (in milliseconds).
        timestamp = int(str(row[1]) + '000')

        # Get the humidity.
        humidity = row[2]

        # Append the data point.
        data.append([timestamp, humidity])

    return json.dumps(data)

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

# Define the device flags data router item.
@app.route('/data/device/<id>/flags')
def device_flags(id):

    # Select all available device ids.
    rows = db.select('SELECT * FROM Flag WHERE Device = ? ORDER BY Timestamp ASC', (id,));

    # Gather flags.
    flags = []
    for row in rows:

        # Add flags to the array.
        flags.append({'x': int(str(row[1]) + '000'), 'title': row[2]})

    # Return as a string.
    return json.dumps(flags)

# Run it!
if __name__ == '__main__':
    app.run()
