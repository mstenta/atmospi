atmospi
=======

Atmospheric monitoring app for logging and graphing temperatures and humidities over time using a Raspberry Pi and DS18B20, DHT11, DHT22, and AM2302 sensor(s).

This project has two main pieces:

1. some simple Python scripts that run on cron to gather data from attached sensors, and
2. a [Flask](http://flask.pocoo.org) web application for viewing the data in graph form via a web browser.

A Puppet script is provided for automating the setup process. All you need to do is hook up your sensors, install Raspbian, and run the commands below. Alternatively, there are manual setup instructions further below. (Note: currently only DS18B20 sensors are set up by the Puppet script. DHTxx sensors are not.)

Currently this documentation assumes you are running Raspian on a Raspberry Pi.

Automatic Setup (with Puppet)
-------------------------------

    ssh pi@[hostname]
    git clone https://github.com/mstenta/atmospi.git
    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get install puppet
    ./atmospi/puppet/puppet-apply.sh

Manual Setup
------------

1) SSH into Raspberry Pi

    ssh pi@[hostname]

2) Upgrade all packages.

    sudo apt-get update
    sudo apt-get upgrade

3) Install SQLite3 and Apache2 with the WSGI moduile.

    sudo apt-get install sqlite3 apache2 libapache2-mod-wsgi

4) Install Flask via PIP.

    sudo apt-get install python-pip
    sudo pip install Flask

5) Clone the repository into pi's home directory.

    git clone https://github.com/mstenta/atmospi.git

6) Create a SQLite database called log.db in the atmospi directory.

    sqlite3 log.db
    CREATE TABLE Temperature(Device TEXT, Timestamp INT, C REAL, F REAL);
    CREATE TABLE Humidity(Device TEXT, Timestamp INT, H REAL);
    CREATE TABLE Flag(Device TEXT, Timestamp INT, Value TEXT);
    CREATE INDEX temperature_timestamp ON Temperature(Timestamp);
    CREATE INDEX humidity_timestamp ON Humidity(Timestamp);
    CREATE INDEX flag_timestamp ON Flag(Timestamp);
    CREATE INDEX temperature_device ON Temperature(Device);
    CREATE INDEX humidity_device ON Humidity(Device);
    CREATE INDEX flag_device ON Flag(Device);
    .exit

7) Add the Apache virtual host (provided) and restart Apache.

    sudo ln -s /home/pi/atmospi/atmospi.vhost /etc/apache2/sites-enabled/atmospi
    sudo apache2ctl restart

DS18B20 Temperature Sensor Setup
--------------------------------

Refer to Adafruit's tutorial for connecting the DS18B20 sensors: http://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/hardware

Note that you can connect as many DS18B20 sensors to your Pi as you'd like. Atmospi will automatically detect them and log their measurements.

If you use the Puppet script to install, a cron job is already set up to take measurements. If you are setting up manually, do the following:

1) Set up measure-ds18b20.py to run on a cron job as root.

    sudo crontab -e
    */5 * * * * /home/pi/atmospi/Atmospi/measure-ds18b20.py >/dev/null 2>&1

DHT11 / DHT22 / AM2302 Temperature and Humidity Sensor Setup
------------------------------------------------------------

Refer to Adafruit's tutorial for connecting the sensors: http://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging/wiring

While Raspbian comes with libraries for reading temperature from DS18B20 sensors, reading from a DHTxx humidity and temperature sensor is a little more involved. The Puppet script (automatic install) DOES NOT set up automated DHT reading, so you need to do that manually, by following the instructions below.

Also note that you can connect as many DHT sensors to your Pi as you'd like, but each requires its own data pin. Unlike the DS18B20 sensors, Atmospi cannot automatically detect DHT sensors, so you need to specify which ones are connected in your config.py file (see below).

1) Install python-dev.

    sudo apt-get install python-dev

2) Download and compile the C library for Broadcom BCM 2835 from http://www.airspayce.com/mikem/bcm2835/

    cd ~
    wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.36.tar.gz
    tar -xzf bcm2835-1.36.tar.gz
    rm bcm2835-1.36.tar.gz
    cd bcm2835-1.36
    ./configure
    make
    sudo make check
    sudo make install

3) Build the dhtreader.so library using the setup.py and dhtreader.c files in Adafruit's DHT Python Driver example: https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code/tree/master/Adafruit_DHT_Driver_Python

    cd ~
    git clone https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code.git
    cd Adafruit-Raspberry-Pi-Python-Code/Adafruit_DHT_Driver_Python
    python setup.py build
    cp build/lib.linux-armv6l-2.7/dhtreader.so ~/atmospi/Atmospi

Basically you just want to end up with a library file called dhtreader.so in the main ~/atmospi/Atmospi directory.

4) Edit settings.py and describe the sensors that are attached (see example in default_settings.py).

5) Set up measure-dht.py to run on a cron job as root.

    sudo crontab -e
    */5 * * * * /home/pi/atmospi/Atmospi/measure-dht.py >/dev/null 2>&1

