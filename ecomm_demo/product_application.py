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

    def add_product(self, label, gtin, commit=False):
        return self.table.new_row(label=label, gtin=gtin, commit=commit)

    def get_products(self):
        for x in self.table.query.all():
            yield ProductLogic(x)
