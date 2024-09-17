from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class Products(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.name}'


class Customers(models.Model):
    name = models.CharField(max_length=200)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    current_amount = models.DecimalField(max_digits=12, decimal_places=2)
    loan = models.DecimalField(max_digits=12, decimal_places=2)
    debt = models.DecimalField(max_digits=12, decimal_places=2)
    loan_balance = models.DecimalField(max_digits=12, decimal_places=2)
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'Клиент: {self.name}'


class Order(models.Model):
    customer = models.ForeignKey(to=Customers, on_delete=models.CASCADE)
    type_sale = models.CharField(default='Наличный расчёт', max_length=100)

    def __str__(self):
        return f'Заказ для {self.customer.name}'


class OrderDetail(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1)])
    total_amount = models.DecimalField(default=0, max_digits=12, decimal_places=2)

    def __str__(self):
        return f' ID Заказа:{self.order.id}'


class BarterOrder(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Products, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    total_amount = models.DecimalField(default=0, max_digits=12, decimal_places=2)

    def __str__(self):
        return f'ID Заказа:{self.order.id}'



