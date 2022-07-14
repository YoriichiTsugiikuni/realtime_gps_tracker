from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_pymongo import PyMongo
from marshmallow import Schema, ValidationError,fields
from bson.json_util import dumps
from json import loads
import os
from dotenv import load_dotenv
from datetime import datetime





  
load_dotenv()

info = {}

app = Flask(__name__)
CORS(app)
#setup location of database
app.config["MONGO_URI"] = "mongodb+srv://rtvtracker:hinokamikagura@rtvgpssystem.zrtglzc.mongodb.net/?retryWrites=true&w=majority" 
mongo = PyMongo(app)


#Rules database information has to conform to
class TankSchema(Schema):
    lat = fields.String(required=True)
    long = fields.String(required=True)
    dateTime = fields.DateTime(required=True)


@app.route("/tank", methods = ["POST"])
def add_new_tank():
    request_dict = request.json

    new_gps = TankSchema().load(request_dict)
    gps_document=mongo.db.gps.insert_one(new_gps)
    gps_id=gps_document.inserted_id
    gps=mongo.db.gps_data.find_one({"_id":gps_id})
    gps_json=loads(dumps(gps))
       
    return jsonify(gps_json)


    
    # tank_document = mongo.db.tanks.insert_one(new_tank)
    # tank_id = tank_document.inserted_id

    # tank = mongo.db.tanks.find_one({"_id": tank_id})

    # tank_json = loads(dumps(tank))

    # status = False
    # if TankSchema.percentage_full >=80 :
    #     if TankSchema.percentage_full<=100 :
    #     {
    #         status = True
    #     }

    #     else:
    #     {
    #         status = False
    #     }
    # }

#     now = datetime.now()
#     current_time = now.strftime("%H:%M:%S")
    
# return {"led": status, "msg": "Data was saved in database successfully", "date": "current_time"} 


if __name__ == '__main__':
  app.run(debug=True, port=3000, host="0.0.0.0")



