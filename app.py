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
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

# Convert the query results to a dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")
def precipitation():
#   create our session(link) from Python to the DB
    session = Session(engine)

    # Query Measurement
    results = (session.query(Measurement.date, Measurement.pcp).order_by(Measurement.date))

    date_pcp = []

    for row in results:
        dict= {}

   
    mydate = dt.date(mydate)-dt.datetime(days=365)

    session.close()

  
    return jsonify(all_names)

@app.route("/api/v1.0/stations")
def stations():
   #   create our session(link) from Python to the DB
    session = Session(engine)
"""Return a list of all station names"""

# Query all stations

    results = session.query(Station.name).all()

# Convert list of tuples into normal list

    all_stations = list(np.ravel(results))

    session.close()

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
#   create our session(link) from Python to the DB  
    session = Session(engine)



    session.close()


    return jsonify(all_names)

@app.route("/api/v1.0/<start>")
def start():
#   create our session(link) from Python to the DB  
    session = Session(engine)



    session.close()

  

    return jsonify(all_names)


@app.route("/api/v1.0/<start>/<end>")
def start_end():
#   create our session(link) from Python to the DB    
    session = Session(engine)

    
    

    session.close()

    
   

    return jsonify(_____)


if __name__ == '__main__':
    app.run(debug=True)
