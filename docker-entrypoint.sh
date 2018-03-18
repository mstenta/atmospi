#!/bin/bash
set -e

# If the SQLite3 database doesn't exist, create it.
if ! [ -e /home/pi/atmospi/log.db ]; then
    sqlite3 /home/pi/atmospi/log.db "CREATE TABLE Devices(DeviceID INTEGER PRIMARY KEY, Type TEXT, SerialID TEXT, Label TEXT);"
    sqlite3 /home/pi/atmospi/log.db "CREATE TABLE Temperature(DeviceID INT, Timestamp INT, C REAL);"
    sqlite3 /home/pi/atmospi/log.db "CREATE TABLE Humidity(DeviceID INT, Timestamp INT, H REAL);";
    sqlite3 /home/pi/atmospi/log.db "CREATE TABLE Flag(DeviceID INT, Timestamp INT, Value TEXT);";
    sqlite3 /home/pi/atmospi/log.db "CREATE INDEX temperature_dt ON Temperature(DeviceID, Timestamp);";
    sqlite3 /home/pi/atmospi/log.db "CREATE INDEX humidity_dt ON Humidity(DeviceID, Timestamp);";
    sqlite3 /home/pi/atmospi/log.db "CREATE INDEX flag_dt ON Flag(DeviceID, Timestamp);";
fi

# Execute the arguments passed into this script.
echo "Attempting: $@"
exec "$@"

