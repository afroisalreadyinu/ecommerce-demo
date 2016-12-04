import unittest
from collections import namedtuple

from ecomm_demo.product_application import ProductApplication, StorageApplication
from common import MockTable

GTIN = '00845982006196'
ProductRow = namedtuple('UserRow', 'label gtin company')
StorageRow = namedtuple('StorageRow', 'label company')

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


class TestStorageApplication(unittest.TestCase):

    def test_new_storage_location(self):
        storage_table = MockStorageTable()
        storage_app = StorageApplication(storage_table)
        storage_app.new_storage_location('New location', 'Acme Inc')
        self.assertEqual(len(storage_table.existing), 1)
        self.assertEqual(storage_table.existing[0].label, 'New location')
