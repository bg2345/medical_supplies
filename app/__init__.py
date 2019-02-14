# import Flask class from flask module
from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config



# create instance of app variable
app = Flask(__name__)

# all other variable instanes need to come after the app instance
bootstrap = Bootstrap(app)
app.config.from_object(Config)

# once app variable is created, import the routes to load home page
from app import routes
