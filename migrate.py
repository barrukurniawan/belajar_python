from flask import Flask
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import datetime

app = Flask(__name__)

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="barru",
    password="SMAN60jakarta",
    hostname="barru.mysql.pythonanywhere-services.com",
    databasename="barru$default",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

from db import db

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

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

if __name__ == '__main__':
    db.init_app(app)
    manager.run()