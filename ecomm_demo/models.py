from flask_sqlalchemy import SQLAlchemy
from ecomm_demo.application import app

db = SQLAlchemy(app)

class EcommerceModel:

    @classmethod
    def new_row(cls, *args, commit=False, **kwargs):
        row = cls(*args, **kwargs)
        db.session.add(row)
        if commit:
            db.session.commit()
        return row

class User(db.Model, EcommerceModel):
    __tablename__ = 'user'
    email = db.Column(db.String(), primary_key=True)
    pw_hash = db.Column(db.String(), nullable=False)
    company_id = db.Column(
        db.Integer,
        db.ForeignKey('company.id', ondelete='RESTRICT'),
        nullable=False,
    )
    company = db.relationship(
        'Company',
        backref=db.backref('members', order_by=[email]),
        foreign_keys=[company_id],
    )

class Company(db.Model, EcommerceModel):
    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(), nullable=False)


class Product(db.Model, EcommerceModel):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(), nullable=False)
    gtin = db.Column(db.String(14), nullable=False)
    company_id = db.Column(
        db.Integer,
        db.ForeignKey('company.id', ondelete='RESTRICT'),
        nullable=False,
    )
    company = db.relationship(
        'Company',
        backref=db.backref('products', order_by=[id]),
        foreign_keys=[company_id],
    )
