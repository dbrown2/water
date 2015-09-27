#!/usr/bin/env python
# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request
from flask import make_response, jsonify
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import dates
from numpy import random, loadtxt
from StringIO import StringIO
from datetime import datetime
import os

# Meter Calibration
CUFT = 1.0/10 # cubic feet per count
GAL = 7.48052*CUFT # gallons per count
LITER = 28.3168*CUFT # liters per count

path = '/home/pi/python/water/'
# matplotlib date format object
hfmt = dates.DateFormatter('%m/%d %H:%M')

def read_data(filename, debug=False):
    if debug: print " Reading from ",filename
    if os.path.isfile(filename):
        t, counts = loadtxt(filename, skiprows=1, unpack=True)
        #ct = [datetime.fromtimestamp(t_secs) for t_secs in t]
        dts = map(datetime.fromtimestamp, t)
        # fds = dates.date2num(dts) # converted
        return dts, counts

# create the application object
app = Flask(__name__)

# use decorators to link the function to a url
@app.route('/')
def home():
    return redirect(url_for('index_page'))

@app.route('/about')
def about():
    return "About page"

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template


@app.route('/index')
def index_page():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid credentials.  Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route('/JSON/water_use/rate') 
def water_use_rate_JSON():
    dts, counts = read_data(path + 'counts.log', debug=False)
    app.logger.info("Generated JSON water use rate")
    return jsonify({'time':list(dts),
                    'rate_Gal_per_min': list(counts * GAL)})


@app.route('/water_use/rate')
def water_use_rate():
    dts, counts = read_data(path + 'counts.log', debug=False)
    fig = Figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.step(dts, counts * GAL)
    ax.set_ylim(0,8)
    locator = dates.HourLocator(interval=6)
    ax.xaxis.set_major_locator(locator)
    fmt = dates.DateFormatter("%b%e %R")
    ax.xaxis.set_major_formatter(fmt)
    ax.set_xlabel('Time')
    ax.set_ylabel('Usage [Gal/min]')
    fig.autofmt_xdate()
    ax.set_title('Water Use Rate')
    ax.grid('on')
    rate_max = (counts * GAL).max()
    total = (counts * GAL).sum()
    ax.text(ax.get_xlim()[0], 0.9*rate_max, 'Total Usage: %d Gal' %(total))
    fig.autofmt_xdate()
    canvas = FigureCanvas(fig)
    # output = BytesIO()
    output = StringIO()  # python 2.7x
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response


@app.route('/water_use/cumulative')
def water_use_cumulative():
    dts, counts = read_data(path + 'counts.log', debug=False)
    fig = Figure()
    ax = fig.add_subplot(1, 1, 1)
    cumulative = (counts*GAL).cumsum()
    ax.step(dts, cumulative)
    locator = dates.HourLocator(interval=6)
    ax.xaxis.set_major_locator(locator)
    fmt = dates.DateFormatter("%b%e %R")
    ax.xaxis.set_major_formatter(fmt)
    ax.set_xlabel('Time')
    ax.set_ylabel('Cumulative Usage [Gal]')
    ax.set_title('Water Usage, Cumulative')
    ax.grid('on')
    ax.grid('on')
    fig.autofmt_xdate()
    total = (counts * GAL).sum()
    ax.text(ax.get_xlim()[0], 0.9*total, 'Total Usage: %d Gal' %(total))
    canvas = FigureCanvas(fig)
    # output = BytesIO()
    output = StringIO()  # python 2.7x
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    app.logger.info("Generated Cumulative Plots")
    return response

@app.route('/JSON/water_use/total')
def water_use_total():
    dts, counts = read_data(path + 'counts.log', debug=False)
    response = jsonify({"total_gallons": int((counts * GAL).sum())})
    return response


###########################################################
# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
