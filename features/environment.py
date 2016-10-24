import os
import sys
import tempfile
from ecomm_demo import app
from ecomm_demo.run import create_db

def before_feature(context, feature):
    app.config['TESTING'] = True
    context.db, context.db_path = tempfile.mkstemp()
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///{}".format(context.db_path)
    create_db()
    context.client = app.test_client()


def after_feature(context, feature):
    os.close(context.db)
    os.unlink(context.db_path)
