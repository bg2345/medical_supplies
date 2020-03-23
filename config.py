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

    STRIPE_SECRET_KEY = 'sk_test_mS3YPTSkwtC2aybEht1QpRjS'


# # setup our database URI, which is the location of our database file/server
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABSE_URL') or \
#         'sqlite:///' + os.path.join(BASEDIR, 'app.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # uri for postgres local databse
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

    # mail variables for Google account
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = 1
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['bgardynski@gmail.com']
