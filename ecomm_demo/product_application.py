from sqlalchemy import exc


class ProductLogic:

    def __init__(self, product, stock):
        self.product = product
        self.stock = stock

    def to_dict(self):
        stock_dict = {'physical': self.stock.physical,
                      'sold': self.stock.sold,
                      'reserved': self.stock.reserved}
        return {'id': self.product.id,
                'label': self.product.label,
                'gtin': self.product.gtin,
                'stock': stock_dict}

class ProductApplication:

    def __init__(self, product_table, stock_table):
        self.product_table = product_table
        self.stock_table = stock_table

    def add_product(self, label, gtin, company, commit=False):
        return self.product_table.new_row(
            label=label, gtin=gtin,
            company=company, commit=commit)

    def get_products(self, company):
        no_stock_dict = {'physical': 0, 'atp': 0, 'sold': 0, 'reserved': 0}
        for x in self.product_table.query.filter_by(company=company):
            yield ProductLogic(x, no_stock_dict)

    def get_or_create(self, table, **fields):
        try:
            row = table.query.filter_by(**fields).one()
        except exc.SQLAlchemyError:
            row = table.new_row(**fields)
        return row

    def intake_for_product(self, storage_location, product, intake_value):
        stock_row = self.get_or_create(
            self.stock_table, storage=storage_location, product=product)
        stock_row.physical += intake_value
        return ProductLogic(product, stock_row)

    def intake_for_product_list(self, storage_location, product_intake_list):
        results = []
        errors = []
        for intake_entry in product_intake_list:
            try:
                product = self.product_table.query.filter_by(
                    company=storage_location.company,
                    gtin=intake_entry['gtin']
                ).one()
            except exc.SQLAlchemyError:
                errors.append({'gtin': intake_entry['gtin'], 'error': 'No such product'})
            else:
                results.append(self.intake_for_product(storage_location, product, intake_entry['intake']))
        return {'intakes': results, 'errors': errors}


    def stock_for_storage(self, storage):
        for stock in self.stock_table.query.filter_by(storage=storage):
            yield ProductLogic(stock.product, stock)


class StorageApplication:
    def __init__(self, storage_table):
        self.storage_table = storage_table

    def new_storage_location(self, label, company, commit=True):
        return self.storage_table.new_row(
            label=label, company=company, commit=commit
        )

    def get_all_for_company(self, company):
        return self.storage_table.query.filter_by(company=company)

    def get_for_company(self, company, _id):
        return self.storage_table.query.filter_by(company=company, id=_id).one()
