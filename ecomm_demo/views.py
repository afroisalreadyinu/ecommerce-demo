from flask import jsonify, request, session, abort
from sqlalchemy import exc
from passlib.apps import custom_app_context

from .models import db, User, Product
from .user_application import UserApplication, UserApplicationError
from .application import app


user_app = UserApplication(User, custom_app_context)

@app.route("/")
def index():
    if 'email' in session:
        return jsonify({'email': session['email']})
    return jsonify({})

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    user = user_app.signup(email=data['email'],
                           password=data['password'],
                           company=data['company'])
    session['email'] = user.email
    return jsonify({'email':user.email,
                    'company': user.company})


@app.route("/logout")
def logout():
    if 'email' in session:
        del session['email']
    return jsonify({})

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = user_app.login(data['email'], data['password'])
    if not user:
        abort(401)
    session['email'] = user.email
    return jsonify({"email":user.email})

@app.route("/products", methods=["POST"])
def add_products():
    data = request.get_json()
    for product in data:
        product = Product.new_row(commit=True, **product)
    return jsonify({"status": "ok"})

@app.route("/products", methods=["GET"])
def get_products():
    def to_dict(p):
        return {'id': p.id, 'label': p.label, 'gtin': p.gtin}
    products = Product.query.all()
    return jsonify([to_dict(p) for p in products])
