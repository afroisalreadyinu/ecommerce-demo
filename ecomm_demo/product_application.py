class ProductLogic:

    def __init__(self, product, stock):
        self.product = product
        self.stock = stock

    def to_dict(self):
        return {'id': self.product.id,
                'label': self.product.label,
                'gtin': self.product.gtin,
                'stock': self.stock}

class ProductApplication:

    def __init__(self, table):
        self.table = table

    def add_product(self, label, gtin, company, commit=False):
        return self.table.new_row(label=label, gtin=gtin,
                                  company=company, commit=commit)

    def get_products(self, company):
        no_stock_dict = {'physical': 0, 'atp': 0, 'sold': 0, 'reserved': 0}
        for x in self.table.query.filter_by(company=company):
            yield ProductLogic(x, no_stock_dict)

class StorageApplication:
    def __init__(self, storage_table):
        self.storage_table = storage_table

    def new_storage_location(self, label, company, commit=True):
        return self.storage_table.new_row(
            label=label, company=company, commit=commit
        )

    def get_all_for_company(self, company):
        return self.storage_table.query.filter_by(company=company)
