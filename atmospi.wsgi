#!/usr/bin/python

import sys
import logging

logging.basicConfig(stream=sys.stderr)

sys.path.insert(0,"/home/pi/atmospi")

from Atmospi import app as application
