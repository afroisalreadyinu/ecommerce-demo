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


class Invitation(db.Model, EcommerceModel):
    __tablename__ = 'invitation'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), nullable=False)
    nonce = db.Column(db.String(), nullable=False)
    company_id = db.Column(
        db.Integer,
        db.ForeignKey('company.id', ondelete='RESTRICT'),
        nullable=False,
    )
    company = db.relationship(
        'Company',
        backref=db.backref('invitations', order_by=[email]),
        foreign_keys=[company_id],
    )


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

class Storage(db.Model, EcommerceModel):
    __tablename__ = 'storage'
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(), nullable=False)
    company_id = db.Column(
        db.Integer,
        db.ForeignKey('company.id', ondelete='RESTRICT'),
        nullable=False,
    )
    company = db.relationship(
        'Company',
        backref=db.backref('storage_locations', order_by=[id]),
        foreign_keys=[company_id],
    )

class Stock(db.Model, EcommerceModel):
    __tablename__ = 'stock'
    id = db.Column(db.Integer, primary_key=True)
    physical = db.Column(db.Integer, default=0, nullable=False)
    sold = db.Column(db.Integer, default=0, nullable=False)
    reserved = db.Column(db.Integer, default=0, nullable=False)
    storage_id = db.Column(
        db.Integer,
        db.ForeignKey('storage.id', ondelete='RESTRICT'),
        nullable=False,
    )
    storage = db.relationship(
        'Storage',
        backref=db.backref('stocks', order_by=[id]),
        foreign_keys=[storage_id],
    )
    product_id = db.Column(
        db.Integer,
        db.ForeignKey('product.id', ondelete='RESTRICT'),
        nullable=False,
    )
    product = db.relationship(
        'Product',
        backref=db.backref('stocks', order_by=[id]),
        foreign_keys=[product_id],
    )

    @classmethod
    def new_row(cls, **kwargs):
        kwargs.setdefault('physical', 0)
        kwargs.setdefault('sold', 0)
        kwargs.setdefault('reserved', 0)
        return super().new_row(**kwargs)
