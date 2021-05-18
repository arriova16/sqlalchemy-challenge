import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine('sqlite:///Resources/hawaii.sqlite')

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect = True)


# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/end<br/>"
    )

# Convert the query results to a dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")
def precipitation():
#   create our session(link) from Python to the DB
    session = Session(engine)

    # Query Measurement
    results = (session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date)).all()
    
    session.close()
    date_prcp = []

    for date, prcp in results:
        dict= {}
        dict["date"] = date
        dict["prcp"] = prcp
        date_prcp.append(dict)
   

    return jsonify(date_prcp)

@app.route("/api/v1.0/stations")
def stations():
   #   create our session(link) from Python to the DB
    session = Session(engine)
# """Return a list of all station names"""

# Query all stations
    results = session.query(Station.name).all()
    
    session.close()

# Convert list of tuples into normal list

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)




# Query the dates and temperature observations of the most active station for the last 
# year of data.
# Return a JSON list of temperature observations (TOBS) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
#   create our session(link) from Python to the DB  
    session = Session(engine)

    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= query_date).all()

    session.close()

    most_recent = list(np.ravel(results))

    return jsonify(most_recent)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def start(start=None, end=None):
#   create our session(link) from Python to the DB  
    session = Session(engine)
    if not end : 
        results= session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
   filter(Measurement.date >= start).all()

    else:

        results= session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
   filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    

  
    session.close()

    most_recent = list(np.ravel(results))

    return jsonify(most_recent)

# /api/v1.0/<start> and /api/v1.0/<start>/<end>
# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.


if __name__ == '__main__':
    app.run(debug=True)
