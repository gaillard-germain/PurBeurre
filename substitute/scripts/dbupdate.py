from substitute.models import Product
from .dbfeed import Dbfeed


class Dbupdate:

    @classmethod
    def update(cls):
        """ Updates datas from openfoodfacts API to Product"""

        print('Querying datas...')

        pages = Dbfeed.get_products(100, 1, 'last_modified_t')

        for page in pages:
            for entry in page:
                Dbfeed.add_product(entry)

        print('Total: {} products'.format(len(Product.objects.all())))


def run():
    Dbupdate.update()
