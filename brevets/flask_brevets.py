"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import datetime
import acp_times  # Brevet time calculations
import config

import logging

import os
from pymongo import MongoClient

###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()


#client = MongoClient('mongodb://' +os.environ['MONGODB_HOSTNAME'], 27017)
client = MongoClient('mongodb://' + 'flaskdb', 27017)
db = client.brevet
brevet_collection = db.controls
###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', 999, type=float)
    dist = request.args.get('dist', 200, type=float)
    startTimeStr = request.args.get('startTime', type=str)
    app.logger.debug("start time: {}".format(startTimeStr))
    app.logger.debug("dist: {}".format(dist))
    app.logger.debug("km={}".format(km))
    app.logger.debug("request.args: {}".format(request.args))
    # FIXME!
    # Right now, only the current time is passed as the start time
    # and control distance is fixed to 200
    # You should get these from the webpage!
    open_time = acp_times.open_time(km, dist, arrow.now()).format('YYYY-MM-DDTHH:mm')
    close_time = acp_times.close_time(km, dist, arrow.now()).format('YYYY-MM-DDTHH:mm')
    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)

@app.route("/_store_data", methods = ["POST"])
def store_data():
    try:
        in_data = request.json
        app.logger.debug("in try")
        controls = in_data["controls"]
        date_time = in_data["startTime"]
        total_dist = in_data["dist"]
        storageMongo(controls, date_time, total_dist)
        app.logger.debug("data done")
        id = output.inserted_id
        return flask.jsonify(result = {},
            status = 1,
            mongoid = id)
    except: return flask.jsonify(result = {},
        status = 0,
        mongoid = 'NA')

def storageMongo(controls, startTime, dist):
    output = brevet_collection.insert_one({
        "controls": controls,
        "date_time": startTime,
        "total_dist": dist
    })

@app.route("/_display_data")
def display_data():
    app.logger.debug("trying to display")
    try:
        controls = get_brevets()
        app.logger.debug(controls)
        return flask.jsonify(result = {
            "controls": controls},
            status = 1)
    except:
        return flask.jsonify(result = {},
            status = 0)

#############

def get_brevets():
    app.logger.debug("in get func")
    coll = brevet_collection.find().sort("_id", -1).limit(1)
    for data in coll:
        app.logger.debug("returning")    
        return data["controls"]

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
