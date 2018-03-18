#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite

# Import settings.
try:
    from settings import settings
except ImportError:
    from default_settings import settings


# Database select query helper.
def query(sql, args=()):

    # Try connecting and executing the query.
    try:

        # Open the database connection.
        con = lite.connect(settings['db'])
        db = con.cursor()

        # Execute the select.
        db.execute(sql, args)

        # Fetch all the resulting rows.
        rows = db.fetchall()

        # Commit the changes to the db.
        con.commit()

        # Return the rows.
        return rows

    # If there was an error, roll back and print it.
    except lite.Error, e:
        if con:
            con.rollback()
        print('Error querying the database.')
        print(e)
        return False

    # At the end, close the database connection.
    finally:
        if con:
            con.close()

