#Import dependencies
from time import strptime
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
import numpy as np
import pandas as pd

engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def home():
    return(
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/temp/start/end<br/>')


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Calculate the date one year from the last date in data set.
    last_date = dt.date(2017,8,23)
    one_yr = dt.timedelta(days=365)
    prev_yrs = last_date - one_yr
    # Perform a query to retrieve the data and precipitation scores
    prec_scores = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>= prev_yrs).all()
    session.close()
    #Dictionary with date as a key and precipitation as a value
    precip_results= {date:prcp for date, prcp in prec_scores}
    return jsonify(precip_results)

    

@app.route("/api/v1.0/stations")
def stations():
    total_num = session.query((Station.station)).all()

    session.close()
    stations = list(np.ravel(total_num))
    return jsonify(stations = stations)


@app.route("/api/v1.0/tobs")
def tobs():
    last_date = dt.date(2017,8,23)

    one_yr = dt.timedelta(days=365)

    prev_yrs = last_date - one_yr

    active = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= prev_yrs).all()

    session.close()

    temp = list(np.ravel(active))
    return jsonify(temp = temp)


    


@app.route("/api/v1.0/temp/<start>/<end>")

def tempstartend(start = None, end = None):
    format_data = "%Y,%m,%d"
    start_end_results = session.query(func.max(Measurement.tobs), func.min(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= dt.datetime.strptime(start, format_data)).filter(Measurement.date <= dt.datetime.strptime(end, format_data)).all()
    print(start_end_results)
    json_results = list(np.ravel(start_end_results))
    # print(f" The min, max and avg are {json_results}")
    return jsonify(json_results = json_results)

#strftime is for printing the string as time
#strptime is for converting the string as time
if __name__ == "__main__":
    app.run(debug=True)