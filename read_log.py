# read and show contents of log files

from numpy import random, loadtxt
import os, time, datetime
import matplotlib.pyplot as plt
from matplotlib import dates

# Meter Calibration
CUFT = 1.0/10 # cubic feet per count
GAL = 7.48052*CUFT # gallons per count
LITER = 28.3168*CUFT # liters per count


###########################################################
# start the server with the 'run()' method
if __name__ == '__main__':
    fname1 = 'counts.log'
    fname2 = 'counts_july.log'
    fname = fname1
    t, cnts = loadtxt(fname, skiprows=1, unpack=True)
    dts = map(datetime.datetime.fromtimestamp, t)
    dfds = dates.date2num(dts) # converted

    # matplotlib date format object
    hfmt = dates.DateFormatter('%m/%d %H:%M')

    dts = map(datetime.datetime.fromtimestamp, t)
    fds = dates.date2num(dts) # converted

    # matplotlib date format object
    hfmt = dates.DateFormatter('%m/%d %H:%M')


    plt.plot_date(dts, cnts*GAL)
    plt.title("%s" % fname)
    ax = plt.gca()
    fig = plt.gcf()
    #ax.xaxis.set_major_locator(dates.HourLocator())
    ax.xaxis.set_major_locator(dates.DayLocator())
    ax.xaxis.set_major_formatter(hfmt)
    ax.set_ylim(0,4)
    ax.set_xlabel('Time')
    ax.set_ylabel('Usage [Gal/min]')
    xmin = ax.get_xlim()[0]
    ax.text(xmin, 0.2, 'Total Usage: %d Gal' % (round((cnts * GAL).sum())))
    ax.grid('on')
    fig.autofmt_xdate()

    plt.show()
    print dates
