import json
import os
import random

from django.shortcuts import render, get_object_or_404
from django.http.response import JsonResponse

from basketapp.models import Basket
from mainapp.models import ProductCategory, Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.conf import settings
from django.core.cache import cache
from django.views.decorators.cache import cache_page

# Create your views here.

JSON_PATH = 'mainapp/json'


def read_json_from_file(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r') as infile:
        return json.load(infile)


def load_from_json(file_name):
    if settings.LOW_CACHE:
        key = f'file__{file_name}'
        data = cache.get(key)
        if data is None:
            data = read_json_from_file(file_name)
            cache.set(key, data)
        return data
    else:
        return read_json_from_file(file_name)


def get_links_menu():
    if settings.LOW_CACHE:
        key = f'product__links_menu'
        data = cache.get(key)
        if data is None:
            data = ProductCategory.objects.filter(is_active=True)
            cache.set(key, data)
        return data
    else:
        return ProductCategory.objects.filter(is_active=True)

def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else:
        return []


def get_hot_product():
    products = Product.objects.all()

    return random.sample(list(products), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]
    return same_products


module_dir = os.path.dirname(__file__)


menu = [
    {'href': 'index', 'name': 'главная'},
    {'href': 'products:index', 'name': 'продукты'},
    {'href': 'contact', 'name': 'контакты'},
]


def index(request):
    context = {'title': 'Магазин', 'menu': menu}
    return render(request, 'mainapp/index.html', context)


def products(request, pk=None, page=1):
    title = 'Продукты'
    links_menu = get_links_menu()

    basket = get_basket(request.user)

    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

    if pk is not None:
        if pk == 0:
            products = Product.objects.filter(is_active=True, category__is_active=True
                                              ).order_by('price').select_related()
            category = {'name': 'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True
                                              ).order_by('price').select_related()

        paginator = Paginator(products.select_related(), 2)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        content = {
            'title': title,
            'links_menu': links_menu,
            'products': products_paginator,
            'category': category,
            'menu': menu,
            'basket': basket,
        }

        return render(request, 'mainapp/products_list.html', content)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    content = {
        'title': title,
        'links_menu': links_menu,
        'hot_product': hot_product,
        'same_products': same_products,
        'menu': menu,
        'basket': basket,
    }
    return render(request, 'mainapp/products.html', content)


def products_ajax(request, pk=None, page=1):
    links_menu = get_links_menu()
    if pk is not None:
        if pk == 0:
            category = {
                'pk': 0,
                'name': 'все'
            }
            products = Product.objects.filter(
                is_active=True, category__is_active=True
            ).order_by('price')
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(
                category__pk=pk, is_active=True, category__is_active=True
            ).order_by('price')

        paginator = Paginator(products, 2)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        content = {
            'links_menu': links_menu,
            'category': category,
            'products': products_paginator,
        }

        return render(request, 'includes/inc_products_list_content.html',
                      context=content)



def contact(request):
    title = 'о нас'

    locations = load_from_json('contact__locations')

    context = {
        'title': 'Контакты',
        'locations': locations,
        'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/contact.html', context)


def context_(request):
    content = {
        'title': 'магазин',
        'header': 'Добро пожаловать на сайт',
        'username': 'Иван Иванов',
        'products': [
            {'name': 'Стулья', 'price': 4535},
            {'name': 'Диваны', 'price': 1535},
            {'name': 'Кровати', 'price': 2535},
        ]
    }
    return render(request, 'mainapp/test_context.html', content)


def main(request):
    title = 'главная'
    products = (
        Product.objects
        .filter(is_active=True, category__is_active=True)
        .select_related()[:3]
    )
    content = {
        'title': title,
        'products': products,
    }
    return render(request, 'mainapp/index.html', content)


def product(request, pk):
    title = 'продукты'
    links_menu = get_links_menu()

    product = get_object_or_404(Product, pk=pk)

    content = {
        'title': title,
        'links_menu': links_menu,
        'product': product,
    }
    return render(request, 'mainapp/product.html', content)


def product_price(request, pk):
    product = Product.objects.filter(pk=pk)

    if product:
        return JsonResponse({'price': product[0].price})
    else:
        return JsonResponse({'price': 0})
