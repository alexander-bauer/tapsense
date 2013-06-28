#!/usr/bin/env python

import signal
import sys

import taptester
import settings

# Listen for SIGINT and exit gracefully.
def sigint_handler(signal, frame):
    tt.stop()
    print '\nOver and out.'
    sys.exit(0)
signal.signal(signal.SIGINT, sigint_handler)

# Set up a TapTester, and calibrate if possible.
tt = taptester.TapTester()

tt.onTap = settings.onTap

# Listen forever, or until terminated by SIGINT.
while True:
    tt.listen()
