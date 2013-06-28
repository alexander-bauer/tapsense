# TapSense

TapSense is a small wrapper for pyAudio, which exposes a simple plugin
system for applications or events that need to be triggered by short
bursts of audio, such as clapping.

It is written in Python, and the invocations for plugins must also be
written in Python, but they can invoke non-Python functions by
whatever means is appropriate. They could also send web requests,
write to files, or invoke other programs.

Additional documentation will be added when the the program is more
developed.
