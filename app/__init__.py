# import Flask class from flask module
from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager



# create instance of app variable
app = Flask(__name__)


# all other variable instanes need to come after the app instance
bootstrap = Bootstrap(app)
app.config.from_object(Config)


# app variagles for database usage
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# app variables for login
# login = LoginManager(app)

# when a page requires somebody to login, the application will isntead route them to the correct route described below
# login.login_view = 'login'


# once app variable is created, import the routes to load home page
from app import routes
