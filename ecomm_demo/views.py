from flask import jsonify, request, session, abort
from sqlalchemy import exc
from passlib.apps import custom_app_context

from ecomm_demo import app
from .models import db, User, Product

@app.teardown_request
def teardown_request(exception):
    if exception:
        db.session.rollback()
        db.session.remove()
    else:
        db.session.commit()
        db.session.remove()


class UserApplicationError(Exception):
    pass

class UserApplication:
    def __init__(self, table):
        self.table = table

    def signup(self, email, password, company):
        if any(x.strip() == '' for x in (email, password, company)):
            raise UserApplicationError('Invalid input for user signup')
        user = self.table.new_row(email=email,
                                  pw_hash=custom_app_context.encrypt(password),
                                  company=company)
        return user

user_app = UserApplication(User)

@app.route("/")
def index():
    if 'email' in session:
        return jsonify({'email': session['email']})
    return jsonify({})

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    pw_hash = custom_app_context.encrypt(data['password'])
    user = user_app.signup(email=data['email'],
                           password=data['password'],
                           company=data['company'])
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
    return jsonify({"status": "ok"})

@app.route("/products", methods=["GET"])
def get_products():
    def to_dict(p):
        return {'id': p.id, 'label': p.label, 'gtin': p.gtin}
    products = Product.query.all()
    return jsonify([to_dict(p) for p in products])
