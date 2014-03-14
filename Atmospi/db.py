#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite

# Import settings.
try:
    from settings import settings
except ImportError:
    from default_settings import settings

# Database select query helper.
def select(query, args=()):

    # Try connecting and executing the query.
    try:

        # Open the database connection.
        con = lite.connect(settings['db'])
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
