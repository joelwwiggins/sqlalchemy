
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask,jsonify

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
db=automap_base()
# reflect the tables
db.prepare(engine,reflect=True)

# Save references to each table
measure=db.classes.measurement
station=db.classes.station

# Create our session (link) from Python to the DB
session=Session(engine)


#set up flask app
app=Flask(__name__)

#List the routes available on the homepage
@app.route("/")
def home():
    """All available routes"""
    return (
        f"<H1>Routes currently available<H1><br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    rain=session.query(measure.date, measure.prcp).\
    order_by(measure.date).\
    all()

    rain_df=pd.DataFrame(rain)
    rain_df1=rain_df.sort_values('date')
    rain_date_index=rain_df1.set_index('date')
    rain_cleaned=rain_date_index.dropna()
    rain_cleaned
    rain_cleaned_dict=rain_cleaned.to_dict()
    return jsonify(rain_cleaned_dict)

@app.route("/api/v1.0/stations")
def stations():
    results=session.query(measure.station, func.count(measure.station)).group_by(measure.station).\
            order_by(func.count(measure.station).desc()).all()
    return jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs():
    """Most Active Stations"""   
    tobs=session.query(measure.station, func.count(measure.station)).group_by(measure.station).\
    order_by(func.count(measure.station).desc()).all()
    return jsonify(tobs)

@app.route("/api/v1.0/<start>/<end>")
def startdate(start,end):
    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range."""
    rain=session.query(func.min(measure.tobs), func.max(measure.tobs),func.avg(measure.tobs)).filter(measure.date>=start).filter(measure.date<=end).all()

    return jsonify (rain)

@app.route("/api/v1.0/<start>")
def juststart(start,end):
    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range."""
    rain=session.query(func.min(measure.tobs), func.max(measure.tobs),func.avg(measure.tobs)).filter(measure.date>=start).all()

    return jsonify (rain)

if __name__ == '__main__':
    app.run(debug=True)