import unittest
from collections import namedtuple

from ecomm_demo.product_application import ProductApplication
from common import MockTable

GTIN = '00845982006196'
ProductRow = namedtuple('UserRow', 'label gtin company')

class MockProductTable(MockTable):
    ROW_CLASS = ProductRow

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
