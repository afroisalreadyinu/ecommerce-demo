import unittest
from collections import namedtuple

from ecomm_demo.views import UserApplication

UserRow = namedtuple('UserRow', 'email pw_hash company')

class MockUserTable:

    def new_row(self, email, pw_hash, company):
        return UserRow(email, pw_hash, company)

class TestuserApplication(unittest.TestCase):

    def test_signup_no_error(self):
        app = UserApplication(MockUserTable())
        user = app.signup('goofy@acme.com', 'testpass', 'Acme Inc')
        self.assertEqual(user.email, 'goofy@acme.com')
