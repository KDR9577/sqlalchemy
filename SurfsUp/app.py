# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Msmnt = Base.classes.measurement
Stn = Base.classes.station

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
    return (
        f"Kenny Ross<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():

    #session link
    session = Session(engine)
    previous = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    #Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data).
    sel = [Msmnt.date, Msmnt.prcp]

    year_prcp = session.query(*sel).\
        filter(Msmnt.date <= previous).all()

    session.close()

    #Convert to a dictionary using date as the key and prcp as the value.
    results = {date: prcp for date, prcp in year_prcp}

    return jsonify(results)

@app.route("/api/v1.0/stations")
def stations():

    #session link
    session = Session(engine)
    results = session.query(Stn.station).all()

    #Return a JSON list of stations from the dataset.
    stations = list(np.ravel(results))

    session.close()

    return jsonify(stations=stations)

@app.route("/api/v1.0/tobs")
def temps_tobs():
    
    #Query the dates and temperature observations of the most-active station for the previous year of data.
        
    #Return a JSON list of temperature observations for the previous year.
    session = Session(engine)
    results = session.query(Stn.station).all()

    #Return a JSON list of stations from the dataset.
    tobs = list(np.ravel(results))

    session.close()

    return jsonify(tobs=tobs)

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

    results = list(np.ravel(stats))

    return jsonify(results)

@app.route("/api/v1.0/<start>/<end>")
def end_date(end):
    
    #create session link
    session = Session(engine)

    #Return a list of the minimum temperature, the average temperature, and the maximum temperature for the dates from the start date to the end date, inclusive.
    sel = [func.min(Msmnt.tobs), func.max(Msmnt.tobs), func.avg(Msmnt.tobs)]

    #For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
    # all_stats = session.query(*sel).\
    #     filter(Msmnt.date <= start and >= begin).all()
    
    session.close

if __name__ == '__main__':
    app.run(debug=True)