# 1. import Flask
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import pandas as pd
import numpy as np
from flask import Flask, jsonify

engine = create_engine("sqlite:///databases/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the invoices and invoice_items tables
Measurement = Base.classes.measurements
Stations = Base.classes.stations

# Create our session (link) from Python to the DB
session = Session(engine)
# connection = engine.connect()
# 2. Create an app, being sure to pass __name__
app = Flask(__name__)

# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    
    return "Welcome to my 'Home' page!"

#how do I write at proper query to return the precip data I need.
@app.route("/api/v1.0/precipitation")
def precipitation():
    date_prcp_dict = session.query(Measurement.date, Measurement.prcp).limit(365).all()
    prcp_dict = {}
    for row in date_prcp_dict:
        prcp_dict.update({row[0]: row[1]})

    return jsonify(prcp_dict)


@app.route("/api/v1.0/stations")
def stations():
    stations_dict = session.query(Stations.id, Stations.station).all()
    stations_dict_json = {}
    for row in stations_dict:
        stations_dict_json.update({row[0]: row[1]})

    return jsonify(stations_dict_json)


@app.route("/api/v1.0/tobs")
def tobs():
    tobs_dict = session.query(Measurement.id, Measurement.tobs).limit(365).all()
    tobs_dict_json = {}
    for row in tobs_dict:
        tobs_dict_json.update({row[0]: row[1]})

    return jsonify(tobs_dict_json)

@app.route("/api/v1.0/<start>")
def date(start):
    tmin = session.query(Measurement.tobs).order_by(Measurement.date).filter(Measurement.date > start).all()
    tmin = min(tmin)
    tmax = session.query(Measurement.tobs).order_by(Measurement.date).filter(Measurement.date > start).all()
    tmax = max(tmax)
    tavg = session.query(Measurement.date, Measurement.tobs).order_by(Measurement.date).filter(Measurement.date > start).all()
    start_avg = 0
    for row in tavg:
        start_avg += row[1]
    tavg_len = len(tavg)
    tavg_value = start_avg/tavg_len
    tmin_list = list(np.ravel(tmin))
    tmax_list = list(np.ravel(tmax))
    tavg_list = list(np.ravel(tavg_value))
    return jsonify(tmin_list, tmax_list, tavg_list)

@app.route("/api/v1.0/<start>/<end>")
def dates(start, end):
    # start = 
    # end =
    tmin = session.query(Measurement.tobs).order_by(Measurement.date).filter(end >= Measurement.date).filter(Measurement.date > start).all()
    tmin = min(tmin)
    tmax = session.query(Measurement.tobs).order_by(Measurement.date).filter(end >= Measurement.date).filter(Measurement.date > start).all()
    tmax = max(tmax)
    tavg = session.query(Measurement.date, Measurement.tobs).order_by(Measurement.date).filter(end >= Measurement.date).filter(Measurement.date > start).all()
    start_end_avg = 0
    for row in tavg:
        start_end_avg += row[1]
    tavg_len = len(tavg)
    tavg_value = start_end_avg/tavg_len
    tmin_list = list(np.ravel(tmin))
    tmax_list = list(np.ravel(tmax))
    tavg_list = list(np.ravel(tavg_value))
    return jsonify(tmin_list, tmax_list, tavg_list)

if __name__ == "__main__":
    app.run(debug=True)




# if __name__ == "__main__":
#     app.run(debug=True)


# @app.route("/<start>")
# def about():
#     print("Server received request for 'About' page...")
#     return "Welcome to my 'About' page!"

# if __name__ == "__main__":
#     app.run(debug=True)