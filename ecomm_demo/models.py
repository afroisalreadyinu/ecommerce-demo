from flask.ext.sqlalchemy import SQLAlchemy
from ecomm_demo import app

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    email = db.Column(db.String(), primary_key=True)
    pw_hash = db.Column(db.String(), nullable=False)
    company = db.Column(db.String(), nullable=False)
