from django.db import models
from django.contrib.auth.models import User

from string import ascii_lowercase
from collections import Counter


class Allergen(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=200, unique=True)
    brands = models.CharField(max_length=200)
    tags = models.CharField(max_length=400)
    ingredients = models.TextField()
    additives = models.CharField(max_length=300, null=True, blank=True)
    allergens = models.ManyToManyField(Allergen, related_name='products',
                                       blank=True)
    nutriscore = models.CharField(max_length=1)
    labels = models.CharField(max_length=400, null=True, blank=True)
    stores = models.CharField(max_length=200, null=True, blank=True)
    link = models.CharField(max_length=200)
    compared_to = models.CharField(max_length=200)
    image_url = models.CharField(max_length=200)
    keywords = models.CharField(max_length=500)
    last_modified_t = models.BigIntegerField()

    def __str__(self):
        return self.name

    @classmethod
    def get_product(cls, query):
        words = query.split("+")
        products = []
        for word in words:
            products += cls.objects.filter(keywords__icontains=word)
        try:
            product = max(Counter(products), key=Counter(products).get)
            return product

        except ValueError:
            return 0

    @classmethod
    def get_alternatives(cls, product, filter):

        alternatives = cls.objects.filter(tags__icontains=product.compared_to)
        alternatives = alternatives.exclude(id=product.id)

        if filter != 'no filter':
            alternatives = alternatives.exclude(allergens__name=filter)
            filter = 'sans {}'.format(filter)
        else:
            filter = 'Aucun'

        nutriscores = ascii_lowercase[:ascii_lowercase.index('e')+1]
        for letter in nutriscores[nutriscores.index(product.nutriscore)+1:]:
            alternatives = alternatives.exclude(nutriscore=letter)

        return alternatives


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite = models.ManyToManyField(Product, related_name='profiles',
                                      blank=True)

    def __str__(self):
        return self.user.username
