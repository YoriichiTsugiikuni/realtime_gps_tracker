from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_pymongo import PyMongo
from marshmallow import Schema, ValidationError,fields
from bson.json_util import dumps
from json import loads
import os
from dotenv import load_dotenv
from datetime import datetime
from flask_googlemaps import GoogleMaps
from flask import Flask, render_template 
from flask_googlemaps import Map





  
load_dotenv()

info = {}

app = Flask(__name__)
CORS(app)
#setup location of database
app.config["MONGO_URI"] = os.getenv("mongostring") 
mongo = PyMongo(app)
#GoogleMaps(app, key="AIzaSyDywRQDYl4bXm3bR58kkz2psPkO5sDZVTE")



#Rules database information has to conform to
class TankSchema(Schema):
    lat = fields.String(required=True)
    long = fields.String(required=True)
    dateTime = fields.DateTime(required=True)

@app.route("/data",methods = ["GET"])
def dataGET(): 
    kokushi = mongo.db.gps.find()
    juuni_kizuki = loads(dumps(kokushi))
    return jsonify(juuni_kizuki)

@app.route("/tank", methods = ["POST"])
def add_new_tank():
    request_dict = request.json
    new_gps = TankSchema().load(request_dict)

    gps_document=mongo.db.gps.insert_one(new_gps)
    gps_id=gps_document.inserted_id

    gps=mongo.db.gps.find_one({"_id":gps_id})
    gps_json=loads(dumps(gps))
       
    return jsonify(gps_json)

@app.route("/")
def mapview():
    # creating a map in the view
    mymap = Map(
        identifier="view-side",
        lat=37.4419,
        lng=-122.1419,
        markers=[(37.4419, -122.1419)]
    )
    sndmap = Map(
        identifier="sndmap",
        lat=37.4419,
        lng=-122.1419,
        markers=[
          {
             'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
             'lat': 37.4419,
             'lng': -122.1419,
             'infobox': "<b>Hello World</b>"
          },
          {
             'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
             'lat': 37.4300,
             'lng': -122.1400,
             'infobox': "<b>Hello World from other place</b>"
          }
        ]
    )
    return render_template('index.html', mymap=mymap, sndmap=sndmap)



if __name__ == '__main__':
  app.run(debug=True, port=3000, host="0.0.0.0")



