# Import the dependencies.
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import and_
import datetime as dt



#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///C:/Users/librarypc/Documents/DATA-PT-EAST-JULY-071524/Homework/10-Advanced-SQL/Starter_Code/Resources/hawaii.sqlite")


# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)



# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
measurement = Base.classes.measurement

station = Base.classes.station

# Create a session

session = Session(bind = engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)




#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome(): 
    return (
        f"/api/v1.0/precipitation:<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/2016-08-23/2017-08-23"
    )
@app.route("/api/v1.0/precipitation")
def names():


    date_new = session.query(measurement.date).order_by(measurement.date.desc()).first()[0]

    date_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    data_ret =session.query(measurement.date, measurement.prcp).filter( 
    and_(
    measurement.date >= date_year
)).all()
    
    dict = []
    for data in data_ret: 
        dict.append({
            'date': data.date, 
            'prcp': data.prcp
        })

    return jsonify(dict)
@app.route("/api/v1.0/stations")
def names2():
    sta = session.query(station.station).all()

    dict2 = []
    for ston in sta:
        dict2.append({
            'Station': ston.station
        })

    return jsonify(dict2)
@app.route("/api/v1.0/tobs")
def names3():
    date_new = session.query(measurement.date).order_by(measurement.date.desc()).first()[0]
    date_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    date_query = session.query(measurement.station, measurement.tobs).filter(and_(measurement.station == "USC00519281", measurement.date >= date_year)).all()

    dict3 = []
    for que in date_query:
        dict3.append({
            'Station': que.station,
            'Tobs': que.tobs
        })

    return jsonify(dict3)
@app.route("/api/v1.0/<start>/<end>")
def name4(start, end): 
    stats = session.query(
    func.min(measurement.tobs).label('min'),
    func.max(measurement.tobs).label('max'),
    func.avg(measurement.tobs).label('avg')
    ).filter(and_(
        measurement.date >= start, 
        measurement.date <= end 
    )).all()

    dict4 = {
        'min': stats[0].min,
        'max':stats[0].max,
        'avg':stats[0].avg
    }


    return jsonify(dict4)

if __name__ == '__main__': 
    app.run(debug=True)