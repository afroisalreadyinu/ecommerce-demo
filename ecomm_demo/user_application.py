from passlib.apps import custom_app_context

class UserApplicationError(Exception):
    pass

class UserApplication:
    def __init__(self, table):
        self.table = table

    def signup(self, email, password, company):
        if any(x.strip() == '' for x in (email, password, company)):
            raise UserApplicationError('Invalid input for user signup')
        user = self.table.new_row(email=email,
                                  pw_hash=custom_app_context.encrypt(password),
                                  company=company)
        return user
