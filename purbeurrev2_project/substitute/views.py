from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

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
    context = {'form': form}
    return render(request, 'registration/signup.html', context)


def logout_request(request):
    logout(request)
    return render(request, 'registration/logout.html')


def index(request):
    if request.method == 'POST':
        form = ProductSearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data.get('query')
            query = unidecode.unidecode(query)
            query = re.split(r'\W+', query)
            query = "+".join(filter(None,query))
            return redirect('substitute:results', query=query)
    else:
        form = ProductSearchForm()
    context = {'form': form}
    return render(request, 'substitute/index.html', context)


def results(request, query):
    words = query.split("+")
    products = []
    for word in words:
        products += Product.objects.filter(keywords__icontains=word)
    try:
        product = max(Counter(products), key=Counter(products).get)
    except ValueError:
        raise Http404("Aucun produit correspondant")

    query_list = (Q(tags__icontains=product.compared_to)&
                  (Q(nutriscore__icontains='a')|
                   Q(nutriscore__icontains='b')|
                   Q(nutriscore__icontains='c')))
    alternatives = Product.objects.filter(query_list).exclude(id=product.id)
    paginator = Paginator(alternatives, 9)
    page = request.GET.get('page')
    try:
        alternatives = paginator.page(page)
    except PageNotAnInteger:
        alternatives = paginator.page(1)
    except EmptyPage:
        alternatives = paginator.page(paginator.num_pages)
    context = {
        'product': product,
        'alternatives': alternatives,
        'paginate': True
    }
    return render(request, 'substitute/results.html', context)


def detail(request, product_id):
    product = Product.objects.get(id=product_id)
    context = {'product': product}
    return render(request, 'substitute/detail.html', context)
