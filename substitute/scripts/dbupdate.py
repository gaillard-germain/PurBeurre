import requests

from substitute.models import Product


class Dbupdate:
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
    def update(cls):
        """ Updates datas from openfoodfacts API to Product"""

        counter = 0
        all_products = Product.objects.all()

        for product in all_products:
            api_query = 'https://fr.openfoodfacts.org/api/v0/product/{}.json'
            api_query = api_query.format(product.off_id)

            result = requests.get(api_query)
            result = result.json()

            print(result['code'], result['status_verbose'])

            if int(result['status']):
                result = result['product']

                if product.last_modified_t < int(result['last_modified_t']):
                    new_product = Product(
                        id = product.id,
                        name=cls.check_value(result, 'product_name',
                                             product.name),
                        brands=cls.check_value(result, 'brands',
                                               product.brands),
                        tags=cls.check_value(result, 'categories_tags',
                                             product.tags),
                        ingredients=cls.check_value(result,
                                                    'ingredients_text_fr',
                                                    product.ingredients),
                        additives=cls.check_value(result, 'additives_tags',
                                                  product.additives),
                        allergens=cls.check_value(result, 'allergens_tags',
                                                  product.allergens),
                        nutriscore=cls.check_value(result, 'nutriscore_grade',
                                                   product.nutriscore),
                        labels=cls.check_value(result, 'labels',
                                               product.labels),
                        stores=cls.check_value(result, 'stores_tags',
                                               product.stores),
                        link=cls.check_value(result, 'url',
                                             product.link),
                        compared_to=cls.check_value(result,
                                                    'categories_hierarchy',
                                                    product.compared_to),
                        image_url=cls.check_value(result, 'image_url',
                                                  product.image_url),
                        keywords=cls.check_value(result, '_keywords',
                                                 product.keywords),
                        off_id=cls.check_value(result,'_id', product.off_id),
                        last_modified_t=cls.check_value(result,
                                                        'last_modified_t',
                                                        product.last_modified_t)
                    )
                    new_product.save()
                    counter += 1
        print('{} products updated'.format(counter))


def run():
    Dbupdate.update()
