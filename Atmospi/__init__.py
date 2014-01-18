#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import sqlite3 as lite
import json
from flask import Flask
from flask import render_template

# Database select query helper.
def db_select(query, args=()):

    # Try connecting and executing the query.
    try:

        # Define the database file location.
        db_file = '/home/pi/atmospi/log.db'

        # Open the database connection.
        con = lite.connect(db_file)
        db = con.cursor()

        # Execute the select.
        db.execute(query, args)

        # Fetch all the resulting rows.
        rows = db.fetchall()

        # Return the rows.
        return rows

    # If there was an error, roll back and print it.
    except lite.Error, e:
        if con:
            con.rollback()
        return 'Error selecting from the database file. ' + e

    # At the end, close the database connection.
    finally:
        if con:
            con.close()

# Create a new Flask app.
app = Flask(__name__)

# Define the index router item.
@app.route('/')
def index():

    # Return the rendered index.
    return render_template('index.html')

# Define the temperature devices router item.
@app.route('/data/devices/temperature')
def devices():

    # Select all available device ids.
    rows = db_select('SELECT Device FROM Temperature GROUP BY Device');

    # Build an array of device ids.
    devices = []
    for row in rows:
        devices.append(str(row[0]))

    # Return as a string.
    return json.dumps(devices)

# Define the device temperature data router item.
@app.route('/data/device/<id>/temperature')
def device_data(id):

    # Select temperature readings for the specific device.
    rows = db_select('SELECT * FROM Temperature WHERE Device = ? ORDER BY Timestamp ASC', (id,))

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

# Define the device flags data router item.
@app.route('/data/device/<id>/flags')
def device_flags(id):

    # Select all available device ids.
    rows = db_select('SELECT * FROM Flag WHERE Device = ? ORDER BY Timestamp ASC', (id,));

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
