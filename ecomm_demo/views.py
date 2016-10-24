from flask import jsonify, request, session
from passlib.apps import custom_app_context

from ecomm_demo import app
from .models import db, User

@app.route("/")
def index():
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
