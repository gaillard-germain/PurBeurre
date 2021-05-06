from django.test import TestCase

from unittest.mock import patch

from ..models import Product
from ..scripts.dbfeed import Dbfeed


class MockResponse:

    def __init__(self):
        self.status_code = 200

    def json(self):
        return {
            "products": [{
                "product_name": "Fake Product",
                "brands": "Fake Brands",
                "categories_tags": ["fake"],
                "ingredients_text_fr": "fake",
                "additives_tags": ["Efake"],
                "allergens_tags": ["fake"],
                "nutriscore_grade": "f",
                "labels": "fake",
                "stores_tags": ["Fake"],
                "url": "https://fake",
                "categories_hierarchy": ["fake1", "fake2", "fake3"],
                "image_url": "https://fakeimage",
                "_keywords": "fake",
                "_id": 111,
                "last_modified_t": 1,
            }]
        }


class DBfeedTestCase(TestCase):

    @patch('requests.get', return_value=MockResponse())
    def test_dbfeed_add_product(self, mocked):
        old_prod = Product.objects.count()
        Dbfeed.feed(20, 1)
        new_prod = Product.objects.count()
        self.assertEqual(new_prod, old_prod+1)
