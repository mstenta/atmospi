# Inherit from the official Python 2 image.
FROM python:2

# Run apt-get update+upgrade.
RUN apt-get -y update && apt-get -y upgrade

# Install the Adafruit_Python_DHT library.
RUN apt-get -y install python-dev \
  && git clone https://github.com/adafruit/Adafruit_Python_DHT.git /home/pi/atmospi/Adafruit_Python_DHT \
  && (cd /home/pi/atmospi/Adafruit_Python_DHT && python /home/pi/atmospi/Adafruit_Python_DHT/setup.py install) \
  && rm -r /home/pi/atmospi/Adafruit_Python_DHT

# Install cron and set up a crontab for measuring DS18B20 sensors.
RUN apt-get -y install cron \
  && echo "*/5 * * * * root /home/pi/atmospi/Atmospi/measure-ds18b20.py >/dev/null 2>&1" | tee /etc/cron.d/atmospi

# Install SQLite3
RUN apt-get -y install sqlite3

# Install Apache and mod_wsgi.
RUN apt-get -y install apache2 libapache2-mod-wsgi

# Install Flask
RUN pip install flask

# Set up virtual host configuration.
COPY atmospi.vhost /etc/apache2/sites-available/000-default.conf

# Copy the app into /home/pi/atmospi.
RUN mkdir -p /home/pi/atmospi
COPY . /home/pi/atmospi/

# Expose port 80.
EXPOSE 80

# Provide our own docker-entrypoint.sh.
COPY docker-entrypoint.sh /usr/local/bin/
#ENTRYPOINT ["docker-entrypoint.sh"]

# Run Apache.
CMD ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]

