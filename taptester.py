# Composed almost entirely by Russell Borogove from Stack Overflow:
# http://stackoverflow.com/a/4160733.

# Open a microphone in pyAudio and listen for taps.

import pyaudio
import struct
import math
import settings

FORMAT = pyaudio.paInt16 
SHORT_NORMALIZE = (1.0/32768.0)
CHANNELS = 2
RATE = 44100  
INPUT_BLOCK_TIME = 0.05
INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)

# Ignore sustained noises.
MAX_TAP_BLOCKS = 0.15/INPUT_BLOCK_TIME

def get_rms( block ):
    # RMS amplitude is defined as the square root of the mean over
    # time of the square of the amplitude. So we need to convert this
    # string of bytes into a string of 16-bit samples...

    # We will get one short out for each two chars in the string.
    count = len(block)/2
    format = "%dh"%(count)
    shorts = struct.unpack( format, block )

    # Iterate over the block.
    sum_squares = 0.0
    for sample in shorts:
        # Sample is a signed short in +/- 32768. Normalize it to 1.0.
        n = sample * SHORT_NORMALIZE
        sum_squares += n*n

    return math.sqrt( sum_squares / count )

class TapTester(object):
    def __init__(self):
        self.pa = pyaudio.PyAudio()
        self.stream = self.open_mic_stream()
        self.tap_threshold = settings.threshold
        self.noisycount = MAX_TAP_BLOCKS+1 
        self.quietcount = 0 
        self.errorcount = 0

    def stop(self):
        self.stream.close()

    def find_input_device(self):
        device_index = None            
        for i in range( self.pa.get_device_count() ):     
            devinfo = self.pa.get_device_info_by_index(i)   
            print( "Device %d: %s"%(i,devinfo["name"]) )

            for keyword in ["pulse","mic","input"]:
                if keyword in devinfo["name"].lower():
                    print( "Found an input: device %d - %s"%(i,devinfo["name"]) )
                    device_index = i
                    return device_index

        if device_index == None:
            print( "No preferred input found; using default input device." )

        return device_index

    def open_mic_stream( self ):
        device_index = self.find_input_device()

        stream = self.pa.open(   format = FORMAT,
                                 channels = CHANNELS,
                                 rate = RATE,
                                 input = True,
                                 input_device_index = device_index,
                                 frames_per_buffer = INPUT_FRAMES_PER_BLOCK)

        return stream

    # listen detects the noisiness of a sample of input from the
    # audiostream, and calls 'self.onTap()' if it detects a tap.
    def listen(self):
        try:
            block = self.stream.read(INPUT_FRAMES_PER_BLOCK)
        except IOError, e:
            # Damn.
            self.errorcount += 1
            print( "(%d) Error recording: %s"%(self.errorcount,e) )
            self.noisycount = 1
            return

        amplitude = get_rms( block )
        if amplitude > self.tap_threshold:
            # This is a noisy block.
            self.quietcount = 0
            self.noisycount += 1
        else:            
            # This is a quiet block.
            if 1 <= self.noisycount <= MAX_TAP_BLOCKS:
                self.onTap()
            self.noisycount = 0
            self.quietcount += 1
