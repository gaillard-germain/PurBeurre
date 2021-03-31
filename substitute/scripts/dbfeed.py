import requests

from substitute.models import Product
# from psycopg2.errors import StringDataRightTruncation, NotNullViolation


class Dbfeed:
    @staticmethod
    def check_value(dict, key):
        """ Checks if the field exist in the json from openfoodfacts API
            and return a formated value"""

        value = None

        try:
            value = dict[key]
            if not value:
                value = None

            elif key == 'categories_hierarchy':
                try:
                    value = value[2]
                except IndexError:
                    value = value[0]

            elif isinstance(value, list):
                value = ', '.join(value)

            if value:
                value = value.replace("en:", "")
                value = value.replace("fr:", "")

        except KeyError as error:
            print("product {} doesn't have {} field".format(dict['code'],
                                                            error))
            print("set it to NULL")

        return value

    @classmethod
    def feed(cls, page_size, page_nbr):
        """ Added datas from openfoodfacts API to Product"""

        print('Deleting the former products')
        Product.objects.all().delete()
        print('Querying datas...')
        for i in range(page_nbr):
            search = 'https://fr.openfoodfacts.org/cgi/search.pl?\
search_terms=&tagtype_0=purchase_places&tag_contains_0=contains&tag_0=france&\
tagtype_1=states&tag_contains_1=contains&tag_1=complete&\
sort_by=unique_scans_n&page_size={}&page={}&json=1'.format(page_size, i+1)

            all = requests.get(search)
            all = all.json()['products']

            for entry in all:
                product = Product(
                    name=cls.check_value(entry, 'product_name'),
                    brands=cls.check_value(entry, 'brands'),
                    tags=cls.check_value(entry, 'categories_tags'),
                    ingredients=cls.check_value(entry, 'ingredients_text_fr'),
                    additives=cls.check_value(entry, 'additives_tags'),
                    allergens=cls.check_value(entry, 'allergens_tags'),
                    nutriscore=cls.check_value(entry, 'nutriscore_grade'),
                    labels=cls.check_value(entry, 'labels'),
                    stores=cls.check_value(entry, 'stores_tags'),
                    link=cls.check_value(entry, 'url'),
                    compared_to=cls.check_value(entry, 'categories_hierarchy'),
                    image_url=cls.check_value(entry, 'image_url'),
                    keywords=cls.check_value(entry, '_keywords'))

                try:
                    product.save()
                except Exception as error:
                    print(error)
                    pass


def run():
    Dbfeed.feed(500, 4)
