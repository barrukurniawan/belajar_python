
import datetime
from db import db
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)

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


class User(db.Model):

    __tablename__ = "user"

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(50), index=True)
    email = db.Column(db.String(100), index=True, unique=True)
    password = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now())
    deleted_at = db.Column(db.DateTime, nullable=True)