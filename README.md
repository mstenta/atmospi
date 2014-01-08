atmospi
=======

Scripts for logging temperature and humidity using a Raspberry Pi with DS18B20 and DHT22 sensor(s).

Dependencies
------------

(This documentation assumes that you're running Raspbian.)

**sqlite3**

    sudo apt-get install sqlite3

Setup
-----

1. SSH into Raspberry Pi

    ssh pi@[hostname]

2. Clone the repository into pi's home directory.

    git clone https://github.com/mstenta/atmospi.git

3. Create a SQLite database called log.db in the atmospi directory.

    sqlite3 log.db
    .tables
    CREATE TABLE Temperature(Device TEXT, Timestamp INT, C REAL, F REAL);
    .exit

4. Set it up to run on a cron job as root.

    sudo crontab -e
    */5 * * * * /home/pi/atmospi/measure.py
