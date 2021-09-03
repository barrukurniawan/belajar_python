
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from db import db, app
from models import User
import datetime
import re

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

@app.route('/login')
def login_page():
    return render_template("register.html")

@app.route('/register', methods=["POST"])
def create_message():
    register = User()

    regex_symbol = '[@_!#$%^&*()<>?/\|}{~:[\]]'
    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

    if(re.search(regex_symbol, request.json['name'])) or (re.search(regex_symbol, request.json['password'])):
        response = {
            "data": "Nama atau password tidak valid",
            "message": "Tidak boleh mengandung symbol",
            "status": 'FAILED_REGISTER'
        }
        return response

    if(re.search(regex, request.json['email'])):
        print ("valid email")
    else:
        response = {
            "data": "Email tidak valid",
            "message": "Cek kembali email anda",
            "status": 'FAILED_REGISTER'
        }
        return response

    check_user = User.query.filter(User.deleted_at == None) \
                    .filter(User.email == request.json['email']).first()

    if check_user is not None:
        response = {
            "data": "Email sudah terdaftar, gunakan Email lain",
            "message": "Gagal Registrasi",
            "status": 'FAILED_REGISTER'
        }
        return response

    register.name = request.json['name']
    register.email = request.json['email']
    register.password = request.json['password']
    register.created_at = datetime.datetime.now()
    register.updated_at = datetime.datetime.now()

    db.session.add(register)
    db.session.commit()

    response = {
        "data": "berhasil",
        "message": "created user!",
        "status": 'SUCCESS_REGISTER'
    }

    return response

@app.route('/list-user', methods=["GET"])
def list_user():
    customer = User.query.filter(User.deleted_at == None).all()

    data = []
    for x in customer:
        data.append({
            "username" : x.name,
            "email" : x.email
        })

    response = {
        "data": data,
        "message": "list user!",
        "status": 'SUCCESS_USER_LIST'
    }

    return response

@app.route('/login', methods=["POST"])
def login():
    response = {
        "data": "User's not found",
        "message": "Email atau Password Anda Salah",
        "status": 'FAILED_LOGIN'
    }

    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    regex_symbol = '[@_!#$%^&*()<>?/\|}{~:[\]]'


    if(re.search(regex, request.json['email'])):
        print ("valid email")
    else:
        response = {
            "data": "Email tidak valid",
            "message": "Cek kembali email anda",
            "status": 'FAILED_LOGIN'
        }
        return response

    if(re.search(regex_symbol, request.json['password'])):
        response = {
            "data": "Password tidak valid",
            "message": "Tidak boleh mengandung symbol",
            "status": 'FAILED_LOGIN'
        }
        return response

    check_user = User.query.filter(User.deleted_at == None) \
                    .filter(User.email == request.json['email']) \
                    .filter(User.password == request.json['password']).first()

    if check_user is not None:
        response = {
            "data": "Welcome " + str(check_user.name),
            "message": "Anda Berhasil Login",
            "status": 'SUCCESS_LOGIN'
        }

    return response