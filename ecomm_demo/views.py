from flask import jsonify, request, session, abort
from sqlalchemy import exc
from passlib.apps import custom_app_context

from .models import db, User, Product, Company, Invitation
from .user_application import CompanyApplication, UserApplication, UserApplicationError
from .product_application import ProductApplication
from .application import app

company_app = CompanyApplication(Company, Invitation)
user_app = UserApplication(User, company_app, custom_app_context)
product_app = ProductApplication(Product)

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
                           company_label=data['company'])
    session['email'] = user.email
    return jsonify({'email':user.email,
                    'company': user.company.label})


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
    user = user_app.authenticate(session.get('email'))
    if not user:
        abort(401)
    data = request.get_json()
    for product in data:
        new_product = product_app.add_product(commit=True, company=user.company, **product)
    return jsonify({"status": "ok"})

@app.route("/products", methods=["GET"])
def get_products():
    user = user_app.authenticate(session.get('email'))
    if not user:
        abort(401)
    products = product_app.get_products(user.company)
    return jsonify([p.to_dict() for p in products])
