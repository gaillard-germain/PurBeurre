from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from collections import Counter
from string import ascii_lowercase

from .forms import SignUpForm, ProductSearchForm
from .models import Product, Profile
from .parser import Parser


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
            query = Parser.parse_entry(query)
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

    alternatives = Product.objects.filter(tags__icontains=product.compared_to)
    alternatives = alternatives.exclude(id=product.id)
    nutriscores = ascii_lowercase[:ascii_lowercase.index('e')+1]
    for letter in nutriscores[nutriscores.index(product.nutriscore)+1:]:
        alternatives = alternatives.exclude(nutriscore=letter)

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
    response = {'allowed': False}
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        toggle = request.POST.get('toggle')
        product = Product.objects.get(id=product_id)
        if request.user.is_authenticated:
            profile, created = Profile.objects.get_or_create(user=request.user)
            response['allowed'] = True
            if toggle == 'on':
                profile.favorite.add(product)
            else:
                profile.favorite.remove(product)
    return JsonResponse(response)


def favorites(request):
    if request.user.is_authenticated:
        profile, created = Profile.objects.get_or_create(user=request.user)
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


def legal_notice(request):
    return render(request, 'substitute/legalnotice.html')
