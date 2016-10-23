import os
import sys
import tempfile
from ecomm_demo import app, create_db

def before_feature(context, feature):
    app.config['TESTING'] = True
    context.db, app.config['DATABASE'] = tempfile.mkstemp()
    create_db()
    context.client = app.test_client()


def after_feature(context, feature):
    os.close(context.db)
    os.unlink(app.config['DATABASE'])
