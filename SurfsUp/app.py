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
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table

# Measurement = Base.classes.measurement
# Station = Base.classes.station


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
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for 'About' page...")
    return "Welcome to my 'About' page!"
    # session = Session(engine)
    # session.close()


@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'About' page...")
    return "Welcome to my 'About' page!"    
    # session = Session(engine)
    # session.close()

@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'About' page...")
    return "Welcome to my 'About' page!"    
    # session = Session(engine)
    # session.close()

@app.route("/api/v1.0/<start>")
def start():
    print("Server received request for 'About' page...")
    return "Welcome to my 'About' page!"   
    # session = Session(engine)
    # session.close()

@app.route("/api/v1.0/<start>/<end>")
def start_end():
    print("Server received request for 'About' page...")
    return "Welcome to my 'About' page!"    
    # session = Session(engine)
    # session.close()



session.close()

if __name__ == "__main__":
    app.run(debug=True)