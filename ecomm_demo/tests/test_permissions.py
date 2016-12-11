import unittest
from werkzeug.exceptions import Unauthorized
from ecomm_demo import permissions
from ecomm_demo.user_application import UserApplication, CompanyApplication

from ecomm_demo.tests.common import (
    UserRow, MockUserTable,
    MockCompanyTable, MockSecurityContext
    )

class PermissionsTests(unittest.TestCase):

    def test_login_decorator_valid(self):
        users = MockUserTable([UserRow('test@test.com', 'testpass', 'Acme Inc')])
        user_app = UserApplication(users, None, None)
        logged_in = permissions.make_logged_in(user_app, {'email': 'test@test.com'})
        @logged_in
        def test_view(user):
            return user
        self.assertEqual(test_view(), users.existing[0])


    def test_login_decorator_valid(self):
        user_app = UserApplication(MockUserTable([]), None, None)
        logged_in = permissions.make_logged_in(user_app, {'email': 'test@test.com'})
        @logged_in
        def test_view(user):
            return user
        with self.assertRaises(Unauthorized):
            test_view()
