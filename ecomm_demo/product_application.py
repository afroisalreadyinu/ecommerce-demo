from sqlalchemy import exc
from types import SimpleNamespace as Bunch


class ProductLogic:

    def __init__(self, product, stock):
        self.product = product
        self.stock = stock

    def to_dict(self):
        return {'id': self.product.id,
                'label': self.product.label,
                'gtin': self.product.gtin,
                'stock': self.stock}


class StockLogic:
    REPLICATED_FIELDS = ['physical', 'sold', 'reserved']
    def __init__(self, stock_row):
        self.stock = stock_row

    @property
    def atp(self):
        return self.stock.physical - (self.stock.sold + self.stock.reserved)

    def __getattr__(self, attr):
        if attr in self.REPLICATED_FIELDS:
            return getattr(self.stock, attr)
        raise AttributeError()

    @classmethod
    def null_stock(cls):
        zero_value = Bunch(physical=0, sold=0, reserved=0)
        return StockLogic(zero_value)

    @classmethod
    def from_product_stocks(self, stocks):
        physical = sum(stock.physical for stock in stocks)
        sold = sum(stock.sold for stock in stocks)
        reserved = sum(stock.reserved for stock in stocks)
        stock_row = Bunch(physical=physical, sold=sold, reserved=reserved)
        return StockLogic(stock_row)

    def to_dict(self):
        fields = self.REPLICATED_FIELDS + ['atp']
        return {field:getattr(self, field) for field in fields}


class ProductApplication:

    def __init__(self, product_table, stock_table):
        self.product_table = product_table
        self.stock_table = stock_table

    def add_product(self, label, gtin, company):
        return ProductLogic(self.product_table.new_row(
            label=label, gtin=gtin,
            company=company), StockLogic.null_stock())

    def products_for_company(self, company):
        for product in self.product_table.query.filter_by(company=company):
            stocks_logic = StockLogic.from_product_stocks(product.stocks)
            yield ProductLogic(product, stocks_logic)

    def intake_for_product(self, storage_location, product, intake_value):
        stock_row = self.stock_table.get_or_create(
            storage=storage_location, product=product)
        stock_row.physical += intake_value
        return ProductLogic(product, StockLogic(stock_row))

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
            yield ProductLogic(stock.product, StockLogic(stock))



class StorageApplication:
    def __init__(self, storage_table):
        self.storage_table = storage_table

    def new_storage_location(self, label, company):
        return self.storage_table.new_row(label=label, company=company)

    def get_all_for_company(self, company):
        return self.storage_table.query.filter_by(company=company)

    def get_for_company(self, company, _id):
        return self.storage_table.query.filter_by(company=company, id=_id).one()
