import os
from base64 import b64encode

from sqlalchemy import exc

import attr

class UserApplicationError(Exception):
    pass

@attr.s
class Email:
    recipient = attr.ib()
    subject = attr.ib()
    content = attr.ib()

def create_invitation_nonce():
    random_bytes = os.urandom(8)
    return b64encode(random_bytes).decode('utf-8')[:-1]

class CompanyApplication:

    def __init__(self, company_table, invitation_table):
        self.company_table = company_table
        self.invitation_table = invitation_table

    def get(self, label):
        try:
            company = self.company_table.query.filter_by(label=label).one()
        except exc.SQLAlchemyError:
            return None
        else:
            return company

    def create(self, label):
        return self.company_table.new_row(label=label)

    def invite_to_company(self, current, invitee_email):
        subject = "Please join Ecommerce Demo"
        content = "{} has invited you to join {}.".format(current.email, current.company.label)
        invitation = self.invitation_table.new_row(
            nonce=create_invitation_nonce(),
            company=current.company,
            email=invitee_email)
        return Email(invitee_email, subject, content)

    def get_invitations(self, company):
        return self.invitation_table.query.filter_by(company=company)

    def get_by_nonce(self, nonce):
        try:
            return self.invitation_table.query.filter_by(nonce=nonce).one()
        except exc.SQLAlchemyError:
            return None

class UserApplication:

    def __init__(self, user_table, company_app, security_context):
        self.user_table = user_table
        self.company_app = company_app
        self.security_context = security_context

    def signup(self, email, password, company_label):
        if any(x.strip() == '' for x in (email, password, company_label)):
            raise UserApplicationError('Invalid input for user signup')
        try:
            company = self.company_app.get(company_label)
            if company is None:
                company = self.company_app.create(company_label)
            user = self.user_table.new_row(
                email=email,
                pw_hash=self.security_context.encrypt(password),
                company=company)
            self.user_table.commit()
        except exc.SQLAlchemyError:
            raise UserApplicationError('User exists')
        return user


    def login(self, email, password):
        if any(x.strip() == '' for x in (email, password)):
            raise UserApplicationError('Invalid input for user signup')
        try:
            user = self.user_table.query.filter_by(email=email).one()
        except exc.SQLAlchemyError:
            return None
        if self.security_context.verify(password, user.pw_hash):
            return user
        else:
            return None

    def authenticate(self, email):
        if not email:
            return None
        try:
            user = self.user_table.query.filter_by(email=email).one()
        except exc.SQLAlchemyError:
            return None
        return user
