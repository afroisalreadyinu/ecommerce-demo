from collections import namedtuple
from sqlalchemy import exc

UserRow = namedtuple('UserRow', 'email pw_hash company')
CompanyRow = namedtuple('CompanyRow', 'label')

class ResultSet:

    def __init__(self, result):
        self.result = result

    def one(self):
        if self.result:
            return self.result[0]
        raise exc.SQLAlchemyError()

    def __iter__(self):
        return iter(self.result)


class MockTable:
    ROW_CLASS = None

    def __init__(self, existing=None):
        self.existing = existing or []

    def new_row(self, **kwargs):
        row = self.ROW_CLASS(**kwargs)
        self.existing.append(row)
        return row

    def get_or_create(self, **kwargs):
        try:
            return self.filter_by(**kwargs).one()
        except exc.SQLAlchemyError:
            return self.new_row(**kwargs)

    @property
    def query(self):
        return self

    def filter_by(self, **filters):
        results = [x for x in self.existing
                   if all(getattr(x, attr) == val for attr,val in filters.items())]
        return ResultSet(results)

    def commit(self):
        pass

class MockUserTable(MockTable):
    ROW_CLASS = UserRow

class MockCompanyTable(MockTable):
    ROW_CLASS = CompanyRow

class MockSecurityContext:

    def __init__(self, fail=False):
        self.fail = fail

    def encrypt(self, password):
        return 'encrypted'

    def verify(self, password, hash):
        return not self.fail
