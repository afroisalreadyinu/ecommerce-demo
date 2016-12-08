import unittest
from collections import namedtuple
from sqlalchemy import exc

from ecomm_demo.product_application import ProductApplication, StorageApplication
from common import MockTable, CompanyRow

GTIN = '00845982006196'
ProductRow = namedtuple('UserRow', 'label gtin company')

class StorageRow:
    def __init__(self, company, label, id=None):
        self.company = company
        self.label = label
        self.id = id

class MockProductTable(MockTable):
    ROW_CLASS = ProductRow

class MockStorageTable(MockTable):
    ROW_CLASS = StorageRow

class TestProductApplication(unittest.TestCase):

    def test_create_product(self):
        product_table = MockProductTable()
        app = ProductApplication(product_table)
        product = app.add_product(label='A label', gtin=GTIN, company='puma')
        self.assertEqual(product.label, 'A label')
        self.assertEqual(len(product_table.existing), 1)
        self.assertEqual(product_table.existing[0].company, 'puma')


    def test_query_products(self):
        existing = [ProductRow(label='test', gtin=GTIN, company='puma')]
        app = ProductApplication(MockProductTable(existing=existing))
        products = app.get_products('puma')
        self.assertEqual(len(list(products)), 1)

    def test_intake_for_product_no_initial_stock(self):
        existing = [ProductRow(label='test', gtin=GTIN, company='puma')]
        app = ProductApplication(MockProductTable(existing=existing))
        product_intake_list = [{'gtin': GTIN, 'intake': 2}]
        company = CompanyRow('puma')
        storage_location = StorageRow(company=company, label='Shop 1')
        result = app.intake_for_products(storage_location, product_intake_list)
        self.assertEqual(len(result), 1)


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
