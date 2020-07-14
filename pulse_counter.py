#!/usr/bin/env python
# set up GPIO pin as input with pull-up resistor
# setup for water meter pulse counter

import RPi.GPIO as GPIO
from time import time, sleep
from datetime import datetime
import os, sys

DEBUG = False
# Meter Calibration
CUFT = 1.0/10 # cubic feet per count
GAL = 7.48052 # gallons per cu ft
LITER = 28.3168 # liters per cu ft
# other constants
channel = 40 # BCM 21 - meter uses board pins 39 GND and 40 (pull-up on 40) 
counts = 0 # counts per interval
INTERVAL = 60 # sample window in sec
path = '/home/pi/water'
filename = 'counts.log'
def now(): return datetime.ctime(datetime.now())
header = "Water Meter Usage Log (timestamp counts/min), %s\n" % now()

GPIO.setmode(GPIO.BOARD) # BCM)
GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def count(ch, debug=True): #False):
    global counts
    counts += 1
    if debug: print 'Ch %d: counts %d' % (ch, counts)
file_path = os.path.join(path, filename)
def writedata(file_path, data, debug=False):
    if debug: print " Writing to ",filename," data: ", data
    if not os.path.isfile(file_path):
        # create a new file if it is not found
        print "Creating new file %s, at %s" %(filename, now())
        with open(file_path, "w") as f: f.write(header)
    with open(file_path, "a") as f:
        f.write("%s\n" % data)
    if debug: print "  Closing"
    # sys.stdout.flush()

if __name__ == '__main__':
    print "Starting counter"
    start_time = time()
    try:
        GPIO.add_event_detect(channel, GPIO.FALLING, callback=count, \
	bouncetime=50)
        if DEBUG:
            print "Counts:"
            print "------"

        i = 0
        while True: # time()-start_time < 60:
            if DEBUG: print "%d " % counts,
            #data = json.dumps([round(time()), counts])
            data = '%d %d' % (round(time()), counts)
            counts = 0 # reset counts
            writedata(filename, data)
            i+=1
            if i >= 60:
                sys.stdout.flush()
                i = 0
            sleep(INTERVAL)
        print "Done"

    finally:
        GPIO.remove_event_detect(channel)
        print "Done"



#state = GPIO.input(channel)
#print state
# to get date and time from timestamp
# print datetime.fromtimestamp(time())
