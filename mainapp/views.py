import json
import os

from django.shortcuts import render

# Create your views here.

links_menu = [
    {'href': 'home', 'name': 'домой'},
    {'href': 'product', 'name': 'продукты'},
    {'href': 'contacts', 'name': 'контакты'},
]

module_dir = os.path.dirname(__file__)


def main(request):
    content = {
        'title': 'Меню',
        'links_menu': links_menu,
    }
    return render(request, 'mainapp/index.html', content)


def products(request):

    file_path = os.path.join(module_dir, 'data/products.json')
    products = json.load(open(file_path, encoding='utf-8'))

    content = {
        'title': 'Меню',
        'links_menu': links_menu,
        'products': products
    }
    return render(request, 'mainapp/products.html', content)


def contact(request):
    content = {
        'title': 'Меню',
        'links_menu': links_menu,
    }
    return render(request, 'mainapp/contact.html', content)


def context(request):
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
