from sqlalchemy import exc

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

    def new_row(self, commit=False, **kwargs):
        row = self.ROW_CLASS(**kwargs)
        self.existing.append(row)
        return row

    @property
    def query(self):
        return self

    def filter_by(self, **filters):
        results = [x for x in self.existing
                   if all(getattr(x, attr) == val for attr,val in filters.items())]
        return ResultSet(results)
