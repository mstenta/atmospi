# Atmospi settings.
settings = {

    # Absolute path to the SQLite database file.
    'db': '/home/pi/atmospi/log.db',

    # Define the DHT devices and the GPIO pin they are connected to.
    #
    # dht_devices should be a dictionary of dictionaries. The name of each
    # dictionary will be used as the device's unique ID.
    #
    # For example:
    #
    # 'dht_devices': {
    #     'Name of sensor': {
    #         'type': 'DHT22',
    #         'pin': 22
    #     }
    # }
    #
    # Available device types: DHT11, DHT22, AM2302
    'dht_devices': {}
}
