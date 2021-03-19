import requests

from substitute.models import Product


class Dbfeed:
    @staticmethod
    def format_value(dict, key):
        """ Checks if the field exist in the json from openfoodfacts API
            and return a formated value"""

        value = None

        try:
            value = dict[key]
            if not value:
                value = None

            elif isinstance(value, list):
                value = ', '.join(value)

            if value:
                value = value.replace("en:", "")

        except KeyError as error:
            print("product {} doesn't have {} field".format(dict['code'],
                                                            error))
            print("set it to NULL")

        return value

    @classmethod
    def feed(cls):
        """ Returns datas from openfoodfacts API """

        print('Querying datas...')
        search = 'https://fr.openfoodfacts.org/cgi/search.pl?search_terms=&\
        tagtype_0=states&tag_contains_0=contains&tag_0=checked&\
        sort_by=unique_scans_n&page_size=30&page=1&json=1'

        all = requests.get(search)
        all = all.json()['products']

        Product.objects.all().delete()

        for entry in all:
            product = Product(
                name = cls.format_value(entry, 'product_name'),
                brands = cls.format_value(entry, 'brands'),
                tags = cls.format_value(entry, 'categories_tags'),
                ingredients = cls.format_value(entry, 'ingredients_text_fr'),
                additives = cls.format_value(entry, 'additives_tags'),
                allergens = cls.format_value(entry, 'allergens_tags'),
                nutriscore = cls.format_value(entry, 'nutriscore_grade'),
                labels = cls.format_value(entry, 'labels'),
                stores = cls.format_value(entry, 'stores_tags'),
                link = cls.format_value(entry, 'url'),
                compared_to = cls.format_value(entry, 'compared_to_category'),
                image_url = cls.format_value(entry, 'image_url'))

            product.save()


def run():
    Dbfeed.feed()
