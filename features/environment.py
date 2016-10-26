import os
import sys
import tempfile
import json
from ecomm_demo import app
from ecomm_demo.run import create_db

class Client:
    def __init__(self, test_client):
        self.test_client = test_client

    def post_json(self, url, data):
        response = self.test_client.post(
            url, data=json.dumps(data), content_type='application/json')
        return response

    def __getattr__(self, attr):
        return getattr(self.test_client, attr)

def before_feature(context, feature):
    app.config['TESTING'] = True
    context.db, context.db_path = tempfile.mkstemp()
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///{}".format(context.db_path)
    create_db()
    context.client = Client(app.test_client())


def after_feature(context, feature):
    os.close(context.db)
    os.unlink(context.db_path)
