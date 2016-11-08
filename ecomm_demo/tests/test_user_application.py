import unittest
from collections import namedtuple
from sqlalchemy import exc

from ecomm_demo.user_application import (
    UserApplication,
    UserApplicationError,
    CompanyApplication
    )

UserRow = namedtuple('UserRow', 'email pw_hash company')

VALID_EMAIL = 'goofy@acme.com'
VALID_PASS = 'testpass'
VALID_COMPANY = 'Acme Inc'

class ResultSet:

    def __init__(self, result):
        self.result = result

    def one(self):
        if self.result:
            return self.result[0]
        raise exc.SQLAlchemyError()

class MockUserTable:

    def __init__(self, existing=None):
        self.existing = existing or []

    def new_row(self, email, pw_hash, company, commit):
        return UserRow(email, pw_hash, company)

    @property
    def query(self):
        return self

    def filter_by(self, **filters):
        return ResultSet(self.existing)

class MockSecurityContext:

    def __init__(self, fail=False):
        self.fail = fail

    def encrypt(self, password):
        return 'encrypted'

    def verify(self, password, hash):
        return not self.fail


class TestuserApplication(unittest.TestCase):

    def test_signup_no_error(self):
        app = UserApplication(MockUserTable(),
                              CompanyApplication(),
                              MockSecurityContext())
        user = app.signup(VALID_EMAIL, VALID_PASS, VALID_COMPANY)
        self.assertEqual(user.email, 'goofy@acme.com')


    def test_signup_error_on_empty_arg(self):
        app = UserApplication(MockUserTable(),
                              CompanyApplication(),
                              MockSecurityContext())
        with self.assertRaises(UserApplicationError):
            user = app.signup('', 'testpass', 'Acme Inc')


    def test_signup_user_exists(self):
        class DuplicateUserMockTable:
            def new_row(self, *_, **__):
                raise exc.SQLAlchemyError()
        app = UserApplication(DuplicateUserMockTable(),
                              CompanyApplication(),
                              MockSecurityContext())
        with self.assertRaises(UserApplicationError):
            app.signup(VALID_EMAIL, VALID_PASS, VALID_COMPANY)


    def test_login_no_error(self):
        existing = [UserRow(VALID_EMAIL, VALID_PASS, VALID_COMPANY)]
        app = UserApplication(MockUserTable(existing=existing),
                              CompanyApplication(),
                              MockSecurityContext())
        user = app.login(VALID_EMAIL, VALID_PASS)
        self.assertEqual(user.email, VALID_EMAIL)


    def test_login_empty_string(self):
        existing = [UserRow(VALID_EMAIL, VALID_PASS, VALID_COMPANY)]
        app = UserApplication(MockUserTable(existing=existing),
                              CompanyApplication(),
                              MockSecurityContext())
        with self.assertRaises(UserApplicationError):
            user = app.login('', '')

    def test_login_none_on_wrong_password(self):
        existing = [UserRow(VALID_EMAIL, VALID_PASS, VALID_COMPANY)]
        app = UserApplication(MockUserTable(existing=existing),
                              CompanyApplication(),
                              MockSecurityContext(fail=True))
        self.assertIsNone(app.login(VALID_EMAIL, VALID_PASS))

    def test_login_none_on_user_nonexistent(self):
        app = UserApplication(MockUserTable(),
                              CompanyApplication(),
                              MockSecurityContext())
        self.assertIsNone(app.login(VALID_EMAIL, VALID_PASS))
