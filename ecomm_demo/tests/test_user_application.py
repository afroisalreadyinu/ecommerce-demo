import unittest
from collections import namedtuple
from sqlalchemy import exc

from ecomm_demo.user_application import UserApplication, UserApplicationError

UserRow = namedtuple('UserRow', 'email pw_hash company')

VALID_EMAIL = 'goofy@acme.com'
VALID_PASS = 'testpass'
VALID_COMPANY = 'Acme Inc'

class MockUserTable:

    def new_row(self, email, pw_hash, company):
        return UserRow(email, pw_hash, company)

class MockSecurityContext:
    def encrypt(self, password):
        return 'encrypted'

class TestuserApplication(unittest.TestCase):

    def test_signup_no_error(self):
        app = UserApplication(MockUserTable(), MockSecurityContext())
        user = app.signup(VALID_EMAIL, VALID_PASS, VALID_COMPANY)
        self.assertEqual(user.email, 'goofy@acme.com')


    def test_signup_error_on_empty_arg(self):
        app = UserApplication(MockUserTable(), MockSecurityContext())
        with self.assertRaises(UserApplicationError):
            user = app.signup('', 'testpass', 'Acme Inc')


    def test_signup_user_exists(self):
        class DuplicateUserMockTable:
            def new_row(self, *_, **__):
                raise exc.SQLAlchemyError()
        app = UserApplication(DuplicateUserMockTable(), MockSecurityContext())
        with self.assertRaises(UserApplicationError):
            app.signup(VALID_EMAIL, VALID_PASS, VALID_COMPANY)
