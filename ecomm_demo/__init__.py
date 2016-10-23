from flask import Flask, jsonify
from flask.ext.sqlalchemy import SQLAlchemy

class Config:
    SECRET_KEY = "notreallysecret"
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/facetweet.db'
    BASE_URL = "localhost:6001"

app = Flask('ecommerce-demo')
app.config.from_object(Config)
db = SQLAlchemy(app)

@app.route("/")
def index():
    return jsonify({})

def run_app():
    app.debug = True
    app.run(port=6001)

def create_db():
    with app.app_context():
        db.create_all()
