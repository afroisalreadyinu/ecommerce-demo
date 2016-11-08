from sqlalchemy import exc

class UserApplicationError(Exception):
    pass

class CompanyApplication:

    def __init__(self, company_table):
        self.company_table = company_table

class UserApplication:
    def __init__(self, user_table, company_app, security_context):
        self.user_table = user_table
        self.company_app = company_app
        self.security_context = security_context

    def signup(self, email, password, company):
        if any(x.strip() == '' for x in (email, password, company)):
            raise UserApplicationError('Invalid input for user signup')
        try:
            user = self.user_table.new_row(
                email=email,
                pw_hash=self.security_context.encrypt(password),
                company=company,
                commit=True)
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
