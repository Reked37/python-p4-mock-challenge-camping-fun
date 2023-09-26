#!/usr/bin/env python3

from models import db, Activity, Camper, Signup
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os
import ipdb
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api=Api(app)

@app.route('/')
def home():
    return 'Hello Campers!!'

#Campers
@app.route('/campers', methods=['GET', 'POST'])
def campers():
    if request.method == 'GET':
        campers_list=[camper.to_dict() for camper in Camper.query.all()]
        response=make_response(
            jsonify(campers_list),
            200
        )
        return response
    elif request.method == 'POST':
        try:
            new_camper=Camper(
                name=request.get_json()['name'],
                age=request.get_json()['age']
            )
            db.session.add(new_camper)
            db.session.commit()
            camper_dict=new_camper.to_dict()
        
            response=make_response(
                jsonify(camper_dict),
                201
            )
            return response
        except:
            return jsonify({"errors": 'validation errors'}), 400

@app.route('/campers/<int:id>', methods=['PATCH', 'GET'])
def campers_by_id(id):
    if request.method == 'GET':
        camper=Camper.query.filter_by(id=id).first()

        if not camper:
            return {"error": "Camper not found"}, 404

        # camper_data=camper.to_dict(rules='signups',)
        camper_data=camper.to_dict(rules=['-signups.camper',])

        response=make_response(
            jsonify(camper_data),
            200
        )
        return response
    elif request.method == 'PATCH':
        camper= Camper.query.filter_by(id=id).first()
        if not camper:
            return {"error":"Camper not found"}, 404

        try:
            data= request.get_json()
            for attr, value in data.items():
                setattr(camper, attr, value)
            db.session.add(camper)
            db.session.commit()
            camper_dict=camper.to_dict()
            response=make_response(jsonify(camper_dict),202)
            return response
        except:
            return {"errors": ['validation errors']}, 400

#Activities
@app.route('/activities')
def get_activities():
    activities=Activity.query.all()
    activities_dict=[activity.to_dict() for activity in activities]
    return jsonify(activities_dict), 200

@app.route('/activities/<int:id>', methods=['DELETE'])
def delete_activities_by_id(id):
    activity=Activity.query.filter_by(id=id).first()
    try:
        db.session.delete(activity)
        db.session.commit()
        response_body={
            "delete_successful": True,
            "message":"Activity deleted."
     }

        response=make_response(
            response_body,
            204
        )
        return response
    except:
        return {"error": "Activity not found"}, 404

#Signups
@app.route('/signups', methods=['POST'])
def post_signups():
    try:
        new_signup=Signup(
            time=request.get_json()['time'],
            activity_id=request.get_json()['activity_id'],
            camper_id=request.get_json()['camper_id'],
        )
        db.session.add(new_signup)
        db.session.commit()
        signup_dict=new_signup.to_dict()
        return jsonify(signup_dict), 201
    except:
        return {"errors":["validation errors"]}, 400

if __name__ == '__main__':
    app.run(port=5555, debug=True)
