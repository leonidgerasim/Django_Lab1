from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from .models import Products, Customers, Order, OrderDetail, BarterOrder
from .forms import (AddProductsForm, SearchCustomersForm, AddCustomersForm, AddOrderDetailsFormProduct,
                    AddOrderDetailsFormQuantity)
from django.db.models import Sum

# Create your views here.


def index(request):
    context = {'title': 'Главная'}
    return render(request, 'main/main.html', context)


def customers(request):
    error = ''
    customer = ''
    valid = ''
    if request.method == 'POST':
        form = SearchCustomersForm(data=request.POST)
        valid = form.is_valid() and Customers.objects.filter(name=request.POST['name']).exists()
        if valid:
            customer = Customers.objects.filter(name=request.POST['name'])
        else:
            error = 'Ошибка'
            customer = 'Такого клиента нет'
    else:
        form = SearchCustomersForm()
    context = {'title': 'Клиенты',
               'form': form,
               'customer': customer,
               'error': error,
               'valid': valid,
               'customer_id': customer.id}
    return render(request, 'main/customers.html', context)


def customer_order(request, customer_id):
    customer = get_object_or_404(Customers, pk=customer_id)
    context = {'title': 'Заказы ' + str(customer.name),
               'orders': Order.objects.filter(customer=customer),
    }
    return render(request, 'main/customer_order.html', context)


def order_detail(request):
    return render(request, 'main/order_detail.html')


def products_list(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']
        quantity = request.POST['quantity']
        product = Products(name=name, description=description, price=price, quantity=quantity)
        product.save()
        return redirect('products')

    products = Products.objects.all()
    context = {'title': 'Список товаров',
               'products': products}
    return render(request, 'main/products.html', context)


def add_product(request):
    if request.method == 'POST':
        form = AddProductsForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('main:products_list'))
    else:
        form = AddProductsForm()
    context = {'title': 'Добавить Новый Товар',
               'form': form}
    return render(request, 'main/add_product.html', context)


def add_customers(request):
    data = ''
    if request.method == 'POST':
        name = request.POST['name']
        total_amount = request.POST['total_amount']


    else:
        form = AddCustomersForm()
    context = {'title': 'Добавить Клиента',
               'data': data}
    return render(request, 'main/add_customers.html', context)


def create_order(request):
    if request.method == 'POST':
        customer_id = request.POST['customer_name']
        type_sale = request.POST["calculation"]
        customer = Customers.objects.get(id=customer_id)
        order = Order(customer=customer, type_sale=type_sale)
        order.save()
        return HttpResponseRedirect(reverse('main:create_order_detail', args=[order.pk, 'f']))

    context = {'title': 'Создать заказ',
               'customers': Customers.objects.all()}
    return render(request, 'main/create_order.html', context)


def create_order_detail(request, order_id, product_id):
    order = get_object_or_404(Order, pk=order_id)
    total_amount = 0
    type_sale = order.type_sale
    customer = order.customer
    product_f = ''
    flag = True if type_sale == 'Бартер' else False
    if request.method == 'POST' and product_id == 'f':
        product_form = AddOrderDetailsFormProduct(data=request.POST)
        quantity_form = ''
        if product_form.is_valid():
            product_id = product_form.cleaned_data.get("product").id
            return HttpResponseRedirect(reverse('main:order_detail', args=[order.pk, product_id]))
    elif request.method == 'POST' and product_id != 'f':
        product_form = AddOrderDetailsFormProduct(disabled=True,
                                                  initial=(int(product_id),Products.objects.get(id=int(product_id))))

        quantity_form = AddOrderDetailsFormQuantity(max_quantity=Products.objects.get(id=int(product_id)).quantity,
                                                    data=request.POST)
        product_f = Products.objects.get(id=int(product_id))

        if quantity_form.is_valid():
            product = Products.objects.get(id=int(product_id))
            quantity = quantity_form.cleaned_data.get("quantity")

            total_amount = int(quantity) * product.price
            order_detail = OrderDetail(order=order, product=product,
                                       quantity=quantity,
                                       total_amount=total_amount)
            order_detail.save()
            b = product.quantity - int(quantity)
            Products.objects.filter(id=product.id).update(quantity=b)
            Order.objects.filter(id=order_id).update(total_amount=order.total_amount + total_amount)

            if type_sale == 'Наличный Расчёт':
                a = customer.total_amount
                s = a + total_amount
                Customers.objects.filter(id=customer.id).update(total_amount=s)

            elif type_sale == 'Безналичный Расчёт':
                s = customer.total_amount + total_amount
                current_amount = customer.current_amount - total_amount
                Customers.objects.filter(id=customer.id).update(total_amount=s, current_amount=current_amount)
            elif type_sale == 'Кредит':
                s = customer.total_amount + total_amount
                current_amount = 0
                debt = customer.debt + total_amount - customer.current_amount
                loan_balance = customer.loan - debt
                Customers.objects.filter(id=customer.id).update(total_amount=s,
                                                                current_amount=current_amount,
                                                                debt=debt,
                                                                loan_balance=loan_balance)

            return HttpResponseRedirect(reverse('main:create_order_detail', args=[order.pk, 'f']))

    elif product_id != 'f':
        product_form = AddOrderDetailsFormProduct(disabled=True,
                                                  initial=(int(product_id), Products.objects.get(id=int(product_id))))
        product_f = Products.objects.get(id=int(product_id))

        if type_sale == 'Безналичный Расчёт':
            max_quantity = min(Products.objects.get(id=int(product_id)).quantity,
                               customer.current_amount/product_f.price)
        elif type_sale == 'Кредит':
            max_quantity = min(Products.objects.get(id=int(product_id)).quantity,
                               (customer.current_amount + customer.loan_balance)/product_f.price)
        else:
            max_quantity = Products.objects.get(id=int(product_id)).quantity

        quantity_form = AddOrderDetailsFormQuantity(max_quantity=max_quantity)

    else:
        product_form = AddOrderDetailsFormProduct()
        quantity_form = ''

    if type_sale == 'Взаимозачёт':
        return HttpResponseRedirect(reverse('main:barter', args=[order.pk]))

    context = {'title': 'Заказ '+str(order_id),
               'products': Products.objects.all(),
               'order_detail': OrderDetail.objects.filter(order=order),
               'total_amount': total_amount,
               'total_amount_order': Order.objects.get(id=order_id).total_amount,
               'order_id': order_id,
               'product_id': product_id,
               'product_f': product_f,
               'flag': flag,
               'product_form': product_form,
               'quantity_form': quantity_form,
               }
    return render(request, 'main/create_order_detail.html', context)


