#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import sqlite3 as lite
from flask import Flask
from flask import render_template

# Create a new Flask app.
app = Flask(__name__)

# Define the webroot index route.
@app.route('/')
def index():
    try:
        con = lite.connect('/home/pi/atmospi/log.db')
        db = con.cursor()

        # Get the current timestamp as an integer.
        timestamp = int(time.time())

        # Calculate the timestamp 72 hours ago.
        past_timestamp = int(timestamp - (72 * 60 * 60))

        # Select temperature readings.
        db.execute('SELECT * FROM Temperature WHERE Timestamp > ? ORDER BY Timestamp ASC', (past_timestamp,))

        # Fetch all the results.
        rows = db.fetchall()

        # Return the rendered index.
        return render_template('index.html', data=rows, timestamp=past_timestamp)

    except lite.Error, e:
        if con:
            con.rollback()
        return 'Error connecting to the database file.'

    finally:
        if con:
            con.close()

# Run it!
if __name__ == '__main__':
    app.run()
