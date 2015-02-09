# Atmospi settings.
settings = {

    # Absolute path to the SQLite database file.
    'db': '/home/pi/atmospi/log.db',

    # How far into the past should data be loaded (in seconds)?
    # Default to 1 week.
    'range_seconds': 60 * 60 * 24 * 7,

    # The number of digits after the decimal place that will be stored.
    'precision': 2,
}
