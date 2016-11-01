from flask.ext.sqlalchemy import SQLAlchemy
from ecomm_demo import app

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    email = db.Column(db.String(), primary_key=True)
    pw_hash = db.Column(db.String(), nullable=False)
    company = db.Column(db.String(), nullable=False)

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(), nullable=False)
    gtin = db.Column(db.String(14), nullable=False)
