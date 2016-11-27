class ProductLogic:

    def __init__(self, product):
        self.product = product

    def to_dict(self):
        return {'id': self.product.id,
                'label': self.product.label,
                'gtin': self.product.gtin}

class ProductApplication:

    def __init__(self, table):
        self.table = table

    def add_product(self, label, gtin, company, commit=False):
        return self.table.new_row(label=label, gtin=gtin,
                                  company=company, commit=commit)

    def get_products(self, company):
        for x in self.table.query.filter_by(company=company):
            yield ProductLogic(x)
