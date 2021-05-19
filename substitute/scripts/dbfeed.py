import requests

from substitute.models import Product, Profile, Allergen


class Dbfeed:
    ALLERGEN_DICT = {
        "gluten": "gluten",
        "crustaceans": "crustacés",
        "eggs": "oeufs",
        "fish": "poisson",
        "peanuts": "arachides",
        "oats": "avoine",
        "soybeans": "soja",
        "milk": "lait",
        "celery": "céleri",
        "nuts": "fruits à coques",
        "mustard": "moutarde",
        "molluscs": "mollusques",
        "sesame-seeds": "graines de sésame",
        "sulphur-dioxide-and-sulphites": "sulfites"
    }

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
    def add_allergens(cls, product, allergens_list):
        """ Adds products-allergens many-to-many relations """

        if allergens_list:
            for allergen_name in allergens_list:
                allergen_name = allergen_name.lower().split(':')[-1]
                if allergen_name in cls.ALLERGEN_DICT:
                    allergen_name = cls.ALLERGEN_DICT[allergen_name]
                    allergen, created = Allergen.objects.get_or_create(
                        name=allergen_name
                    )
                    product.allergens.add(allergen)
        else:
            allergen, created = Allergen.objects.get_or_create(
                name="aucun"
            )
            product.allergens.add(allergen)

    @classmethod
    def add_product(cls, entry):
        """ Adds a product to database """

        product = Product(
            id = int(entry['_id']),
            name=cls.check_value(entry, 'product_name'),
            brands=cls.check_value(entry, 'brands'),
            tags=cls.check_value(entry, 'categories_tags'),
            ingredients=cls.check_value(entry, 'ingredients_text_fr'),
            additives=cls.check_value(entry, 'additives_tags'),
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
            cls.add_allergens(product, entry['allergens_tags'])

        except Exception as error:
            print(error)
            pass

    @classmethod
    def feed(cls):
        """ Adds datas from openfoodfacts API to Product"""

        print('Deleting the formers tables...')

        Profile.objects.all().delete()
        Product.objects.all().delete()
        Allergen.objects.all().delete()

        print('Querying datas...')

        pages = cls.get_products(500, 4, 'unique_scans_n')

        for page in pages:
            for entry in page:
                cls.add_product(entry)

        print('Total: {} products'.format(len(Product.objects.all())))


def run():
    Dbfeed.feed()
