from flask import jsonify, request, session, abort
from sqlalchemy import exc
from passlib.apps import custom_app_context

from .models import db, User, Product, Company, Invitation, Storage, Stock
from .user_application import CompanyApplication, UserApplication, UserApplicationError
from .product_application import ProductApplication, StorageApplication
from .application import app
from .permissions import make_logged_in

company_app = CompanyApplication(Company, Invitation)
user_app = UserApplication(User, company_app, custom_app_context)
product_app = ProductApplication(Product, Stock)
storage_app = StorageApplication(Storage)

logged_in = make_logged_in(user_app, session)

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
    return jsonify({"email":user.email, "company":user.company.label})

@app.route('/invite', methods=['POST'])
@logged_in
def invite(user):
    data = request.get_json()
    invitation = company_app.invite_to_company(user, data['invitee_email'])
    return jsonify({'recipient': invitation.recipient})

@app.route('/invite', methods=['GET'])
@logged_in
def get_invitations(user):
    invitations = [{'email':i.email, 'nonce':i.nonce}
                   for i in company_app.get_invitations(user.company)]
    return jsonify(invitations)

@app.route('/signup-with-invitation', methods=['POST'])
def signup_with_invitation():
    data = request.get_json()
    invitation = company_app.get_by_nonce(data['nonce'])
    if invitation is None:
        abort(401)
    user = user_app.signup(invitation.email,
                           data['password'],
                           invitation.company.label)
    return jsonify({'status': 'OK'})


@app.route("/products", methods=["POST"])
@logged_in
def add_products(user):
    data = request.get_json()
    for product in data:
        new_product = product_app.add_product(commit=True, company=user.company, **product)
    return jsonify({"status": "ok"})

@app.route("/products", methods=["GET"])
@logged_in
def get_products(user):
    user = user_app.authenticate(session.get('email'))
    if not user:
        abort(401)
    products = product_app.get_products(user.company)
    return jsonify([p.to_dict() for p in products])

@app.route("/storage", methods=["POST"])
@logged_in
def new_storage(user):
    data = request.get_json()
    storage = storage_app.new_storage_location(data['label'], user.company)
    return jsonify({'label': storage.label, 'id': storage.id})

@app.route("/storage", methods=["GET"])
@logged_in
def list_storage_locations(user):
    storages = storage_app.get_all_for_company(user.company)
    return jsonify([{'id': x.id, 'label':x.label} for x in storages])

@app.route("/storage/<storage_id>/intake", methods=['POST'])
@logged_in
def stock_intake(user, storage_id):
    data = request.get_json()
    storage = storage_app.get_for_company(user.company, storage_id)
    if not storage:
        abort(404)
    new_stocks = product_app.intake_for_product_list(storage, data)
    return jsonify(new_stocks)
