#!/usr/bin/python
# -*- coding: utf-8 -*-

import db

# Import settings.
try:
    from settings import settings
except ImportError:
    from default_settings import settings

# Data query helper function.
def query(device_id, device_type, range_min=0, range_max=0):

    # Start with an empty result set.
    results = []

    # Determine the table name and fields based on the device type.
    if device_type == 'temperature':
        table = 'Temperature'
        fields = 'Timestamp, ' + settings['t_unit']
    elif device_type == 'humidity':
        table = 'Humidity'
        fields = 'Timestamp, H'
    elif device_type == 'flags':
        table = 'Flag'
        fields = 'Timestamp, Value'
    else:
        return results

    # Build the query and arguments...
    query = 'SELECT ' + fields + ' FROM ' + table + ' WHERE DeviceID = ?'
    args = (device_id,)

    # If min and max values are provided...
    if (range_min and range_max):
        query += ' AND Timestamp BETWEEN ? AND ?'
        args += (range_min, range_max)

    # Always order by timestamp ascending.
    query += ' ORDER BY Timestamp ASC'

    # Execute the select query.
    rows = db.select(query, args)

    # Build a series of timestamps and data.
    for row in rows:

        # Convert the timestamp to milliseconds.
        timestamp = row[0] * 1000

        # Get the data.
        data = row[1]

        # Append the data point (flags are specially formatted).
        if device_type == 'flags':
            results.append({'x': timestamp, 'title': data})
        else:
            results.append([timestamp, data])

    # Return the data array.
    return results
