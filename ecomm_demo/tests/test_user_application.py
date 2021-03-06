import unittest
from collections import namedtuple
from sqlalchemy import exc

from ecomm_demo.user_application import (
    UserApplication,
    UserApplicationError,
    CompanyApplication,
    create_invitation_nonce
    )
from common import (
    MockTable, MockUserTable, MockCompanyTable,
    MockSecurityContext, UserRow, CompanyRow)

InvitationRow = namedtuple('InvitationRow', 'nonce company email')

VALID_EMAIL = 'goofy@acme.com'
VALID_PASS = 'testpass'
VALID_COMPANY = 'Acme Inc'

class MockInvitationTable(MockTable):
    ROW_CLASS = InvitationRow


class TestuserApplication(unittest.TestCase):

    def test_signup_no_error(self):
        app = UserApplication(MockUserTable(),
                              CompanyApplication(MockCompanyTable(), None),
                              MockSecurityContext())
        user = app.signup(VALID_EMAIL, VALID_PASS, VALID_COMPANY)
        self.assertEqual(user.email, 'goofy@acme.com')


    def test_signup_error_on_empty_arg(self):
        app = UserApplication(MockUserTable(),
                              CompanyApplication(None, None),
                              MockSecurityContext())
        with self.assertRaises(UserApplicationError):
            user = app.signup('', 'testpass', 'Acme Inc')


    def test_signup_user_exists(self):
        class DuplicateUserMockTable:
            def new_row(self, *_, **__):
                raise exc.SQLAlchemyError()
        mock_company_table = MockCompanyTable()
        app = UserApplication(DuplicateUserMockTable(),
                              CompanyApplication(mock_company_table, None),
                              MockSecurityContext())
        with self.assertRaises(UserApplicationError):
            app.signup(VALID_EMAIL, VALID_PASS, VALID_COMPANY)



    def test_login_no_error(self):
        existing = [UserRow(VALID_EMAIL, VALID_PASS, VALID_COMPANY)]
        app = UserApplication(MockUserTable(existing=existing),
                              CompanyApplication(None, None),
                              MockSecurityContext())
        user = app.login(VALID_EMAIL, VALID_PASS)
        self.assertEqual(user.email, VALID_EMAIL)


    def test_login_empty_string(self):
        existing = [UserRow(VALID_EMAIL, VALID_PASS, VALID_COMPANY)]
        app = UserApplication(MockUserTable(existing=existing),
                              CompanyApplication(None, None),
                              MockSecurityContext())
        with self.assertRaises(UserApplicationError):
            user = app.login('', '')

    def test_login_none_on_wrong_password(self):
        existing = [UserRow(VALID_EMAIL, VALID_PASS, VALID_COMPANY)]
        app = UserApplication(MockUserTable(existing=existing),
                              CompanyApplication(None, None),
                              MockSecurityContext(fail=True))
        self.assertIsNone(app.login(VALID_EMAIL, VALID_PASS))

    def test_login_none_on_user_nonexistent(self):
        app = UserApplication(MockUserTable(),
                              CompanyApplication(None, None),
                              MockSecurityContext())
        self.assertIsNone(app.login(VALID_EMAIL, VALID_PASS))

    def test_authenticate_false(self):
        app = UserApplication(MockUserTable(),
                              CompanyApplication(None, None),
                              MockSecurityContext())
        self.assertIsNone(app.authenticate(VALID_EMAIL))
        self.assertIsNone(app.authenticate(None))
        self.assertIsNone(app.authenticate(' '))

    def test_authenticate_true(self):
        user = UserRow(VALID_EMAIL, VALID_PASS, VALID_COMPANY)
        app = UserApplication(MockUserTable([user]),
                              CompanyApplication(None, None),
                              MockSecurityContext())
        self.assertEqual(app.authenticate(VALID_EMAIL), user)


class TestCompanyApplication(unittest.TestCase):

    def test_get_company_empty(self):
        app = CompanyApplication(MockCompanyTable(), None)
        self.assertIsNone(app.get('puma'))

    def test_get_company(self):
        companies = [CompanyRow('puma')]
        app = CompanyApplication(MockCompanyTable(companies), None)
        self.assertEqual(app.get('puma'), companies[0])

    def test_create_company(self):
        table = MockCompanyTable()
        app = CompanyApplication(table, None)
        self.assertEqual(app.create('puma').label, 'puma')
        self.assertEqual(len(table.existing), 1)
        self.assertEqual(table.existing[0].label, 'puma')

    def test_invite_creates_email(self):
        user = UserRow(VALID_EMAIL, VALID_PASS, CompanyRow(label=VALID_COMPANY))
        app = CompanyApplication(MockCompanyTable(), MockInvitationTable())
        email = app.invite_to_company(user, 'invitee@puma.com')
        self.assertEqual(email.recipient, 'invitee@puma.com')

    def test_invite_creates_invitation(self):
        user = UserRow(VALID_EMAIL, VALID_PASS, CompanyRow(label=VALID_COMPANY))
        invitation_table = MockInvitationTable()
        app = CompanyApplication(MockCompanyTable(), invitation_table)
        app.invite_to_company(user, 'invitee@puma.com')
        self.assertEqual(len(invitation_table.existing), 1)
        invitation = invitation_table.existing[0]
        self.assertEqual(invitation.email, 'invitee@puma.com')
        self.assertEqual(invitation.company, user.company)
        self.assertEqual(len(invitation.nonce), 11, invitation.nonce)

    def test_nonce_generator(self):
        self.assertNotEqual(create_invitation_nonce(),
                            create_invitation_nonce())

    def test_get_invitations(self):
        company = CompanyRow(label=VALID_COMPANY)
        invitation_table = MockInvitationTable([
            InvitationRow(email='invitee1@x.com', nonce='123', company=company),
            InvitationRow(email='invitee2@y.com',
                          nonce='456',
                          company=CompanyRow(label='Other company'))
        ])
        app = CompanyApplication(MockCompanyTable(), invitation_table)
        invitations = list(app.get_invitations(company))
        self.assertEqual(len(invitations), 1)
        self.assertEqual(invitations[0].email, 'invitee1@x.com')

    def test_get_invitation_by_nonce(self):
        company = CompanyRow(label=VALID_COMPANY)
        invitation_table = MockInvitationTable([
            InvitationRow(email='invitee1@x.com', nonce='123', company=None),
            InvitationRow(email='invitee2@y.com', nonce='456', company=None)
        ])
        app = CompanyApplication(MockCompanyTable(), invitation_table)
        invitation = app.get_by_nonce('123')
        self.assertEqual(invitation.email, 'invitee1@x.com')

    def test_get_invitation_by_nonce_none_on_empty(self):
        app = CompanyApplication(MockCompanyTable(), MockInvitationTable())
        self.assertIsNone(app.get_by_nonce('123'))
