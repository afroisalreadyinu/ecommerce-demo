from os.path import abspath, join
from flask import Flask

class Config:
    SECRET_KEY = "notreallysecret"
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/facetweet.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    BASE_URL = "localhost:6001"

js_dir = abspath(join(__file__, '../static/'))
app = Flask('ecommerce-demo',
            static_folder=js_dir,
            static_url_path='/static')
app.config.from_object(Config)

#-----------------------------------------

from flask import jsonify
from .user_application import UserApplicationError

@app.errorhandler(Exception)
def application_error(exc):
    if isinstance(exc, UserApplicationError):
        return jsonify({'error': exc.args[0]}), 400
    #if we can't handle it, leave it to flask
    raise exc
