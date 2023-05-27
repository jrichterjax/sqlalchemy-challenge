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

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

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

#List all available routes on the homepage
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

# Return a dictionary of date and prcp values
@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for 'precipitation' page...")
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').order_by(Measurement.date.desc()).all()
    # Create empty lists
    keys = []
    unique_keys = []
    # Create a list of all dates in the last year of data
    for date in results:
        keys.append(date[0])
    # Create a list of all unique dates in the last year of data    
    for key in keys:
        if key not in unique_keys:
            unique_keys.append(key)
    # Loop through each unique date and append prcp values to create a dictionary
    prcp_dict = {}
    for key in unique_keys:
        prcp_list = []      
        for date, prcp in results:
            if date == key:
                prcp_list.append(prcp)      
        prcp_dict[key] = prcp_list     
    return jsonify(prcp_dict)

# Return a list of all stations
@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'stations' page...")
    all_stations = session.query(Station.station).all()
    stations_list = list(np.ravel(all_stations))
    return jsonify(stations_list)

# Return a list of temperature observations for the most active station for the previous year
@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'tobs' page...")
    station_temps = session.query(Measurement.tobs).filter(Measurement.station == "USC00519281").filter(Measurement.date >= '2016-08-18').all()    
    station_temps_list = list(np.ravel(station_temps))
    return jsonify(station_temps_list)

# Return the min, max and avg temperature for all dates greater than or equal to the start date provided
@app.route("/api/v1.0/<start>")
def start(start):
    print("Server received request for 'start' page...")
    start_temps = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()    
    start_temps_list = list(np.ravel(start_temps))
    return jsonify(start_temps_list)

# Return the min, max and avg temperature for all dates between, and including, the start and end dates provided
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    print("Server received request for 'start/end' page...")
    start_end_temps = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()    
    start_end_temps_list = list(np.ravel(start_end_temps))
    return jsonify(start_end_temps_list)

session.close()

if __name__ == "__main__":
    app.run(debug=True)