#!/usr/bin/env python3

from models import db, Activity, Camper, Signup
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

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

@app.route('/campers', methods=['GET'])
def campers():
    if request.method == 'GET':
        campers=Camper.query.all()
        campers_list=[camper.to_dict() for camper in campers]
        response=make_response(
            jsonify(campers_list),
            200
        )
        return response
        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
