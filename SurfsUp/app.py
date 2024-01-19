# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base(engine)

# reflect the tables
Base.prepare(autoload_with=engine)
Base.classes.keys()
# Save references to each table
Msmnt = Base.classes.measurement
Stn = Base.classes.hawaii_station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
#Start at the homepage. List all the available routes.
@app.route("/")
def start():
    print("Server received request for 'Start' page...")

    #session link
    session = Session(engine)

@app.route("/api/v1.0/precipitation")
def precipitation(precipitation):

    #session link
    session = Session(engine)

    #Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data).
    sel = [Msmnt.prcp, Msmnt.date]

    year_prcp = session.query(*sel).\
        filter(Msmnt.prcp <= (2017, 8, 23)).all()

    session.close()

    #Convert to a dictionary using date as the key and prcp as the value.
    data = []
    for prcp in year_prcp:
        data_dict={"date": "prcp"}

    return jsonify(data)

@app.route("/api/v1.0/stations")
def stations(stations):

    #session link
    session = Session(engine)

    #Return a JSON list of stations from the dataset.
    stations = []

    session.close()

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def temps_tobs(temps, tobs):

    #Query the dates and temperature observations of the most-active station for the previous year of data.
        
    #Return a JSON list of temperature observations for the previous year.

@app.route("/api/v1.0/<start>")
def begin_date(begin):

    #create session link
    session = Session(engine)

    #Return a list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
    sel = [func.min(Msmnt.tobs), func.max(Msmnt.tobs), func.avg(Msmnt.tobs)]

    #For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
    stats = session.query(*sel).\
        filter(Msmnt.date >= begin).all()
    
    session.close()

    #convert to JSON
    temp_stats = []

    for min, max, avg in stats.append():
        temp_stats_dict = {}
        temp_stats_dict["min"] = min
        temp_stats_dict["max"] = max
        temp_stats_dict["avg"] = avg

    return jsonify(results)

@app.route("/api/v1.0/<start>/<end>")
def end_date(end):
    
    #create session link
    session = Session(engine)

    #Return a list of the minimum temperature, the average temperature, and the maximum temperature for the dates from the start date to the end date, inclusive.
    sel = [func.min(Msmnt.tobs), func.max(Msmnt.tobs), func.avg(Msmnt.tobs)]

    #For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
    all_stats = session.query(*sel).\
        filter(Msmnt.date <= start and >= begin).all()
    
    session.close