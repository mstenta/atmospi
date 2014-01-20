atmospi
=======

Atmospheric monitoring app for logging and graphing temperature(s) over time using a Raspberry Pi and DS18B20 sensor(s).

This project has two main pieces: 1) a simple Python script that runs on cron to gather data from attached sensors, and 2) a Flask web application for viewing the data in graph form via a web browser.

Refer to Adafruit's tutorial for connecting the DS18B20: http://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/hardware

Note that you can connect as many sensors to your Pi as you'd like. Atmospi will automatically detect them and log their measurements.

Dependencies
------------

(This documentation assumes that you're running Raspbian.)

**sqlite3**

    sudo apt-get install sqlite3

**Apache with mod_wsgi**

    sudo apt-get install libapache2-mod-wsgi

**Flask**

    sudo apt-get install python-pip
    sudo pip install Flask

Setup
-----

1) SSH into Raspberry Pi

    ssh pi@[hostname]

2) Clone the repository into pi's home directory.

    git clone https://github.com/mstenta/atmospi.git

3) Create a SQLite database called log.db in the atmospi directory.

    sqlite3 log.db
    .tables
    CREATE TABLE Temperature(Device TEXT, Timestamp INT, C REAL, F REAL);
    .exit

4) Set up measurement script to run on a cron job as root.

    sudo crontab -e
    */5 * * * * /home/pi/atmospi/Atmospi/measure-ds18b20.py >/dev/null 2>&1

5) Add the Apache virtual host (provided) and restart Apache.

    sudo ln -s /home/pi/atmospi/atmospi.vhost /etc/apache2/sites-enabled/atmospi
    sudo apache2ctl restart
