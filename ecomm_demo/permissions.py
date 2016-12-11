from functools import wraps
from flask import abort

def make_logged_in(user_app, session):
    def logged_in(view):
        @wraps(view)
        def replacement(*args, **kwargs):
            user = user_app.authenticate(session.get('email'))
            if not user:
                abort(401)
            return view(user, *args, **kwargs)
        return replacement
    return logged_in
