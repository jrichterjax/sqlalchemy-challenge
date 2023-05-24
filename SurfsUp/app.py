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

# reflect an existing database into a new model
Base = automap_base()

engine = create_engine("sqlite:///hawaii.sqlite")

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

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
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for 'precipitation' page...")
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').order_by(Measurement.date.desc()).all()
    prcp_list = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        prcp_list.append(prcp_dict)
    return jsonify(prcp_list)

@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'stations' page...")
    all_stations = session.query(Station.station).all()
    stations_list = list(np.ravel(all_stations))
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'tobs' page...")
    station_temps = session.query(Measurement.tobs).filter(Measurement.station == "USC00519281").filter(Measurement.date >= '2016-08-18').all()    
    station_temps_list = list(np.ravel(station_temps))
    return jsonify(station_temps_list)

@app.route("/api/v1.0/<start>")
def start(start):
    print("Server received request for 'start' page...")
    return "The start date is " + start


@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    print("Server received request for 'start/end' page...")
    return "The start date is " + start + ", and the end date is " + end

session.close()

if __name__ == "__main__":
    app.run(debug=True)