from django.urls import path

import mainapp.views as mainapp
from django.views.decorators.cache import cache_page

app_name = 'mainapp'

urlpatterns = [
    # Common views
    path('', mainapp.products, name='index'),
    path('category/<int:pk>/', mainapp.products, name='category'),
    path('category/<int:pk>/page/<int:page>/', mainapp.products, name='page'),
    path('product/<int:pk>/', mainapp.product, name='product'),
    path('product/<int:pk>/price', mainapp.product_price, name='product_price'),

    # AJAX views
    path('category/<int:pk>/ajax/', cache_page(3600)(mainapp.products_ajax), name='category_ajax'),
    path('category/<int:pk>/page/<int:page>/ajax/', cache_page(3600)(mainapp.products_ajax), name='page_ajax')
]
