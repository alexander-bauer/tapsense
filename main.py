#!/usr/bin/env python

import signal
import sys

import taptester

# Listen for SIGINT and exit gracefully.
def sigint_handler(signal, frame):
    tt.stop()
    print '\nOver and out.'
    sys.exit(0)
signal.signal(signal.SIGINT, sigint_handler)

# Set up a TapTester, and calibrate if possible.
tt = taptester.TapTester()

# Define the function that will be called on tap.
def onTap():
    print 'tap'

tt.onTap = onTap

# Listen forever, or until terminated by SIGINT.
while True:
    tt.listen()
