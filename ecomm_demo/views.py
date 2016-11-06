from flask import jsonify, request, session, abort
from sqlalchemy import exc
from passlib.apps import custom_app_context

from ecomm_demo import app
from .models import db, User, Product

@app.route("/")
def index():
    if 'email' in session:
        return jsonify({'email': session['email']})
    return jsonify({})

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    pw_hash = custom_app_context.encrypt(data['password'])
    user = User.new_row(email=data['email'],
                        pw_hash=pw_hash,
                        company=data['company'])
    db.session.commit()
    session['email'] = user.email
    return jsonify({'email':user.email,
                    'company': user.company})


@app.route("/logout")
def logout():
    if session['email']:
        del session['email']
    return jsonify({})

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    try:
        user = User.query.filter_by(email=data['email']).one()
    except exc.SQLAlchemyError:
        abort(401)
    if custom_app_context.verify(data['password'], user.pw_hash):
        session['email'] = user.email
        return jsonify({"email":user.email})
    else:
        abort(401)

@app.route("/products", methods=["POST"])
def add_products():
    data = request.get_json()
    for product in data:
        product = Product.new_row(**product)
    db.session.commit()
    return jsonify({"status": "ok"})

@app.route("/products", methods=["GET"])
def get_products():
    def to_dict(p):
        return {'id': p.id, 'label': p.label, 'gtin': p.gtin}
    products = Product.query.all()
    return jsonify([to_dict(p) for p in products])
