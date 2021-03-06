
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from db import db, app
from models import User
import datetime

sqldb = SQLAlchemy(app)
# app = Flask(__name__)
# app.config["DEBUG"] = True

# SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
#     username="barru",
#     password="SMAN60jakarta",
#     hostname="barru.mysql.pythonanywhere-services.com",
#     databasename="barru$default",
# )
# app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
# app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# db = SQLAlchemy(app)

# class User(db.Model):

#     __tablename__ = "user"

#     id = db.Column(db.BigInteger, primary_key=True)
#     name = db.Column(db.String(50), index=True)
#     email = db.Column(db.String(100), index=True, unique=True)
#     password = db.Column(db.String(100))
#     created_at = db.Column(db.DateTime, default=datetime.datetime.now())
#     updated_at = db.Column(db.DateTime, default=datetime.datetime.now())
#     deleted_at = db.Column(db.DateTime, nullable=True)

@app.route('/')
def hello_world():
    return 'Hello from Flask!'

@app.route('/register', methods=["POST"])
def create_message():
    register = User()

    print ("FORMNYAAAA")

    register.name = request.json['name']
    register.email = request.json['email']
    register.password = request.json['password']
    register.created_at = datetime.datetime.now()
    register.updated_at = datetime.datetime.now()

    print ('bismillah')
    print (register)

    db.session.add(register)
    db.session.commit()

    response = {
        "data": "berhasil",
        "message": "created user!",
        "status_code": 200
    }

    return response