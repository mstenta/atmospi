#!/usr/bin/python
# -*- coding: utf-8 -*-

import db

# Import settings.
try:
    from settings import settings
except ImportError:
    from default_settings import settings


# Data query helper function.
def query(device_id, device_type, range_min=0, range_max=0, order_by='ASC', limit=0):

    # Start with an empty result set.
    results = []

    # Start an empty tuple for query arguments.
    args = ()

    # Determine the table name and fields based on the device type.
    if device_type == 'temperature':
        table = 'Temperature'
        fields = 'Timestamp, C'
        if settings['t_unit'] == 'F':
            fields = 'Timestamp, round((C * 9.0 / 5.0 + 32.0), ?) as F'
            args += (settings['precision'],)
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
    args += (device_id,)

    # If min and max values are provided...
    if range_min and range_max:
        query += ' AND Timestamp BETWEEN ? AND ?'
        args += (range_min, range_max)

    # Order by the timestamp ascending/descending (default to ascending).
    query += ' ORDER BY Timestamp '
    if order_by == 'ASC' or order_by == 'DESC':
        query += order_by
    else:
        query += 'ASC'

    # Limit the query results, if desired.
    if limit:
        query += ' LIMIT ?'
        args += (limit,)

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
