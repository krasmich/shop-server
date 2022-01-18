import json
import os
import random

from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from mainapp.models import ProductCategory, Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


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

# links_menu = [
#     {'href': 'products_all', 'name': 'все'},
#     {'href': 'products_home', 'name': 'дом'},
#     {'href': 'products_office', 'name': 'офис'},
#     {'href': 'products_modern', 'name': 'модерн'},
#     {'href': 'products_classic', 'name': 'классика'},
# ]

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

    links_menu = ProductCategory.objects.filter(is_active=True)

    basket = get_basket(request.user)

    # basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

    if pk is not None:
        if pk == 0:
            products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
            category = {'name': 'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')

        paginator = Paginator(products, 2)
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

    # same_products = Product.objects.all()[:5]

    content = {
        'title': title,
        'links_menu': links_menu,
        'hot_product': hot_product,
        'same_products': same_products,
        'menu': menu,
        'basket': basket,
    }
    return render(request, 'mainapp/products.html', content)


def contact(request):
    context = {'title': 'Контакты', 'menu': menu}
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
    products = Product.objects.all()[:3]
    content = {'title': title, 'products': products, 'menu': menu}
    return render(request, 'mainapp/index.html', content)


def product(request, pk):
    title = 'продукты'
    content = {
        'title': title,
        'links_menu': ProductCategory.objects.all(),
        'product': get_object_or_404(Product, pk=pk),
    }
    return render(request, 'mainapp/product.html', content)
