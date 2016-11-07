from sqlalchemy import exc

class UserApplicationError(Exception):
    pass

class UserApplication:
    def __init__(self, table, security_context):
        self.table = table
        self.security_context = security_context

    def signup(self, email, password, company):
        if any(x.strip() == '' for x in (email, password, company)):
            raise UserApplicationError('Invalid input for user signup')
        try:
            user = self.table.new_row(email=email,
                                      pw_hash=self.security_context.encrypt(password),
                                      company=company)
        except exc.SQLAlchemyError:
            raise UserApplicationError('User exists')
        return user

    def login(self, email, password):
        if any(x.strip() == '' for x in (email, password)):
            raise UserApplicationError('Invalid input for user signup')
        try:
            user = self.table.query.filter_by(email=email).one()
        except exc.SQLAlchemyError:
            return None
        if self.security_context.verify(password, user.pw_hash):
            return user
        else:
            return None
