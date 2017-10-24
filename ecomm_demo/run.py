from ecomm_demo.application import app
from ecomm_demo.models import db

import ecomm_demo.views

def run_app():
    app.debug = True
    app.run(port=6001)

def create_db():
    with app.app_context():
        db.create_all()
