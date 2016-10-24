from flask import Flask

class Config:
    SECRET_KEY = "notreallysecret"
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/facetweet.db'
    BASE_URL = "localhost:6001"

app = Flask('ecommerce-demo')
app.config.from_object(Config)

import ecomm_demo.views
