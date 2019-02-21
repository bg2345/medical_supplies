# hold all configuration variables for this application here
# should not be uploaded to github with sensitive information
# when uploading to heroku, use import or .get() methods
import os


# define the root/base of this project folder
BASEDIR = os.path.abspath(os.path.dirname(__file__))



class Config(object):
    # secret key is necessary for fors in flask, it is a security measure to protect against attacks like CSRF
    # it should never be given out, and should be something that is difficult to break
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'


# # setup our database URI, which is the location of our database file/server
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABSE_URL') or \
#         'sqlite:///' + os.path.join(BASEDIR, 'app.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # uri for postgres local databse
    # not for Heroku usage yet
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABSE_URL') or \
    'postgresql://postgres:BRUINS4@localhost:5432/ecommerce'
