
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

class Products(db.Model):

    __tablename__ = "products"

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(50), index=True)
    price = db.Column(db.BigInteger, default=0)
    stock = db.Column(db.BigInteger, default=0)
    description = db.Column(db.String(150))
    categories = db.Column(db.String(100))
    merchant_name = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now())
    deleted_at = db.Column(db.DateTime, nullable=True)

class AuthToken(db.Model):

    __tablename__ = "auth_token"

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.Integer, index=True)
    token = db.Column(db.String(128), unique=True)
    expire_in = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())


class AuthRefreshToken(db.Model):

    __tablename__ = "auth_refresh_token"

    id = db.Column(db.BigInteger, primary_key=True)
    refresh_token = db.Column(db.String(128), unique=True)
    token = db.Column(db.String(128))
    expire_in = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now())
    deleted_at = db.Column(db.DateTime, nullable=True)

class AccessAddress(db.Model):

    __tablename__ = "access_address"

    id = db.Column(db.BigInteger, primary_key=True)
    ip_address = db.Column(db.String(128), unique=True)
    count = db.Column(db.Integer)
    expired_at = db.Column(db.DateTime, default=datetime.datetime.now())