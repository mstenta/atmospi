#!/bin/bash

#
# Atmospi setup script.
#
# Usage: ./setup.sh
#

# If Atmospi has already been set up, bail.
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
if [ -f $DIR/setup.log ]; then
    echo "Atmospi has already been set up. Aborting."
    exit 1
fi

# Update software.
sudo apt-get update -y
sudo apt-get upgrade -y

# Install sqlite3
sudo apt-get install -y sqlite3

# Create the SQLite database.
sqlite3 $DIR/log.db "CREATE TABLE Devices(DeviceID INTEGER PRIMARY KEY, Type TEXT, SerialID TEXT, Label TEXT);"
sqlite3 $DIR/log.db "CREATE TABLE Temperature(DeviceID INT, Timestamp INT, C REAL);"
sqlite3 $DIR/log.db "CREATE TABLE Humidity(DeviceID INT, Timestamp INT, H REAL);";
sqlite3 $DIR/log.db "CREATE TABLE Flag(DeviceID INT, Timestamp INT, Value TEXT);";
sqlite3 $DIR/log.db "CREATE INDEX temperature_dt ON Temperature(DeviceID, Timestamp);";
sqlite3 $DIR/log.db "CREATE INDEX humidity_dt ON Humidity(DeviceID, Timestamp);";
sqlite3 $DIR/log.db "CREATE INDEX flag_dt ON Flag(DeviceID, Timestamp);";

# Install the Adafruit_Python_DHT library.
sudo apt-get install -y python-dev
git clone https://github.com/adafruit/Adafruit_Python_DHT.git $DIR/Adafruit_Python_DHT
(cd $DIR/Adafruit_Python_DHT && sudo python $DIR/Adafruit_Python_DHT/setup.py install)
sudo rm -r $DIR/Adafruit_Python_DHT

# Install Python PIP.
sudo apt-get install -y python-pip

# Install Flask via PIP.
sudo pip install flask

# Install Apache and mod_wsgi.
sudo apt-get install -y apache2 libapache2-mod-wsgi

# Symlink the atmospi virtual host into Apache.
sudo ln -s $DIR/atmospi.vhost /etc/apache2/sites-enabled/000-atmospi.conf

# Restart Apache.
sudo apache2ctl restart

# Set up cron job for DS18B20 sensor measurements.
sudo echo "*/5 * * * * root $DIR/Atmospi/measure-ds18b20.py >/dev/null 2>&1" | sudo tee /etc/cron.d/atmospi

# Create a setup.log file to indicate that setup has already happened.
touch $DIR/setup.log

