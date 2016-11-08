import unittest
from collections import namedtuple

from ecomm_demo.product_application import ProductApplication

GTIN = '00845982006196'
ProductRow = namedtuple('UserRow', 'label gtin')

class MockProductTable:

    def __init__(self, existing=None):
        self.existing = existing or []

    def new_row(self, commit, **kwargs):
        return ProductRow(**kwargs)

    @property
    def query(self):
        return self

    def all(self):
        return self.existing

class TestProductApplication(unittest.TestCase):

    def test_create_product(self):
        app = ProductApplication(MockProductTable())
        product = app.add_product(label='A label', gtin=GTIN)
        self.assertEqual(product.label, 'A label')

    def test_query_products(self):
        existing = [ProductRow(label='test', gtin=GTIN)]
        app = ProductApplication(MockProductTable(existing=existing))
        products = app.get_products()
        self.assertEqual(len(list(products)), 1)
