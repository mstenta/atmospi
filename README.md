atmospi
=======

Atmospheric monitoring app for logging and graphing temperatures and humidities
over time using a Raspberry Pi and DS18B20, DHT11, DHT22, and AM2302 sensor(s).

This project has two main pieces:

1. some simple Python scripts that run on cron to gather data from attached
   sensors, and
2. a [Flask](http://flask.pocoo.org) web application for viewing the data in
   graph form via a web browser.

This documentation assumes you have a Raspberry Pi with the Raspbian operating
system.

Sensors
-------

Sensor wiring instructions can be found on Adafruit's website.

* DS18B20: https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/hardware
* DHT11 / DHT22 / AM2302: https://learn.adafruit.com/dht/connecting-to-a-dhtxx-sensor

You can connect as many DS18B20 sensors to your Pi as you'd like. Atmospi will
automatically detect them and log their measurements. Make sure that 1-Wire
GPIO is enabled (this can be enabled via `raspi-config`).

DHT11 / DHT22 / AM2302 sensors each require a separate GPIO data pin, so you
need to tell Atmospi which pin(s) to read from. See instructions below.

Atmospi Setup
-------------

1) SSH into the Raspberry Pi

    ```
    ssh pi@[hostname]
    ```

2) Install Git and clone this repository into /home/pi/atmospi.

   ```
   sudo apt-get install git
   git clone https://github.com/mstenta/atmospi.git
   ```

3) Run the `setup.sh` script.

   ```
   ~/atmospi/setup.sh
   ```

If you prefer, you may also run the commands in `setup.sh` manually, to
understand exactly what is being done.

DS18B20 Temperature Sensor Setup
--------------------------------

The `setup.sh` script will add a cron job that will take measurements from all
DS18B20 sensors connected to the Pi once every 5 minutes.

Sensors will be automatically labeled with their serial ID. If you would like
to change this label, run the following query for each sensor:

    UPDATE Devices SET Label = "New label" WHERE Type = 'ds18b20' AND SerialID = '28-000000000001';

DHT11 / DHT22 / AM2302 Temperature and Humidity Sensor Setup
------------------------------------------------------------

DHTxx sensors must be manually configured.

1) Insert rows into the Devices database to describe each of your sensors. For
   example:

    ```
    INSERT INTO Devices (DeviceID, Type, SerialID, Label) VALUES (NULL, 'dht22', '22', 'Upstairs DHT22');
    ```

2) Set up measure-dht.py to run on a cron job as root.

    ```
    sudo echo "*/5 * * * * root /home/pi/atmospi/Atmospi/measure-dht.py  >/dev/null 2>&1" | sudo tee --append /etc/cron.d/atmospi
    ```

