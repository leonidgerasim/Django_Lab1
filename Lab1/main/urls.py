from django.contrib import admin
from django.urls import path, include
from .views import (index, products_list, add_product, customers, create_order, add_customers, create_order_detail,
                    barter, customer_order, order_detail)
app_name = 'main'

urlpatterns = [
    path('', index, name='index'),
    path('products_list/', products_list, name='products_list'),
    path('add_product/', add_product, name='add_product'),
    path('customers/', customers, name='customers'),
    path('customer_orders/<int:customer_id>', customer_order, name='customer_order'),
    path('order_detail/<int:order_id>', order_detail, name='order_detail'),
    path('add_customers/', add_customers, name='add_customers'),
    path('create_order/', create_order, name='create_order'),
    path('create_order_detail/<int:order_id>/<str:product_id>', create_order_detail, name='create_order_detail'),
    path('barter/<int:order_id>', barter, name='barter'),
]
