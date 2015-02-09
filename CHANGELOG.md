v0.2.0
------
Adds device identification (see https://github.com/mstenta/atmospi/issues/10)

This release requires manual updates of both the datbase and settings.py.

First, create a new Devices table in the SQLite database:

    CREATE TABLE Devices(DeviceID INT PRIMARY KEY, Type TEXT, SerialID TEXT, Label TEXT);

Second, add records for each of your devices. Below is an example of each type.

DS18B20:
    INSERT INTO Devices (DeviceID, Type, SerialID, Label) VALUES (NULL, 'ds18b20', '28-000000000001', 'Basement Temperature');

DHT22:
    INSERT INTO Devices (DeviceID, Type, SerialID, Label) VALUES (NULL, 'dht22', '22', 'DHT22 Sensor on Pin 22');

AM2302:
    INSERT INTO Devices (DeviceID, Type, SerialID, Label) VALUES (NULL, 'am2302', '16', 'AM2302 Sensor on Pin 16');

Third, add a new DeviceID column to the Temperature, Humidity, and Flag tables:

    ALTER TABLE Temperature ADD COLUMN DeviceID INT;
    ALTER TABLE Humidity ADD COLUMN DeviceID INT;
    ALTER TABLE Flag ADD COLUMN DeviceID INT;

Fourth, populate the new DeviceID columns with your new sensor information. For example, if you have a DHT22 sensor that was previously labelled "Upstairs DHT22" in settings.ph, and it now has a DeviceID of 1 in the Devices table, run the following:

    UPDATE Temperature SET DeviceID = 1 WHERE Device = "Upstairs DHT22";
    UPDATE Humidity SET DeviceID = 1 WHERE Device = "Upstairs DHT22";
    UPDATE Flag SET DeviceID = 1 WHERE Device = "Upstairs DHT22";

Fifth, remove the Device column from the Temperature, Humidity, and Flag databases.

    BEGIN TRANSACTION;
    CREATE TEMPORARY TABLE Temperature_backup(DeviceID INT, Timestamp INT, C REAL, F REAL);
    INSERT INTO Temperature_backup SELECT DeviceID, Timestamp, C, F FROM Temperature;
    DROP TABLE Temperature;
    CREATE TABLE Temperature(DeviceID INT, Timestamp INT, C REAL, F REAL);
    INSERT INTO Temperature SELECT DeviceID, Timestamp, C, F FROM Temperature_backup;
    DROP TABLE Temperature_backup;
    COMMIT;

    BEGIN TRANSACTION;
    CREATE TEMPORARY TABLE Humidity_backup(DeviceID INT, Timestamp INT, H REAL);
    INSERT INTO Humidity_backup SELECT DeviceID, Timestamp, H FROM Humidity;
    DROP TABLE Humidity;
    CREATE TABLE Humidity(DeviceID INT, Timestamp INT, H REAL);
    INSERT INTO Humidity SELECT DeviceID, Timestamp, H FROM Humidity_backup;
    DROP TABLE Humidity_backup;
    COMMIT;

    BEGIN TRANSACTION;
    CREATE TEMPORARY TABLE Flag_backup(a,b);
    INSERT INTO Flag_backup SELECT a,b FROM Flag;
    DROP TABLE Flag;
    CREATE TABLE Flag(a,b);
    INSERT INTO Flag SELECT a,b FROM Flag_backup;
    DROP TABLE Flag_backup;
    COMMIT;

Finally, clean up and reindex:

    DROP INDEX temperature_device;
    DROP INDEX humidity_device;
    DROP INDEX flag_device;
    CREATE INDEX temperature_device ON Temperature(DeviceID);
    CREATE INDEX humidity_device ON Humidity(DeviceID);
    CREATE INDEX flag_device ON Flag(DeviceID);

And remove the dht_devices variable from settings.py, as it is no longer used.

v0.1.0
------
This is an initial pre-release for folks running Atmospis. Following releases may start to introduce database and/or settings.py changes that require some manual updating. If so, these release notes will be used to document the necessary steps.
