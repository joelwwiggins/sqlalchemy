%matplotlib inline
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
        f"<H1"
    )

