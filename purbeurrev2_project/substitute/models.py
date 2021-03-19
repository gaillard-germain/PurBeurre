from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=200)
    brands = models.CharField(max_length=200)
    tags = models.CharField(max_length=400)
    ingredients = models.TextField(null=True, blank=True)
    additives = models.CharField(max_length=300, null=True, blank=True)
    allergens = models.CharField(max_length=300, null=True, blank=True)
    nutriscore = models.CharField(max_length=1, null=True, blank=True)
    labels = models.CharField(max_length=300, null=True, blank=True)
    stores = models.CharField(max_length=200, null=True)
    link = models.CharField(max_length=200)
    compared_to = models.CharField(max_length=200)
    image_url = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite = models.ManyToManyField(Product, related_name='profiles', blank=True)

    def __str__(self):
        return self.user.name
