from flask import Flask
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

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

if __name__ == '__main__':
    db.init_app(app)
    manager.run()