# pianobar.py
#
# This file is a small extension for snapsense which interfaces with
# the third party Pandora Radio client "pianobar." Its website is
# linked below. It pauses or plays the current song by writing to the
# pianobar ctl file.
#
# To use this extension, add "from pianobar import *" to the bottom of
# your settings.py.

import os

#xdg_home = os.getenv("XDG_CONFIG_HOME")
#if xdg_home != "":
#    ctlpath = xdg_home + "/pianobar/ctl"
#else:
ctlpath = os.path.expanduser("~") + "/.config/pianobar/ctl"
print ctlpath

def onTap():
    with open(ctlpath, "w") as ctl:
        ctl.write("p")

def onDoubleTap():
    with open(ctlpath, "w") as ctl:
        ctl.write("n")
