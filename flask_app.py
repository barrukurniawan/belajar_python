
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from db import db, app
from models import User, Products, AuthToken, AuthRefreshToken
import datetime
import re
import time
import random
import string
import hashlib

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

@app.route('/daftar')
def login_page():
    return render_template("register.html")

@app.route('/register', methods=["POST"])
def create_user():
    register = User()

    regex_symbol = '[@_!#$%^&*()<>?/\|}{~:[\]]'
    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

    if (request.json['password']).strip() == "" or (request.json['name']).strip() == "" or (request.json['email']).strip() == "":
        response = {
            "data": "Email/Username/Password tidak boleh kosong",
            "message": "Gagal Registrasi",
            "status": 'FAILED_REGISTER'
        }
        return response

    if(re.search(regex_symbol, request.json['name'])) or (re.search(regex_symbol, request.json['password'])):
        response = {
            "data": "Nama atau password tidak valid",
            "message": "Tidak boleh mengandung symbol",
            "status": 'FAILED_REGISTER'
        }
        return response

    if "SELECT" in request.json['name'] or "SELECT" in request.json['password'] or "FROM" in request.json['name'] or "FROM" in request.json['password']:
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

@app.route('/update-profile', methods=["POST"])
def update_user():

    token = __validate_token(access_token=request.headers['Authorization'])
    if token is False:
        response = {
            "data": "User's not found",
            "message": "Email atau Password Anda Salah",
            "status": 'FAILED_LOGIN'
        }
        return response

    regex_symbol = '[@_!#$%^&*()<>?/\|}{~:[\]]'

    if (request.json['name']).strip() == "":
        response = {
            "data": "Email/Username/Password tidak boleh kosong",
            "message": "Gagal Update Profile",
            "status": 'FAILED_UPDATE_PROFILE'
        }
        return response

    if(re.search(regex_symbol, request.json['name'])):
        response = {
            "data": "Nama tidak valid",
            "message": "Tidak boleh mengandung symbol",
            "status": 'FAILED_UPDATE_PROFILE'
        }
        return response
    print (token['owner_id'])
    check_user = User.query.filter(User.deleted_at == None) \
                    .filter(User.id == token['owner_id']).first()

    if check_user is not None:
        check_user.name = request.json['name']
        check_user.updated_at = datetime.datetime.now()

        db.session.add(check_user)
        db.session.commit()

        response = {
            "data": "Username Anda menjadi " + str(check_user.name),
            "message": "Berhasil Perbarui Profile",
            "status": 'SUCCESS_UPDATE_PROFILE'
        }
        return response

    response = {
        "data": "Tidak berhasil perbarui username",
        "message": "Gagal Update Profile",
        "status": 'FAILED_UPDATE_PROFILE'
    }

    return response

@app.route('/delete-user', methods=["DELETE"])
def delete_user():

    token = __validate_token(access_token=request.headers['Authorization'])
    if token is False:
        response = {
            "data": "User's not found",
            "message": "Email atau Password Anda Salah",
            "status": 'FAILED_LOGIN'
        }
        return response

    regex_symbol = '[@_!#$%^&*()<>?/\|}{~:[\]]'

    if (request.json['password']).strip() == "":
        response = {
            "data": "Email/Username/Password tidak boleh kosong",
            "message": "Gagal Hapus Akun",
            "status": 'FAILED_DELETE_PROFILE'
        }
        return response

    if(re.search(regex_symbol, request.json['password'])):
        response = {
            "data": "Nama tidak valid",
            "message": "Tidak boleh mengandung symbol",
            "status": 'FAILED_DELETE_PROFILE'
        }
        return response

    check_user = User.query.filter(User.deleted_at == None) \
                    .filter(User.id == token['owner_id']).first()

    if request.json['password'] != check_user.password:
        response = {
            "data": "Salah Password",
            "message": "Gagal Hapus Akun",
            "status": 'FAILED_DELETE_PROFILE'
        }
        return response

    if check_user is not None:
        user_name = check_user.name
        check_user.deleted_at = datetime.datetime.now()

        db.session.add(check_user)
        db.session.commit()

        response = {
            "data": "Sedih melihatmu pergi " + str(user_name),
            "message": "Berhasil Hapus User",
            "status": 'SUCCESS_DELETE_PROFILE'
        }
        return response

    response = {
        "data": "Gajadi dihapus Ye Ye",
        "message": "Gagal Hapus Akun",
        "status": 'FAILED_DELETE_PROFILE'
    }

    return response

