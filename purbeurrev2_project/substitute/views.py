from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q


import unidecode
import re
from collections import Counter

from .forms import SignUpForm, ProductSearchForm
from .models import Product, Profile


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()
            group, created = Group.objects.get_or_create(name='pb_members')
            user.groups.add(group)
            Profile.objects.create(user=user)
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


def my_account(request):
    return render(request, 'registration/myaccount.html')


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
    paginator = Paginator(alternatives.order_by('nutriscore'), 9)
    page = request.GET.get('page')
    try:
        alternatives = paginator.page(page)
    except PageNotAnInteger:
        alternatives = paginator.page(1)
    except EmptyPage:
        alternatives = paginator.page(paginator.num_pages)
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        favorites = Product.objects.filter(profiles=profile)
    else:
        favorites = []
    context = {
        'product': product,
        'alternatives': alternatives,
        'favorites': favorites,
        'paginate': True
    }
    return render(request, 'substitute/results.html', context)


def detail(request, product_id):
    product = Product.objects.get(id=product_id)
    context = {'product': product}
    return render(request, 'substitute/detail.html', context)


def togglefav(request):
    response = {"message": "Action non autorisée", "allowed": False}
    if request.method == 'POST' and request.is_ajax():
        product_id = request.POST.get('product_id')
        toggle = request.POST.get('toggle')
        product = Product.objects.get(id=product_id)
        if request.user.is_authenticated:
            profile = Profile.objects.get(user=request.user)
            response['message'] = 'OK'
            response['allowed'] = True
            if toggle == 'on':
                profile.favorite.add(product)
            else:
                profile.favorite.remove(product)
        else:
            response['message'] = "Veuillez vous connecter SVP."
            response['allowed'] = False
    return JsonResponse(response)


def favorites(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        favorites = Product.objects.filter(profiles=profile)
        paginator = Paginator(favorites.order_by('nutriscore'), 9)
        page = request.GET.get('page')
        try:
            favorites = paginator.page(page)
        except PageNotAnInteger:
            favorites = paginator.page(1)
        except EmptyPage:
            favorites = paginator.page(paginator.num_pages)
        context = {
        'favorites': favorites,
        'paginate': True
        }
        return render(request, 'substitute/favorites.html', context)
    else:
        return redirect('accounts/login')
