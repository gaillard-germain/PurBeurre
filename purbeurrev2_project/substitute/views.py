from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

import unidecode
import re
from collections import Counter

from .forms import SignUpForm, ProductSearchForm
from .models import Product


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def logout_request(request):
    logout(request)
    return render(request, 'registration/logout.html')


def index(request):
    if request.method == 'POST':
        form = ProductSearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data.get('query')
            query = unidecode.unidecode(query)
            return redirect('substitute:results', query=query)
    else:
        form = ProductSearchForm()
    return render(request, 'substitute/index.html', {'form': form})


def results(request, query):
    words = re.split(r'\W+', query)
    products = []
    for word in words:
        products += Product.objects.filter(keywords__icontains=word)
    try:
        product = max(Counter(products), key=Counter(products).get)
    except ValueError:
        raise Http404("Aucun produit correspondant")

    alternatives = Product.objects.filter(tags__icontains=product.compared_to)
    paginator = Paginator(alternatives, 9)
    page = request.GET.get('page')
    try:
        alternatives = paginator.page(page)
    except PageNotAnInteger:
        alternatives = paginator.page(1)
    except EmptyPage:
        alternatives = paginator.page(paginator.num_pages)
    context = {
        'alternatives': alternatives,
        'product': product,
        'paginate': True
    }
    return render(request, 'substitute/results.html', context)


def detail(request, product_id):
    product = Product.objects.get(id=product_id)
    context = {'product': product}
    return render(request, 'substitute/detail.html', context)