def barter(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    offset = False
    total_amount_barter = BarterOrder.objects.filter(order=order).aggregate(s=Sum("total_amount"))['s'] if BarterOrder.objects.filter(order=order).exists() else 0

    if order.type_sale == 'Бартер':
        total_amount_order = OrderDetail.objects.filter(order=order).aggregate(s=Sum("total_amount"))['s']
        total_amount = max(total_amount_order - total_amount_barter, 0)

    elif order.type_sale == 'Взаимозачёт':
        total_amount_order = ''
        offset = True
        total_amount = order.customer.debt

    if request.method == 'POST':
        product_id = request.POST["product"]
        quantity = request.POST["quantity"]
        product = Products.objects.get(id=product_id)
        total_amount_barter = int(quantity) * product.price
        barter_order = BarterOrder(order=order,
                          product=product,
                          quantity=quantity,
                          total_amount=total_amount_barter)
        barter_order.save()
        c = product.quantity + int(quantity)
        Products.objects.filter(id=product.id).update(quantity=c)
        if offset:
            debt = max(order.customer.debt - total_amount_barter, 0)
            Customers.objects.filter(id=order.customer.id).update(debt=debt,
                                                                  loan_balance=order.customer.loan - debt)
        return HttpResponseRedirect(reverse('main:barter', args=[order.pk]))


    context = {'title': 'Заказ'+str(order_id),
               'products': Products.objects.all(),
               'total_amount_order': total_amount_order,
               'total_amount_barter': total_amount_barter,
               'order_id': order_id,
               'total_amount': total_amount,
               'order_detail': OrderDetail.objects.filter(order=order),
               'products_barter': BarterOrder.objects.filter(order=order),
               'product_f': 'f',
               'flag': total_amount == 0,
               'offset': offset,
               }
    return render(request, 'main/barter.html', context)


# def offset(request, order_id):
#     order = get_object_or_404(Order, pk=order_id)
#     total_amount = BarterOrder.objects.filter(order=order).aggregate(s=Sum("total_amount"))
#     if request.method == 'POST':
#         product_id = request.POST["product"]
#         quantity = request.POST["quantity"]
#         product = Products.objects.get(id=product_id)
#         total_amount_barter = int(quantity) * product.price
#         barter_order = BarterOrder(order=order,
#                           product=product,
#                           quantity=quantity,
#                           total_amount=total_amount_barter)
#         barter_order.save()
#         c = product.quantity + int(quantity)
#         Products.objects.filter(id=product.id).update(quantity=c)
#         return HttpResponseRedirect(reverse('main:offset', args=[order.pk]))
#     customer = order.customer
#     s = customer.total_amount + total_amount['s']
#     Customers.objects.filter(id=customer.id).update(total_amount=s)
#     context = {'title': 'Заказ' + str(order_id),
#                'order_id': order_id,
#                'total_amount': total_amount['s'],
#                'products_barter': BarterOrder.objects.filter(order=order)}
#     return render(request, 'main/offset.html', context)
