#!/usr/bin/env python

import signal
import sys

import settings
import taptester

# Listen for SIGINT and exit gracefully.
def sigint_handler(signal, frame):
    tt.stop()
    print '\nOver and out.'
    sys.exit(0)
signal.signal(signal.SIGINT, sigint_handler)

# Set up a TapTester, and calibrate if possible.
tt = taptester.TapTester()


# If settings.onTap is defined, make it the callback.
if callable(settings.onTap):
    tt.onTap = settings.onTap
else:
    # Use this simple function as a default.
    def onTap():
        print 'Tap!'

    tt.onTap = onTap

# Same for double-tap
if callable(settings.onDoubleTap):
    tt.onDoubleTap = settings.onDoubleTap
else:
    def onDoubleTap():
        print 'Double-tap!'
    tt.onDoubleTap = onDoubleTap

# Listen forever, or until terminated by SIGINT.
while True:
    tt.listen()
