from flask import jsonify, request, session, abort
from sqlalchemy import exc
from passlib.apps import custom_app_context

from ecomm_demo import app
from .models import db, User

@app.route("/")
def index():
    if 'email' in session:
        return jsonify({'email': session['email']})
    return jsonify({})

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    pw_hash = custom_app_context.encrypt(data['password'])
    user = User(email=data['email'],
                pw_hash=pw_hash,
                company=data['company'])
    db.session.add(user)
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
