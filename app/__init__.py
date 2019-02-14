# import Flask class from flask module
from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy



# create instance of app variable
app = Flask(__name__)


# all other variable instanes need to come after the app instance
bootstrap = Bootstrap(app)
app.config.from_object(Config)


# app variagles for database usage
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# once app variable is created, import the routes to load home page
from app import routes
