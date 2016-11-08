import unittest
from collections import namedtuple

from ecomm_demo.product_application import ProductApplication

ProductRow = namedtuple('UserRow', 'label gtin')

class MockProductTable:

    def new_row(self, **kwargs):
        return ProductRow(**kwargs)

class TestProductApplication(unittest.TestCase):

    def test_create_product(self):
        app = ProductApplication(MockProductTable())
        product = app.add_product(label='A label', gtin='00845982006196')
        self.assertEqual(product.label, 'A label')