@app.route('/list-user', methods=["GET"])
def list_user():
    params=request.args

    customer = User.query.filter(User.deleted_at == None)

    current_page = 1
    limit_per_page = 5
    if "page" in params:
        if (params["page"]).strip() != "":
            current_page = int(params["page"])

    if "limit" in params:
        if (params["limit"]).strip() != "":
            limit_per_page = int(params["limit"])

    if 'username' in params:
        if (params['username']).strip() != '':
            customer = customer.filter(User.name.like("%{}%".format(params["username"])))

    if 'email' in params:
        if (params['email']).strip() != '':
            customer = customer.filter(User.email.like("%{}%".format(params["email"])))

    customer_paginate = customer.paginate(current_page, limit_per_page, error_out=False)
    # customer.all()

    data = []
    for x in customer_paginate.items:
        data.append({
            "username" : x.name,
            "email" : x.email
        })

    pagination = dict(
                    limit_per_page=limit_per_page,
                    current_page=current_page,
                    total_data=customer.count()
                )

    response = {
        "data": data,
        "message": "List of registered users",
        "status": 'SUCCESS_USER_LIST',
        "pagination": pagination,
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
        token = __save_token(user_id=int(check_user.id))

        response = {
            "data": "Welcome " + str(check_user.name),
            "message": "Anda Berhasil Login",
            "status": 'SUCCESS_LOGIN',
            "credentials": {
                "access_token": token["access_token"],
                "refresh_token": token["refresh_token"],
                "expired_in": int(token["access_token_expired_in"])
            }
        }

    return response

def __validate_token(access_token=None):
    http_headers = request.headers

    if access_token is None:
        access_token = http_headers["Authorization"]

    check_token = AuthToken.query.filter_by(token=access_token).first()
    db.session.commit()

    if check_token is not None:
        today = datetime.datetime.today()
        today_in_seconds = time.mktime(today.timetuple())
        if int(today_in_seconds) < int(check_token.expire_in):
            return {
                "status": True,
                "owner_id": check_token.user_id
            }
        else:
            return False
    else:
        return False

def __save_token(user_id):

    access_token = __generate_token(user_id=user_id)
    refresh_token = __generate_token(user_id=user_id)

    """ set expire time in microtime"""
    today = datetime.datetime.today()
    expire_in = today + datetime.timedelta(seconds=int(3600))
    expire_in_seconds = time.mktime(expire_in.timetuple())

    refresh_token_expire_in = today + datetime.timedelta(seconds=int(3600))
    refresh_token_expire_in_seconds = time.mktime(refresh_token_expire_in.timetuple())

    """ save access token """
    at = AuthToken()
    at.user_id = user_id
    at.token = access_token
    at.expire_in = expire_in_seconds
    at.created_at = datetime.datetime.now()
    db.session.add(at)
    db.session.commit()

    """ save refresh token """
    rt = AuthRefreshToken()
    rt.token = access_token
    rt.refresh_token = refresh_token
    rt.expire_in = refresh_token_expire_in_seconds
    rt.created_at = datetime.datetime.now()
    rt.updated_at = datetime.datetime.now()
    db.session.add(rt)
    db.session.commit()

    return {
        "access_token": access_token,
        "access_token_expired_in": at.expire_in,
        "refresh_token": refresh_token
    }

def __generate_token(user_id):

    prepare_token = "%s%s%s%s" % (str(time.time()), str(user_id), str(random.randint(100000, 999999)),
                                  'BARRUTAMPAN')
    token = hashlib.sha256(bytes(prepare_token, encoding='ascii')).hexdigest()

    return token