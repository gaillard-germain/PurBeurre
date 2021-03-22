from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )


class ProductSearchForm(forms.Form):
    query = forms.CharField(label='Rechercher',
                            max_length=30,
                            initial='produit')
    query.widget.attrs.update({'class': 'form-control col-6'})
