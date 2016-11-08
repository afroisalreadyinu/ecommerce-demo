class ProductApplication:

    def __init__(self, table):
        self.table = table

    def add_product(self, label, gtin, commit=False):
        return self.table.new_row(label=label, gtin=gtin, commit=commit)
