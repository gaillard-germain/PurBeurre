import requests

from substitute.models import Product, Profile


class Dbfeed:
    @staticmethod
    def check_value(dict, key, default=None):
        """ Checks if the field exist in the json from openfoodfacts API
            and return a formated value"""

        value = default

        try:
            value = dict[key]
            if not value:
                value = default

            elif key == 'categories_hierarchy':
                try:
                    value = value[2]
                except IndexError:
                    value = value[0]

            elif isinstance(value, list):
                value = ', '.join(value)

            if value and isinstance(value, str):
                value = value.replace("en:", "")
                value = value.replace("fr:", "")

        except KeyError as error:
            pass

        return value

    @classmethod
    def get_products(cls, page_size, page_nbr, sort_by):
        """ Returns a list of products pages from OpenFoodFacts API """

        pages = []
        for i in range(page_nbr):
            search = 'https://fr.openfoodfacts.org/cgi/search.pl?\
search_terms=&tagtype_0=purchase_places&tag_contains_0=contains&tag_0=france&\
tagtype_1=states&tag_contains_1=contains&tag_1=complete&\
sort_by={}&page_size={}&page={}&json=1'.format(sort_by, page_size, i+1)

            all = requests.get(search)
            all = all.json()['products']

            pages.append(all)
        return pages

    @classmethod
    def add_product(cls, entry):
        product = Product(
            id = int(entry['_id']),
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
            keywords=cls.check_value(entry, '_keywords'),
            last_modified_t=cls.check_value(entry, 'last_modified_t'))

        try:
            product.save()
        except Exception as error:
            print(error)
            pass

    @classmethod
    def feed(cls):
        """ Added datas from openfoodfacts API to Product"""

        print('Deleting the formers products and profiles')

        Profile.objects.all().delete()
        Product.objects.all().delete()

        print('Querying datas...')

        pages = cls.get_products(500, 4, 'unique_scans_n')

        for page in pages:
            for entry in page:
                cls.add_product(entry)

        print('Total: {} products'.format(len(Product.objects.all())))


def run():
    Dbfeed.feed()
