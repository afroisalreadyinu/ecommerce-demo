import unittest
from collections import namedtuple
from sqlalchemy import exc
from types import SimpleNamespace as Bunch

from ecomm_demo.product_application import ProductApplication, StorageApplication, StockLogic, ProductLogic
from common import MockTable, CompanyRow

GTIN = '00845982006196'
GTIN_2 = '00845982006875'

class ProductRow:
    def __init__(self, label, gtin, company, stocks=None):
        self.label = label
        self.gtin = gtin
        self.company = company
        self.stocks = stocks or []

class StorageRow:
    def __init__(self, company, label, id=None):
        self.company = company
        self.label = label
        self.id = id

class StockRow:
    def __init__(self, storage, product, physical=0, sold=0, reserved=0):
        self.storage = storage
        self.product = product
        self.physical = physical
        self.sold = sold
        self.reserved = reserved

class MockProductTable(MockTable):
    ROW_CLASS = ProductRow

class MockStorageTable(MockTable):
    ROW_CLASS = StorageRow

class MockStockTable(MockTable):
    ROW_CLASS = StockRow

class TestProductApplication(unittest.TestCase):

    def test_create_product(self):
        product_table = MockProductTable()
        app = ProductApplication(product_table, MockStockTable())
        product = app.add_product(label='A label', gtin=GTIN, company='puma')
        self.assertEqual(product.product.label, 'A label')
        self.assertEqual(len(product_table.existing), 1)
        self.assertEqual(product_table.existing[0].company, 'puma')


    def test_products_for_company(self):
        stocks = [StockRow(None, None, physical=10, sold=3, reserved=2),
                  StockRow(None, None, physical=8, sold=2, reserved=1)]
        existing = [ProductRow(label='test', gtin=GTIN,
                               company='puma', stocks=stocks)]
        app = ProductApplication(
            MockProductTable(existing=existing), MockStockTable())
        products = list(app.products_for_company('puma'))
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].product.label, 'test')
        self.assertEqual(products[0].stock.physical,18)

    def test_intake_for_product_no_initial_stock(self):
        app = ProductApplication(None, MockStockTable())
        company = CompanyRow('puma')
        storage_location = StorageRow(company=company, label='Shop 1')
        product = ProductRow(label='test', gtin=GTIN, company='puma')
        result = app.intake_for_product(storage_location, product, 2)
        self.assertEqual(result.product.gtin, product.gtin)
        self.assertEqual(result.stock.physical, 2)

    def test_intake_for_product_stock_exists(self):
        company = CompanyRow('puma')
        product = ProductRow(label='test', gtin=GTIN, company=company)
        storage_location = StorageRow(company=company, label='Shop 1')
        existing_stock = [StockRow(product=product, storage=storage_location, physical=3)]
        app = ProductApplication(None, MockStockTable(existing_stock))
        result = app.intake_for_product(storage_location, product, 2)
        self.assertEqual(result.product.gtin, product.gtin)
        self.assertEqual(result.stock.physical, 5)

    def test_intake_for_product_list(self):
        company = CompanyRow('puma')
        products = [ProductRow(label='test', gtin=GTIN, company=company),
                    ProductRow(label='other test', gtin=GTIN_2, company=company)]
        storage_location = StorageRow(company=company, label='Shop 1')
        existing_stock = [
            StockRow(product=products[0], storage=storage_location, physical=3),
        ]
        app = ProductApplication(MockProductTable(products),
                                 MockStockTable(existing_stock))
        intake_list = [
            {'gtin': GTIN, 'intake': 2},
            {'gtin': GTIN_2, 'intake': 5},
            {'gtin': 'blahblah', 'intake': 5}
        ]
        result = app.intake_for_product_list(storage_location, intake_list)
        self.assertEqual(result['errors'][0]['error'], 'No such product')
        self.assertEqual(result['errors'][0]['gtin'], 'blahblah')
        self.assertEqual(len(result['intakes']), 2)

    def test_stock_for_storage(self):
        existing_stock = [
            StockRow(product='prod 1', storage='storage', physical=3),
            StockRow(product='prod 2', storage='other storage', physical=3),
        ]
        app = ProductApplication(None, MockStockTable(existing_stock))
        stock = list(app.stock_for_storage('storage'))
        self.assertEqual(len(stock), 1)
        self.assertEqual(stock[0].product, 'prod 1')


