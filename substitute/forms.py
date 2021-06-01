from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import Allergen


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )


class ProductSearchForm(forms.Form):
    FILTER_CHOICES = [
        ('no filter', 'Aucun filtre (allergènes)')
    ]

    for allergen in Allergen.objects.all().exclude(name='aucun'):
        FILTER_CHOICES.append((allergen.name, 'Sans {}'.format(allergen.name)))

    query = forms.CharField(label='Rechercher',
                            max_length=30,)
    query.widget.attrs.update({'class': 'form-control col-6',
                               'id': 'search_input',
                               'content': 'text/html; charset=UTF-8',
                               'placeholder': 'Produit'})

    filter = forms.CharField(label='filtre sans',
                             widget=forms.Select(choices=FILTER_CHOICES))
    filter.widget.attrs.update({'class': 'd-block form-control col-8 my-2',
                               'id': 'filter_choices'})
