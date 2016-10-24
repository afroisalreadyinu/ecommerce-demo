from ecomm_demo import app
from ecomm_demo.models import db

def run_app():
    init_app()
    app.debug = True
    app.run(port=6001)

def create_db():
    with app.app_context():
        db.create_all()
