from flask import Flask

class Config:
    SECRET_KEY = "notreallysecret"
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/facetweet.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    BASE_URL = "localhost:6001"

app = Flask('ecommerce-demo')
app.config.from_object(Config)

#-----------------------------------------

from flask import jsonify
from .user_application import UserApplicationError

@app.errorhandler(Exception)
def application_error(exc):
    if isinstance(exc, UserApplicationError):
        return jsonify({'error': exc.args[0]}), 400