class TestStorageApplication(unittest.TestCase):

    def test_new_storage_location(self):
        storage_table = MockStorageTable()
        storage_app = StorageApplication(storage_table)
        storage_app.new_storage_location('New location', 'Acme Inc')
        self.assertEqual(len(storage_table.existing), 1)
        self.assertEqual(storage_table.existing[0].label, 'New location')

    def test_filter_by_company(self):
        company = CompanyRow('Comp 1')
        storage_table = MockStorageTable([
            StorageRow(label='St1', company=company, id=1),
            StorageRow(label='St2', company=CompanyRow('Comp 2'), id=2)
        ])
        storage_app = StorageApplication(storage_table)
        storages = list(storage_app.get_all_for_company(company))
        self.assertEqual(len(storages), 1)
        self.assertEqual(storages[0].label, 'St1')

    def test_get_by_id_and_company(self):
        company = CompanyRow('Comp 1')
        storage_table = MockStorageTable([
            StorageRow(label='St1', company=company, id=1),
            StorageRow(label='St2', company=CompanyRow('Comp 2'), id=2)
        ])
        storage_app = StorageApplication(storage_table)
        storage = storage_app.get_for_company(company, 1)
        self.assertEqual(storage.label, 'St1')

    def test_get_by_id_and_company_invalid(self):
        company = CompanyRow('Comp 1')
        storage_table = MockStorageTable([
            StorageRow(label='St1', company=company, id=1),
            StorageRow(label='St2', company=CompanyRow('Comp 2'), id=2)
        ])
        storage_app = StorageApplication(storage_table)
        with self.assertRaises(exc.SQLAlchemyError):
            storage = storage_app.get_for_company(company, 2)

class TestStockLogic(unittest.TestCase):

    def test_null_stock(self):
        null_stock = StockLogic.null_stock()
        self.assertEqual(null_stock.physical, 0)
        self.assertEqual(null_stock.sold, 0)
        self.assertEqual(null_stock.reserved, 0)
        self.assertEqual(null_stock.atp, 0)

    def test_to_dict(self):
        stock = StockLogic(Bunch(physical=0, sold=0, reserved=0))
        self.assertDictEqual(stock.to_dict(),
                             {'physical': 0, 'sold': 0, 'reserved': 0, 'atp': 0})

    def test_from_product_stocks(self):
        stock_list = [Bunch(physical=10, sold=5, reserved=2),
                      Bunch(physical=5, sold=3, reserved=1)]
        stock_logic = StockLogic.from_product_stocks(stock_list)
        #the values should simply be summed
        self.assertEqual(stock_logic.physical, 15)
        self.assertEqual(stock_logic.sold, 8)
        self.assertEqual(stock_logic.reserved, 3)
        self.assertEqual(stock_logic.atp, 4)

    def test_from_product_empty_stocks(self):
        stock_logic = StockLogic.from_product_stocks([])
        self.assertEqual(stock_logic.physical, 0)
        self.assertEqual(stock_logic.sold, 0)
        self.assertEqual(stock_logic.reserved, 0)
        self.assertEqual(stock_logic.atp, 0)

class TestProductLogic(unittest.TestCase):

    def test_to_dict(self):
        product = Bunch(id=3, label='testing', gtin=GTIN)
        stock = Bunch(physical=10, sold=4, reserved=1)
        product_logic = ProductLogic(product, StockLogic(stock))
        product_dict = product_logic.to_dict()
        stock_dict = product_dict.pop('stock').to_dict()
        self.assertDictEqual(product_dict, {'id': 3, 'label': 'testing', 'gtin': GTIN})
        self.assertDictEqual(stock_dict, {'physical': 10, 'sold': 4, 'reserved': 1, 'atp': 5})
